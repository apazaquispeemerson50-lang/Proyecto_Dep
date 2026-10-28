
import streamlit as st
import pandas as pd
from datetime import date

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Control de Mediciones",
    page_icon="⚡",
    layout="wide"
)

st.title("Mediciones")
st.caption(
    "Proyecto_Dep | Registro, cálculo y validación de mediciones de campo"
)

# =====================================================
# DATOS DE EJEMPLO
# =====================================================

if "registros_mediciones" not in st.session_state:
    st.session_state.registros_mediciones = []

# =====================================================
# INDICADORES
# =====================================================

registros = st.session_state.registros_mediciones

total = len(registros)
conformes = sum(
    1 for r in registros if r["Estado"] == "Conforme"
)
por_revisar = total - conformes

c1, c2, c3 = st.columns(3)

c1.metric("📋 Mediciones registradas", total)
c2.metric("✅ Conformes", conformes)
c3.metric("⚠️ Por revisar", por_revisar)

st.divider()

# =====================================================
# FORMULARIO
# =====================================================

st.subheader("📝 Registrar nueva medición")

with st.form("formulario_medicion"):

    col1, col2 = st.columns(2)

    with col1:
        suministro = st.text_input(
            "Código de suministro *",
            placeholder="Ej. 10002541"
        )

        sed = st.text_input(
            "Código de SED",
            placeholder="Ej. 00903A"
        )

        tecnico = st.text_input(
            "Nombre del técnico",
            placeholder="Nombre del responsable"
        )

        fecha_medicion = st.date_input(
            "Fecha de medición",
            value=date.today()
        )

    with col2:
        referencia = st.number_input(
            "Medición de referencia",
            min_value=0.0,
            value=100.0,
            step=1.0,
            format="%.2f"
        )

        campo = st.number_input(
            "Medición tomada en campo",
            min_value=0.0,
            value=97.0,
            step=1.0,
            format="%.2f"
        )

        tolerancia = st.number_input(
            "Desviación máxima permitida (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.5
        )

    observacion = st.text_area(
        "Observaciones",
        placeholder="Describe alguna incidencia encontrada..."
    )

    guardar = st.form_submit_button(
        "🧮 Calcular y registrar",
        type="primary",
        use_container_width=True
    )

# =====================================================
# CÁLCULOS Y REGISTRO
# =====================================================

if guardar:

    if not suministro.strip():
        st.error("Debes ingresar el código de suministro.")

    elif referencia <= 0:
        st.error(
            "La medición de referencia debe ser mayor que cero."
        )

    else:
        diferencia = campo - referencia
        diferencia_abs = abs(diferencia)

        desviacion = (
            diferencia_abs / referencia
        ) * 100

        estado = (
            "Conforme"
            if desviacion <= tolerancia
            else "Por revisar"
        )

        nuevo_registro = {
            "Fecha": fecha_medicion.strftime("%Y-%m-%d"),
            "Suministro": suministro.strip(),
            "SED": sed.strip(),
            "Técnico": tecnico.strip(),
            "Referencia": referencia,
            "Medición de campo": campo,
            "Diferencia": round(diferencia, 2),
            "Desviación (%)": round(desviacion, 2),
            "Tolerancia (%)": tolerancia,
            "Estado": estado,
            "Observaciones": observacion.strip()
        }

        st.session_state.registros_mediciones.append(
            nuevo_registro
        )

        st.session_state.ultimo_calculo = nuevo_registro

        st.rerun()

# =====================================================
# RESULTADO DEL ÚLTIMO CÁLCULO
# =====================================================

if "ultimo_calculo" in st.session_state:

    resultado = st.session_state.ultimo_calculo

    st.subheader("📊 Resultado del cálculo")

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Diferencia absoluta",
        f'{abs(resultado["Diferencia"]):.2f}'
    )

    r2.metric(
        "Desviación",
        f'{resultado["Desviación (%)"]:.2f}%'
    )

    r3.metric(
        "Estado",
        resultado["Estado"]
    )

    if resultado["Estado"] == "Conforme":
        st.success(
            "La desviación está dentro de la tolerancia "
            "configurada para este ejemplo."
        )
    else:
        st.warning(
            "La desviación supera la tolerancia configurada. "
            "Se recomienda revisar la medición."
        )

# =====================================================
# HISTORIAL DE MEDICIONES
# =====================================================

st.divider()
st.subheader("📚 Historial de mediciones")

if st.session_state.registros_mediciones:

    df = pd.DataFrame(
        st.session_state.registros_mediciones
    )

    filtro = st.text_input(
        "Buscar por suministro o SED",
        placeholder="Escribe un código..."
    )

    if filtro.strip():
        mascara = (
            df["Suministro"].astype(str).str.contains(
                filtro, case=False, na=False
            )
            |
            df["SED"].astype(str).str.contains(
                filtro, case=False, na=False
            )
        )
        df_mostrar = df[mascara]
    else:
        df_mostrar = df

    st.dataframe(
        df_mostrar,
        use_container_width=True,
        hide_index=True
    )

    archivo_csv = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "📥 Descargar historial en CSV",
        data=archivo_csv,
        file_name="historial_mediciones.csv",
        mime="text/csv",
        use_container_width=True
    )

else:
    st.info(
        "Todavía no hay mediciones registradas. "
        "Completa el formulario para comenzar."
    )

st.caption(
    "Proyecto_Dep | Prototipo demostrativo. "
    "Los registros se conservan únicamente durante la sesión "
    "y no se comparten entre usuarios."
)
