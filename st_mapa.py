import streamlit as st
from datetime import date, time, datetime, timedelta
import streamlit.components.v1 as components
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


#Sistema_Mapas_S
st.set_page_config(layout="wide")

# Custom CSS for better layout and styling
st.markdown(
    """
    <style>
    .main-header {
        color: #FF6600; /* Movimiento Ciudadano orange */
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 30px;
    }
    .subheader {
        color: #FF6600;
        font-size: 1.8em;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 2px solid #FF6600;
        padding-bottom: 5px;
    }
    .st-sidebar .st-radio div {
        display: flex;
        flex-direction: column;
    }
    .st-sidebar .st-radio label {
        margin-bottom: 10px;
    }
    .st-form {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #FF6600;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .st-file_uploader {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 50px 0;
        text-align: center;
    }
    .login-box {
        background-color: #f0f2f6;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 400px;
    }
    .stTextInput label {
        font-size: 1.2em;
        font-weight: bold;
    }
    .stButton button {
        background-color: #FF6600;
        color: white;
        font-size: 1.2em;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #e65c00;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Sistema de Gestión de Secretaría Técnica")

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Login Page Logic ---
if not st.session_state.logged_in:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.header("Registro")  # Based on the image
    st.markdown("---")

    login_code = st.text_input("Código de Inicio", type="password", key="login_code_input")

    if st.button("Ingresar", key="login_button"):
        if login_code == "igualdad2025":
            st.session_state.logged_in = True
            st.rerun()  # Rerun the app to show the main content
        else:
            st.error("Código incorrecto. Inténtalo de nuevo.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Main Application (Tabs) ---
else:
    # Sidebar for navigation
    st.sidebar.title("Navegación")
    page = st.sidebar.radio("Ir a", ["Mapa Público", "Ficha Técnica"])

    if page == "Mapa Público":
        st.markdown("<h1 class='main-header'>Mapa Público</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style='text-align: center; font-size: 1.2em;'>
                Aquí puedes ver el mapa público:
            </p>
            """
            , unsafe_allow_html=True
        )
        # Using streamlit.components.v1 to embed the content
        iframe_src = "https://www.google.com/maps/d/u/0/embed?mid=1WfvdE-PSaqE1OBsgYSdsHLccw83ApNY&ehbc=2E312F"
        components.iframe(iframe_src, height=600)

    elif page == "Ficha Técnica":
        st.markdown("<h1 class='main-header'>FICHA TÉCNICA DE RECORRIDO Y/O JUNTA VECINAL</h1>", unsafe_allow_html=True)

        # Dictionary to store all form data
        form_data = {}

        with st.form("ficha_tecnica_form", clear_on_submit=False):
            st.markdown("<h3 class='subheader'>INFORMACIÓN PRINCIPAL</h3>", unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                form_data['folio'] = st.text_input("FOLIO:", value="", key="folio_input")
            with col2:
                form_data['fecha_elaboracion'] = st.date_input("FECHA DE ELABORACIÓN:", date.today(), help="",
                                                               key="fecha_elaboracion_input")
            with col3:
                form_data['tipo_evento'] = st.selectbox("Tipo de evento:", ["Recorrido", "Junta Vecinal"], help="",
                                                        key="tipo_evento_select")
            with col4:
                form_data['seccion_main'] = st.text_input("Sección:", help="", key="seccion_input_main")

            col1, col2 = st.columns(2)
            with col1:
                form_data['nombre_evento'] = st.text_input("NOMBRE DEL EVENTO:", help="", key="nombre_evento_input")
            with col2:
                form_data['distrito_local'] = st.text_input("Distrito local:", help="", key="distrito_local_input")

            col1, col2, col3 = st.columns(3)
            with col1:
                form_data['distrito_federal'] = st.text_input("Distrito federal:", help="",
                                                              key="distrito_federal_input")
            with col2:
                form_data['fecha_evento'] = st.date_input("Fecha del evento:", date.today(), help="",
                                                          key="fecha_evento_input")
            with col3:
                col_hora_inicio, col_hora_fin = st.columns(2)
                with col_hora_inicio:
                    hora_inicio = st.time_input("Hora inicio:", time(9, 0), help="", key="hora_inicio_input")
                    form_data['hora_inicio'] = hora_inicio
                with col_hora_fin:
                    hora_fin = st.time_input("Hora fin:", time(17, 0), help="", key="hora_fin_input")
                    form_data['hora_fin'] = hora_fin

            duracion_display = ""
            if hora_inicio and hora_fin:
                start_datetime = datetime.combine(date.today(), hora_inicio)
                end_datetime = datetime.combine(date.today(), hora_fin)

                if end_datetime < start_datetime:
                    end_datetime += timedelta(days=1)

                duration_delta = end_datetime - start_datetime
                total_seconds = int(duration_delta.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                duracion_display = f"{hours}h {minutes}m"
            form_data['duracion'] = st.text_input("Duración:", value=duracion_display, disabled=True, help="",
                                                  key="duracion_display_input")

            col1, col2 = st.columns(2)
            with col1:
                form_data['pronostico_climatico'] = st.text_input("Pronóstico climático:", help="",
                                                                  key="pronostico_climatico_input")
            with col2:
                form_data['vestimenta'] = st.text_input("Vestimenta:", help="", key="vestimenta_input")

            form_data['quienes_encabezan'] = st.text_input("Quienes encabezan:", help="", key="quienes_encabezan_input")
            form_data['objetivo'] = st.text_area("Objetivo:", help="", key="objetivo_text_area")
            form_data['antecedentes'] = st.text_area("Antecedentes:", help="", key="antecedentes_text_area")

            st.markdown("<h3 class='subheader'>RESPONSABLES</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                form_data['responsable_evento'] = st.text_input("Responsable del evento", help="",
                                                                key="responsable_evento_input")
            with col2:
                form_data['contacto_responsable'] = st.text_input("Contacto del responsable:", help="",
                                                                  key="contacto_responsable_input")

            col1, col2 = st.columns(2)
            with col1:
                form_data['comite_recepcion'] = st.text_input("Comité de recepción:", help="",
                                                              key="comite_recepcion_input")
            with col2:
                form_data['contacto_comite'] = st.text_input("Contacto del comité:", help="",
                                                             key="contacto_comite_input")

            st.markdown("<h3 class='subheader'>INFORMACIÓN DE SECCIÓN</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                form_data['no_viviendas'] = st.number_input("No. de viviendas:", min_value=0, step=1, help="",
                                                            key="no_viviendas_input")
            with col2:
                form_data['votantes_seccion'] = st.number_input("Votantes en la sección:", min_value=0, step=1, help="",
                                                                key="votantes_seccion_input")
            with col3:
                form_data['votantes_necesarios'] = st.number_input("Votantes necesarios para ganar sección:",
                                                                   min_value=0, step=1, help="",
                                                                   key="votantes_necesarios_input")

            st.markdown("<h4 class='subheader'>Resultados elecciones a presidencia municipal:</h4>",
                        unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                form_data['resultados_2024'] = st.text_input("2024:", help="", key="resultados_2024_input")
            with col2:
                form_data['resultados_2021'] = st.text_input("2021:", help="", key="resultados_2021_input")

            st.markdown("<h3 class='subheader'>SITUACIÓN DE RIESGO</h3>", unsafe_allow_html=True)
            form_data['situacion_riesgo'] = st.radio("Situación de riesgo:", ["Baja", "Media", "Alta"], help="",
                                                     key="situacion_riesgo_radio")
            if form_data['situacion_riesgo'] != "Baja":
                form_data['motivo_riesgo'] = st.text_area("Motivo de la situación de riesgo:", help="",
                                                          key="motivo_riesgo_text_area")
            else:
                form_data['motivo_riesgo'] = ""

            form_data['control_seguridad'] = st.text_input("Control de seguridad:",
                                                           value="Policía de Monterrey / Fuerza Civil", help="",
                                                           key="control_seguridad_input")

            if form_data['tipo_evento'] == "Recorrido":
                st.markdown("<h3 class='subheader'>DETALLES DEL RECORRIDO</h3>", unsafe_allow_html=True)
                form_data['quienes_acompanan'] = st.text_input("Quienes acompañan:", help="",
                                                               key="quienes_acompanan_input")
                form_data['no_acompanantes'] = st.number_input("No. de acompañantes:", min_value=0, step=1, help="",
                                                               key="no_acompanantes_input")
                form_data['punto_partida'] = st.text_input("Punto de partida (calles y link de Google Maps):", help="",
                                                           key="punto_partida_input")
                form_data['punto_final'] = st.text_input("Punto final (calles y link de Google Maps):", help="",
                                                         key="punto_final_input")
                form_data['descripcion_recorrido'] = st.text_area("Descripción del recorrido:", help="",
                                                                  key="descripcion_recorrido_text_area")

                st.markdown("<h4 class='subheader'>Información del Recorrido:</h4>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    form_data['recorrido_colonia'] = st.text_input("Colonia:", help="", key="recorrido_colonia_input")
                    form_data['recorrido_casas'] = st.number_input("Casas:", min_value=0, step=1, help="",
                                                                   key="recorrido_casas_input")
                    form_data['recorrido_distancia'] = st.text_input("Distancia:", help="",
                                                                     key="recorrido_distancia_input")
                with col2:
                    form_data['recorrido_seccion'] = st.text_input("Sección:", help="", key="recorrido_seccion_input")
                    form_data['recorrido_manzanas'] = st.number_input("Manzanas:", min_value=0, step=1, help="",
                                                                      key="recorrido_manzanas_input")
                    form_data['recorrido_votantes'] = st.number_input("Votantes:", min_value=0, step=1, help="",
                                                                      key="recorrido_votantes_input")

                st.subheader("Croquis del recorrido:")
                croquis_recorrido = st.file_uploader("Cargar imagen del croquis", type=["png", "jpg", "jpeg"],
                                                     key="croquis_recorrido_uploader")
                form_data['croquis_recorrido'] = croquis_recorrido.name if croquis_recorrido else None
                if croquis_recorrido:
                    st.image(croquis_recorrido, caption="Croquis del Recorrido", use_column_width=True)

            elif form_data['tipo_evento'] == "Junta Vecinal":
                st.markdown("<h3 class='subheader'>DETALLES DE LA JUNTA VECINAL</h3>", unsafe_allow_html=True)
                form_data['quienes_asisten'] = st.text_input("Quienes asisten:", help="", key="quienes_asisten_input")
                form_data['poblacion_asistente'] = st.text_input("Población asistente:", help="",
                                                                 key="poblacion_asistente_input")
                form_data['punto_reunion'] = st.text_input("Punto de reunión:", help="", key="punto_reunion_input")
                form_data['no_asistentes'] = st.number_input("No. de asistentes:", min_value=0, step=1, help="",
                                                             key="no_asistentes_input")
                form_data['hora_inicio_reunion'] = st.time_input("Hora inicio de reunión:", time(10, 0), help="",
                                                                 key="hora_inicio_reunion_input")
                form_data['duracion_reunion'] = st.text_input("Duración de reunión:", help="",
                                                              key="duracion_reunion_input")
                form_data['tipo_espacio'] = st.text_input("Tipo de espacio:", help="", key="tipo_espacio_input")
                form_data['tipo_reunion'] = st.text_input("Tipo de reunión:", help="", key="tipo_reunion_input")
                form_data['descripcion_reunion'] = st.text_area("Descripción de la reunión:", help="",
                                                                key="descripcion_reunion_text_area")
                form_data['expectativas_reunion'] = st.text_area("Expectativas de la reunión:", help="",
                                                                 key="expectativas_reunion_text_area")

                st.markdown("<h4 class='subheader'>Orden del día:</h4>", unsafe_allow_html=True)
                num_puntos_dia = st.number_input("Número de puntos en el orden del día:", min_value=0, step=1,
                                                 key="num_puntos_dia_input")
                orden_del_dia_entries = []
                for i in range(num_puntos_dia):
                    col_hora_punto, col_descripcion_punto = st.columns([1, 3])
                    with col_hora_punto:
                        hora_punto = st.time_input(f"Hora Punto {i + 1}:", key=f"hora_punto_{i}", help="")
                    with col_descripcion_punto:
                        punto_dia = st.text_input(f"Punto del día {i + 1}:", key=f"punto_dia_{i}", help="")
                    orden_del_dia_entries.append({"Hora": hora_punto, "Punto": punto_dia})
                form_data['orden_del_dia'] = orden_del_dia_entries

                st.markdown("<h4 class='subheader'>AUTORIDADES</h4>", unsafe_allow_html=True)
                form_data['asistencia_autoridad'] = st.radio("Asistencia de autoridad:", ["Sí", "No"], help="",
                                                             key="asistencia_autoridad_radio")
                if form_data['asistencia_autoridad'] == "Sí":
                    form_data['contacto_autoridad'] = st.text_input("Contacto de autoridad:", help="",
                                                                    key="contacto_autoridad_input")
                else:
                    form_data['contacto_autoridad'] = ""

            st.markdown("<h3 class='subheader'>POBLACIÓN VOTANTE ESTIMADA</h3>", unsafe_allow_html=True)
            col_totales, col_necesarios = st.columns(2)
            with col_totales:
                form_data['totales_votantes'] = st.number_input("Totales:", min_value=0, step=1, help="",
                                                                key="totales_input")
            with col_necesarios:
                form_data['necesarios_votantes'] = st.number_input("Necesarios:", min_value=0, step=1, help="",
                                                                   key="necesarios_input")

            col_mujeres, col_hombres = st.columns(2)
            with col_mujeres:
                form_data['mujeres_votantes'] = st.number_input("Mujeres:", min_value=0, step=1, help="",
                                                                key="mujeres_input")
            with col_hombres:
                form_data['hombres_votantes'] = st.number_input("Hombres:", min_value=0, step=1, help="",
                                                                key="hombres_input")

            st.markdown("<h4 class='subheader'>Distribución por Generación:</h4>", unsafe_allow_html=True)
            col_boomers, col_genx = st.columns(2)
            with col_boomers:
                form_data['baby_boomers'] = st.number_input("Baby boomers (61+ años):", min_value=0, step=1, help="",
                                                            key="baby_boomers_input")
            with col_genx:
                form_data['generacion_x'] = st.number_input("Generación X (45-60 años):", min_value=0, step=1, help="",
                                                            key="generacion_x_input")

            col_millenials, col_genz = st.columns(2)
            with col_millenials:
                form_data['millenials'] = st.number_input("Millenials (29-44 años):", min_value=0, step=1, help="",
                                                          key="millenials_input")
            with col_genz:
                form_data['generacion_z'] = st.number_input("Generación Z (18-28 años):", min_value=0, step=1, help="",
                                                            key="generacion_z_input")

            st.markdown("<h3 class='subheader'>OBSERVACIONES</h3>", unsafe_allow_html=True)
            form_data['observaciones'] = st.text_area("Observaciones:", help="", key="observaciones_text_area")
            st.subheader("Evidencia fotográfica de las observaciones:")
            evidencia_fotografica = st.file_uploader("Cargar imágenes de observaciones", type=["png", "jpg", "jpeg"],
                                                     accept_multiple_files=True, key="evidencia_fotografica_uploader")
            form_data['evidencia_fotografica_names'] = [f.name for f in
                                                        evidencia_fotografica] if evidencia_fotografica else []
            form_data['evidencia_fotografica_files'] = evidencia_fotografica if evidencia_fotografica else []
            if evidencia_fotografica:
                for i, uploaded_file in enumerate(evidencia_fotografica):
                    st.image(uploaded_file, caption=f"Evidencia {i + 1}", use_column_width=True)

            form_data['responsable_llenado'] = st.text_input("Responsable del llenado:", help="",
                                                             key="responsable_llenado_input")

            submitted = st.form_submit_button("Guardar Ficha Técnica")

        # Move download button outside the form
        if submitted:
            st.success("Ficha Técnica guardada exitosamente!")

            # --- Generate PDF content using ReportLab ---
            def create_pdf(form_data, uploaded_files=None):
                # Create a BytesIO buffer for the PDF
                buffer = io.BytesIO()
                
                # Create the PDF document
                doc = SimpleDocTemplate(buffer, pagesize=A4)
                story = []
                
                # Get styles
                styles = getSampleStyleSheet()
                
                # Create custom styles
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=30,
                    alignment=TA_CENTER,
                    textColor=colors.HexColor('#FF6600')
                )
                
                subtitle_style = ParagraphStyle(
                    'CustomSubtitle',
                    parent=styles['Heading2'],
                    fontSize=14,
                    spaceAfter=20,
                    spaceBefore=20,
                    textColor=colors.HexColor('#FF6600')
                )
                
                normal_style = styles['Normal']
                
                # Title
                story.append(Paragraph("FICHA TÉCNICA DE RECORRIDO Y/O JUNTA VECINAL", title_style))
                story.append(Spacer(1, 20))
                
                # Main Information Section
                story.append(Paragraph("INFORMACIÓN PRINCIPAL", subtitle_style))
                
                # Create table for main information
                main_info_data = [
                    ["FOLIO:", str(form_data.get('folio', ''))],
                    ["FECHA DE ELABORACIÓN:", str(form_data.get('fecha_elaboracion', ''))],
                    ["TIPO DE EVENTO:", str(form_data.get('tipo_evento', ''))],
                    ["SECCIÓN:", str(form_data.get('seccion_main', ''))],
                    ["NOMBRE DEL EVENTO:", str(form_data.get('nombre_evento', ''))],
                    ["DISTRITO LOCAL:", str(form_data.get('distrito_local', ''))],
                    ["DISTRITO FEDERAL:", str(form_data.get('distrito_federal', ''))],
                    ["FECHA DEL EVENTO:", str(form_data.get('fecha_evento', ''))],
                    ["HORA INICIO:", str(form_data.get('hora_inicio', ''))],
                    ["HORA FIN:", str(form_data.get('hora_fin', ''))],
                    ["DURACIÓN:", str(form_data.get('duracion', ''))],
                    ["PRONÓSTICO CLIMÁTICO:", str(form_data.get('pronostico_climatico', ''))],
                    ["VESTIMENTA:", str(form_data.get('vestimenta', ''))],
                    ["QUIENES ENCABEZAN:", str(form_data.get('quienes_encabezan', ''))],
                ]
                
                main_table = Table(main_info_data, colWidths=[2*inch, 4*inch])
                main_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(main_table)
                story.append(Spacer(1, 20))
                
                # Objective and Background
                if form_data.get('objetivo'):
                    story.append(Paragraph("OBJETIVO", subtitle_style))
                    story.append(Paragraph(str(form_data.get('objetivo', '')), normal_style))
                    story.append(Spacer(1, 15))
                
                if form_data.get('antecedentes'):
                    story.append(Paragraph("ANTECEDENTES", subtitle_style))
                    story.append(Paragraph(str(form_data.get('antecedentes', '')), normal_style))
                    story.append(Spacer(1, 15))
                
                # Responsibles Section
                story.append(Paragraph("RESPONSABLES", subtitle_style))
                responsables_data = [
                    ["RESPONSABLE DEL EVENTO:", str(form_data.get('responsable_evento', ''))],
                    ["CONTACTO DEL RESPONSABLE:", str(form_data.get('contacto_responsable', ''))],
                    ["COMITÉ DE RECEPCIÓN:", str(form_data.get('comite_recepcion', ''))],
                    ["CONTACTO DEL COMITÉ:", str(form_data.get('contacto_comite', ''))],
                ]
                
                responsables_table = Table(responsables_data, colWidths=[2*inch, 4*inch])
                responsables_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(responsables_table)
                story.append(Spacer(1, 20))
                
                # Section Information
                story.append(Paragraph("INFORMACIÓN DE SECCIÓN", subtitle_style))
                seccion_data = [
                    ["NO. DE VIVIENDAS:", str(form_data.get('no_viviendas', ''))],
                    ["VOTANTES EN LA SECCIÓN:", str(form_data.get('votantes_seccion', ''))],
                    ["VOTANTES NECESARIOS:", str(form_data.get('votantes_necesarios', ''))],
                    ["RESULTADOS 2024:", str(form_data.get('resultados_2024', ''))],
                    ["RESULTADOS 2021:", str(form_data.get('resultados_2021', ''))],
                ]
                
                seccion_table = Table(seccion_data, colWidths=[2*inch, 4*inch])
                seccion_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(seccion_table)
                story.append(Spacer(1, 20))
                
                # Risk Situation
                story.append(Paragraph("SITUACIÓN DE RIESGO", subtitle_style))
                riesgo_data = [
                    ["SITUACIÓN DE RIESGO:", str(form_data.get('situacion_riesgo', ''))],
                    ["MOTIVO DE RIESGO:", str(form_data.get('motivo_riesgo', ''))],
                    ["CONTROL DE SEGURIDAD:", str(form_data.get('control_seguridad', ''))],
                ]
                
                riesgo_table = Table(riesgo_data, colWidths=[2*inch, 4*inch])
                riesgo_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(riesgo_table)
                story.append(Spacer(1, 20))
                
                # Event-specific details
                if form_data.get('tipo_evento') == "Recorrido":
                    story.append(Paragraph("DETALLES DEL RECORRIDO", subtitle_style))
                    recorrido_data = [
                        ["QUIENES ACOMPAÑAN:", str(form_data.get('quienes_acompanan', ''))],
                        ["NO. DE ACOMPAÑANTES:", str(form_data.get('no_acompanantes', ''))],
                        ["PUNTO DE PARTIDA:", str(form_data.get('punto_partida', ''))],
                        ["PUNTO FINAL:", str(form_data.get('punto_final', ''))],
                        ["DESCRIPCIÓN:", str(form_data.get('descripcion_recorrido', ''))],
                    ]
                    
                    recorrido_table = Table(recorrido_data, colWidths=[2*inch, 4*inch])
                    recorrido_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(recorrido_table)
                    story.append(Spacer(1, 20))
                
                elif form_data.get('tipo_evento') == "Junta Vecinal":
                    story.append(Paragraph("DETALLES DE LA JUNTA VECINAL", subtitle_style))
                    junta_data = [
                        ["QUIENES ASISTEN:", str(form_data.get('quienes_asisten', ''))],
                        ["POBLACIÓN ASISTENTE:", str(form_data.get('poblacion_asistente', ''))],
                        ["PUNTO DE REUNIÓN:", str(form_data.get('punto_reunion', ''))],
                        ["NO. DE ASISTENTES:", str(form_data.get('no_asistentes', ''))],
                        ["HORA INICIO REUNIÓN:", str(form_data.get('hora_inicio_reunion', ''))],
                        ["DURACIÓN REUNIÓN:", str(form_data.get('duracion_reunion', ''))],
                        ["TIPO DE ESPACIO:", str(form_data.get('tipo_espacio', ''))],
                        ["TIPO DE REUNIÓN:", str(form_data.get('tipo_reunion', ''))],
                    ]
                    
                    junta_table = Table(junta_data, colWidths=[2*inch, 4*inch])
                    junta_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(junta_table)
                    story.append(Spacer(1, 20))
                
                # Voter Population - Only show non-empty fields
                story.append(Paragraph("POBLACIÓN VOTANTE ESTIMADA", subtitle_style))
                votantes_data = []
                
                # Add only non-empty population fields
                if form_data.get('totales_votantes'):
                    votantes_data.append(["TOTALES:", str(form_data.get('totales_votantes', ''))])
                if form_data.get('necesarios_votantes'):
                    votantes_data.append(["NECESARIOS:", str(form_data.get('necesarios_votantes', ''))])
                if form_data.get('mujeres_votantes'):
                    votantes_data.append(["MUJERES:", str(form_data.get('mujeres_votantes', ''))])
                if form_data.get('hombres_votantes'):
                    votantes_data.append(["HOMBRES:", str(form_data.get('hombres_votantes', ''))])
                if form_data.get('baby_boomers'):
                    votantes_data.append(["BABY BOOMERS (61+):", str(form_data.get('baby_boomers', ''))])
                if form_data.get('generacion_x'):
                    votantes_data.append(["GENERACIÓN X (45-60):", str(form_data.get('generacion_x', ''))])
                if form_data.get('millenials'):
                    votantes_data.append(["MILLENNIALS (29-44):", str(form_data.get('millenials', ''))])
                if form_data.get('generacion_z'):
                    votantes_data.append(["GENERACIÓN Z (18-28):", str(form_data.get('generacion_z', ''))])
                
                # Only create table if there's data
                if votantes_data:
                    votantes_table = Table(votantes_data, colWidths=[2*inch, 4*inch])
                    votantes_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(votantes_table)
                    story.append(Spacer(1, 20))
                
                # Observations
                if form_data.get('observaciones'):
                    story.append(Paragraph("OBSERVACIONES", subtitle_style))
                    story.append(Paragraph(str(form_data.get('observaciones', '')), normal_style))
                    story.append(Spacer(1, 15))
                
                # Add uploaded images if any
                if uploaded_files:
                    story.append(Paragraph("EVIDENCIA FOTOGRÁFICA", subtitle_style))
                    
                    for i, uploaded_file in enumerate(uploaded_files):
                        try:
                            # Create a temporary file to save the uploaded image
                            temp_img = io.BytesIO(uploaded_file.read())
                            temp_img.seek(0)
                            
                            # Add image caption
                            story.append(Paragraph(f"Imagen {i+1}: {uploaded_file.name}", normal_style))
                            story.append(Spacer(1, 10))
                            
                            # Add image to PDF (resize to fit page width)
                            img = Image(temp_img, width=5*inch, height=3*inch, kind='proportional')
                            story.append(img)
                            story.append(Spacer(1, 15))
                            
                            # Reset file pointer for potential reuse
                            uploaded_file.seek(0)
                            
                        except Exception as e:
                            # If image processing fails, just add the filename
                            story.append(Paragraph(f"Imagen {i+1}: {uploaded_file.name} (Error al procesar)", normal_style))
                            story.append(Spacer(1, 10))
                
                # Responsible for filling
                story.append(Paragraph("RESPONSABLE DEL LLENADO", subtitle_style))
                story.append(Paragraph(str(form_data.get('responsable_llenado', '')), normal_style))
                
                # Build the PDF
                doc.build(story)
                
                # Get the value of the buffer
                pdf_bytes = buffer.getvalue()
                buffer.close()
                
                return pdf_bytes
            
            # Generate the PDF with uploaded files
            uploaded_files = form_data.get('evidencia_fotografica_files', [])
            pdf_bytes = create_pdf(form_data, uploaded_files)
            
            # Download button for PDF
            st.download_button(
                label="📄 Descargar Ficha Técnica (PDF)",
                data=pdf_bytes,
                file_name=f"ficha_tecnica_{form_data['folio'] or 'sin_folio'}.pdf",
                mime="application/pdf"
            )