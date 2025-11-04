# ==========================================================
# R-L-C TRANSMISSION LINE TOOLKIT (PRO VERSION)
# ----------------------------------------------------------
# Developed by: Ella Mae M. Marmol
# Course: EE 421 - Power System Analysis (Lab)
# Laboratory Activity 2: Power System Modelling Part 1
# ----------------------------------------------------------
# Features:
#   ✅ Computes Resistance, Inductance, and Capacitance
#   ✅ Auto GMR & GMD computation
#   ✅ Beginner-friendly interface with clear guidance
#   ✅ Displays per-unit-length and total values
#   ✅ Advanced geometry support for three-phase lines
# ==========================================================

import streamlit as st
import math
import pandas as pd

# ----------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ----------------------------------------------------------
st.set_page_config(page_title="R-L-C Transmission Line Toolkit", page_icon="⚡", layout="wide")

st.title("⚡ R–L–C Transmission Line Toolkit (Pro Version)")
st.markdown("""
This toolkit helps Electrical Engineering students compute the **resistance, inductance, and capacitance**
of single-phase and three-phase overhead transmission lines.

> 💡 Designed for **EE 421 - Power System Analysis Laboratory (Power System Modelling Part 1)**  
> Follow the guided steps and beginner instructions in each tab.
""")

# ----------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------
MU_0 = 4 * math.pi * 1e-7       # Permeability of free space (H/m)
EPSILON_0 = 8.854e-12           # Permittivity of free space (F/m)
TEMP_CONST = {"Copper": 234.5, "Aluminum": 228.1}

# ----------------------------------------------------------
# TAB SETUP
# ----------------------------------------------------------
tabs = st.tabs(["🧮 Resistance", "🌀 Inductance", "⚡ Capacitance", "📊 Summary"])

# ==========================================================
# 🧮 RESISTANCE TAB
# ==========================================================
with tabs[0]:
    st.header("🧮 Resistance Calculation")
    st.markdown("""
    ### 📘 Beginner Instructions
    Enter the known values for your conductor and line.
    The app will automatically correct resistivity for temperature and compute both **resistance per km** and **total resistance**.
    """)

    # --- Input section
    col1, col2 = st.columns(2)
    with col1:
        material = st.selectbox("Select Conductor Material", ["Copper", "Aluminum"])
        rho1 = st.number_input("Initial Resistivity ρ₁ (Ω·m at reference T₁)", value=1.724e-8 if material == "Copper" else 2.82e-8)
        area_mm2 = st.number_input("Cross-sectional Area (mm²)", value=300.0)
        length_km = st.number_input("Line Length (km)", value=10.0)
    with col2:
        temp1 = st.number_input("Reference Temperature T₁ (°C)", value=20.0)
        temp2 = st.number_input("Operating Temperature T₂ (°C)", value=50.0)
        temp_const = TEMP_CONST[material]
        st.write(f"Temperature Constant (θ) = {temp_const} °C (for {material})")

    # --- Calculations
    area_m2 = area_mm2 * 1e-6
    rho2 = rho1 * ((temp2 + temp_const) / (temp1 + temp_const))
    R_per_km = (rho2 / area_m2) * 1000
    R_total = R_per_km * length_km

    # --- Output
    st.subheader("🧾 Computed Results")
    st.markdown(f"""
    **Corrected Resistivity ρ₂:** {rho2:.4e} Ω·m  
    **Resistance per km:** {R_per_km:.6f} Ω/km  
    **Total Resistance:** {R_total:.6f} Ω
    """)

    st.info("🔹 Increasing temperature raises resistivity and total resistance.")

# ==========================================================
# 🌀 INDUCTANCE TAB
# ==========================================================
with tabs[1]:
    st.header("🌀 Inductance Calculation")
    st.markdown("""
    ### 📘 Beginner Instructions
    - For **Single-phase** lines, provide the spacing between the two conductors.  
    - For **Three-phase** lines, enter the coordinates of each phase conductor (x, y).  
    The app automatically computes **GMR**, **GMD**, and displays **inductance per km** and **total inductance**.
    """)

    # --- Input selection
    system_type = st.radio("System Type", ["Single-phase", "Three-phase (transposed)"], horizontal=True)
    radius_mm = st.number_input("Conductor Radius (mm)", value=10.0)
    r_m = radius_mm / 1000

    # Optional GMR input
    user_gmr = st.number_input("GMR (m) [Enter 0 to auto-calculate 0.7788×r]", min_value=0.0, value=0.0)
    gmr = 0.7788 * r_m if user_gmr == 0 else user_gmr

    length_km = st.number_input("Line Length (km)", value=10.0, key="induct_length")
    length_m = length_km * 1000

    # --- Single-phase mode
    if "Single" in system_type:
        spacing_m = st.number_input("Conductor Spacing (m)", value=2.0)
        GMD = spacing_m

    # --- Three-phase mode
    else:
        st.markdown("Enter phase coordinates in meters (A, B, C):")
        xA = st.number_input("xA", value=0.0)
        yA = st.number_input("yA", value=10.0)
        xB = st.number_input("xB", value=6.0)
        yB = st.number_input("yB", value=10.0)
        xC = st.number_input("xC", value=12.0)
        yC = st.number_input("yC", value=10.0)

        Dab = math.sqrt((xA - xB)**2 + (yA - yB)**2)
        Dbc = math.sqrt((xB - xC)**2 + (yB - yC)**2)
        Dca = math.sqrt((xC - xA)**2 + (yC - yA)**2)
        GMD = (Dab * Dbc * Dca)**(1/3)

        st.markdown(f"**Phase Spacings:** Dab={Dab:.3f} m, Dbc={Dbc:.3f} m, Dca={Dca:.3f} m")

    # --- Inductance computation
    L_per_m = (MU_0 / (2 * math.pi)) * math.log(GMD / gmr)
    L_per_km = L_per_m * 1000
    L_total = L_per_m * length_m

    # --- Output
    st.subheader("🧾 Computed Results")
    st.markdown(f"""
    **GMR:** {gmr:.6f} m  
    **GMD:** {GMD:.6f} m  
    **Inductance per km:** {L_per_km:.6e} H/km  
    **Total Inductance:** {L_total:.6e} H
    """)
    st.info("🔹 Increasing conductor spacing increases inductance.")

