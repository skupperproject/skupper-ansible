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
        self.platform = self.my_hostvars['platform'] if 'platform' in self.my_hostvars else 'kubernetes'
        self.kubeconfig = self.my_hostvars['kubeconfig'] if 'kubeconfig' in self.my_hostvars else ''
        self.context = self.my_hostvars['context'] if 'context' in self.my_hostvars else ''
        self.namespace = self.my_hostvars['namespace'] if 'namespace' in self.my_hostvars else ''
        init = self.my_hostvars['init'] if 'init' in self.my_hostvars else dict()
        self.podman_endpoint = init['podmanEndpoint'] if 'podmanEndpoint' in init else ""
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
