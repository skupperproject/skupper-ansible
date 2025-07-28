import os
import pwd
import shutil
import tempfile
import typing as t
from unittest import TestCase
from unittest.mock import patch
from ansible.module_utils import basic
from ansible_collections.skupper.v2.tests.unit.utils.ansible_module_mock import (
    set_module_args,
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
    fail_json,
    get_bin_path,
    CommandArgs,
    CommandResponse,
    RegexMatcher
)


class TestControllerModule(TestCase):

    def setUp(self):
        self.mock_module = patch.multiple(basic.AnsibleModule,
                                          exit_json=exit_json,
                                          fail_json=fail_json,
                                          get_bin_path=get_bin_path)
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)

        self._image: str = ""
        self._run_commands: dict[CommandArgs, CommandResponse] = dict()

        # do not use real datahome path
        self.temphome = tempfile.mkdtemp()

        def data_home_mock():
            return self.temphome

        self.mock_data_home = patch(
            'ansible_collections.skupper.v2.plugins.module_utils.common.data_home', new=data_home_mock)
        self.mock_config_home = patch(
            'ansible_collections.skupper.v2.plugins.module_utils.common.config_dir', new=data_home_mock)
        self.mock_run_command = patch(
            'ansible_collections.skupper.v2.plugins.module_utils.command.run_command', new=self.run_command)
        self.mock_data_home.start()
        self.mock_config_home.start()
        self.mock_run_command.start()
        self.addCleanup(self.mock_data_home.stop)
        self.addCleanup(self.mock_config_home.stop)
        self.addCleanup(self.mock_run_command.stop)
        self.addCleanup(self.clean_temp_home)
        try:
            from ansible_collections.skupper.v2.plugins.modules import controller
            self.module = controller
        except ImportError:
            pass

    def clean_temp_home(self):
        shutil.rmtree(os.path.join(self.temphome, "system-controller"),
                      ignore_errors=True)
        shutil.rmtree(os.path.join(self.temphome, "systemd"),
                      ignore_errors=True)
        os.rmdir(self.temphome)

    def run_command(self, module, args) -> t.Tuple[int, str, str]:
        for ca, cr in self._run_commands.items():
            if ca.matches(args):
                return cr.code, cr.out, cr.err
        print("COMMAND NOT MOCKED: {}".format(args))
        return 0, "", ""

    def create_service(self, module, namespace) -> bool:
        self._create_service_ns = namespace
        return self._create_service_ret

    def delete_service(self, module, namespace) -> bool:
        self._delete_service_ns = namespace
        return True

    def systemctl_command(self) -> list:
        cmd = ["systemctl"]
        if os.getuid() != 0:
            cmd.append("--user")
        return cmd

    def expected_container_name(self):
        return "{}-skupper-controller".format(pwd.getpwuid(os.getuid())[0])

    def test_install_systemd_unavailable(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.append("list-units")
        self._run_commands[CommandArgs(args=systemd_cmd)] = CommandResponse(code=1, err="mock")
        with patch.object(basic.AnsibleModule, "warn") as mock_warn:
            with self.assertRaises(AnsibleExitJson) as exit:
                set_module_args({"action": "install"})
                self.module.main()
        mock_warn.assert_called_once_with("unable to detect systemd: mock")
        self.assertFalse(exit.exception.changed)
    
    def test_install_list_units_fails(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["list-units", "--all", "--no-pager", "--output=json"])
        self._run_commands[CommandArgs(args=systemd_cmd)] = CommandResponse(code=1, err="mock")
        with self.assertRaises(AnsibleFailJson) as ex:
            set_module_args({"action": "install"})
            self.module.main()
        self.assertTrue(str(ex.exception.__str__()).__contains__(
            "error listing service units: mock"), ex.exception.msg)
    
    def test_install_list_units_bad_data(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["list-units", "--all", "--no-pager", "--output=json"])
        self._run_commands[CommandArgs(args=systemd_cmd)] = CommandResponse(code=0, out="bad-data")
        with patch.object(basic.AnsibleModule, "warn") as mock_warn:
            with self.assertRaises(AnsibleExitJson) as exit:
                set_module_args({"action": "install"})
                self.module.main()
        mock_warn.assert_called_once_with(RegexMatcher("invalid json data: *"))
        self.assertFalse(exit.exception.changed)
    
    def test_install_service_exists(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["list-units", "--all", "--no-pager", "--output=json"])
        self._run_commands[CommandArgs(args=systemd_cmd)] = CommandResponse(code=0, out='[{"unit": "skupper-controller.service"}]')
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({"action": "install"})
            self.module.main()
        self.assertFalse(exit.exception.changed)

    def test_install_container_exists(self):
        expected_name = self.expected_container_name()
        self._run_commands[CommandArgs(args=["podman", "version"])] = CommandResponse(code=0)
        self._run_commands[CommandArgs(args=["docker", "version"])] = CommandResponse(code=0)
        self._run_commands[CommandArgs(args=["podman", "inspect", expected_name])] = CommandResponse(code=0)
        with patch.object(basic.AnsibleModule, "debug") as mock_debug:
            with self.assertRaises(AnsibleExitJson) as exit:
                set_module_args({"action": "install", "platform": "podman"})
                self.module.main()
        mock_debug.assert_called_once_with("{} container already exists (platform: podman)".format(expected_name))
        self.assertFalse(exit.exception.changed)

    def test_install_enable_podman_fails(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["enable", "--now", "podman.socket"])
        self._run_commands[CommandArgs(args=systemd_cmd)] = CommandResponse(code=1, err="mock")
        self._run_commands[CommandArgs(args=["docker", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        self._run_commands[CommandArgs(args=["podman", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        with self.assertRaises(AnsibleFailJson) as ex:
            set_module_args({"action": "install"})
            self.module.main()
        self.assertTrue(str(ex.exception.__str__()).__contains__(
            "error enabling podman.socket service: mock"), ex.exception.msg)

    def test_install_container_create_fails(self):
        # improve run_command mock to include a command prefix check
        self._run_commands[CommandArgs(args=["podman", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        self._run_commands[CommandArgs(args=["docker", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        mock_error = "mock error creating container"
        self._run_commands[CommandArgs(args=["podman", "run", "-d"], prefix=True)] = CommandResponse(code=1, err=mock_error)
        self._run_commands[CommandArgs(args=["docker", "run", "-d"], prefix=True)] = CommandResponse(code=1, err=mock_error)
        expected_name = self.expected_container_name()
        with self.assertRaises(AnsibleFailJson) as ex:
            set_module_args({"action": "install"})
            self.module.main()
        self.assertEqual(ex.exception.msg[1], "error creating container '{}': {}".format(expected_name, mock_error))
        with self.assertRaises(AnsibleFailJson) as ex:
            set_module_args({"action": "install", "platform": "docker"})
            self.module.main()
        self.assertEqual(ex.exception.msg[1], "error creating container '{}': {}".format(expected_name, mock_error))

    def test_install_startup_scripts_create_fails(self):
        self._run_commands[CommandArgs(args=["podman", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        self._run_commands[CommandArgs(args=["docker", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        with patch("os.makedirs") as mock_makedirs:
            mock_makedirs.side_effect = Exception("mock exception creating dirs")
            with self.assertRaises(AnsibleFailJson) as ex:
                set_module_args({"action": "install"})
                self.module.main()
        self.assertEqual(ex.exception.msg[1], "unable to create startup scripts: mock exception creating dirs")

        def open_raise(*args, **kwargs):
            if len(args) > 1 and "start.sh" in args[0] and "w" in args[1]:
                raise Exception("mock exception writing start.sh")

        open_mock = patch('builtins.open', new=open_raise)
        open_mock.start()
        self.addCleanup(open_mock.stop)

        with self.assertRaises(AnsibleFailJson) as ex:
            set_module_args({"action": "install"})
            self.module.main()
        self.assertEqual(ex.exception.msg[1], "unable to create startup scripts: mock exception writing start.sh")

    def test_install_service_create_fails(self):
        self._run_commands[CommandArgs(args=["podman", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        self._run_commands[CommandArgs(args=["docker", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["enable", "--now", "skupper-controller.service"])
        self._run_commands[CommandArgs(systemd_cmd)] = CommandResponse(code=1, err="mock error")
        # fail on creation of service file
        with patch('ansible_collections.skupper.v2.plugins.modules.controller.ControllerModule.create_service') as mock_create_service:
            mock_create_service.side_effect = Exception("skupper-controller.service")
            with self.assertRaises(AnsibleFailJson) as ex:
                set_module_args({"action": "install"})
                self.module.main()
            self.assertEqual(ex.exception.msg[1], "unable to create systemd service: skupper-controller.service")
        # warn on systemctl service creation
        with patch.object(basic.AnsibleModule, "warn") as mock_warn:
            with self.assertRaises(AnsibleExitJson) as exit:
                set_module_args({"action": "install"})
                self.module.main()
        mock_warn.assert_called_with("error enabling service 'skupper-controller.service': mock error")
        self.assertTrue(exit.exception.changed)

    def test_install_podman(self):
        self._test_install("podman")

    def test_install_podman_custom_image(self):
        self._image = "quay.io/skupper/system-controller:custom"
        self._test_install("podman")

    def test_install_docker(self):
        self._test_install("docker")

    def _test_install(self, platform: str):
        # must be imported after data_home is mocked
        from ansible_collections.skupper.v2.plugins.module_utils.system import (
            base_mounts,
            env,
            runas,
            userns,
        )

        # expected container run command
        run_command_args = [
            platform, "run", "-d", "--pull", "always", "--name",
            self.expected_container_name(), "--label=application=skupper-v2",
            "--network", "host", "--security-opt", "label=disable", "-u",
            runas(platform), "--userns=%s" % (userns(platform))
        ]
        for source, dest in base_mounts(platform, platform).items():
            run_command_args.extend(["-v", "%s:%s:z" % (source, dest)])
        env_dict = env(platform, platform)
        for var, val in env_dict.items():
            run_command_args.extend(["-e", "%s=%s" % (var, val)])
        run_command_args.append(self._image or "quay.io/skupper/system-controller:v2-dev")
        run_command = CommandArgs(args=run_command_args)
        self._run_commands[run_command] = CommandResponse()
        self._run_commands[CommandArgs(args=["podman", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        self._run_commands[CommandArgs(args=["docker", "inspect", self.expected_container_name()])] = CommandResponse(code=1)

        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({"action": "install"})
            self.module.main()
        self.assertTrue(exit.exception.changed)
        self.assertTrue(run_command.called)

        self.assertTrue(os.path.exists("{}/{}/start.sh".format(self.temphome, "system-controller/internal/scripts")))
        self.assertTrue(os.path.exists("{}/{}/stop.sh".format(self.temphome, "system-controller/internal/scripts")))

        systemd_path = "systemd/user"
        if os.getuid() == 0:
            systemd_path = "systemd/system"
        self.assertTrue(os.path.exists("{}/{}/skupper-controller.service".format(self.temphome, systemd_path, "skupper-controller.service")))
    
    def test_uninstall_no_changes(self):
        # service does not exist
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["list-units", "--all", "--no-pager", "--output=json"])
        self._run_commands[CommandArgs(args=systemd_cmd)] = CommandResponse(code=0, out='[]')
        self._run_commands[CommandArgs(args=["podman", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        self._run_commands[CommandArgs(args=["docker", "inspect", self.expected_container_name()])] = CommandResponse(code=1)
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({"action": "uninstall"})
            self.module.main()
        self.assertFalse(exit.exception.changed)

    def _create_service_file(self):
        systemd_path = "systemd/user"
        if os.getuid() == 0:
            systemd_path = "systemd/system"
        base_path = "{}/{}".format(self.temphome, systemd_path)
        os.makedirs(base_path)
        service_file = "{}/skupper-controller.service".format(base_path)
        with open(service_file, "w") as f:
            f.write("dummy content\n")

    def _create_startup_scripts(self):
        base_path = "{}/{}".format(self.temphome, "system-controller/internal/scripts")
        os.makedirs(base_path)
        for script in ["start.sh", "stop.sh"]:
            with open("{}/{}".format(base_path, script), "w") as f:
                f.write("dummy content\n")

    def test_uninstall_podman(self):
        self._uninstall("podman")

    def test_uninstall_docker(self):
        self._uninstall("docker")

    def _uninstall(self, platform: str):
        # create expected resources
        self._create_service_file()
        self._create_startup_scripts()

        # service defined
        systemctl = self.systemctl_command()

        # mock commands
        inspect_cmd = CommandArgs(args=[platform, "inspect", self.expected_container_name()])
        disable_cmd = CommandArgs(args=systemctl + ["disable", "--now", "skupper-controller.service"])
        reload_cmd = CommandArgs(args=systemctl + ["daemon-reload"])
        reset_cmd = CommandArgs(args=systemctl + ["reset-failed"])
        container_rm_cmd = CommandArgs(args=[platform, "rm", "--force", self.expected_container_name()])
        mock_commands = [disable_cmd, reload_cmd, reset_cmd, container_rm_cmd, inspect_cmd]
        for ca in mock_commands:
            self._run_commands[ca] = CommandResponse()

        # special mock commands
        list_cmd = CommandArgs(args=systemctl + ['list-units', '--all', '--no-pager', '--output=json'])
        self._run_commands[list_cmd] = CommandResponse(code=0, out='[{"unit": "skupper-controller.service"}]')
        special_commands = [list_cmd]

        if platform == "podman":
            fail_platform = "docker"
        else:
            fail_platform = "podman"
        inspect_fail_cmd = CommandArgs(args=[fail_platform, "inspect", self.expected_container_name()])
        self._run_commands[inspect_fail_cmd] = CommandResponse(code=1)

        # assert changed
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({"action": "uninstall"})
            self.module.main()
        self.assertTrue(exit.exception.changed)

        # assert commands called
        for ca in mock_commands + special_commands:
            self.assertTrue(ca.called(), "Expected command not called: {}".format(ca))

        # assert startup scripts path removed
        scripts_path = "{}/{}".format(self.temphome, "system-controller")
        self.assertFalse(os.path.exists(scripts_path))

    def test_uninstall_service_remove_fails(self):
        # create expected resources
        self._create_service_file()
        self._create_startup_scripts()

        # service defined
        systemctl = self.systemctl_command()

        # mock commands
        disable_cmd = CommandArgs(args=systemctl + ["disable", "--now", "skupper-controller.service"])
        self._run_commands[disable_cmd] = CommandResponse(code=1, err="mock error")
        reload_cmd = CommandArgs(args=systemctl + ["daemon-reload"])
        self._run_commands[reload_cmd] = CommandResponse(code=1, err="mock error")
        reset_cmd = CommandArgs(args=systemctl + ["reset-failed"])
        self._run_commands[reset_cmd] = CommandResponse(code=1, err="mock error")

        # special mock commands
        list_cmd = CommandArgs(args=systemctl + ['list-units', '--all', '--no-pager', '--output=json'])
        self._run_commands[list_cmd] = CommandResponse(code=0, out='[{"unit": "skupper-controller.service"}]')
        special_commands = [disable_cmd, reload_cmd, reset_cmd, list_cmd]

        # assert changed
        with patch("os.remove") as remove_mock:
            remove_mock.side_effect = Exception("mock remove error")
            with patch.object(basic.AnsibleModule, "warn") as mock_warn:
                with self.assertRaises(AnsibleExitJson) as exit:
                    set_module_args({"action": "uninstall"})
                    self.module.main()

        self.assertTrue(exit.exception.changed)

        # assert commands called
        for ca in special_commands:
            self.assertTrue(ca.called(), "Expected command not called: {}".format(ca))

        systemd_path = "systemd/user"
        if os.getuid() == 0:
            systemd_path = "systemd/system"
        service_file = "{}/{}/skupper-controller.service".format(self.temphome, systemd_path)

        self.assertEqual(len(mock_warn.mock_calls), 4)
        remove_mock.assert_called()
        self.assertEqual(mock_warn.call_args_list[0].args[0], "error stopping service '{}': {}".format("skupper-controller.service", "mock error"))
        self.assertEqual(mock_warn.call_args_list[1].args[0], "error removing service file '{}': {}".format(service_file, "mock remove error"))
        self.assertEqual(mock_warn.call_args_list[2].args[0], "error running systemd command '{}': {}".format(reload_cmd.args, "mock error"))
        self.assertEqual(mock_warn.call_args_list[3].args[0], "error running systemd command '{}': {}".format(reset_cmd.args, "mock error"))

    def test_uninstall_container_remove_fails(self):
        # mock commands
        systemctl = self.systemctl_command()
        list_cmd = CommandArgs(args=systemctl + ['list-units', '--all', '--no-pager', '--output=json'])
        self._run_commands[list_cmd] = CommandResponse(code=0, out='[]')

        container_rm_cmd = CommandArgs(args=["podman", "rm", "--force", self.expected_container_name()])
        self._run_commands[container_rm_cmd] = CommandResponse(code=1, err="mock error")

        # assert changed
        with self.assertRaises(AnsibleFailJson) as ex:
            set_module_args({"action": "uninstall"})
            self.module.main()

        self.assertEqual(ex.exception.msg[1], "error removing {} container: {}".format(self.expected_container_name(), "mock error"))

    def test_uninstall_path_remove_fails(self):
        # create expected resources
        self._create_startup_scripts()

        # service defined
        systemctl = self.systemctl_command()

        # special mock commands
        list_cmd = CommandArgs(args=systemctl + ['list-units', '--all', '--no-pager', '--output=json'])
        self._run_commands[list_cmd] = CommandResponse(code=0, out='[{"unit": "skupper-controller.service"}]')
        special_commands = [list_cmd]

        with patch.object(basic.AnsibleModule, "warn") as mock_warn:
            with patch("shutil.rmtree") as mock_rmtree:
                mock_rmtree.side_effect = Exception("mock exception removing dirs")
                with self.assertRaises(AnsibleExitJson) as exit:
                    set_module_args({"action": "uninstall"})
                    self.module.main()

        # assert commands called
        for ca in special_commands:
            self.assertTrue(ca.called(), "Expected command not called: {}".format(ca))

        self.assertTrue(mock_rmtree.assert_called)
        scripts_path = "{}/{}".format(self.temphome, "system-controller")
        mock_warn.assert_called_with("unable to remove {}: {}".format(scripts_path, "mock exception removing dirs"))
        self.assertTrue(os.path.exists(scripts_path))

        self.assertTrue(exit.exception.changed)
