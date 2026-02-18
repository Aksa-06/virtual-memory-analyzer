import random
from backend.memory import VirtualMemory

def simulate(processes, frames, accesses=500):
    vm = VirtualMemory(frames)

    for _ in range(accesses):
        pid = random.randint(1, processes)
        base = random.randint(1, 15)
        page = random.randint(base, base + 4)
        vm.access(pid, page)

    return vm.page_faults