# ==========================================================
# ⚡ CAPACITANCE TAB
# ==========================================================
with tabs[2]:
    st.header("⚡ Capacitance Calculation")
    st.markdown("""
    ### 📘 Beginner Instructions
    - For **Single-phase**, enter the spacing and height above ground.  
    - For **Three-phase**, provide the coordinates (x, y) for each phase.  
    The app uses the **image method** to consider ground effects and shows **C per km** and **total C**.
    """)

    # --- Inputs
    system_type_c = st.radio("System Type", ["Single-phase", "Three-phase (transposed)"], horizontal=True, key="cap_system")
    radius_mm_c = st.number_input("Conductor Radius (mm)", value=10.0, key="cap_radius")
    r_m_c = radius_mm_c / 1000
    height_m = st.number_input("Average Conductor Height above Ground (m)", value=10.0)
    length_km_c = st.number_input("Line Length (km)", value=10.0, key="cap_length")
    length_m_c = length_km_c * 1000

    # --- Single-phase
    if "Single" in system_type_c:
        spacing_c = st.number_input("Spacing between Conductors (m)", value=2.0)
        D_eq = math.sqrt(spacing_c**2 + (2 * height_m)**2)
        GMD = spacing_c

    # --- Three-phase
    else:
        st.markdown("Enter coordinates for each phase center:")
        xA = st.number_input("xA (m)", value=0.0, key="cap_xA")
        yA = st.number_input("yA (m)", value=10.0, key="cap_yA")
        xB = st.number_input("xB (m)", value=6.0, key="cap_xB")
        yB = st.number_input("yB (m)", value=10.0, key="cap_yB")
        xC = st.number_input("xC (m)", value=12.0, key="cap_xC")
        yC = st.number_input("yC (m)", value=10.0, key="cap_yC")

        Dab = math.sqrt((xA - xB)**2 + (yA - yB)**2)
        Dbc = math.sqrt((xB - xC)**2 + (yB - yC)**2)
        Dca = math.sqrt((xC - xA)**2 + (yC - yA)**2)
        GMD = (Dab * Dbc * Dca)**(1/3)

        # Image method for each phase
        DpA = 2 * yA
        DpB = 2 * yB
        DpC = 2 * yC
        Dp = (DpA * DpB * DpC)**(1/3)
        D_eq = math.sqrt(GMD * Dp)

        st.markdown(f"**Computed GMD = {GMD:.6f} m**  |  **Equivalent Height Effect = {Dp:.6f} m**")

    # --- Capacitance calculation
    C_per_m = (2 * math.pi * EPSILON_0) / math.log(D_eq / r_m_c)
    C_per_km = C_per_m * 1000
    C_total = C_per_m * length_m_c

    # --- Output
    st.subheader("🧾 Computed Results")
    st.markdown(f"""
    **GMD (Effective):** {GMD:.6f} m  
    **Capacitance per km:** {C_per_km:.6e} F/km  
    **Total Capacitance:** {C_total:.6e} F
    """)
    st.info("🔹 Increasing height above ground decreases capacitance.")

# ==========================================================
# 📊 SUMMARY TAB
# ==========================================================
with tabs[3]:
    st.header("📊 Summary of Results")
    st.markdown("Here’s a consolidated view of all computed parameters.")

    data = {
        "Parameter": ["Resistance (Ω/km)", "Resistance Total (Ω)",
                      "Inductance (H/km)", "Inductance Total (H)",
                      "Capacitance (F/km)", "Capacitance Total (F)"],
        "Value": [R_per_km, R_total, L_per_km, L_total, C_per_km, C_total]
    }
    df = pd.DataFrame(data)
    st.table(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Summary as CSV", csv, "RLC_Summary.csv", "text/csv")

    st.markdown("""
    ---
    **Interpretation Notes:**
    - Resistance increases with temperature.
    - Inductance increases with conductor spacing.
    - Capacitance decreases with both spacing and conductor height.
    ---
    **Developed by:** *Ella Mae M. Marmol*  
    Bicol University – Electrical Engineering Department
    """)

