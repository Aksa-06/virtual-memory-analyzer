def detect_thrashing(loads, faults, cpu):
    """
    Detect thrashing point where page faults increase dramatically 
    and CPU utilization drops significantly.
    """
    # Check for extreme memory pressure scenario
    max_faults = max(faults)
    min_faults = min(faults)
    
    # If page fault rate is consistently above 90%, we're in thrashing
    if min_faults > 450:  # 90% of 500 accesses
        return loads[0]  # Thrashing starts at the first process
    
    # Original detection logic for moderate scenarios
    for i in range(1, len(loads)):
        # Check for significant page fault increase (2x or more)
        fault_increase = faults[i] / faults[i-1] if faults[i-1] > 0 else 2
        
        # Check for CPU utilization drop
        cpu_drop = cpu[i-1] - cpu[i] if i > 0 else 0
        
        # Thrashing detected if:
        # 1. Page faults increase significantly (2x or more)
        # 2. CPU drops by 10% or more
        # 3. CPU is below 60% (indicating memory management overhead)
        if fault_increase >= 2.0 and cpu_drop >= 10 and cpu[i] < 60:
            return loads[i]
    
    # Alternative detection: find where CPU starts declining
    max_cpu_index = cpu.index(max(cpu))
    
    for i in range(max_cpu_index + 1, len(loads)):
        if cpu[i] < cpu[i-1] - 5:  # Declining CPU
            if faults[i] > faults[i-1] * 1.3:  # Rising faults
                return loads[i]
    
    # If CPU is consistently below 10%, indicate thrashing
    if max(cpu) < 10:
        return loads[0]
    
    return None

