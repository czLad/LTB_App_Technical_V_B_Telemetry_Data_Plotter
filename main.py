"""
Program Name: Satellite Telemetry Plotter
Author: Min Phone Myat Zaw
Created: September 21, 2024
Description:
    This program dynamically plots selected telemetry data for a satellite.
    Users can select up to 3 columns from the dataset to plot, and the program
    will annotate the peak and lowest values for each plot. The plot is displayed
    with dynamic y-axes based on the user's selection.

Usage:
    Run the script and input the column numbers to plot.
    Example: 1, 2, 3 (to plot 3 columns)

Dependencies:
    - matplotlib
    - pandas
    - tkinter

"""

import tkinter as tk
from tkinter import messagebox
from tkinter import font
import time
import matplotlib.pyplot as plt
import pandas as pd

# ------- Class Definition ----------- 

# Annotation_Max_Min object like a  C++ struct all public access members
class Annotation_Max_Min:
    """Class to represent peak and minimum annotations."""
    def __init__(self, peak_xy, min_xy):
        self.peak_xy = peak_xy  # (x, y) coordinates for peak
        self.min_xy = min_xy    # (x, y) coordinates for minimum

# ------- Function definitons ----------- 
        
# Recursively calls annotate_axs_max_min_levels to create annotation levels using plot precedence
# Helper function: annotate_axs_max_min_no_overlap(ax, label, xy, color='black', last_position_above=True, level=1)
def annotate_axs_max_min_levels(ax, col_names, annotation_max_mins, colors, last_position_above=True, level=1):
    if(level!=1):
        last_position_above = annotate_axs_max_min_no_overlap(ax, f'Peak {col_names[level-1]}', xy=annotation_max_mins[level-1].peak_xy, color=colors[level-1], last_position_above=last_position_above, level=level)
        last_position_above = annotate_axs_max_min_no_overlap(ax, f'Lowest {col_names[level-1]}', xy=annotation_max_mins[level-1].min_xy, color=colors[level-1], last_position_above=last_position_above, level=level)
        annotate_axs_max_min_levels(ax, col_names, annotation_max_mins, colors, last_position_above=True, level=level-1)
    else:
        last_position_above = annotate_axs_max_min_no_overlap(ax, f'Peak {col_names[level-1]}', xy=annotation_max_mins[level-1].peak_xy, color=colors[level-1], last_position_above=last_position_above, level=level)
        last_position_above = annotate_axs_max_min_no_overlap(ax, f'Lowest {col_names[level-1]}', xy=annotation_max_mins[level-1].min_xy, color=colors[level-1], last_position_above=last_position_above, level=level)

# Annotates the peaks and lows on a plot without overlapping using plot precedence
def annotate_axs_max_min_no_overlap(ax, label, xy, color='black', last_position_above=True, level=1):
    """Dynamically annotate a point with alternating vertical offset and mirrored arrow."""
    if last_position_above:
        offset_y = -7 * level  # Text below
        xytext = (10, offset_y)
        arrowprops = dict(arrowstyle="wedge,tail_width=0.7", facecolor=color, connectionstyle="arc3,rad=-0.2")
    else:
        offset_y = 7 * level  # Text above
        xytext = (10, offset_y)
        arrowprops = dict(arrowstyle="wedge,tail_width=0.7", facecolor=color, connectionstyle="arc3,rad=0.2")
    
    ax.annotate(label, xy=xy, xytext=xytext, textcoords='offset points', 
                arrowprops=arrowprops, fontsize=8, zorder=13)
    
    return not last_position_above

# Recursively Generates A Suptitle for the Figure
def get_fig_title_string(title_string, col_names=[], col_names_size=1):
    if(len(col_names) != 1):
        # Create a new list without the last element
        new_col_names = col_names[:-1]
        return get_fig_title_string(title_string + " " + col_names[col_names_size-1] + ",", new_col_names, col_names_size=len(col_names)-1)
    else:
        return title_string + " " + col_names[col_names_size-1]

# ---------------------------------------- MAIN ---------------------------- 
# def main():
#     # Plot interactive mode
#     plt.ion()

