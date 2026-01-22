import streamlit as st
import pandas as pd
import requests
import datetime

# Configuración de la página
st.set_page_config(page_title="Guardián Financiero", page_icon="🛡️", layout="centered")

# --- LÓGICA DE MODO DEMO ---
# Intentamos conectar al backend real. Si falla, usamos datos falsos para la presentación.
API_URL = "http://localhost:8000" 

def obtener_datos():
    try:
        # Intentar conectar con API Real
        resp_saldo = requests.get(f"{API_URL}/saldo/1", timeout=2)
        resp_tx = requests.get(f"{API_URL}/auditoria/movimientos", timeout=2)
        return resp_saldo.json()["saldo"], resp_tx.json(), "🟢 Conectado a API Real"
    except:
        # FALLBACK: Datos simulados para la reunión
        saldo_fake = 450.00
        tx_fake = [
            {"date": "2025-01-21 14:30", "description": "Farmacia", "amount": -45.00, "status": "completed"},
            {"date": "2025-01-20 09:15", "description": "Supermercado", "amount": -32.50, "status": "completed"},
            {"date": "2025-01-19 03:00", "description": "Transferencia Desconocida", "amount": -200.00, "status": "flagged"},
        ]
        return saldo_fake, tx_fake, "🟠 Modo Demo (Simulado)"

# Obtener datos
saldo, movimientos, estado_conexion = obtener_datos()

# --- INTERFAZ GRÁFICA ---
st.title("🛡️ Monitor Familiar")
st.caption(f"Estado del Sistema: {estado_conexion}")

# Métricas
col1, col2 = st.columns(2)
col1.metric("Saldo Disponible", f"${saldo} USD")
col2.metric("Nivel de Riesgo", "BAJO", delta_color="normal")

st.divider()

# Tabla de Auditoría
st.subheader("Últimos Movimientos")
if movimientos:
    df = pd.DataFrame(movimientos)
    
    # Función para colorear filas peligrosas
    def resaltar_riesgo(row):
        return ['background-color: #ffcccc' if row['status'] == 'flagged' else '' for _ in row]

    st.dataframe(df.style.apply(resaltar_riesgo, axis=1), use_container_width=True)
else:
    st.info("No hay movimientos recientes.")

# Botones de Acción
st.subheader("Acciones de Cuidador")
col_a, col_b = st.columns(2)
if col_a.button("✅ Aprobar Gastos"):
    st.success("Gastos validados correctamente.")
if col_b.button("🚨 BLOQUEAR CUENTA"):
    st.error("¡Cuenta bloqueada! Se ha enviado SMS al titular.")