import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 📈 Título de la App
st.title("Aplicación de Análisis de Datos 📊")

# 📁 Subida de Archivo
archivo = st.file_uploader("🗂️ Carga un archivo CSV o Excel", type=["csv", "xlsx"])

# 📂 Lectura del Archivo
if archivo is not None:
    if archivo.name.endswith('.csv'):
         df = pd.read_csv(archivo, encoding='latin1', sep=None, engine='python', on_bad_lines='skip')
    elif archivo.name.endswith('.xlsx'):
        df = pd.read_excel(archivo)

    # 🔢 Vista previa de los datos
    st.subheader("🔢 Vista previa de los datos:")
    st.dataframe(df)

    # 📃 Resumen General
    st.subheader("📃 Resumen General:")
    st.write(f"Cantidad de registros: {df.shape[0]}")
    st.write(f"Cantidad de columnas: {df.shape[1]}")
    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    columnas_categoricas = df.select_dtypes(include=['object']).columns.tolist()
    st.write(f"Columnas numéricas detectadas: {', '.join(columnas_numericas)}")

    # 🛀 Agrupación de datos
    if columnas_categoricas:
        st.subheader("🛀 Agrupar Datos:")
        seleccion_categorias = st.multiselect("Selecciona las columnas para agrupar", columnas_categoricas)

        operacion = st.radio(
            "✅ ¿Qué quieres hacer con los datos agrupados?",
            ("Contar registros", "Sumar columna numérica")
        )

        if len(seleccion_categorias) == 2:
            filtro_categoria = st.selectbox("Selecciona la categoría para aplicar un filtro", seleccion_categorias)
            categoria_filtrada = st.selectbox(f"Selecciona un valor de {filtro_categoria}", df[filtro_categoria].dropna().unique())
            df = df[df[filtro_categoria] == categoria_filtrada]
            seleccion_categorias = [c for c in seleccion_categorias if c != filtro_categoria]

        if seleccion_categorias:
            if operacion == "Sumar columna numérica" and columnas_numericas:
                seleccion_numerica = st.selectbox("Selecciona la columna numérica a sumar", columnas_numericas)
                resumen = df.groupby(seleccion_categorias)[seleccion_numerica].sum().reset_index()
                valores = resumen[seleccion_numerica]
            elif operacion == "Contar registros":
                resumen = df.groupby(seleccion_categorias).size().reset_index(name='Conteo')
                valores = resumen['Conteo']
            categorias = resumen.apply(lambda x: " | ".join(str(x[c]) for c in seleccion_categorias), axis=1)

            st.subheader("📜 Resultado del Agrupamiento:")
            st.dataframe(resumen)

            # 🌀 Gráficos
            st.subheader("🌀 Gráficos del Agrupamiento:")

            mostrar_barras = st.checkbox("🔹 Mostrar Gráfico de Barras")
            if mostrar_barras:
                st.markdown("**Opciones de Barras:**")
                mostrar_valores_barras = st.checkbox("Mostrar valores reales en Barras")
                mostrar_porcentaje_barras = st.checkbox("Mostrar porcentaje en Barras")

                plt.figure(figsize=(12,7))
                colores = plt.cm.tab20.colors
                total_valores = sum(valores)
                plt.bar(categorias, valores, color=colores[:len(valores)])

                for i, valor in enumerate(valores):
                    etiqueta = ""
                    if mostrar_valores_barras:
                        etiqueta += f"{valor:.0f}"
                    if mostrar_porcentaje_barras:
                        porcentaje = (valor / total_valores) * 100
                        etiqueta += f" ({porcentaje:.1f}%)"
                    plt.text(i, valor, etiqueta, ha='center', va='bottom', fontsize=8)

                plt.title("Agrupación de Datos - Barras")
                plt.xlabel("Categorías")
                plt.ylabel("Valor")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(plt)

            mostrar_torta = st.checkbox("🍰 Mostrar Gráfico de Torta")
            if mostrar_torta:
                st.markdown("**Opciones de Torta:**")
                mostrar_valores_torta = st.checkbox("Mostrar valores reales en Torta")
                mostrar_porcentaje_torta = st.checkbox("Mostrar porcentaje en Torta", value=True)

                etiquetas = []
                total_valores = sum(valores)
                for i, valor in enumerate(valores):
                    etiqueta = categorias[i]
                    detalles = []
                    if mostrar_valores_torta:
                        detalles.append(f"{valor:.0f}")
                    if mostrar_porcentaje_torta:
                        porcentaje = (valor / total_valores) * 100
                        detalles.append(f"{porcentaje:.1f}%")
                    if detalles:
                        etiqueta += " (" + ", ".join(detalles) + ")"
                    etiquetas.append(etiqueta)

                plt.figure(figsize=(8,8))
                plt.pie(valores, labels=etiquetas, startangle=140)
                plt.axis('equal')
                plt.title("Agrupación de Datos - Torta")
                st.pyplot(plt)