#     # Load the dataset
#     file_path = './sat_realtime_telemetry.csv'
#     data = pd.read_csv(file_path)
#     # Convert 'Satellite Date/Time UTC' to datetime
#     data['Satellite Date/Time UTC'] = pd.to_datetime(data['Satellite Date/Time UTC'])

#     # Display available columns
#     print("Available columns:")
#     for i, col in enumerate(data.columns):
#         print(f"{i}: {col}")

#     # Game loop begins here
#     while True:

#         # Step 2: Get user input for column selection
#         user_input = input("Enter the column numbers you want to plot (up to 3), separated by commas: (e.g. 1,2,3) \nSatellite Date/Time UTC is by default represented by the X-axis\n")

#         if user_input.lower() == "exit":
#             print("--------Exiting the program---------\n")
#             break

#         # Create selected columns list
#         selected_columns = user_input.split(",")
#         selected_columns = [int(col.strip()) for col in selected_columns if col.strip().isdigit()]

#         # Verify selected columns and remove 'Satellite Date/Time UTC' if chosen
#         if 0 in selected_columns:
#             selected_columns.remove(0)

#         # Step 3: Validate that user has selected 1 to 3 columns
#         if not (1 <= len(selected_columns) <= 3):
#             raise ValueError("You must select between 1 and 3 columns.")
#         # Raise Error if invalid column selected
#         if len(data.columns) in selected_columns:
#             raise ValueError(f"You must select a column between 1 and {len(data.columns)-1}.")

#         # Create a figure and the main axis
#         fig, ax1 = plt.subplots(figsize=(10, 6))  # Adjusted to 10x6 to fit better in smaller windows

#         #ax2 = ax1
        
#         fig.canvas.manager.set_window_title("LTB_sat_realtime_telemetry_plot")  # Set the window title

#         colors = ['tab:blue', 'tab:green', 'tab:red']  # Color for each plot
#         #texts = []  # List to store annotation texts for adjustment
#         last_position_above = True  # To alternate annotation positions

#         annotation_max_mins = []
#         col_names = []

#         overall_min = float('inf')
#         overall_max = float('-inf')

#         # col_name = data.columns[col_idx]
#         overall_min = min(data[data.columns[col_idx]].min() for idx, col_idx in enumerate(selected_columns))
#         overall_max = max(data[data.columns[col_idx]].max() for idx, col_idx in enumerate(selected_columns))

#         # Add some buffer for better visualization
#         margin = (overall_max  - overall_min) * 0.05

#         print("overall_min outside loop: ", overall_min)
#         print("overall_max outside loop: ", overall_max)
#         # need to set overall max min to avoid clipping
#         ax1.set_ylim(overall_min - margin, overall_max + margin)

#         # Plot the selected columns and annotate peaks and lows
#         for idx, col_idx in enumerate(selected_columns):
#             col_name = data.columns[col_idx]
#             col_names.append(col_name)
#             color = colors[idx % len(colors)]  # Assign colors in a loop
#             print("col_idx: ", col_idx)
#             # Determine whether to use ax1 or a twin axis for the plot
#             if idx == 0:
#                 ax = ax1  # First column is plotted on the primary axis
#                 #ax2 = ax
#             else:
#                 ax = ax1.twinx()  # Create a twin axis for the second and third columns

#             # Position the third y-axis if there are three columns
#             if idx == 2:
#                 ax.spines['right'].set_position(('outward', 60))

            
#             print(f"axes{idx}", ax1)
#             # Plot the selected column on the current axis
#             ax.plot(data['Satellite Date/Time UTC'], data[col_name], color=color, label=col_name)
#             ax.set_ylabel(col_name, color=color)

#             # Annotate the peaks and lows for each plot
#             peak_time = data['Satellite Date/Time UTC'].iloc[data[col_name].idxmax()]
#             min_time = data['Satellite Date/Time UTC'].iloc[data[col_name].idxmin()]

#             print("overall_min inside loop: ", overall_min)
#             print("overall_max inside loop: ", overall_max)
#             # not sure why but have to keep setting ylim to avoid clipping and accurate max min representation
#             # suspicion is matplot lip automatically reset set_ylim everytime it is not specified
#             ax.set_ylim(overall_min - margin, overall_max + margin)

