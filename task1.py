# Name: Sriharshith Bala
# ID: 2026AAPS0225H

# Importing all necessary libraries
import csv
import os
import matplotlib.pyplot as plt # type: ignore

# Function to apply low-pass filter on realtime data
# alpha is the smoothing factor (0<alpha<1), threshold is the maximum allowed change between consecutive readings
def low_pass_filter(current_value, previous_value, alpha=0.3, threshold=100.0):
    # Return the current value if there is no previous value to compare with
    if previous_value is None:
        return current_value
    # If difference exceeds threshold, return previous value to avoid sudden spikes
    if abs(current_value - previous_value) > threshold:
        return previous_value
    # Apply the low-pass filter formula to smooth the data
    return alpha * current_value + (1 - alpha) * previous_value

# Function to plot the data
def plot(x, original_y, filtered_y):
    # Clear the previous plot
    ax.clear()
    # Plotting the original and filtered readings on the graph
    ax.plot(x, original_y, label="Original Readings", color="red", linewidth=0.75)
    ax.plot(x, filtered_y, label="Filtered Readings", color="green", linewidth=2.5)
    # Setting the title, labels and legend for the graph
    ax.set_title("Depth VS Time Graph")
    ax.set_xlabel("Time")
    ax.set_ylabel("Depth")
    ax.legend()
    # Text indicating how to stop the graph
    ax.text(
        0.98, 0.03, "Press 'q' to stop",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color="black",
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"}
    )
    # Pause to update the plot
    # plt.pause(0.1)
    # Live updation of canvas
    fig.canvas.draw()
    fig.canvas.flush_events()

if __name__ == "__main__":
    # Turn on interactive mode
    plt.ion()
    # Create a figure and axis for plotting
    fig,ax = plt.subplots()
    stop_requested = False

    # Function to stop the graph when 'q' is pressed
    def stop_on_key(event):
        if event.key and event.key.lower() == "q":
            stop_requested = True

    # Connect the key press event to the stop_on_key function
    fig.canvas.mpl_connect("key_press_event", stop_on_key)
    # Setting the title and labels for the graph
    ax.set_title("Depth VS Time Graph")
    ax.set_xlabel("Time")
    ax.set_ylabel("Depth")
    # Creating empty lists to store time, depth and filtered depth values
    times = []
    depths = []
    filtered_depths = []
    # Variable to store the previous filtered depth value, initialized to None later changed to float type (used in low_pass_filter function)
    previous_filtered_depth = None

    # Getting the path of the CSV file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'Depth Data.csv')

    # Reading the CSV file and plotting the data
    with open(csv_path, newline='') as csvfile:
        read = csv.reader(csvfile, delimiter=',')
        # Skip the header row
        next(read)
        for row in read:
            if row[1] == '#VALUE!':
                # Skip the next row if the current row has '#VALUE!'
                next(read)
            else:
                # Append time & depth values to the list
                times.append(float(row[0].strip()))
                depths.append(float(row[1].strip()))
                # Storing the filtered depth value using low_pass_filter function for the next iteration
                previous_filtered_depth = low_pass_filter(depths[-1], previous_filtered_depth)
                # Appending the filtered depth value to the list
                filtered_depths.append(previous_filtered_depth)
                # Update the plot with new data
                plot(times, depths, filtered_depths)
                # Process graph events, including key presses
                plt.pause(0.01)
                if stop_requested:
                    break

    plt.ioff()  # Turn off interactive mode
    plt.show()  # Show the final plot