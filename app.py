import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.linear_model import LinearRegression

# Load the dataset
df_filtered = pd.read_csv('climate_data.csv')

# Create a Tkinter window
root = tk.Tk()
root.title("Climate Data Visualization")

# Frame for inputs and button
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Input fields and labels for start year and end year
ttk.Label(input_frame, text="Start Year:").grid(row=0, column=0, padx=5, pady=5)
start_year_entry = ttk.Entry(input_frame)
start_year_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="End Year:").grid(row=1, column=0, padx=5, pady=5)
end_year_entry = ttk.Entry(input_frame)
end_year_entry.grid(row=1, column=1, padx=5, pady=5)

# Function to handle mouse wheel scrolling
def on_mousewheel(event):
    if event.num == 4 or event.delta > 0:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5 or event.delta < 0:
        canvas.yview_scroll(1, "units")

# Function to filter data and plot the graphs
def plot_data():
    try:
        start_year = int(start_year_entry.get())
        end_year = int(end_year_entry.get())
        if start_year < 1990 or end_year > 2025 or start_year >= end_year:
            raise ValueError

        # Filter the dataset based on the user input
        df = df_filtered[(df_filtered['Year'] >= start_year) & (df_filtered['Year'] <= end_year)]

        # Check if the filtered dataset is empty
        if df.empty:
            messagebox.showerror("Error", f"No data available for the year range {start_year} to {end_year}.")
        else:
            # Extract features (X) and target variables (y)
            X = df[['Year']]
            y_temperature = df['Temperature']
            y_rain = df['Rainfall']
            y_humidity = df['Humidity']

            # Create and fit a linear regression model for temperature
            model_temperature = LinearRegression()
            model_temperature.fit(X, y_temperature)
            y_pred_temperature = model_temperature.predict(X)

            # Create and fit a linear regression model for rain
            model_rain = LinearRegression()
            model_rain.fit(X, y_rain)
            y_pred_rain = model_rain.predict(X)

            # Create and fit a linear regression model for humidity
            model_humidity = LinearRegression()
            model_humidity.fit(X, y_humidity)
            y_pred_humidity = model_humidity.predict(X)

            # Plotting temperature, rainfall, and humidity with subplots
            fig, axs = plt.subplots(3, 1, figsize=(12, 15))

            # Temperature subplot
            axs[0].scatter(df['Year'], y_temperature, color='black', label='Actual Temperature')
            axs[0].plot(df['Year'], y_pred_temperature, color='blue', linewidth=2, label='Temperature Prediction')
            axs[0].set_xlabel('Year')
            axs[0].set_ylabel('Temperature (°C)')
            axs[0].set_title(f'Temperature Data from {start_year} to {end_year}')
            axs[0].legend()
            axs[0].grid(True)

            # Rainfall subplot
            axs[1].scatter(df['Year'], y_rain, color='red', label='Actual Rainfall')
            axs[1].plot(df['Year'], y_pred_rain, color='green', linewidth=2, label='Rainfall Prediction')
            axs[1].set_xlabel('Year')
            axs[1].set_ylabel('Rainfall (mm)')
            axs[1].set_title(f'Rainfall Data from {start_year} to {end_year}')
            axs[1].legend()
            axs[1].grid(True)

            # Humidity subplot
            axs[2].scatter(df['Year'], y_humidity, color='cyan', label='Actual Humidity')
            axs[2].plot(df['Year'], y_pred_humidity, color='magenta', linewidth=2, label='Humidity Prediction')
            axs[2].set_xlabel('Year')
            axs[2].set_ylabel('Humidity (%)')
            axs[2].set_title(f'Humidity Data from {start_year} to {end_year}')
            axs[2].legend()
            axs[2].grid(True)

            # Adjust layout for better spacing
            plt.tight_layout()

            # Embed the plot into the tkinter window
            canvas_plot = FigureCanvasTkAgg(fig, master=second_frame)
            canvas_plot.draw()
            canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid year range from 1990 to 2025, with start year less than end year.")

# Plot button
plot_button = ttk.Button(input_frame, text="Plot Data", command=plot_data)
plot_button.grid(row=2, columnspan=2, pady=10)

# Frame for the canvas and scrollbar
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas in the frame
canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas
second_frame = ttk.Frame(canvas)

# Add that new frame to a window in the canvas
canvas.create_window((0, 0), window=second_frame, anchor="nw")

# Bind mousewheel events
root.bind_all("<MouseWheel>", on_mousewheel)  # Windows and MacOS
root.bind_all("<Button-4>", on_mousewheel)    # Linux
root.bind_all("<Button-5>", on_mousewheel)    # Linux

# Run the Tkinter event loop
root.mainloop()
