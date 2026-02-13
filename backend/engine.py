import random
from backend.memory import VirtualMemory

def simulate(processes, frames, accesses=500):
    vm = VirtualMemory(frames)

    for _ in range(accesses):
        pid = random.randint(1, processes)
        page = random.randint(1, 20)
        vm.access(pid, page)

    return vm.page_faults
