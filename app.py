import streamlit as st
import pandas as pd
import graphviz
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Estratégico Camacol - Asobancaria",
    layout="wide",
    page_icon="📊"
)

def generar_datos_completos(n=500):
    """Genera un dataset sintético robusto para los 5 ejes del dashboard."""
    np.random.seed(42)
    
    # --- 1. Perfil y Mercado ---
    edades = np.random.randint(23, 65, n)
    generos = np.random.choice(['Femenino', 'Masculino'], n)
    ocupaciones = np.random.choice(['Empleado', 'Independiente', 'Pensionado', 'Empresario'], n, p=[0.6, 0.3, 0.05, 0.05])
    contratos = np.random.choice(['Indefinido', 'Prestación Servicios', 'Obra Labor', 'Termino Fijo'], n)
    vivienda_ant = np.random.choice(['Arriendo', 'Familiar', 'Propia', 'Otra'], n)
    vive_ahi = np.random.choice(['Sí', 'No'], n, p=[0.75, 0.25]) # 25% Inversionistas
    
    # --- 2. Cierre Financiero ---
    bancos_list = ['Banco Davivienda', 'Bancolombia', 'Banco de Bogotá', 'BBVA', 'Banco Caja Social']
    bancos = np.random.choice(bancos_list, n)
    
    valor_vivienda = np.random.randint(135, 500, n) * 1000000 
    ltv = np.random.uniform(0.5, 0.8, n) # Loan to Value 50-80%
    monto_credito = valor_vivienda * ltv
    
    # Composición del pago
    ahorro_previo = valor_vivienda * np.random.uniform(0.1, 0.3, n)
    subsidio = valor_vivienda - monto_credito - ahorro_previo
    subsidio = np.maximum(subsidio, 0) # Ajuste para no tener negativos
    # Recalcular crédito para cerrar exacto
    monto_credito = valor_vivienda - ahorro_previo - subsidio
    
    meses_ahorro = np.random.randint(6, 36, n)
    codeudor = np.random.choice(['Sí', 'No'], n, p=[0.4, 0.6])
    
    # --- 3. Carga y Riesgo ---
    ingresos = np.random.randint(3, 20, n) * 1000000
    # Si hay codeudor, aumentamos ingresos ficticiamente para el cálculo
    ingresos_unificados = np.where(codeudor == 'Sí', ingresos * 1.6, ingresos)
    
    cuota_mensual = monto_credito * 0.011 # Aprox tasa actual
    arriendo_previo = np.where(vivienda_ant == 'Arriendo', ingresos * 0.25, 0)
    
    intencion_abono = np.random.choice(['Alta', 'Media', 'Baja'], n)
    
    # --- 4. Sostenibilidad ---
    conoce_verde = np.random.choice(['Sí', 'No'], n)
    certificacion = np.random.choice(['EDGE', 'CASA', 'LEED', 'Sin Certificación'], n, p=[0.25, 0.2, 0.05, 0.5])
    tipo_entrega = np.random.choice(['Obra Gris', 'Acabados'], n, p=[0.6, 0.4])
    gasto_remodelacion = np.where(tipo_entrega == 'Obra Gris', valor_vivienda * 0.15, valor_vivienda * 0.05)
    usa_credito_obra = np.random.choice(['Sí', 'No'], n, p=[0.3, 0.7])
    fase_remodelacion = np.random.choice(['Planea', 'Contrata', 'Financia', 'Finalizado'], n)
    
    # --- 5. Experiencia ---
    nps_banco_val = np.random.randint(1, 8, n) # Escala 1-7
    nps_constr_val = np.random.randint(1, 8, n)
    calificacion_calidad = np.random.randint(3, 8, n)
    calificacion_precio = np.random.randint(3, 8, n)
    
    aspectos_neg = ['Atención Cliente', 'Demora Entrega', 'Acabados', 'Trámites Banco', 'Costos Adicionales']
    aspectos_pos = ['Ubicación', 'Diseño', 'Zonas Comunes', 'Precio', 'Asesoría']
    feedback_neg = np.random.choice(aspectos_neg, n)
    feedback_pos = np.random.choice(aspectos_pos, n)

    df = pd.DataFrame({
        'ID_Cliente': range(1000, 1000 + n),
        'Edad': edades, 'Genero': generos, 'Ocupacion': ocupaciones, 'Contrato': contratos,
        'Vivienda_Anterior': vivienda_ant, 'Vive_Ahi': vive_ahi,
        'Banco': bancos, 'Valor_Vivienda': valor_vivienda, 'Monto_Credito': monto_credito,
        'Ahorro': ahorro_previo, 'Subsidio': subsidio, 'Meses_Ahorro': meses_ahorro, 'Codeudor': codeudor,
        'Ingresos': ingresos_unificados, 'Cuota': cuota_mensual, 'Arriendo_Previo': arriendo_previo,
        'Intencion_Abono': intencion_abono,
        'Conoce_Verde': conoce_verde, 'Certificacion': certificacion, 'Tipo_Entrega': tipo_entrega,
        'Gasto_Remodelacion': gasto_remodelacion, 'Usa_Credito_Obra': usa_credito_obra, 'Fase_Remodelacion': fase_remodelacion,
        'NPS_Banco': nps_banco_val, 'NPS_Constructora': nps_constr_val,
        'Calidad': calificacion_calidad, 'Precio': calificacion_precio,
        'Aspecto_Negativo': feedback_neg, 'Aspecto_Positivo': feedback_pos
    })
    return df

