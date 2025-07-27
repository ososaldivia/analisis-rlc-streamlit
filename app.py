# Aplicación Streamlit: Trigonometría en Corriente Alterna (RLC)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd
import os

st.set_page_config(page_title="Análisis RLC en CA", layout="centered")
st.title("🔌 Análisis de circuito RLC en Corriente Alterna")

st.sidebar.header("Parámetros del circuito")
R = st.sidebar.number_input("Resistencia R (Ω)", value=10.0)
L = st.sidebar.number_input("Inductancia L (H)", value=0.1)
C = st.sidebar.number_input("Capacitancia C (F)", value=0.001)
f = st.sidebar.number_input("Frecuencia (Hz)", value=50.0)
V = st.sidebar.number_input("Voltaje (V)", value=100.0)

# Resultados globales para exportación
resultados_dict = {}

if st.sidebar.button("Resolver"):
    w = 2 * np.pi * f
    XL = w * L
    XC = 1 / (w * C)
    Z = np.sqrt(R**2 + (XL - XC)**2)
    phi = np.arctan((XL - XC) / R)
    I = V / Z

    S = V * I
    P = S * np.cos(phi)
    Q = S * np.sin(phi)

    # Guardar resultados
    resultados_dict = {
        "ω (rad/s)": w,
        "XL (Ω)": XL,
        "XC (Ω)": XC,
        "Z (Ω)": Z,
        "φ (°)": np.degrees(phi),
        "I (A)": I,
        "S (VA)": S,
        "P (W)": P,
        "Q (VAR)": Q
    }

    st.subheader("🧮 Paso a paso")
    for paso, (clave, valor) in enumerate(resultados_dict.items(), 1):
        st.markdown(f"- Paso {paso}: {clave} = {valor:.2f}")

    # Señales de voltaje y corriente
    t = np.linspace(0, 1/f, 500)
    v_t = V * np.sin(w * t)
    i_t = I * np.sin(w * t - phi)

    fig1, ax1 = plt.subplots()
    ax1.plot(t, v_t, label="Voltaje", color="blue")
    ax1.plot(t, i_t, label="Corriente", color="green")
    ax1.set_title("Señales de Voltaje y Corriente")
    ax1.set_xlabel("Tiempo (s)")
    ax1.set_ylabel("Amplitud")
    ax1.legend()
    st.pyplot(fig1)

    # Triángulo de potencia
    fig2, ax2 = plt.subplots()
    ax2.plot([0, P], [0, 0], label="P (W)", color="orange")
    ax2.plot([P, P], [0, Q], label="Q (VAR)", color="red")
    ax2.plot([0, P], [0, Q], label="S (VA)", color="purple")
    ax2.set_title("Triángulo de Potencia")
    ax2.set_xlabel("P (W)")
    ax2.set_ylabel("Q (VAR)")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)

    # Diagrama fasorial
    fig3, ax3 = plt.subplots()
    ax3.quiver(0, 0, V, 0, angles='xy', scale_units='xy', scale=1, color='blue', label='Voltaje')
    ax3.quiver(0, 0, I*np.cos(-phi), I*np.sin(-phi), angles='xy', scale_units='xy', scale=1, color='green', label='Corriente')
    ax3.set_xlim(-V*1.2, V*1.2)
    ax3.set_ylim(-I*1.2, I*1.2)
    ax3.set_aspect('equal')
    ax3.grid(True)
    ax3.set_title("Diagrama Fasorial")
    ax3.set_xlabel("Re")
    ax3.set_ylabel("Im")
    ax3.legend()
    st.pyplot(fig3)

    st.success("✅ Análisis completo realizado.")

    # Exportar resultados a PDF y Excel
    st.subheader("📤 Exportar resultados")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Descargar PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Resultados del análisis RLC en CA", ln=True)
            for k, v in resultados_dict.items():
                pdf.cell(200, 10, txt=f"{k}: {v:.2f}", ln=True)
            pdf.output("resultados_rlc.pdf")
            st.success("PDF generado como 'resultados_rlc.pdf'")

    with col2:
        if st.button("📊 Descargar Excel"):
            df = pd.DataFrame(list(resultados_dict.items()), columns=["Magnitud", "Valor"])
            df.to_excel("resultados_rlc.xlsx", index=False)
            st.success("Excel generado como 'resultados_rlc.xlsx'")
