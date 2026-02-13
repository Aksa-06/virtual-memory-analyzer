class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []

    def access(self, page):
        if page in self.cache:
            self.cache.remove(page)
        self.cache.append(page)

    def evict(self):
        return self.cache.pop(0)
