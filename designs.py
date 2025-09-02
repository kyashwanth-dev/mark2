import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_battery(ax):
    ax.add_patch(patches.Rectangle((0.3, 0.2), 0.4, 0.6, color='blue'))
    ax.add_patch(patches.Rectangle((0.3, 0.8), 0.4, 0.2, color='orange'))
    ax.text(0.5, 0.85, '+', ha='center', va='center', fontsize=16, color='black')

def draw_resistor(ax):
    ax.add_patch(patches.Rectangle((0.2, 0.4), 0.6, 0.2, color='orange'))
    ax.text(0.5, 0.5, '470Ω', ha='center', va='center', fontsize=10, color='black')
    ax.plot([0.0, 0.2], [0.5, 0.5], color='black')
    ax.plot([0.8, 1.0], [0.5, 0.5], color='black')

def draw_led(ax):
    ax.add_patch(patches.RegularPolygon((0.5, 0.5), numVertices=3, radius=0.2, orientation=0, color='red'))
    ax.plot([0.5, 0.5], [0.3, 0.1], color='black')
    ax.plot([0.45, 0.45], [0.3, 0.1], color='black')
    ax.text(0.5, 0.75, 'LED', ha='center', va='center', fontsize=10, color='black')

def draw_sensor(ax):
    ax.add_patch(patches.Circle((0.5, 0.5), 0.2, color='lightblue'))
    ax.text(0.5, 0.5, '👁', ha='center', va='center', fontsize=14)
    ax.text(0.5, 0.75, 'Sensor', ha='center', va='center', fontsize=10)

def draw_component_grid():
    fig, axs = plt.subplots(2, 2, figsize=(6, 6))
    axs = axs.flatten()

    for ax in axs:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    draw_battery(axs[0])
    draw_resistor(axs[1])
    draw_led(axs[2])
    draw_sensor(axs[3])

    plt.tight_layout()
    plt.show()

draw_component_grid()
