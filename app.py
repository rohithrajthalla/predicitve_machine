import streamlit as st
import pandas as pd
import pickle

# Title
st.title("Predictive Maintenance Web App")

# Sidebar for user inputs
st.sidebar.header("Input Machine Parameters")
st.sidebar.markdown("### Parameter Descriptions")
st.sidebar.markdown("""
- **TWF**: Tool Wear Failure (1 = Failure, 0 = No Failure)
- **HDF**: Heat Dissipation Failure (1 = Failure, 0 = No Failure)
- **PWF**: Power Failure (1 = Failure, 0 = No Failure)
- **OSF**: Overstrain Failure (1 = Failure, 0 = No Failure)
- **RNF**: Random Failure (1 = Failure, 0 = No Failure)
- **Product ID**: A unique ID for each machine being monitored (like a serial number).
- **Type_L**: Binary indicator for one category of machine (1 = Machine belongs to Type L).
- **Type_M**: Binary indicator for another category of machine (1 = Machine belongs to Type M).
""")


# Function to collect user inputs
def user_input_features():
    air_temp = st.sidebar.slider('Air Temperature [K]', 295.0, 305.0, 300.0)
    process_temp = st.sidebar.slider('Process Temperature [K]', 305.0, 315.0, 310.0)
    rpm = st.sidebar.slider('Rotational Speed [rpm]', 1200, 3000, 1500)
    torque = st.sidebar.slider('Torque [Nm]', 10.0, 100.0, 40.0)
    tool_wear = st.sidebar.slider('Tool Wear [min]', 0, 300, 100)
    
    # Additional machine failure parameters
    TWF = st.sidebar.slider('TWF', 0, 1, 0)
    HDF = st.sidebar.slider('HDF', 0, 1, 0)
    PWF = st.sidebar.slider('PWF', 0, 1, 0)
    OSF = st.sidebar.slider('OSF', 0, 1, 0)
    RNF = st.sidebar.slider('RNF', 0, 1, 0)
    
    # Categorical variables
    product_id = st.sidebar.selectbox('Product ID', [7003, 1003, 1004, 1005, 1006])
    type_l = st.sidebar.selectbox('Type_L', [True, False])
    type_m = st.sidebar.selectbox('Type_M', [True, False])

    data = {
        'Air_temperature_K': air_temp,
        'Process_temperature_K': process_temp,
        'Rotational_speed_rpm': rpm,
        'Torque_Nm': torque,
        'Tool_wear_min': tool_wear,
        'TWF': TWF,
        'HDF': HDF,
        'PWF': PWF,
        'OSF': OSF,
        'RNF': RNF,
        'Product_ID': product_id,
        'Type_L': type_l,
        'Type_M': type_m
    }

    return pd.DataFrame(data, index=[0])

# Get user input
input_df = user_input_features()

# Display user input
st.subheader('User Input:')
st.write(input_df)

# Load the saved XGBoost model
try:
    with open('xgb_model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Ensure input columns match the order of the training data
    input_df = input_df[model.get_booster().feature_names]

    # Predict using the model
    if st.button('Predict'):
        prediction = model.predict(input_df)
        st.subheader('Prediction:')
        if prediction[0] == 1:
            st.write('Machine Failure')
            st.write("Possible reasons for failure:")
            # Check the relevant features for failure
            if input_df['TWF'].values[0] == 1:
                st.write("- Tool Wear Failure")
            if input_df['HDF'].values[0] == 1:
                st.write("- Heat Dissipation Failure")
            if input_df['PWF'].values[0] == 1:
                st.write("- Power Failure")
            if input_df['OSF'].values[0] == 1:
                st.write("- Overstrain Failure")
            if input_df['RNF'].values[0] == 1:
                st.write("- Random Failure")
        else:
            st.write('No Machine Failure')
            st.write("The machine is operating within normal parameters. All critical factors are within safe limits.")

except FileNotFoundError:
    st.error("Model not found. Please upload 'xgb_model.pkl' to the repository.")
