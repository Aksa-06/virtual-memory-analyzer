from backend.lru import LRU

class VirtualMemory:
    def __init__(self, frames):
        self.frames = frames
        self.memory = {}
        self.lru = LRU(frames)
        self.page_faults = 0

    def access(self, pid, page):
        key = (pid, page)
        if key in self.memory:
            self.lru.access(key)
            return

        self.page_faults += 1

        if len(self.memory) >= self.frames:
            victim = self.lru.evict()
            del self.memory[victim]

        self.memory[key] = pid
        self.lru.access(key)
