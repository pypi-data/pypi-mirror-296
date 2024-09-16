import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import matplotlib.gridspec as gridspec
from matplotlib import rcParams

# Set modern style
rcParams.update({
    "font.size": 12,
    "font.family": "DejaVu Sans",
    "axes.facecolor": "#f2f2f2",
    "axes.edgecolor": "#cccccc",
    "axes.grid": True,
    "grid.color": "#cccccc",
    "grid.linestyle": "--",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "figure.facecolor": "#f2f2f2",
})

# Grid size
GRID_SIZE = 50
simulation_started = False

# Initialize the grid with dead cells (all 0s)
def initialize_empty_grid(size):
    """
    Initialize a grid with all dead cells.
    Args:
        size (int): The size of the grid (size x size).
    Returns:
        np.array: Initialized grid.
    """
    return np.zeros((size, size), dtype=int)

# Predefined initial conditions
def add_glider(grid):
    """
    Add a 'Glider' pattern to the grid.
    Args:
        grid (np.array): The grid to modify.
    """
    glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
    grid[1:4, 1:4] = glider
    return grid

def add_blinker(grid):
    """
    Add a 'Blinker' pattern (oscillator) to the grid.
    Args:
        grid (np.array): The grid to modify.
    """
    blinker = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
    grid[25:28, 25:28] = blinker
    return grid

def add_still_life_block(grid):
    """
    Add a still life block pattern (2x2) to the grid.
    Args:
        grid (np.array): The grid to modify.
    """
    block = np.array([[1, 1], [1, 1]])
    grid[10:12, 10:12] = block
    return grid

# Update the grid based on Conway's Game of Life rules
def update_grid(grid):
    """
    Update the grid following Conway's Game of Life rules.
    Args:
        grid (np.array): Current grid.
    Returns:
        np.array: Updated grid for the next step.
    """
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            live_neighbors = np.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            if grid[i, j] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[i, j] = 0  # Dies
            else:
                if live_neighbors == 3:
                    new_grid[i, j] = 1  # Becomes alive
    return new_grid

def on_click(event, grid, ax, fig):
    """
    Handle click events to toggle cell states between alive and dead.
    Args:
        event: Matplotlib click event.
        grid (np.array): The grid.
        ax: Axis for plotting.
        fig: The figure.
    """
    if event.inaxes == ax and not simulation_started:
        x, y = int(event.xdata), int(event.ydata)
        grid[y, x] = 1 - grid[y, x]  # Toggle between alive and dead
        ax.clear()
        ax.imshow(grid, cmap='Blues')  # Updated color map for a modern look
        ax.grid(True, color='#d3d3d3', linestyle='--', linewidth=0.5)  # Light grid lines
        ax.set_xticks(np.arange(-0.5, GRID_SIZE, 1))
        ax.set_yticks(np.arange(-0.5, GRID_SIZE, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        fig.canvas.draw()

def on_button_click(event, grid, fig):
    """
    Handle the 'Start' button click event to begin the simulation.
    Args:
        event: Button click event.
        grid (np.array): The grid.
        fig: The figure to close.
    """
    global simulation_started
    simulation_started = True
    plt.close(fig)

def animate(grid, steps=100):
    """
    Animate the Game of Life.
    Args:
        grid (np.array): The initial grid.
        steps (int): The number of steps to animate.
    """
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#f2f2f2')  # Light background for the plot

    def update(frame):
        nonlocal grid
        grid = update_grid(grid)
        ax.clear()
        ax.imshow(grid, cmap='Blues')  # Updated color map
        ax.grid(True, color='#d3d3d3', linestyle='--', linewidth=0.5)  # Light grid lines
        ax.set_xticks(np.arange(-0.5, GRID_SIZE, 1))
        ax.set_yticks(np.arange(-0.5, GRID_SIZE, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title(f"Step {frame}", fontsize=14, color='#333333')

    ani = animation.FuncAnimation(fig, update, frames=steps, repeat=False)
    plt.show()

def setup_initial_configuration(grid):
    """
    Set up the grid configuration interactively.
    Args:
        grid (np.array): The initial grid.
    Returns:
        np.array: Modified grid with the setup.
    """
    fig = plt.figure(figsize=(10, 8))
    gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])  # GridSpec for better layout
    ax = fig.add_subplot(gs[0])  # Grid plot on top

    ax.imshow(grid, cmap='Blues')  # Updated color map
    ax.grid(True, color='#d3d3d3', linestyle='--', linewidth=0.5)  # Light grid lines
    ax.set_xticks(np.arange(-0.5, GRID_SIZE, 1))
    ax.set_yticks(np.arange(-0.5, GRID_SIZE, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title("Click to toggle cells. Press Start to begin simulation.", fontsize=14, color='#333333')

    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, grid, ax, fig))

    # Button area (bottom)
    button_ax = fig.add_subplot(gs[1])
    button_ax.axis('off')  # Hide axis for buttons panel

    # Adjust button sizes and positions for better layout
    button_width = 0.15
    button_height = 0.08

    # Glider button
    glider_ax = plt.axes([0.05, 0.02, button_width, button_height])
    glider_button = Button(glider_ax, 'Glider', color='#4CAF50', hovercolor='#388E3C')
    glider_button.on_clicked(lambda event: (add_glider(grid), ax.imshow(grid, cmap='Blues'), fig.canvas.draw()))

    # Blinker button
    blinker_ax = plt.axes([0.25, 0.02, button_width, button_height])
    blinker_button = Button(blinker_ax, 'Blinker', color='#03A9F4', hovercolor='#0288D1')
    blinker_button.on_clicked(lambda event: (add_blinker(grid), ax.imshow(grid, cmap='Blues'), fig.canvas.draw()))

    # Block button
    block_ax = plt.axes([0.45, 0.02, button_width, button_height])
    block_button = Button(block_ax, 'Block', color='#FFEB3B', hovercolor='#FBC02D')
    block_button.on_clicked(lambda event: (add_still_life_block(grid), ax.imshow(grid, cmap='Blues'), fig.canvas.draw()))

    # Start button
    start_ax = plt.axes([0.75, 0.02, button_width, button_height])
    start_button = Button(start_ax, 'Start', color='#FF5722', hovercolor='#E64A19')
    start_button.on_clicked(lambda event: on_button_click(event, grid, fig))

    plt.tight_layout()  # Make sure everything fits nicely
    plt.show()

    return grid

def run_game():
    """
    Run the Game of Life simulation.
    """
    grid = initialize_empty_grid(GRID_SIZE)  # Set up an empty grid
    grid = setup_initial_configuration(grid)  # Let user set up the initial configuration

    if simulation_started:
        animate(grid, steps=200)  # Start animation once configuration is complete

def main():
    """
    Main function for running the Game of Life.
    """
    print("Welcome to the Interactive Game of Life!")
    run_game()

if __name__ == "__main__":
    main()
