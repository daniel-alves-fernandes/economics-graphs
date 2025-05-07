import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive, FloatSlider, Button, VBox, Layout
from IPython.display import display

# Fixed Parameters
i_fixed = 100  # Fixed Investment for AD Fixed

# Function to compute Aggregate Demand (AD)
def compute_AD(Y, c0, MPC):
    return c0 + MPC * Y

# Function to find equilibrium output where Y = AD
def find_equilibrium(i, c0, MPC):
    if (1 - MPC) <= 0:
        return np.inf  # Avoid division by zero or negative
    return (i + c0) / (1 - MPC)

# Plotting Function
def plot_AD(i_variable, MPC):
    # Fixed axes limits
    Y_min, Y_max = 0, 600
    AD_min, AD_max = 0, 600
    Y = np.linspace(Y_min, Y_max, 500)

    # Recalculate c0_fixed based on MPC to ensure AD Fixed passes through (250, 250)
    c0_fixed_current = 250 * (1 - MPC)

    # Compute AD_fixed
    AD_fixed = compute_AD(Y, c0_fixed_current, MPC)

    # Compute AD_variable: AD_variable = AD_fixed + (i_variable - i_fixed)
    delta_i = i_variable - i_fixed
    AD_variable = AD_fixed + delta_i

    # Compute Equilibrium Points
    Y_fixed_eq = 250  # Always at (250,250)
    Y_variable_eq = 250 + (delta_i) / (1 - MPC) if (1 - MPC) != 0 else np.inf

    # Initialize Plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot Equilibrium Line Y = AD (45-degree line)
    ax.plot(Y, Y, label='Equilibrium Line (Y = AD)', color='black', linestyle='--')

    # Plot AD Fixed Curve
    ax.plot(Y, AD_fixed, label=f'AD Fixed (i = {i_fixed})', color='blue', linewidth=2)

    # Plot AD Variable Curve
    ax.plot(Y, AD_variable, label=f'AD Variable (i = {i_variable})', color='red', linewidth=2)

    # Plot Equilibrium for AD Fixed
    ax.plot(Y_fixed_eq, Y_fixed_eq, 'bo')  # Blue circle without label
    # Add label "250" above the Fixed Equilibrium Point
    ax.annotate('250',
                xy=(Y_fixed_eq, Y_fixed_eq),
                xytext=(0, 10),  # 10 points above the point
                textcoords='offset points',
                ha='center',
                va='bottom',
                fontsize=10,
                color='blue')

    # Plot Equilibrium for AD Variable if within Y range
    if Y_min <= Y_variable_eq <= Y_max:
        ax.plot(Y_variable_eq, Y_variable_eq, 'ro')  # Red circle without label
        # Add label for Variable Equilibrium Point directly above the point
        ax.annotate(f'{Y_variable_eq:.0f}',
                    xy=(Y_variable_eq, Y_variable_eq),
                    xytext=(0, 10),  # 10 points above the point
                    textcoords='offset points',
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color='red')

    # Labels and Title
    ax.set_xlabel('Output (Y)', fontsize=14)
    ax.set_ylabel('Aggregate Demand (AD)', fontsize=14)
    ax.set_title('Aggregate Demand and Equilibrium Output', fontsize=16)
    ax.grid(True)

    # Set Fixed Axes Limits
    ax.set_xlim(Y_min, Y_max)
    ax.set_ylim(AD_min, AD_max)

    # Legend
    # Only include meaningful labels in the legend
    handles, labels = ax.get_legend_handles_labels()
    # Remove empty labels (equilibrium points have no labels)
    handles = [h for h, l in zip(handles, labels) if l]
    labels = [l for l in labels if l]
    ax.legend(handles, labels, loc='upper left')

    plt.show()

# Default Slider Values
i_default = 100
MPC_default = 0.6

# Create Sliders for Investment (i_variable) and MPC
i_slider = FloatSlider(
    value=i_default,
    min=0,
    max=200,
    step=1,
    description='Investment (i):',
    style={'description_width': 'initial'},
    layout=Layout(width='400px')
)

MPC_slider = FloatSlider(
    value=MPC_default,
    min=0,
    max=1,
    step=0.01,
    description='MPC:',
    style={'description_width': 'initial'},
    layout=Layout(width='400px')
)

# Function to Reset Sliders to Default Values
def reset_sliders(button):
    i_slider.value = i_default
    MPC_slider.value = MPC_default

# Create a Reset Button
reset_button = Button(
    description='Reset',
    button_style='info',
    tooltip='Reset sliders to default values',
    layout=Layout(width='100px')
)
reset_button.on_click(reset_sliders)

# Arrange Sliders and Button in a Vertical Box
controls = VBox([i_slider, MPC_slider, reset_button])

# Create the Interactive Plot
interactive_plot = interactive(
    plot_AD,
    i_variable=i_slider,
    MPC=MPC_slider
)


reset_button

interactive_plot