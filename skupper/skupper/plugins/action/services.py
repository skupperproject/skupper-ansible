from ansible.utils.vars import merge_hash
from . import BaseActionModule
from ..module_utils.types import Service, ServiceTarget, ServiceParam


class ActionModule(BaseActionModule):

    @staticmethod
    def remove_service_targets_labels(svc: Service):
        """
        Remove targets and labels from service specification.
        Labels and targets are evaluated and managed separately,
        as they can be individually added/removed.
        :param svc:
        """
        if 'targets' in svc.__dict__:
            delattr(svc, 'targets')
        if 'labels' in svc.__dict__:
            delattr(svc, 'labels')

    @staticmethod
    def labels_dict_to_list(labels: dict, delete: bool = False) -> list[str]:
        ll = list[str]()
        for k, v in labels.items():
            ll.append(("%s=%s" % (k, v) if not delete else ("%s-" % k)))
        return ll

    @staticmethod
    def labels_as_dict(labels: list) -> dict[str, str]:
        ld = dict[str, str]()
        if not labels:
            return ld
        for label in labels:
            k, v = label.split("=")
            ld[k] = v
        return ld

    def run(self, tmp=None, task_vars=None):
        # parsing arguments and initializing result dict
        result = super(ActionModule, self).run(tmp, task_vars)
        module_args = self.module_args()

        # determining services to create and delete
        # services = task_vars['vars']['services'] if 'services' in task_vars['vars'] else dict()
        services = self.get_my_host_or_task_var('skupper_service_list', task_vars, list())
        existing_services = task_vars['vars']['existing_services'] if 'existing_services' in task_vars['vars'] \
            else list()

        # lists with ServiceParam dictionaries to be passed as arguments to the module
        create = list()
        delete = list()

        # extracting service names
        service_names = [s['name'] for s in services if 'name' in s.keys()]
        existing_service_names = [s['name'] for s in existing_services if 'name' in s.keys()]

        # services to be removed or updated
        for ex_svc_info in existing_services:
            svc_name = ex_svc_info['name']
            if svc_name not in service_names:
                delete.append(ServiceParam(name=svc_name).vars())
            else:
                svc_info = next(s for s in services if s['name'] == svc_name)
                ex_svc = Service(**ex_svc_info)
                ex_labels = self.labels_as_dict(ex_svc.labels if ex_svc.labels else dict())
                svc = Service(**svc_info)
                labels = self.labels_as_dict(svc.labels if svc.labels else dict())
                # removing targets and labels to compare service definition only
                self.remove_service_targets_labels(ex_svc)
                self.remove_service_targets_labels(svc)
                # svc spec has changed (delete and create service and targets)
                if vars(ex_svc) != vars(svc):
                    delete.append(ServiceParam(name=svc_name).vars())
                    create.append(ServiceParam(
                        name=svc_name,
                        spec=svc.vars(),
                        labels=self.labels_dict_to_list(labels),
                        targets=list[ServiceTarget](svc_info['targets'] if 'targets' in svc_info else list())
                    ).vars())
                    continue

                # validating existing targets
                del_targets = list[dict]()
                if 'targets' in ex_svc_info:
                    ex_targets = ex_svc_info['targets']
                    if 'targets' not in svc_info:
                        del_targets += ex_targets
                        # delete.append(ServiceParam(name=svc_name, targets=ex_targets).vars())
                    else:
                        targets = svc_info['targets']
                        all_target_ports = list[str]()
                        for port in svc.ports:
                            all_target_ports.append("%d:%d" % (port, port))
                        for target in targets:
                            if 'ports' not in target:
                                target['ports'] = all_target_ports

                        for ex_target in ex_targets:
                            if ex_target not in targets:
                                del_targets.append(ServiceTarget(**ex_target).vars())
                        # if len(del_targets) > 0:
                        #     delete.append(ServiceParam(name=svc_name, targets=del_targets).vars())

                # validating labels
                del_labels = dict()
                # removed or modified labels
                for key, val in ex_labels.items():
                    if key not in labels:
                        del_labels[key] = val
                if len(del_targets) > 0 or len(del_labels) > 0:
                    delete.append(ServiceParam(name=svc_name,
                                               targets=del_targets,
                                               labels=self.labels_dict_to_list(del_labels, True)
                                               ).vars())

        for svc_info in services:
            svc_name = svc_info['name']
            # new service found
            svc = Service(**svc_info)

            # adding target ports if missing
            targets = svc_info['targets'] if 'targets' in svc_info else list()
            all_target_ports = list[str]()
            for port in svc.ports:
                all_target_ports.append("%d:%d" % (port, port))
            for target in targets:
                if 'ports' not in target:
                    target['ports'] = all_target_ports

            labels = self.labels_as_dict(svc.labels if svc.labels else dict())
            if svc_name not in existing_service_names:
                create.append(ServiceParam(
                    name=svc_name,
                    spec=svc.vars(),
                    labels=self.labels_dict_to_list(labels),
                    targets=targets
                ).vars())
                continue

            # validating new targets
            ex_svc_info = next(s for s in existing_services if s['name'] == svc_name)
            ex_targets = ex_svc_info['targets'] if 'targets' in ex_svc_info else list()
            add_targets = list[dict]()
            for target in targets:
                if target not in ex_targets:
                    add_targets.append(ServiceTarget(**target).vars())

            # validating new labels
            ex_svc = Service(**ex_svc_info)
            ex_labels = self.labels_as_dict(ex_svc.labels if ex_svc.labels else dict())
            add_labels = dict[str, str]()
            for key, val in labels.items():
                if key not in ex_labels:
                    add_labels[key] = val

            if len(add_targets) > 0 or len(add_labels) > 0:
                create.append(ServiceParam(name=svc_name,
                                           targets=add_targets,
                                           labels=self.labels_dict_to_list(add_labels)).vars())

        # executing module
        module_args['create'] = create
        module_args['delete'] = delete
        result = merge_hash(result, self._execute_module(module_args=module_args, task_vars=task_vars, tmp=tmp))
        return result