#             # Create an Annotation object for the peak and min values
#             annotation_max_min = Annotation_Max_Min(
#                 peak_xy=(peak_time, data[col_name].max()),
#                 min_xy=(min_time, data[col_name].min())
#             )
#             annotation_max_mins.append(annotation_max_min)

#             if idx == len(selected_columns) - 1:
#                 #annotate_max_min_of_layered_axs
#                 annotate_axs_max_min_levels(ax, col_names, annotation_max_mins, colors, last_position_above=last_position_above, level=len(selected_columns))

#         fig.tight_layout(rect=[0,0,1,1])
#         #Suptitle needs to be dynamic
#         fig.suptitle(get_fig_title_string('Satellite Telemetry:', col_names, col_names_size=len(col_names)), fontsize=10, y=0.995)

#         plt.draw()  # Draw the figure without blocking the loop
#         plt.pause(0.001)  # Pause briefly to allow the figure to be updated

# ------- Backend and Plotting Logic ----------- 
        
def plot_selected_columns(data, selected_columns):
    # Create a figure and the main axis
    fig, ax1 = plt.subplots(figsize=(10, 6))  # Adjusted to 10x6 to fit better in smaller windows
    #ax2 = ax1
    
    fig.canvas.manager.set_window_title("LTB_sat_realtime_telemetry_plot")  # Set the window title
    colors = ['tab:blue', 'tab:green', 'tab:red']  # Color for each plot
    #texts = []  # List to store annotation texts for adjustment
    last_position_above = True  # To alternate annotation positions
    annotation_max_mins = []
    col_names = []
    overall_min = float('inf')
    overall_max = float('-inf')
    # col_name = data.columns[col_idx]
    overall_min = min(data[data.columns[col_idx]].min() for idx, col_idx in enumerate(selected_columns))
    overall_max = max(data[data.columns[col_idx]].max() for idx, col_idx in enumerate(selected_columns))
    # Add some buffer for better visualization
    margin = (overall_max  - overall_min) * 0.05
    print("overall_min outside loop: ", overall_min)
    print("overall_max outside loop: ", overall_max)
    # need to set overall max min to avoid clipping
    ax1.set_ylim(overall_min - margin, overall_max + margin)
    # Plot the selected columns and annotate peaks and lows
    for idx, col_idx in enumerate(selected_columns):
        col_name = data.columns[col_idx]
        col_names.append(col_name)
        color = colors[idx % len(colors)]  # Assign colors in a loop
        print("col_idx: ", col_idx)
        # Determine whether to use ax1 or a twin axis for the plot
        if idx == 0:
            ax = ax1  # First column is plotted on the primary axis
            #ax2 = ax
        else:
            ax = ax1.twinx()  # Create a twin axis for the second and third columns
        # Position the third y-axis if there are three columns
        if idx == 2:
            ax.spines['right'].set_position(('outward', 60))
        
        print(f"axes{idx}", ax1)
        # Plot the selected column on the current axis
        ax.plot(data['Satellite Date/Time UTC'], data[col_name], color=color, label=col_name)
        ax.set_ylabel(col_name, color=color)
        # Annotate the peaks and lows for each plot
        peak_time = data['Satellite Date/Time UTC'].iloc[data[col_name].idxmax()]
        min_time = data['Satellite Date/Time UTC'].iloc[data[col_name].idxmin()]
        print("overall_min inside loop: ", overall_min)
        print("overall_max inside loop: ", overall_max)
        # not sure why but have to keep setting ylim to avoid clipping and accurate max min representation
        # suspicion is matplot lip automatically reset set_ylim everytime it is not specified
        ax.set_ylim(overall_min - margin, overall_max + margin)
        # Create an Annotation object for the peak and min values
        annotation_max_min = Annotation_Max_Min(
            peak_xy=(peak_time, data[col_name].max()),
            min_xy=(min_time, data[col_name].min())
        )
        annotation_max_mins.append(annotation_max_min)
        if idx == len(selected_columns) - 1:
            #annotate_max_min_of_layered_axs
            annotate_axs_max_min_levels(ax, col_names, annotation_max_mins, colors, last_position_above=last_position_above, level=len(selected_columns))
    fig.tight_layout(rect=[0,0,1,1])
    #Suptitle needs to be dynamic
    fig.suptitle(get_fig_title_string('Satellite Telemetry:', col_names, col_names_size=len(col_names)), fontsize=10, y=0.995)
    plt.draw()  # Draw the figure without blocking the loop
    plt.pause(0.001)  # Pause briefly to allow the figure to be updated

