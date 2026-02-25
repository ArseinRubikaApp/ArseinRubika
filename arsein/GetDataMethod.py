from threading import Thread


class GetDataMethod(Thread):
    def __init__(self, target=None, args=()):
        super().__init__(target=target, args=args)
        self._getdata = None
        self._error = None

    def run(self):
        try:
            if self._target is not None:
                self._getdata = self._target(*self._args)
        except Exception as e:
            self._error = e

    def show(self):
        super().start()
        super().join()

        if self._error is not None:
            raise self._error

        if self._getdata is not None:
            return self._getdata
        return ""
