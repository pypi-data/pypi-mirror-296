
class Predicate:
    def __init__(self, func):
        self.func = func

    def __call__(self, item):
        return self.func(item)