# --- Interfaz Principal ---
st.title("🏦 Dashboard Estratégico: Camacol - Superfinanciera")
st.markdown("Análisis integral del comprador de vivienda, cierre financiero y sostenibilidad.")

# Carga de Datos
if 'data' not in st.session_state:
    st.session_state['data'] = generar_datos_completos()

uploaded_file = st.sidebar.file_uploader("Cargar Excel (Opcional)", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.session_state['data'] = df
        st.sidebar.success("Datos cargados correctamente.")
    except:
        st.sidebar.error("Error cargando archivo. Usando datos simulados.")

df = st.session_state['data']

# Tabs de Navegación
tabs = st.tabs([
    "1. Perfil y Mercado", 
    "2. Cierre Financiero", 
    "3. Carga y Riesgo", 
    "4. Sostenibilidad y Obra", 
    "5. Experiencia (NPS)",
    "🛠️ Esquema Técnico"
])

# --- TAB 1: PERFIL Y MERCADO ---
with tabs[0]:
    st.subheader("👤 Perfil del Comprador y Mercado")
    
    # Filtros
    c1, c2, c3 = st.columns(3)
    f_edad = c1.slider("Rango de Edad", int(df['Edad'].min()), int(df['Edad'].max()), (25, 50))
    f_viv = c2.multiselect("Vivienda Anterior", df['Vivienda_Anterior'].unique(), default=df['Vivienda_Anterior'].unique())
    
    df_t1 = df[(df['Edad'].between(f_edad[0], f_edad[1])) & (df['Vivienda_Anterior'].isin(f_viv))]

    # KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("Ticket Promedio Venta", f"${df_t1['Valor_Vivienda'].mean()/1e6:,.0f} M")
    tasa_inv = (len(df_t1[df_t1['Vive_Ahi']=='No']) / len(df_t1)) * 100
    k2.metric("Tasa Inversión (No viven ahí)", f"{tasa_inv:.1f}%")
    k3.metric("NPS Promedio (Constructora)", f"{df_t1['NPS_Constructora'].mean():.1f}/7")

    # Gráficos
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("**Pirámide Poblacional (Género/Edad)**")
        # Simulación de pirámide con plotly bar
        df_pyr = df_t1.groupby(['Genero', pd.cut(df_t1['Edad'], bins=[20,30,40,50,60,70])]).size().reset_index(name='Count')
        df_pyr['Count'] = np.where(df_pyr['Genero'] == 'Masculino', -df_pyr['Count'], df_pyr['Count'])
        df_pyr['Edad_Str'] = df_pyr['Edad'].astype(str)
        fig_pyr = px.bar(df_pyr, x='Count', y='Edad_Str', color='Genero', orientation='h', 
                         color_discrete_map={'Masculino': '#1f77b4', 'Femenino': '#e377c2'})
        st.plotly_chart(fig_pyr, use_container_width=True)

    with col_g2:
        st.markdown("**Ocupación y Tipo de Contrato**")
        fig_tree = px.treemap(df_t1, path=['Ocupacion', 'Contrato'], title="Distribución Laboral")
        st.plotly_chart(fig_tree, use_container_width=True)

# --- TAB 2: CIERRE FINANCIERO ---
with tabs[1]:
    st.subheader("💰 Salud Financiera y Estructura de Pagos")
    
    # Filtros
    banco_sel = st.multiselect("Filtrar Banco", df['Banco'].unique(), default=df['Banco'].unique())
    df_t2 = df[df['Banco'].isin(banco_sel)]

    # KPIs
    k1, k2, k3 = st.columns(3)
    ltv_prom = (df_t2['Monto_Credito'].sum() / df_t2['Valor_Vivienda'].sum()) * 100
    k1.metric("LTV Promedio (Préstamo/Valor)", f"{ltv_prom:.1f}%")
    k2.metric("Meses Ahorro Promedio", f"{df_t2['Meses_Ahorro'].mean():.1f} meses")
    tasa_unif = (len(df_t2[df_t2['Codeudor']=='Sí']) / len(df_t2)) * 100
    k3.metric("Tasa Unificación Ingresos (Codeudor)", f"{tasa_unif:.1f}%")

    # Gráficos
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Cascada de Financiación Promedio**")
        vals = [df_t2['Ahorro'].mean(), df_t2['Subsidio'].mean(), df_t2['Monto_Credito'].mean()]
        fig_water = go.Figure(go.Waterfall(
            measure=["relative", "relative", "relative", "total"],
            x=["Ahorro", "Subsidio", "Crédito", "Total Vivienda"],
            y=[vals[0], vals[1], vals[2], 0],
            text=[f"{v/1e6:.0f}M" for v in vals] + [f"{sum(vals)/1e6:.0f}M"]
        ))
        st.plotly_chart(fig_water, use_container_width=True)
    
    with c2:
        st.markdown("**Participación por Banco**")
        fig_bar = px.bar(df_t2['Banco'].value_counts(), orientation='h')
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 3: CARGA Y RIESGO ---
with tabs[2]:
    st.subheader("⚠️ Análisis de Riesgo y Capacidad de Pago")
    
    # KPIs
    ratio_ci = (df['Cuota'].sum() / df['Ingresos'].sum()) * 100
    k1, k2, k3 = st.columns(3)
    k1.metric("Ratio Cuota/Ingreso (Hogar)", f"{ratio_ci:.1f}%")
    
    # Indice sustitución: Cuota vs Arriendo previo (solo para quienes pagaban arriendo)
    df_arriendo = df[df['Arriendo_Previo'] > 0]
    sustitucion = (df_arriendo['Cuota'].mean() / df_arriendo['Arriendo_Previo'].mean())
    k2.metric("Índice Sustitución (Cuota vs Arriendo)", f"{sustitucion:.2f}x")
    
    abono_alto = (len(df[df['Intencion_Abono']=='Alta']) / len(df)) * 100
    k3.metric("% Intención Abono a Capital", f"{abono_alto:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Scatter: Ingresos vs Cuota (Zonas de Riesgo)**")
        fig_scat = px.scatter(df, x='Ingresos', y='Cuota', color='Intencion_Abono', 
                              size='Monto_Credito', hover_data=['Banco'])
        # Linea de referencia 30% ingreso
        fig_scat.add_shape(type="line", x0=0, y0=0, x1=df['Ingresos'].max(), y1=df['Ingresos'].max()*0.3,
                           line=dict(color="Red", width=2, dash="dash"))
        st.plotly_chart(fig_scat, use_container_width=True)
    
    with col2:
        st.markdown("**Brecha: Arriendo Anterior vs Cuota Actual**")
        # Comparativo promedio agrupado por rango de ingreso
        df['Rango_Ingreso'] = pd.qcut(df['Ingresos'], 4, labels=["Bajo", "Medio-Bajo", "Medio-Alto", "Alto"])
        df_brecha = df[df['Arriendo_Previo']>0].groupby('Rango_Ingreso')[['Arriendo_Previo', 'Cuota']].mean().reset_index()
        fig_brecha = px.bar(df_brecha, x='Rango_Ingreso', y=['Arriendo_Previo', 'Cuota'], barmode='group')
        st.plotly_chart(fig_brecha, use_container_width=True)

# --- TAB 4: SOSTENIBILIDAD Y OBRA ---
with tabs[3]:
    st.subheader("🌱 Sostenibilidad y Mercado Secundario (Remodelación)")
    
    k1, k2, k3 = st.columns(3)
    conciencia = (len(df[df['Conoce_Verde']=='Sí'])/len(df))*100
    k1.metric("Índice Conciencia Verde", f"{conciencia:.1f}%")
    k2.metric("Inv. Promedio Remodelación", f"${df['Gasto_Remodelacion'].mean()/1e6:.1f} M")
    uso_cred = (len(df[df['Usa_Credito_Obra']=='Sí'])/len(df))*100
    k3.metric("Ratio Crédito para Obra", f"{uso_cred:.1f}%")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Certificaciones Sostenibles**")
        fig_don = px.pie(df, names='Certificacion', hole=0.4)
        st.plotly_chart(fig_don, use_container_width=True)
    with c2:
        st.markdown("**Funnel de Remodelación**")
        df_funnel = df.groupby('Fase_Remodelacion').size().reset_index(name='Count')
        # Ordenar lógicamente
        order = {'Planea':1, 'Contrata':2, 'Financia':3, 'Finalizado':4}
        df_funnel['Order'] = df_funnel['Fase_Remodelacion'].map(order)
        df_funnel = df_funnel.sort_values('Order')
        fig_fun = px.funnel(df_funnel, x='Count', y='Fase_Remodelacion')
        st.plotly_chart(fig_fun, use_container_width=True)
    with c3:
        st.markdown("**Gasto por Tipo de Entrega**")
        fig_box = px.box(df, x='Tipo_Entrega', y='Gasto_Remodelacion')
        st.plotly_chart(fig_box, use_container_width=True)

# --- TAB 5: EXPERIENCIA ---
with tabs[4]:
    st.subheader("⭐ Experiencia del Cliente (NPS)")
    
    k1, k2, k3 = st.columns(3)
    k1.metric("NPS Banco (1-7)", f"{df['NPS_Banco'].mean():.1f}")
    k2.metric("NPS Constructora (1-7)", f"{df['NPS_Constructora'].mean():.1f}")
    gap = df['Calidad'].mean() - df['Precio'].mean()
    k3.metric("Gap Calidad - Precio", f"{gap:+.2f}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Matriz de Valor: Precio vs Calidad**")
        fig_mat = px.density_heatmap(df, x='Precio', y='Calidad', nbinsx=7, nbinsy=7, text_auto=True)
        st.plotly_chart(fig_mat, use_container_width=True)
    
    with c2:
        st.markdown("**Pareto: Aspectos Negativos**")
        df_par = df['Aspecto_Negativo'].value_counts().reset_index()
        df_par.columns = ['Aspecto', 'Quejas']
        fig_par = px.bar(df_par, x='Aspecto', y='Quejas')
        st.plotly_chart(fig_par, use_container_width=True)

# --- TAB 6: ESQUEMA TÉCNICO (ERD) ---
with tabs[5]:
    st.header("📘 Diccionario de Datos y Reglas ETL")
    st.markdown("Especificación técnica de campos, formatos y transformaciones requeridas para la ingesta de datos.")

    # Definición del Esquema (Data Dictionary)
    schema_data = [
        {"Campo": "ID_Encuesta", "Tipo de Dato": "Integer (PK)", "Categoría": "Control", "Descripción": "Número único de identificación.", "Regla ETL": "Incremental."},
        {"Campo": "Nombre_Proyecto", "Tipo de Dato": "String / Text", "Categoría": "Control", "Descripción": "Nombre del conjunto o edificio.", "Regla ETL": "Estandarizar nombres (limpieza de tildes/mayúsculas)."},
        {"Campo": "Fase_Compra", "Tipo de Dato": "Categorical", "Categoría": "Control", "Descripción": "Sobre planos, Construcción, Entrega.", "Regla ETL": "Agrupar respuestas similares."},
        {"Campo": "Condicion_Entrega", "Tipo de Dato": "Categorical", "Categoría": "Control", "Descripción": "Obra gris, Acabados.", "Regla ETL": "Binario o Categórico."},
        {"Campo": "Valor_Vivienda", "Tipo de Dato": "Decimal / Float", "Categoría": "Control", "Descripción": "Precio total de la transacción ($).", "Regla ETL": "Eliminar símbolos de moneda y puntos."},
        {"Campo": "Edad", "Tipo de Dato": "Integer", "Categoría": "Caracterización", "Descripción": "Edad del comprador en años.", "Regla ETL": 'Crear "Buckets" (ej: 25-34, 35-44).'},
        {"Campo": "Escolaridad", "Tipo de Dato": "Categorical", "Categoría": "Caracterización", "Descripción": "Primaria, Grado, Posgrado, etc.", "Regla ETL": "Ordenar por nivel jerárquico."},
        {"Campo": "Tipo_Contrato", "Tipo de Dato": "Categorical", "Categoría": "Caracterización", "Descripción": "Término fijo, indefinido, prestación.", "Regla ETL": "Crucial para análisis de riesgo."},
        {"Campo": "Ingresos_Mensuales_Pers", "Tipo de Dato": "Decimal", "Categoría": "Caracterización", "Descripción": "Ingresos del encuestado ($).", "Regla ETL": "Formato numérico puro."},
        {"Campo": "Ingresos_Totales_Hogar", "Tipo de Dato": "Decimal", "Categoría": "Caracterización", "Descripción": "Suma de todos los ingresos del hogar.", "Regla ETL": "Usar para el ratio Cuota/Ingreso."},
        {"Campo": "Hijos_Cant", "Tipo de Dato": "Integer", "Categoría": "Caracterización", "Descripción": "Número de hijos actuales.", "Regla ETL": "Escala numérica."},
        {"Campo": "Plan_Hijos_Futuro", "Tipo de Dato": "Boolean / String", "Categoría": "Caracterización", "Descripción": "Sí / No / No sabe.", "Regla ETL": "Métrica de ciclo de vida del hogar."},
        {"Campo": "Motivo_Compra_Principal", "Tipo de Dato": "Categorical (Tag)", "Categoría": "Razones", "Descripción": "Inversión, Vivienda propia, Cambio.", "Regla ETL": "NLP: Extraer palabra clave de respuesta abierta."},
        {"Campo": "Estatus_Vivienda_Actual", "Tipo de Dato": "Categorical", "Categoría": "Razones", "Descripción": "Habitada, Arrendada, Vendida, Vacía.", "Regla ETL": 'Derivado de "¿Vive ahí?" y "¿Ya arrendó?".'},
        {"Campo": "Valor_Canon_Arriendo", "Tipo de Dato": "Decimal", "Categoría": "Razones", "Descripción": "Valor de arriendo (real o esperado).", "Regla ETL": "Para cálculo de Yield (rentabilidad)."},
        {"Campo": "Ahorro_Tiempo_Meses", "Tipo de Dato": "Integer", "Categoría": "Cierre Financiero", "Descripción": "Tiempo de ahorro previo a la compra.", "Regla ETL": "Convertir años a meses para uniformidad."},
        {"Campo": "Uso_Codeudor", "Tipo de Dato": "Boolean", "Categoría": "Cierre Financiero", "Descripción": "1 = Sí, 0 = No.", "Regla ETL": 'Basado en "unificó ingresos".'},
        {"Campo": "Ingresos_Unificados_Monto", "Tipo de Dato": "Decimal", "Categoría": "Cierre Financiero", "Descripción": "Monto total con codeudor ($).", "Regla ETL": "Solo si Uso_Codeudor es True."},
        {"Campo": "Banco_Credito", "Tipo de Dato": "String", "Categoría": "Cierre Financiero", "Descripción": "Nombre de la entidad financiera.", "Regla ETL": "Estandarizar nombres de bancos."},
        {"Campo": "Cuota_Mensual_Credito", "Tipo de Dato": "Decimal", "Categoría": "Caracterización", "Descripción": "Valor pagado al banco mensualmente.", "Regla ETL": "Para cálculo de carga financiera."},
        {"Campo": "Certificacion_Sust", "Tipo de Dato": "Boolean", "Categoría": "Sostenibilidad", "Descripción": "¿Sabe si tiene certificación?", "Regla ETL": "1 = Sí, 0 = No / No sabe."},
        {"Campo": "Gasto_Remodelacion", "Tipo de Dato": "Decimal", "Categoría": "Remodelaciones", "Descripción": "Monto invertido o por invertir.", "Regla ETL": "Para análisis de mercado secundario."},
        {"Campo": "NPS_Constructora", "Tipo de Dato": "Integer (1-7)", "Categoría": "Expectativas", "Descripción": "Calificación de recomendación.", "Regla ETL": "Escala original (1 a 7)."},
        {"Campo": "NPS_Banco", "Tipo de Dato": "Integer (1-7)", "Categoría": "Expectativas", "Descripción": "Calificación de recomendación.", "Regla ETL": "Escala original (1 a 7)."},
        {"Campo": "Calidad_Precio_Ratio", "Tipo de Dato": "Integer (1-7)", "Categoría": "Expectativas", "Descripción": "Calificación percibida.", "Regla ETL": "Escala original (1 a 7)."},
        {"Campo": "Tag_Positivo", "Tipo de Dato": "Categorical (Tag)", "Categoría": "Expectativas", "Descripción": "Categoría del aspecto positivo.", "Regla ETL": 'NLP: Ej: "Ubicación", "Zonas Verdes".'},
        {"Campo": "Tag_Negativo", "Tipo de Dato": "Categorical (Tag)", "Categoría": "Expectativas", "Descripción": "Categoría del aspecto negativo.", "Regla ETL": 'NLP: Ej: "Retrasos", "Acabados".'}
    ]
    
    df_schema = pd.DataFrame(schema_data)
    st.dataframe(df_schema, use_container_width=True)

    st.divider()
    st.subheader("🕸️ Diagrama de Relaciones (ERD)")
    st.write("Modelo lógico generado dinámicamente a partir del diccionario de datos.")
    
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')
    graph.attr('node', shape='record', style='filled', fillcolor='lightblue')

    # Agrupar campos por Categoría para crear las entidades del modelo
    for categoria in df_schema['Categoría'].unique():
        campos = df_schema[df_schema['Categoría'] == categoria]['Campo'].tolist()
        
        # Crear nodo tipo 'record' con los campos listados verticalmente
        label_campos = "|".join([f"<{c}> {c}" for c in campos])
        label = f"{{ {categoria} | {{ {label_campos} }} }}"
        
        # Color distintivo para la tabla de Control (Principal/PK)
        color = '#ffcc80' if categoria == 'Control' else '#e1f5fe'
        
        graph.node(categoria, label=label, fillcolor=color)
        
        # Establecer relaciones (Modelo Estrella centrado en Control)
        if categoria != 'Control':
            graph.edge('Control', categoria)

    st.graphviz_chart(graph)
