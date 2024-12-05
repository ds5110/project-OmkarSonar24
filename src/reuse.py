import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# Function to render a plot from the given path
def render_plot(plot_path):
    """
    Render the plot from the given file path.
    Args:
        plot_path (str): Path to the plot image file.
    """
    if os.path.exists(plot_path):
        img = mpimg.imread(plot_path)
        plt.imshow(img)
        plt.axis('off')  # Hide axes
        plt.show()
    else:
        print(f"Error: Plot path does not exist: {plot_path}")


# Function to interactively select and render plots
def plot_selection_terminal(plot_paths):
    """
    Allow terminal-based selection of plots to render.
    Args:
        plot_paths (dict): Dictionary mapping plot options to file paths.
    """
    while True:
        print("\nPlease select the plot option:")
        for idx, (key, path) in enumerate(plot_paths.items(), 1):
            print(f"{idx}. {key.capitalize()} Plot")
        print("x. Exit")
        
        choice = input("Enter your option (number or x): ").strip().lower()
        
        if choice == "x":
            print("Exiting...")
            break
        elif choice.isdigit() and int(choice) in range(1, len(plot_paths) + 1):
            key = list(plot_paths.keys())[int(choice) - 1]
            render_plot(plot_paths[key])
        else:
            print("Invalid option selected. Please try again.")
