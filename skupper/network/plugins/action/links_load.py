from ansible.utils.vars import merge_hash
from . import BaseActionModule
from ..module_utils.sites import get_sites


class ActionModule(BaseActionModule):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, tmp=None, task_vars=None):
        # parsing arguments and initializing result dict
        result = super(ActionModule, self).run(tmp, task_vars)
        module_args = self.module_args()
        module_args['sites'] = get_sites(self.hostvars)
        # executing module
        result = merge_hash(result, self._execute_module(module_args=module_args, task_vars=task_vars, tmp=tmp))
        return result
