def get_sites(hostvars) -> list[dict]:
    # map site entry by site id
    sites = list[dict]()
    for host in hostvars:
        hostvar = hostvars[host]
        if 'site' in hostvar:
            try:
                site = hostvar['site']
                sites.append(site)
            except Exception as ex:
                raise RuntimeError('Unable to load site for %s - %s' % (host, ex.__str__()))
        else:
            raise RuntimeError('site information has not been loaded for: %s' % host)
    return sites
