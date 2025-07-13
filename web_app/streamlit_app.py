# web_app/streamlit_app.py

import streamlit as st
import requests
import pandas as pd

# Define the URL of our FastAPI backend
#BACKEND_URL = "http://127.0.0.1:8000/calculate/"

BACKEND_URL = "https://arch-calculator-api.onrender.com/calculate/" # <-- PASTE YOUR RENDER URL HERE


# --- Page Configuration ---
st.set_page_config(
    page_title="QS Materials Calculator",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Architectural Materials Calculator")
st.write("This application calculates the required cement, sand, and gravel for a list of structural elements.")

# --- Session State Initialization ---
# Session state is used to store variables across user interactions.
if 'elements' not in st.session_state:
    st.session_state.elements = []
if 'deductions' not in st.session_state:
    st.session_state.deductions = []

# --- Input Form for Adding Elements ---
with st.expander("➕ Add a New Structural Element", expanded=True):
    with st.form("element_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            elem_type = st.text_input("Element Type", "Wall")
            length = st.number_input("Length (m)", min_value=0.01, value=5.0, step=0.1)
            height = st.number_input("Height / Depth (m)", min_value=0.01, value=3.0, step=0.1)
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
            width = st.number_input("Thickness / Width (m)", min_value=0.01, value=0.225, step=0.01)
        
        # Form submission buttons
        add_col, deduct_col, _ = st.columns([1, 1, 3])
        add_button = add_col.form_submit_button(label="Add as Element")
        deduct_button = deduct_col.form_submit_button(label="Add as Deduction")

        if add_button:
            new_element = {
                "element_type": elem_type,
                "quantity": quantity,
                "dimensions": {"length": length, "width": width, "height": height}
            }
            st.session_state.elements.append(new_element)
            st.success(f"✅ Added Element: {quantity}x {elem_type}")

        if deduct_button:
            new_deduction = {
                "element_type": f"{elem_type} (Opening)",
                "quantity": quantity,
                "dimensions": {"length": length, "width": width, "height": height}
            }
            st.session_state.deductions.append(new_deduction)
            st.warning(f"➖ Added Deduction: {quantity}x {elem_type}")

# --- Display Current Lists ---
st.header("📋 Project Element List")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Gross Elements")
    if st.session_state.elements:
        df_elements = pd.DataFrame(st.session_state.elements)
        st.dataframe(df_elements)
    else:
        st.info("No elements added yet.")

with col2:
    st.subheader("Deductions (Openings)")
    if st.session_state.deductions:
        df_deductions = pd.DataFrame(st.session_state.deductions)
        st.dataframe(df_deductions)
    else:
        st.info("No deductions added yet.")

# --- Final Calculation ---
st.header("🧮 Final Calculation")
mix_ratio = st.text_input("Concrete Mix Ratio (Cement:Sand:Gravel)", "1:2:4")

if st.button("Calculate Total Materials"):
    if not st.session_state.elements:
        st.error("Cannot calculate. Please add at least one element to the list.")
    else:
        # Prepare the request payload for the API
        payload = {
            "mix_ratio": mix_ratio,
            "elements": st.session_state.elements,
            "deductions": st.session_state.deductions
        }
        
        try:
            with st.spinner("Calculating... 🚀"):
                # Send the request to the FastAPI backend
                response = requests.post(BACKEND_URL, json=payload)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                
                results = response.json()

                if results.get("status") == "success":
                    st.success("Calculation Complete!")
                    res_data = results["required_materials"]
                    st.metric("Net Concrete Volume Required", f"{results['net_volume_cubic_meters']:.3f} m³")
                    
                    st.subheader("Required Materials:")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Cement Bags (50kg)", f"{res_data['cement_bags']:.2f}")
                    col2.metric("Sand", f"{res_data['sand_cubic_meters']:.3f} m³")
                    col3.metric("Gravel", f"{res_data['gravel_cubic_meters']:.3f} m³")
                else:
                    st.error(f"API Error: {results.get('message')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the backend API. Is it running? Details: {e}")