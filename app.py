import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Evaluación de Accesibilidad y UX Financiera",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Evaluador de Accesibilidad y UX para Instituciones Financieras")
st.caption(
    "Herramienta de diagnóstico para revisar cumplimiento de accesibilidad, usabilidad y experiencia digital en canales financieros."
)

st.markdown("---")

st.header("1) Contexto de la evaluación")
col1, col2, col3 = st.columns(3)
with col1:
    institucion = st.text_input("Institución financiera", "Banco Demo")
with col2:
    canal = st.selectbox(
        "Canal a evaluar",
        ["Web pública", "Banca en línea", "App móvil", "Kiosco/ATM", "Contact Center"],
    )
with col3:
    fecha_eval = st.date_input("Fecha de evaluación", datetime.date.today())

st.markdown("---")

st.header("2) Dimensiones de evaluación")
st.write(
    "Asigne una puntuación de 1 (deficiente) a 5 (excelente) para cada criterio."
)

criterios = {
    "Perceptible (WCAG)": [
        "Contraste y legibilidad",
        "Textos alternativos en imágenes",
        "Escalabilidad tipográfica",
    ],
    "Operable (WCAG)": [
        "Navegación por teclado",
        "Tiempo suficiente para completar tareas",
        "Estructura consistente de navegación",
    ],
    "Comprensible (WCAG)": [
        "Lenguaje claro en términos financieros",
        "Mensajes de error comprensibles",
        "Confirmaciones de transacciones críticas",
    ],
    "Robusto (WCAG)": [
        "Compatibilidad con lectores de pantalla",
        "Etiquetado correcto de formularios",
        "Compatibilidad multi-dispositivo",
    ],
    "UX Financiera": [
        "Facilidad de onboarding digital",
        "Claridad de comisiones y costos",
        "Confianza y percepción de seguridad",
        "Eficiencia en pagos/transferencias",
    ],
}

resultados = []

for dimension, items in criterios.items():
    with st.expander(dimension, expanded=True):
        for item in items:
            score = st.slider(
                item,
                min_value=1,
                max_value=5,
                value=3,
                key=f"{dimension}-{item}",
            )
            resultados.append({"dimension": dimension, "criterio": item, "puntaje": score})

df = pd.DataFrame(resultados)
resumen = df.groupby("dimension", as_index=False)["puntaje"].mean()
promedio_total = df["puntaje"].mean()


def clasificacion(score: float) -> tuple[str, str]:
    if score >= 4.5:
        return "Excelente", "🟢"
    if score >= 3.5:
        return "Aceptable", "🟡"
    if score >= 2.5:
        return "En riesgo", "🟠"
    return "Crítico", "🔴"

estado, icono = clasificacion(promedio_total)

st.markdown("---")
st.header("3) Resultado del diagnóstico")
metric_a, metric_b, metric_c = st.columns(3)
metric_a.metric("Puntaje promedio", f"{promedio_total:.2f}/5")
metric_b.metric("Estado general", f"{icono} {estado}")
metric_c.metric("Criterios evaluados", f"{len(df)}")

st.subheader("Promedio por dimensión")
st.bar_chart(resumen.set_index("dimension"))

st.subheader("Detalle de criterios")
st.dataframe(
    df.sort_values(["dimension", "puntaje"], ascending=[True, False]),
    use_container_width=True,
)

st.markdown("---")
st.header("4) Plan de mejora")

hallazgos_criticos = df[df["puntaje"] <= 2]
hallazgos_riesgo = df[(df["puntaje"] > 2) & (df["puntaje"] <= 3)]

if hallazgos_criticos.empty and hallazgos_riesgo.empty:
    st.success(
        "No se identifican hallazgos críticos. Mantener monitoreo trimestral y pruebas con usuarios diversos."
    )
else:
    if not hallazgos_criticos.empty:
        st.error("Hallazgos críticos (prioridad alta):")
        for _, row in hallazgos_criticos.iterrows():
            st.write(f"- {row['criterio']} ({row['dimension']})")

    if not hallazgos_riesgo.empty:
        st.warning("Hallazgos en riesgo (prioridad media):")
        for _, row in hallazgos_riesgo.iterrows():
            st.write(f"- {row['criterio']} ({row['dimension']})")

recomendaciones_base = [
    "Implementar pruebas de accesibilidad automatizadas en CI/CD (ej. axe-core, Lighthouse).",
    "Realizar pruebas de usabilidad con personas mayores y usuarios con discapacidad visual o motriz.",
    "Simplificar microcopys financieros y reducir tecnicismos en flujos de alto impacto.",
    "Agregar revisión legal/compliance para garantizar transparencia en costos y consentimiento informado.",
]

st.subheader("Recomendaciones estratégicas")
for rec in recomendaciones_base:
    st.write(f"- {rec}")

st.markdown("---")
if st.button("📥 Exportar reporte (CSV)"):
    reporte = df.copy()
    reporte["institucion"] = institucion
    reporte["canal"] = canal
    reporte["fecha"] = str(fecha_eval)
    csv = reporte.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar reporte CSV",
        data=csv,
        file_name=f"reporte_accesibilidad_ux_{institucion.lower().replace(' ', '_')}.csv",
        mime="text/csv",
    )

st.caption(
    "Sugerencia: combine este diagnóstico con auditoría técnica WCAG 2.2 AA, entrevistas contextuales y analítica de embudos críticos."
)
