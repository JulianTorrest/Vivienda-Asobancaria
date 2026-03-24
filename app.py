import streamlit as st
import pandas as pd
import graphviz
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Camacol - Esquema BD",
    layout="wide",
    page_icon="📊"
)

def generar_datos_dummy():
    """Genera datos de prueba simulando el entorno Asobancaria/Camacol."""
    
    # Tabla 1: Entidades Financieras (Bancos)
    bancos_data = {
        'ID_Banco': [101, 102, 103, 104],
        'Nombre_Banco': ['Banco A', 'Banco B', 'Financiera C', 'Cooperativa D'],
        'Tipo': ['Comercial', 'Comercial', 'Financiera', 'Cooperativa']
    }
    df_bancos = pd.DataFrame(bancos_data)

    # Tabla 2: Proyectos de Vivienda
    proyectos_data = {
        'ID_Proyecto': [5001, 5002, 5003, 5004],
        'Nombre_Proyecto': ['Residencial Altos', 'Edificio Centro', 'Villas del Norte', 'Apartamentos Sur'],
        'Ciudad': ['Bogotá', 'Medellín', 'Cali', 'Barranquilla'],
        'Valor_Proyecto_Millones': [15000, 8000, 5000, 12000]
    }
    df_proyectos = pd.DataFrame(proyectos_data)

    # Tabla 3: Créditos (Tabla de hechos que une Bancos y Proyectos)
    creditos_data = {
        'ID_Credito': range(1000, 1010),
        'ID_Banco': np.random.choice(df_bancos['ID_Banco'], 10),
        'ID_Proyecto': np.random.choice(df_proyectos['ID_Proyecto'], 10),
        'Monto_Desembolsado': np.random.randint(100, 500, 10) * 1000000,
        'Estado': np.random.choice(['Aprobado', 'En Estudio', 'Rechazado'], 10)
    }
    df_creditos = pd.DataFrame(creditos_data)

    return {"Bancos": df_bancos, "Proyectos": df_proyectos, "Créditos": df_creditos}

# --- Interfaz Principal ---
st.title("🏦 Diseño de Dashboard Camacol - Superfinanciera")
st.markdown("Esta aplicación muestra la estructura de datos y el esquema relacional.")

# Sidebar para cargar archivo real (opcional)
uploaded_file = st.sidebar.file_uploader("Cargar Excel Real (Opcional)", type=["xlsx"])

if uploaded_file:
    st.sidebar.success("Archivo cargado. Usando datos del Excel.")
    # Lógica para leer el excel real (simplificada para leer todas las hojas)
    try:
        xls = pd.ExcelFile(uploaded_file)
        data_frames = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
    except Exception as e:
        st.error(f"Error leyendo el archivo: {e}")
        data_frames = generar_datos_dummy()
else:
    st.sidebar.info("Usando datos simulados (Dummy Data).")
    data_frames = generar_datos_dummy()

# Creación de Tabs (Pestañas)
tab1, tab2 = st.tabs(["🗃️ Explorador de Datos", "🕸️ Esquema de Base de Datos (ERD)"])

with tab1:
    st.header("Exploración de Tablas")
    st.write("A continuación se muestran las tablas que componen el modelo de datos:")
    
    # Iterar sobre los dataframes disponibles y mostrarlos
    for nombre_tabla, df in data_frames.items():
        with st.expander(f"Tabla: {nombre_tabla}", expanded=True):
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(df)} registros encontrados.")

with tab2:
    st.header("Diagrama Entidad-Relación")
    st.write("Visualización gráfica de cómo se relacionan las tablas.")
    
    # Crear objeto Graphviz
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR') # De izquierda a derecha
    graph.attr('node', shape='record', style='filled', fillcolor='lightblue')

    # Lógica para dibujar nodos basados en las columnas de los DataFrames
    for nombre_tabla, df in data_frames.items():
        # Crear etiqueta HTML-like para mostrar nombre de tabla y columnas
        cols = "|".join([f"<{col}> {col}" for col in df.columns])
        label = f"{{ {nombre_tabla} | {{ {cols} }} }}"
        graph.node(nombre_tabla, label=label)

    # Definir relaciones (Si son datos dummy, las conocemos. Si es archivo real, se infieren o se dejan sueltas)
    if not uploaded_file:
        # Relaciones hardcoded para el ejemplo dummy
        graph.edge('Bancos:ID_Banco', 'Créditos:ID_Banco', label='1 a N')
        graph.edge('Proyectos:ID_Proyecto', 'Créditos:ID_Proyecto', label='1 a N')
    else:
        st.info("Nota: Para archivos subidos dinámicamente, las relaciones automáticas requieren nombres de columnas coincidentes exactos (FK/PK).")
        # Intento simple de inferencia de relaciones por nombre de columna
        tablas = list(data_frames.keys())
        for i in range(len(tablas)):
            for j in range(len(tablas)):
                if i != j:
                    t1 = tablas[i]
                    t2 = tablas[j]
                    # Intersección de columnas
                    cols_comunes = set(data_frames[t1].columns).intersection(set(data_frames[t2].columns))
                    for col in cols_comunes:
                        # Si comparten una columna (ej: ID_Banco), dibujamos una linea
                        graph.edge(f'{t1}:{col}', f'{t2}:{col}', style='dashed')

    st.graphviz_chart(graph)
