from __future__ import (absolute_import, division, print_function)


__metaclass__ = type


def prepare_command(params: dict) -> list[str]:
    command = list[str]()
    platform = params['platform'] if 'platform' in params else 'kubernetes'
    kubeconfig = params['kubeconfig'] if 'kubeconfig' in params else ''
    context = params['context'] if 'context' in params else ''
    namespace = params['namespace'] if 'namespace' in params else ''

    command.append("skupper")
    command.append("--platform")
    command.append(platform)
    if platform == "kubernetes":
        if kubeconfig != "":
            command.append("--kubeconfig")
            command.append(kubeconfig)
        if context != "":
            command.append("--context")
            command.append(context)
        if namespace != "":
            command.append("--namespace")
            command.append(namespace)

    return command
