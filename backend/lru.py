from collections import OrderedDict

class LRU:
    def __init__(self):
        self.cache = OrderedDict()

    def access(self, page):
        if page in self.cache:
            self.cache.move_to_end(page)
        else:
            self.cache[page] = True

    def evict(self):
        return self.cache.popitem(last=False)[0]

