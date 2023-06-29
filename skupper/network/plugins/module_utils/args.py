def common_args() -> dict:
    return dict(
        platform=dict(type='str', required=False),
        kubeconfig=dict(type='str', required=False),
        context=dict(type='str', required=False),
        namespace=dict(type='str', required=False),
        hostname=dict(type='str', required=False),
        podman_endpoint=dict(type='str', required=False),
    )


def add_fact(result, d):
    facts = result['ansible_facts'] if 'ansible_facts' in result else dict()
    facts |= d
    result['changed'] = True
    result['ansible_facts'] = facts
