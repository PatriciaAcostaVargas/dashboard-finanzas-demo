import streamlit as st
import pandas as pd
import requests
import datetime

# Configuración de la página
st.set_page_config(page_title="Guardián Financiero", page_icon="🛡️", layout="centered")

# --- LÓGICA DE MODO DEMO ---
# Intentamos conectar al backend real. Si falla, usamos datos falsos para la presentación.
API_URL = "http://localhost:8000"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hola, soy tu asistente financiero. Puedo ayudarte con presupuestos, "
                "alertas y movimientos. ¿En qué te gustaría enfocarte hoy?"
            ),
        }
    ]

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
st.title("🛡️ Monitor Financiero Accesible")
st.caption(f"Estado del Sistema: {estado_conexion}")

with st.sidebar:
    st.header("Preferencias de accesibilidad")
    st.checkbox("Modo alto contraste", value=True, help="Mejora la legibilidad de textos y tablas.")
    st.checkbox("Resúmenes en lenguaje claro", value=True, help="Explicaciones cortas y directas.")
    st.checkbox("Recordatorios por voz", value=False, help="Disponible en dispositivos compatibles.")

    st.divider()
    st.subheader("Perfil del usuario")
    st.selectbox("Tipo de usuario", ["Titular", "Cuidador", "Administrador"])
    st.selectbox("Zona horaria", ["GMT-5 (Bogotá)", "GMT-6 (CDMX)", "GMT-3 (Buenos Aires)"])
    st.date_input("Próxima revisión programada", datetime.date.today())

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

    st.dataframe(df.style.apply(resaltar_riesgo, axis=1), width="stretch")
else:
    st.info("No hay movimientos recientes.")

# Botones de Acción
st.subheader("Acciones de Cuidador")
col_a, col_b = st.columns(2)
if col_a.button("✅ Aprobar Gastos"):
    st.success("Gastos validados correctamente.")
if col_b.button("🚨 BLOQUEAR CUENTA"):
    st.error("¡Cuenta bloqueada! Se ha enviado SMS al titular.")

st.divider()

st.subheader("Plan de control y alertas")
col_c, col_d, col_e = st.columns(3)
col_c.metric("Presupuesto Mensual", "$1,200 USD")
col_d.metric("Gasto Actual", "$780 USD", delta="-35%")
col_e.metric("Alertas Activas", "2", delta="+1")
st.progress(0.65, text="65% del presupuesto utilizado")
st.caption("Indicadores con lenguaje claro para facilitar decisiones rápidas.")

st.divider()

st.subheader("Chatbot de apoyo financiero")
st.caption("Responde preguntas frecuentes y explica movimientos con lenguaje accesible.")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Escribe tu consulta sobre gastos, alertas o presupuestos.")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    respuesta = (
        "Gracias por tu pregunta. Puedo ayudarte a revisar tus gastos recientes, "
        "configurar alertas o crear un presupuesto accesible. ¿Quieres que revise "
        "los movimientos de mayor riesgo o ajustar tus límites de gasto?"
    )
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.markdown(respuesta)
