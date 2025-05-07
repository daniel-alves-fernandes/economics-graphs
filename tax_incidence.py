import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interactive, FloatSlider, VBox, Button, Layout
from IPython.display import display


# Fixed equilibrium before tax at (10, 10)
Q_e = 10
P_e = 10
tax_rate = 0.3  # Fixed tax rate at 30%

# Function to compute slopes based on elasticities
def compute_slopes(E_d_abs, E_s, P_e, Q_e):
    b = (P_e / Q_e) / E_d_abs  # Demand slope (positive)
    d = (P_e / Q_e) / E_s      # Supply slope (positive)
    return b, d

# Function to compute intercepts based on slopes and fixed equilibrium
def compute_intercepts(P_e, Q_e, b, d):
    a = P_e + b * Q_e  # Demand intercept
    c = P_e - d * Q_e  # Supply intercept
    return a, c

# Function to find equilibrium with tax
def find_equilibrium_tax(a, c, b, d, tax_rate):
    numerator = a - c * (1 + tax_rate)
    denominator = b + d * (1 + tax_rate)
    Q_e_tax = numerator / denominator
    P_e_tax = a - b * Q_e_tax  # Price consumers pay
    P_s_tax = P_e_tax / (1 + tax_rate)  # Price producers receive
    return Q_e_tax, P_e_tax, P_s_tax

# Function to plot the supply and demand curves with tax and surplus areas
def plot_supply_demand(E_d_abs=1, E_s=1):
    # Compute slopes based on elasticities
    b, d = compute_slopes(E_d_abs, E_s, P_e, Q_e)

    # Compute intercepts based on slopes and fixed equilibrium
    a, c = compute_intercepts(P_e, Q_e, b, d)

    # Define fixed quantity range from 0 to 20
    Q = np.linspace(0, 20, 1000)

    # Demand and Supply curves
    Pd = a - b * Q
    Ps = c + d * Q
    # Supply curve with tax (for plotting purposes)
    Ps_tax = Ps * (1 + tax_rate)

    # Find equilibrium with tax
    Qe_tax, Pe_tax, Ps_tax_eq = find_equilibrium_tax(a, c, b, d, tax_rate)

    # Prepare the plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Set aspect ratio to 1:1
    ax.set_aspect('equal', adjustable='box')

    # Plot Demand and Supply curves
    ax.plot(Q, Pd, label='Demand', color='blue')
    ax.plot(Q, Ps, label='Supply', color='green')
    ax.plot(Q, Ps_tax, label='Supply with Tax', color='red')

    # Mark equilibrium points
    if 0 <= Q_e <= 20 and 0 <= P_e <= 20:
        ax.plot(Q_e, P_e, 'ko', label='Equilibrium without Tax')
        # Add dashed horizontal line from x=0 to x=Q_e at P=Pe
        ax.plot([0, Q_e], [P_e, P_e], color='black', linestyle='--', linewidth=1)
    else:
        print("Equilibrium without tax is outside the plotting range.")

    if 0 <= Qe_tax <= 20 and 0 <= Pe_tax <= 20:
        ax.plot(Qe_tax, Pe_tax, 'ro', label='Equilibrium with Tax')
    else:
        print("Equilibrium with tax is outside the plotting range.")

    # Fill Consumer Surplus
    if 0 <= Qe_tax <= 20 and 0 <= Pe_tax <= 20:
        Q_cs = Q[Q <= Qe_tax]
        Pd_cs = Pd[Q <= Qe_tax]
        ax.fill_between(Q_cs, Pe_tax, Pd_cs, color='blue', alpha=0.3, label='Consumer Surplus')

    # Fill Producer Surplus
    if 0 <= Qe_tax <= 20 and 0 <= Ps_tax_eq <= 20:
        Q_ps = Q[Q <= Qe_tax]
        Ps_ps = Ps[Q <= Qe_tax]
        ax.fill_between(Q_ps, Ps_ps, Ps_tax_eq, color='green', alpha=0.3, label='Producer Surplus')

    # Fill Government Revenue
    if 0 <= Qe_tax <= 20 and 0 <= Pe_tax <= 20 and 0 <= Ps_tax_eq <= 20:
        ax.fill_between([0, Qe_tax], Ps_tax_eq, Pe_tax, color='red', alpha=0.3, label='Government Revenue')

    # Fill Deadweight Loss
    if 0 <= Q_e <= 20 and 0 <= Qe_tax <= 20 and Qe_tax < Q_e:
        Q_dwl = Q[(Q >= Qe_tax) & (Q <= Q_e)]
        Pd_dwl = Pd[(Q >= Qe_tax) & (Q <= Q_e)]
        Ps_dwl = Ps[(Q >= Qe_tax) & (Q <= Q_e)]
        ax.fill_between(Q_dwl, Ps_dwl, Pd_dwl, color='grey', alpha=0.5, label='Deadweight Loss')

    # Labels and titles
    ax.set_xlabel('Quantity')
    ax.set_ylabel('Price')
    ax.set_title('Supply and Demand with Tax (Tax Rate Fixed at 30%)')
    ax.grid(True)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)

    # Set x and y ticks from 0 to 20 with intervals of 2
    ax.set_xticks(np.arange(0, 21, 2))
    ax.set_yticks(np.arange(0, 21, 2))

    # Move legend outside the plot area
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # Adjust layout to make room for the legend and maintain aspect ratio
    plt.subplots_adjust(right=0.75)
    plt.show()

# Create interactive sliders for elasticities with adjusted layouts
Ed_default = 2  # Default value for Elasticity of Demand (absolute value)
Es_default = 2   # Default value for Elasticity of Supply

Ed_slider = FloatSlider(
    min=0.1, max=5, step=0.1, value=Ed_default,
    description='Elasticity of Demand',
    style={'description_width': 'initial'},
    layout=Layout(width='400px')
)
Es_slider = FloatSlider(
    min=0.1, max=5, step=0.1, value=Es_default,
    description='Elasticity of Supply',
    style={'description_width': 'initial'},
    layout=Layout(width='400px')
)

# Function to reset sliders to default values
def reset_sliders(button):
    Ed_slider.value = Ed_default
    Es_slider.value = Es_default

# Create a Refresh button
reset_button = Button(description='Refresh', button_style='info', tooltip='Reset sliders to default values')

# Assign the reset function to the button's on_click event
reset_button.on_click(reset_sliders)

# Layout of sliders and button
controls = VBox([Ed_slider, Es_slider, reset_button])

# Interactive plot
interactive_plot = interactive(
    plot_supply_demand,
    E_d_abs=Ed_slider,
    E_s=Es_slider
)

reset_button


interactive_plot