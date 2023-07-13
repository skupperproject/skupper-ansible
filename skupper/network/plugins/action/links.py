from ansible.utils.vars import merge_hash
from . import BaseActionModule


class ActionModule(BaseActionModule):

    def run(self, tmp=None, task_vars=None):
        # parsing arguments and initializing result dict
        result = super(ActionModule, self).run(tmp, task_vars)
        module_args = self.module_args()

        # determining links to create and delete
        links = task_vars['vars']['links'] if 'links' in task_vars['vars'] else list()
        existing_links = task_vars['vars']['existing_links'] if 'existing_links' in task_vars['vars'] else list()
        create = list()
        delete = list()
        # links to be removed or re-created (cost changed)
        for ex_link in existing_links:
            link = self.get_link(links, ex_link['host'])
            if not link:
                delete.append(ex_link)
            else:
                cost = int(link['cost']) if 'cost' in link else 1
                if cost != int(ex_link['cost']):
                    delete.append(ex_link)
                    if 'token' not in link or link['token'] in (None, ""):
                        link['token'] = self.get_token(link['host'])
                    create.append(link)
        # links to be created
        for link in links:
            ex_link = self.get_link(existing_links, link['host'])
            if not ex_link:
                if 'token' not in link or link['token'] in (None, ""):
                    link['token'] = self.get_token(link['host'])
                create.append(link)

        # executing module
        module_args['create'] = create
        module_args['delete'] = delete
        result = merge_hash(result, self._execute_module(module_args=module_args, task_vars=task_vars, tmp=tmp))
        return result

    @staticmethod
    def get_link(links, host):
        for link in links:
            if link['host'] == host:
                return link
        return None

    def get_token(self, host) -> str:
        hostvar = self.hostvars[host]
        return hostvar['generatedToken'] if 'generatedToken' in hostvar else ""
