import os
import re
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
)

class CommandResponse(object):
    def __init__(self, code=0, out="", err=""):
        self.code: int = code
        self.out : str = out
        self.err : str = err

class RegexMatcher:
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, other):
        return re.match(self.pattern, other) is not None

class TestControllerModule(TestCase):

    def setUp(self):
        self.mock_module = patch.multiple(basic.AnsibleModule,
                                          exit_json=exit_json,
                                          fail_json=fail_json,
                                          get_bin_path=get_bin_path)
        self.mock_module.start()
        self.addCleanup(self.mock_module.stop)

        self._run_commands: dict[str, CommandResponse] = dict()

        # do not use real datahome path
        self.temphome = tempfile.mkdtemp()

        def data_home_mock():
            return self.temphome

        self.mock_data_home = patch(
            'ansible_collections.skupper.v2.plugins.module_utils.common.data_home', new=data_home_mock)
        self.mock_run_command = patch(
            'ansible_collections.skupper.v2.plugins.module_utils.command.run_command', new=self.run_command)
        self.mock_data_home.start()
        self.mock_run_command.start()
        self.addCleanup(self.mock_data_home.stop)
        self.addCleanup(self.mock_run_command.stop)
        try:
            from ansible_collections.skupper.v2.plugins.modules import controller
            self.module = controller
        except ImportError:
            pass

    def clean_temp_home(self):
        shutil.rmtree(os.path.join(self.temphome, "namespaces"),
                      ignore_errors=True)
        shutil.rmtree(os.path.join(self.temphome, "bundles"),
                      ignore_errors=True)

    def add_run_command(self, args: list, response: CommandResponse):
        self._run_commands["\n".join(args)] = response

    def run_command(self, module, args) -> t.Tuple[int, str, str]:
        args_key = "\n".join(args)
        if not args_key in self._run_commands:
          return 0, "", ""
        resp = self._run_commands[args_key]
        return resp.code, resp.out, resp.err

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
    
    def test_install_systemd_unavailable(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.append("list-units")
        self.add_run_command(systemd_cmd, CommandResponse(code=1, err="mock"))
        with patch.object(basic.AnsibleModule, "warn") as mock_warn:
            with self.assertRaises(AnsibleExitJson) as exit:
                set_module_args({"action": "install"})
                self.module.main()
        mock_warn.assert_called_once_with("unable to detect systemd: mock")
        self.assertFalse(exit.exception.changed)
    
    def test_install_list_units_fails(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["list-units", "--all", "--no-pager", "--output=json"])
        self.add_run_command(systemd_cmd, CommandResponse(code=1, err="mock"))
        with self.assertRaises(AnsibleFailJson) as ex:
            set_module_args({"action": "install"})
            self.module.main()
        self.assertTrue(str(ex.exception.__str__()).__contains__(
            "error listing service units: mock"), ex.exception.msg)
    
    def test_install_list_units_bad_data(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["list-units", "--all", "--no-pager", "--output=json"])
        self.add_run_command(systemd_cmd, CommandResponse(code=0, out="bad-data"))
        with patch.object(basic.AnsibleModule, "warn") as mock_warn:
            with self.assertRaises(AnsibleExitJson) as exit:
                set_module_args({"action": "install"})
                self.module.main()
        mock_warn.assert_called_once_with(RegexMatcher("invalid json data: *"))
        self.assertFalse(exit.exception.changed)
    
    def test_install_service_exists(self):
        systemd_cmd = self.systemctl_command()
        systemd_cmd.extend(["list-units", "--all", "--no-pager", "--output=json"])
        self.add_run_command(systemd_cmd, CommandResponse(code=0, out='[{"unit": "skupper-controller.service"}]'))
        with self.assertRaises(AnsibleExitJson) as exit:
            set_module_args({"action": "install"})
            self.module.main()
        self.assertFalse(exit.exception.changed)

    def test_install_container_exists(self):
        pass
    
    def test_install_container_create_fails(self):
        pass

    def test_install_startup_scripts_create_fails(self):
        pass

    def test_install_service_create_fails(self):
        pass
    
    def test_install(self):
        pass
    
    def test_uninstall_container_remove_fails(self):
        pass

    def test_uninstall_path_remove_fails(self):
        pass
    
    def test_uninstall(self):
        pass

