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
