class Hardware:
    def __init__(self, system):
        self._system = system

    def basic_information(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def register(self):
        return

    def update(self):
        return
