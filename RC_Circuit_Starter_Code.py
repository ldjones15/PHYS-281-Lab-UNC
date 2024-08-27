# -*- coding: utf-8 -*-
"""Untitled15.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EBq1RiPJStBK8HWBnGL88oV20Gerbk5S
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def fit_rc_circuit(csv_file, time_spacing, min_time, max_time, initial_guess):
    """
    Perform a nonlinear fit on RC circuit data to extract the time constant (tau).

    Parameters:
    - csv_file: str, the name of the CSV file containing the RC circuit data.
    - time_spacing: float, the time increment between data points (in seconds).
    - min_time: float, the minimum time to start fitting (in seconds).
    - max_time: float, the maximum time to end fitting (in seconds).
    - initial_guess: list, initial guess for the fitting parameters [V0, tau, V_offset].

    Returns:
    - tau: float, the fitted time constant.
    - tau_error: float, the estimated error in the fitted time constant.
    """

    # Load the data
    data = pd.read_csv(csv_file) #could also change to excel file using pd.read_excel

    # Convert the first column to time using the given time spacing
    data['Time (s)'] = pd.to_numeric(data.index * time_spacing, errors='coerce')

    # Select the portion of the data based on the given min and max times
    fitting_data = data[(data['Time (s)'] >= min_time) & (data['Time (s)'] <= max_time)]

    # Check if fitting data is empty
    if fitting_data.empty:
        raise ValueError("No data points found within the specified time range. Please check your min_time and max_time values.")

    time = fitting_data['Time (s)'].values
    voltage = fitting_data['Voltage (V)'].values

    # Define the exponential decay function for the RC circuit
    def exponential_decay(t, V0, tau, V_offset):
        return V0 * np.exp(-t / tau) + V_offset

    # Perform the nonlinear fit
    popt, pcov = curve_fit(exponential_decay, time, voltage, p0=initial_guess)

    # Extract the fitted parameters and calculate the standard deviation (error)
    V0_fitted, tau_fitted, V_offset_fitted = popt
    tau_error = np.sqrt(np.diag(pcov))[1]  # The standard deviation of the tau parameter

    # Output the fitted tau and its error
    return tau_fitted, tau_error

# Example usage
# csv_file = 'your_data.csv'  # Replace with the name of your CSV file
# time_spacing = 0.000002  # Replace with your time spacing (2 microseconds in this example)
# min_time = 0.001  # Replace with the minimum time for fitting
# max_time = 0.01  # Replace with the maximum time for fitting
# initial_guess = [5.0, 0.004, 0.0]  # Replace with your initial guesses for V0, tau, V_offset

# tau, tau_error = fit_rc_circuit(csv_file, time_spacing, min_time, max_time, initial_guess)
# print(f"Fitted Tau: {tau} s")
# print(f"Error in Tau: {tau_error} s")