# ------- UI Frontend with tkinter ----------- 

# Main function
def main():
    def on_submit(event=None):
        user_input = entry_columns.get().strip().lower()
        
        # Exit if user types "exit"
        if user_input.lower() == "exit":
            root.quit()  # Exit the program
            return
        try:
            selected_columns = list(map(int, entry_columns.get().split(',')))
            # Verify selected columns and remove 'Satellite Date/Time UTC' if chosen
            if 0 in selected_columns:
                selected_columns.remove(0)
            # Step 3: Validate that user has selected 1 to 3 columns
            if not (1 <= len(selected_columns) <= 3):
                raise ValueError("You must select between 1 and 3 columns.")
            # Raise Error if invalid column selected
            if len(data.columns) in selected_columns:
                raise ValueError(f"You must select a column between 1 and {len(data.columns)-1}.")
            plot_selected_columns(data, selected_columns)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Load data
    file_path = './sat_realtime_telemetry.csv'
    data = pd.read_csv(file_path)
    data['Satellite Date/Time UTC'] = pd.to_datetime(data['Satellite Date/Time UTC'])

    # Create main window
    root = tk.Tk()
    root.title("Satellite Telemetry Plotter")
    root.geometry("900x600")  # Adjust window size as needed
    root.configure(bg="black")

    # Instructions label
    instructions = ("Enter the column numbers you want to plot (up to 3), separated by commas: (e.g. 1,2,3)\n"
                    "Satellite Date/Time UTC is by default represented by the X-axis")
    instruction_label = tk.Label(root, text=instructions, fg="green", bg="black", font=("Courier", 12, "bold"))
    instruction_label.pack(pady=10)

    # Available Columns label
    label = tk.Label(root, text=f"Available columns (1 to {len(data.columns)-1}):", fg="green", bg="black", font=("Courier", 12, "bold"))
    label.pack()

    # Dynamically generate column names into two sections
    mid_index = len(data.columns) // 2
    columns_left = "\n".join([f"{i}: {col}" for i, col in enumerate(data.columns[:mid_index])])
    columns_right = "\n".join([f"{i}: {col}" for i, col in enumerate(data.columns[mid_index:], start=mid_index)])

    # Create frames for layout organization
    column_frame = tk.Frame(root, bg="black")
    column_frame.pack()

    # Left column
    left_col_label = tk.Label(column_frame, text=columns_left, fg="green", bg="black", font=("Courier", 10), justify="left")
    left_col_label.grid(row=0, column=0, padx=20)

    # Right column
    right_col_label = tk.Label(column_frame, text=columns_right, fg="green", bg="black", font=("Courier", 10), justify="left")
    right_col_label.grid(row=0, column=1, padx=20)

    # Entry field for user input (moved below available columns)
    entry_columns = tk.Entry(root, width=50, font=("Courier", 12), relief="flat", bg="black", fg="green", 
                             highlightthickness=2, highlightbackground="green", highlightcolor="green", 
                             insertbackground="green")  # Green cursor added
    entry_columns.pack(pady=20)
    entry_columns.bind("<Return>", on_submit)  # Bind Enter key to submit

    entry_columns.focus()

    # Submit button with green border and black background
    submit_button_border = tk.Frame(root, highlightbackground="green", highlightthickness=2, bd=0, bg="black")

    submit_button = tk.Button(submit_button_border, text="Submit", command=on_submit, font=("Courier", 12), relief="solid", bg="black", fg="green", 
                          width=10, highlightbackground="green", highlightthickness=2, bd=2, cursor="hand2")
    
    submit_button.pack(pady=10)
    submit_button_border.pack(pady=10)

    # Run the UI loop
    root.mainloop()

# --------- Entry Point --------
if __name__ == "__main__":
    main()