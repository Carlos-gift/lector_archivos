import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la App
st.title("Aplicación de Análisis de Datos 📊")

# Subida de Archivo
archivo = st.file_uploader("Carga un archivo CSV o Excel", type=["csv", "xlsx"])

# Cuando se carga el archivo
if archivo is not None:
    # Detectar el tipo de archivo
    if archivo.name.endswith('.csv'):
        df = pd.read_csv(archivo, encoding='latin1')  # Soporte ñ y tildes
    elif archivo.name.endswith('.xlsx'):
        df = pd.read_excel(archivo)

    st.subheader("Vista previa de los datos:")
    st.dataframe(df)

    # Resumen General
    st.subheader("Resumen General:")
    st.write(f"Cantidad de registros: {df.shape[0]}")
    st.write(f"Cantidad de columnas: {df.shape[1]}")
    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    columnas_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    st.write(f"Columnas numéricas detectadas: {', '.join(columnas_numericas)}")

    # Agrupación de datos
    if columnas_categoricas:
        st.subheader("Agrupar Datos:")
        seleccion_categorias = st.multiselect("Selecciona las columnas para agrupar", columnas_categoricas)

        operacion = st.radio(
            "¿Qué quieres hacer con los datos agrupados?",
            ("Contar registros", "Sumar columna numérica")
        )

        if seleccion_categorias:
            if operacion == "Sumar columna numérica" and columnas_numericas:
                seleccion_numerica = st.selectbox("Selecciona la columna numérica a sumar", columnas_numericas)

                resumen = df.groupby(seleccion_categorias)[seleccion_numerica].sum().reset_index()
                valores = resumen[seleccion_numerica]
                categorias = resumen.apply(lambda x: " | ".join(str(x[c]) for c in seleccion_categorias), axis=1)

            elif operacion == "Contar registros":
                resumen = df.groupby(seleccion_categorias).size().reset_index(name='Conteo')
                valores = resumen['Conteo']
                categorias = resumen.apply(lambda x: " | ".join(str(x[c]) for c in seleccion_categorias), axis=1)

            else:
                resumen = None
                valores = []
                categorias = []

            if resumen is not None:
                st.subheader("Resultado del Agrupamiento:")
                st.dataframe(resumen)

                # Elección de tipo de gráfico
                st.subheader("Gráfico del Agrupamiento:")
                mostrar_barras = st.checkbox("Gráfico de Barras")
                mostrar_torta = st.checkbox("Gráfico de Torta")

                if mostrar_barras:
                    plt.figure(figsize=(12,7))
                    colores = plt.cm.tab20.colors
                    plt.bar(categorias, valores, color=colores[:len(valores)])

                    # Agregar los valores encima de cada barra
                    for i, valor in enumerate(valores):
                        plt.text(i, valor, f'{valor:.0f}', ha='center', va='bottom')

                    plt.title("Agrupación de Datos - Barras", fontsize=14)
                    plt.xlabel("Categorías", fontsize=12)
                    plt.ylabel("Valor", fontsize=12)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(plt)

                if mostrar_torta:
                    plt.figure(figsize=(8,8))
                    plt.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=140)
                    plt.axis('equal')
                    plt.title("Agrupación de Datos - Torta", fontsize=14)
                    st.pyplot(plt)
