from ansible.utils.vars import merge_hash
from . import BaseActionModule


class ActionModule(BaseActionModule):

    def run(self, tmp=None, task_vars=None):
        # parsing arguments and initializing result dict
        result = super(ActionModule, self).run(tmp, task_vars)
        module_args = self.module_args()

        # determining links to create and delete
        links = task_vars['vars']['skupper_link_list'] if 'skupper_link_list' in task_vars['vars'] else list()
        existing_links = task_vars['vars']['existing_links'] if 'existing_links' in task_vars['vars'] else list()
        create = list()
        delete = list()
        # links to be removed or re-created (cost changed)
        for ex_link in existing_links:
            link = None
            # static token links
            # when links are not defined based on inventory host names
            # only validate if the link name still exists and cost has not changed
            if 'host' not in ex_link or ex_link['host'] == "" and 'name' in ex_link and ex_link['name'] != "":
                link = self.get_link(links, ex_link['name'], 'name')
                if link and 'host' not in link:
                    link['host'] = ""
            else:
                # continue searching by matching inventory host names
                link = self.get_link(links, ex_link['host'])
            if not link:
                delete.append({'name': ex_link['name']})
            else:
                cost = int(link['cost']) if 'cost' in link else 1
                if cost != int(ex_link['cost']):
                    delete.append({'name': ex_link['name']})
                    if 'token' not in link or link['token'] in (None, ""):
                        link['token'] = self.get_token(link['host'], task_vars)
                    create.append(link)
        # links to be created
        for link in links:
            ex_link = None
            if 'host' in link and link['host'] != "":
                ex_link = self.get_link(existing_links, link['host'])
            elif 'name' in link and link['name'] != "":
                ex_link = self.get_link(existing_links, link['name'], 'name')
                if ex_link and 'host' not in ex_link:
                    ex_link['host'] = ""
            if not ex_link:
                if 'host' not in link or not link['host']:
                    link['host'] = ""
                if 'token' not in link or link['token'] in (None, ""):
                    link['token'] = self.get_token(link['host'], task_vars)
                create.append(link)

        # executing module
        module_args['create'] = create
        module_args['delete'] = delete
        result = merge_hash(result, self._execute_module(module_args=module_args, task_vars=task_vars, tmp=tmp))
        return result

    @staticmethod
    def get_link(links, host, link_property="host"):
        for link in links:
            if link[link_property] == host:
                return link
        return None

    def get_token(self, host, task_vars) -> str:
        token = self.get_host_or_task_var(host, 'generated_token', task_vars, '')
        return token
