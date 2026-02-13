import matplotlib.pyplot as plt

def draw(loads, faults, cpu):
    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.plot(loads, faults, marker='o', color='tab:red')
    plt.title("Page Faults")

    plt.subplot(1,2,2)
    plt.plot(loads, cpu, marker='o', color='tab:blue')
    plt.title("CPU Utilization")

    plt.tight_layout()
    plt.show()
