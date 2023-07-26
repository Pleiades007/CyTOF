import streamlit as st

# Function to convert decimal hours to hours and minutes
def convert_hours(decimal_hours):
    minutes, seconds = divmod(decimal_hours*3600, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes

# Title
st.title('CyTOF Calculator')

# User inputs
cell_concentration = st.number_input('Enter cell concentration per ml (e.g., for 1.2e6, enter 1.2)', min_value=0.0)
exponent = st.number_input('Enter the exponent for the cell concentration (e.g., for 1.2e6, enter 6)', min_value=0)
cell_concentration *= 10 ** exponent  # Apply the exponent to get the actual cell concentration

volume_counted = st.number_input('Enter volume counted in ul', min_value=0.0, step=0.1)
sample_percent = st.number_input('Enter what percent of the total sample the counted sample is (e.g., for 50%, enter 50)', min_value=0.0, max_value=100.0)
desired_rate = st.number_input('Enter desired rate of cells/second', min_value=0.0)
if desired_rate > 400:
    st.error('WARNING: Rates above 400 increase doublets!')
anticipated_efficiency = st.slider('Enter anticipated machine efficiency (%)', min_value=0, max_value=100, value=65)

# Calculate total cells counted
total_cells_counted = cell_concentration * volume_counted / 1000  # Dividing by 1000 to convert volume_counted from ul to ml

# Display total cells counted
st.write(f'The total number of cells in the counted volume is: {total_cells_counted:.2e}')

# Calculate total cells in the sample
total_cells_sample = total_cells_counted / (sample_percent / 100)

# Display total cells in the sample
st.write(f'The total number of cells in the sample is: {total_cells_sample:.2e}')

# Calculate resuspension volume for 10X stock
stock_volume = total_cells_counted / (10 * desired_rate * 2) * (anticipated_efficiency / 100)  # Adjust the volume based on the anticipated machine efficiency

# Display result
st.markdown(f'Resuspend in <span style="color:red;font-weight:bold">{stock_volume:.0f}</span> ul to get a 10X stock. This volume is adjusted based on an anticipated machine efficiency of {anticipated_efficiency}%.', unsafe_allow_html=True)

# Inputs for adjusting sample
observed_rate = st.number_input('Enter observed rate of cells/second (after diluting 1:10)', min_value=0.0)

# Calculate adjustment
if observed_rate > desired_rate:
    dilution_volume = round((observed_rate / desired_rate - 1) * 1000)  # 1000 because we are adjusting 1 ml of diluted sample
    st.markdown(f'Add <span style="color:green;font-weight:bold">{dilution_volume:.0f}</span> ul of diluent to the 1 ml of diluted sample', unsafe_allow_html=True)
    efficiency = (observed_rate / desired_rate * 100) * (anticipated_efficiency / 100)
elif observed_rate < desired_rate:
    adjustment_stock_volume = round((desired_rate / observed_rate - 1) * 100)  # adjustments are for a 1 ml volume of the 1X sample
    st.markdown('<span style="color:green;font-weight:bold">Add ' + str(adjustment_stock_volume) + ' ul of 10X stock to the 1 ml of diluted sample</span>', unsafe_allow_html=True)
    efficiency = (observed_rate / desired_rate * 100) * (anticipated_efficiency / 100)
else:
    st.write('No adjustment needed')
    efficiency = anticipated_efficiency

# Display efficiency
st.markdown(f'The machine efficiency is: <span style="color:red;font-weight:bold">{efficiency:.0f}%</span>', unsafe_allow_html=True)

# Calculate and display the total run time
run_time_hours = (total_cells_sample / (desired_rate)) / 3600
hours, minutes = convert_hours(run_time_hours)
st.write(f'The total sample will take {hours} hours and {minutes} minutes to run')
