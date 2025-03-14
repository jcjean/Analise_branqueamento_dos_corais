import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from matplotlib import pyplot as plt
import folium
from folium.plugins import HeatMap
from io import BytesIO

# Carregamento dos dados
def load_data():
    try:
        df = pd.read_csv('global_bleaching_environmental.csv', sep=';')
        return df
    except FileNotFoundError:
        st.error("Erro: O arquivo 'global_bleaching_environmental.csv' não foi encontrado.")
        st.stop()

df = load_data()

# Aplicação Streamlit
st.title("Análise de Branqueamento de Corais")

# Exibição opcional do DataFrame
if st.checkbox("Mostrar DataFrame"):
    st.write(df)

# Definição da paleta de cores degradê
custom_palette = ['#191970', '#00008b', '#20b2aa', '#2e8b57']

# Gráfico de barras por oceano
st.subheader("Contagem de Branqueamentos por Oceano")
fig, ax = plt.subplots()
df.groupby('Ocean_Name').size().plot(kind='barh', color=custom_palette, ax=ax)
ax.spines[['top', 'right']].set_visible(False)
st.pyplot(fig)

# Histograma da frequência de ciclones
st.subheader("Histograma da Frequência de Ciclones")
fig, ax = plt.subplots(figsize=(10, 6))
df['Cyclone_Frequency'].plot(kind='hist', bins=20, color=custom_palette[2], ax=ax)
ax.spines[['top', 'right']].set_visible(False)
st.pyplot(fig)

# Gráfico de dispersão: Ciclones x Branqueamento
df['Percent_Bleaching'] = pd.to_numeric(df['Percent_Bleaching'], errors='coerce')
df_grouped = df.groupby('Ecoregion_Name', as_index=False)[['Cyclone_Frequency', 'Percent_Bleaching']].mean()
st.subheader("Frequência de Ciclones vs. Percentual de Branqueamento")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df_grouped, x='Cyclone_Frequency', y='Percent_Bleaching', alpha=0.6, color=custom_palette[1], ax=ax)
st.pyplot(fig)

# Gráfico de barras de Branqueamento por Oceano
st.subheader("Branqueamento por Oceano")
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=df, x='Ocean_Name', y='Percent_Bleaching', ci=None, palette=custom_palette, ax=ax)
plt.xticks(rotation=30)
st.pyplot(fig)

# Mapa
st.subheader("Mapa de Calor do Branqueamento")

df['Latitude_Degrees'] = pd.to_numeric(df['Latitude_Degrees'], errors='coerce')
df['Longitude_Degrees'] = pd.to_numeric(df['Longitude_Degrees'], errors='coerce')
df['Percent_Bleaching'] = pd.to_numeric(df['Percent_Bleaching'], errors='coerce')
df['Percent_Bleaching'].fillna(0, inplace=True)

m = folium.Map(location=[df['Latitude_Degrees'].mean(), df['Longitude_Degrees'].mean()], zoom_start=4)
heat_data = list(zip(df['Latitude_Degrees'], df['Longitude_Degrees'], df['Percent_Bleaching']))
HeatMap(heat_data).add_to(m)

# Exibe o mapa no Streamlit
st_data = BytesIO()
m.save(st_data, close_file=False)
st.components.v1.html(st_data.getvalue().decode(), height=600)
plt.show()
