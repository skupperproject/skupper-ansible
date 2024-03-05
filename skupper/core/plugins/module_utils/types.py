from __future__ import (absolute_import, division, print_function)
import typing

__metaclass__ = type


class Result:
    def __init__(self):
        self.msgs: list = list()
        self.warnings: list = list()
        self.changed: bool = False
        self.failed: bool = False

    def merge(self, other):
        self.msgs += other.msgs
        self.warnings += other.warnings
        if other.changed:
            self.changed = True
        if other.failed:
            self.failed = True

    def result(self):
        d = dict(changed=self.changed,
                 failed=self.failed)
        if len(self.msgs) > 0:
            d['msg'] = self.msgs.__str__()
        if len(self.warnings) > 0:
            d['warnings'] = self.warnings.__str__()
        return d


class Site:
    def __init__(self, **kwargs):
        self.host: str = ""
        self.name: str = ""
        self.id: str = ""
        self.__dict__.update(kwargs)


class Link:
    def __init__(self):
        self.host: str = ""
        self.name: str = ""
        self.cost: int = 1
        self.token: str = ""

    def unmapped(self) -> bool:
        return self.host == ""


class ServiceTarget:
    def __init__(self, **kwargs):
        self.type: str = ""
        self.name: str = ""
        self.ports: typing.Optional[list[str]] = None
        self.__dict__.update(kwargs)

    def vars(self) -> dict:
        return {k: v for k, v in vars(self).items() if v}


class Service:
    def __init__(self, **kwargs):
        self.ports: list[int] = []
        self.protocol: str = ""
        self.targets: typing.Optional[list[dict]] = None
        self.labels: typing.Optional[list] = None
        self.aggregate: typing.Optional[str] = None
        self.generateTlsSecrets: typing.Optional[bool] = None
        self.eventChannel: typing.Optional[bool] = None
        # podman only
        self.containerName: typing.Optional[str] = None
        self.hostIp: typing.Optional[str] = None
        self.hostPorts: typing.Optional[list[str]] = None
        self.__dict__.update(kwargs)
        if self.protocol == "":
            self.protocol = "tcp"

    def vars(self) -> dict:
        return {k: v for k, v in vars(self).items() if v}


class ServiceParam:
    def __init__(self, **kwargs):
        self.name: str = ""
        # spec can be omitted if intention is just to manipulate targets or labels
        self.spec: typing.Optional[dict] = None
        self.targets: typing.Optional[list[ServiceTarget]] = None
        self.labels: typing.Optional[list[str]] = None
        self.__dict__.update(**kwargs)
        if self.spec and 'targets' in self.spec:
            del (self.spec['targets'])
        if self.spec and 'labels' in self.spec:
            del (self.spec['labels'])

    def vars(self) -> dict:
        return {k: v for k, v in vars(self).items() if v}
