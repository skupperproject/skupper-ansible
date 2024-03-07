from ansible.plugins.action import ActionBase


class BaseActionModule(ActionBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.platform = ""
        self.kubeconfig = ""
        self.context = ""
        self.namespace = ""
        self.hostname = ""
        self.podman_endpoint = ""
        self.hostvars = dict()
        self.my_hostvars = dict()

    def run(self, tmp=None, task_vars=None):
        result = super(BaseActionModule, self).run(tmp, task_vars)
        self.hostname = task_vars['vars']['inventory_hostname']
        self.hostvars = task_vars['hostvars'] if 'hostvars' in task_vars else dict()
        self.my_hostvars = self.hostvars[self.hostname] if self.hostname in self.hostvars else dict()
        self.platform = self.get_my_host_or_task_var('platform', task_vars, 'kubernetes')
        self.kubeconfig = self.get_my_host_or_task_var('kubeconfig', task_vars, '')
        self.context = self.get_my_host_or_task_var('context', task_vars, '')
        self.namespace = self.get_my_host_or_task_var('namespace', task_vars, '')
        init = self.get_my_host_or_task_var('init', task_vars, dict())
        self.podman_endpoint = init['podmanEndpoint'] if init and 'podmanEndpoint' in init else ""
        return result

    def module_args(self) -> dict:
        module_args = self._task.args.copy()
        module_args['platform'] = self.platform
        module_args['kubeconfig'] = self.kubeconfig
        module_args['context'] = self.context
        module_args['namespace'] = self.namespace
        module_args['podman_endpoint'] = self.podman_endpoint
        module_args['hostname'] = self.hostname
        return module_args

    def get_my_host_or_task_var(self, variable, task_vars, default):
        if variable in self.my_hostvars:
            return self.my_hostvars[variable]
        elif task_vars and 'vars' in task_vars and variable in task_vars['vars']:
            return task_vars['vars'][variable]
        return default

    def get_host_or_task_var(self, host, variable, task_vars, default):
        if host in self.hostvars and variable in self.hostvars[host]:
            return self.hostvars[host][variable]
        elif task_vars and 'vars' in task_vars and variable in task_vars['vars'] and \
                host in task_vars['vars'] and \
                variable in task_vars['vars'][host]:
            return task_vars['vars'][host][variable]
        return default
