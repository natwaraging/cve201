import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

# --- การตั้งค่าหน้าเว็บ (Page Configuration) ---
st.set_page_config(page_title="Civil Concrete Pro", page_icon="🏗️", layout="wide")

# --- Custom CSS เพื่อความสวยงาม ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Concrete Mixture Calculator Pro")
st.write("เครื่องมือคำนวณวัสดุคอนกรีตมาตรฐานวิศวกรรม (ACI Standard)")

# --- ส่วนรับข้อมูล (Sidebar) ---
with st.sidebar:
    st.header("📍 Input Parameters")
    with st.expander("Size of Structure (m)", expanded=True):
        width = st.number_input("Width (m)", min_value=0.01, value=1.0, step=0.1)
        length = st.number_input("Length (m)", min_value=0.01, value=1.0, step=0.1)
        depth = st.number_input("Thickness/Height (m)", min_value=0.01, value=0.1, step=0.05)
    
    waste_percent = st.slider("Waste Allowance (%)", 0, 20, 5)
    
    ratio_type = st.selectbox(
        "Mixing Ratio (Cement:Sand:Stone)",
        ["1:1.5:3 - High Strength (Beams, Columns)", 
         "1:2:4 - General Purpose (Flooring)", 
         "1:3:5 - Lean Concrete (Leveling)"]
    )

# --- ส่วนการคำนวณ (Engineering Logic) ---
if "1:1.5:3" in ratio_type:
    ratio = (1, 1.5, 3)
elif "1:3:5" in ratio_type:
    ratio = (1, 3, 5)
else:
    ratio = (1, 2, 4)

# คำนวณปริมาตร
net_vol = width * length * depth
total_vol = net_vol * (1 + (waste_percent / 100))
dry_vol = total_vol * 1.54  # Shrinkage factor มาตรฐานงานวิศวกรรม
sum_ratio = sum(ratio)

# แยกปริมาณวัสดุแต่ละชนิด (หน่วย m3)
cement_m3 = (ratio[0] / sum_ratio) * dry_vol
sand_m3 = (ratio[1] / sum_ratio) * dry_vol
stone_m3 = (ratio[2] / sum_ratio) * dry_vol

# แปลงหน่วยเป็นถุงและลิตร
cement_bags = math.ceil(cement_m3 / 0.035)  # ปูน 1 ถุง (50kg) มีปริมาตรประมาณ 0.035 m3
water_liters = cement_bags * 25  # ประมาณการน้ำ 25 ลิตรต่อปูน 1 ถุง (W/C ratio ~0.5)

# --- ส่วนการแสดงผล (Main Panel) ---
col_v1, col_v2, col_v3 = st.columns(3)
col_v1.metric("Net Volume", f"{net_vol:.3f} m³")
col_v2.metric("Total Volume (+Waste)", f"{total_vol:.3f} m³")
col_v3.metric("Dry Volume (Materials)", f"{dry_vol:.3f} m³")

st.divider()

# แบ่งส่วนแสดงตัวเลขและกราฟ
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("✅ Material Required")
    st.success(f"**Cement (50kg):** {cement_bags} Bags")
    st.info(f"**Sand:** {sand_m3:.2f} m³")
    st.info(f"**Stone (3/4\"):** {stone_m3:.2f} m³")
    st.warning(f"**Water (Estimated):** {water_liters:.1f} Liters")

with c2:
    st.subheader("📊 Material Ratio (Dry Volume)")
    # สร้าง Pie Chart
    labels = ['Cement', 'Sand', 'Stone']
    sizes = [cement_m3, sand_m3, stone_m3]
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, shadow=True)
    ax.axis('equal') 
    st.pyplot(fig)
    plt.close(fig)  # คืนค่าหน่วยความจำระบบ

# --- ส่วนอธิบายสูตร (Engineering Formulas) ---
with st.expander("📙 View Engineering Formulas used in this app"):
    st.write("""
    - **Wet Volume:** $V = Width \times Length \times Depth$
    - **Dry Volume:** $V_{dry} = V_{wet} \times 1.54$ (Shrinkage & Voids factor)
    - **Material Calculation:** $Component = (Ratio / \sum Ratio) \times V_{dry}$
    - **Cement Bags:** $Bags = V_{cement} / 0.035$
    """)
    
st.divider()
st.caption("Developed for Application Design Project - Submission Date: 22 April 2026")
