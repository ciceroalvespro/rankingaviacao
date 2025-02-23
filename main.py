# importando as bibliotecas
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# configurando a pagina
st.set_page_config(
    layout="wide",
    page_icon=":bar_chart:",
    page_title="Ranking Aeroportos"
)
# url do banco de dados
base_url = "https://raw.githubusercontent.com/ciceroalvespro/portifolio_python_streamlit/master/Dados%20publicos%20anac/dados_publicos_anac_{}.csv"

#Titulo da página
st.markdown("<h2 style='color:#004E8c'>Ranking e Evolução dos Aeroportos Brasileiros</h2>",
            unsafe_allow_html=True)
st.markdown("<span style='color:#cccc'>*Fonte: Agência Nacional de Aviação Civil - ANAC*</span>",
            unsafe_allow_html=True)

# lista para armazenar os arquivos
dfs = []

# loop para concatenar os arquivos apos colocar no df
for year in range(2013, 2024):
    url = base_url.format(year)
    df = pd.read_csv(url, sep=";")
    dfs.append(df)

# Concatenar todos os DataFrames em um único DataFrame
df = pd.concat(dfs, ignore_index=True)

# df origem (decolagem)
pd.options.mode.copy_on_write = True
# filtrar o pais de origen (Brasil)
df_origem = df[df["AEROPORTO DE ORIGEM (PAÍS)"] == "BRASIL"]
# criar uma coluna com AEROPORTO DE ORIGEM (SIGLA) - AERODROMO
df_origem["AERODROMO"] = df_origem["AEROPORTO DE ORIGEM (SIGLA)"]
# criar uma coluna com o tipo de movimento
df_origem["MOVIMENTO TIPO"] = "DECOLAGEM"
# criar coluna calculada para pax
df_origem["PASSAGEIROS"] = df_origem["PASSAGEIROS PAGOS"] + \
    df_origem["PASSAGEIROS GRÁTIS"]
# separa as colunas ANO - MES - EMPRESA (SIGLA) - AERODROMO - PASSAGEIROS PAGOS - CARGA PAGA (KG) - DECOLAGENS
df_origem = df_origem[["ANO", "MÊS", "MOVIMENTO TIPO", "AERODROMO",
                       "EMPRESA (SIGLA)", "PASSAGEIROS", "CARGA PAGA (KG)", "DECOLAGENS", "CORREIO (KG)"]]

# df destino (pouso)
pd.options.mode.copy_on_write = True
# filtrar o pais de destino (Brasil)
df_destino = df[df["AEROPORTO DE DESTINO (PAÍS)"] == "BRASIL"]
# criar uma coluna com AEROPORTO DE DESTINO (SIGLA) - AERODROMO
df_destino["AERODROMO"] = df_destino["AEROPORTO DE DESTINO (SIGLA)"]
# criar uma coluna com o tipo de movimento
df_destino["MOVIMENTO TIPO"] = "POUSO"
# criar coluna calculada para pax
df_destino["PASSAGEIROS"] = df_destino["PASSAGEIROS PAGOS"] + \
    df_destino["PASSAGEIROS GRÁTIS"]
# separa as colunas ANO - MES - EMPRESA (SIGLA) - AERODROMO - PASSAGEIROS PAGOS - CARGA PAGA (KG) - DECOLAGENS
df_destino = df_destino[["ANO", "MÊS", "MOVIMENTO TIPO", "AERODROMO",
                         "EMPRESA (SIGLA)", "PASSAGEIROS", "CARGA PAGA (KG)", "DECOLAGENS", "CORREIO (KG)"]]

# crando um data frame unico
df_anac = pd.concat([df_origem, df_destino], ignore_index=True)

# filtros
st.sidebar.title("Filtros")
filtro_graficos = st.sidebar.selectbox('Gráficos', ['Passageiros', 'Movimentos', 'Carga Aérea','Evolução'])
filtro_ano = st.sidebar.selectbox("Ano", df_anac["ANO"].unique())
    

if filtro_graficos == "Passageiros":
    # # Título da página
    # st.subheader(":bar_chart: Ranking de Aeroportos Brasileiros")
    # st.markdown("*Fonte: Dados estatísticos publicados pela ANAC - Agência Nacional de Aviação Civil*")

    # st.markdown("#")
    st.markdown("""---""")
    
    # PAX
    # preparando o grafico
    df_anac_group_pax = df_anac[df_anac["ANO"] == filtro_ano]
    df_anac_group_pax = df_anac_group_pax.groupby("AERODROMO")["PASSAGEIROS"].sum().reset_index()
    df_anac_group_pax = df_anac_group_pax.sort_values("PASSAGEIROS", ascending=False)
    df_anac_group_pax = df_anac_group_pax.head(10)
    # criando o grafico pax
    fig_pax = px.bar(df_anac_group_pax, x="AERODROMO", y="PASSAGEIROS", title="Ranking de aeródromos por passageiro - Top 10")
    fig_pax.update_traces(texttemplate='%{value}', textposition='outside')
    #col1.plotly_chart(fig_pax, use_container_width=True)
    fig_pax

elif filtro_graficos == "Movimentos":
    # # Título da página
    # st.subheader(":bar_chart: Ranking de Aeroportos Brasileiros")
    # st.markdown("*Fonte: Dados estatísticos publicados pela ANAC - Agência Nacional de Aviação Civil*")

    # st.markdown("#")
    st.markdown("""---""")
    
    # MOVIMENTOS
    # preparando o grafico
    df_anac_group_atm = df_anac.groupby("AERODROMO")["DECOLAGENS"].sum().reset_index()
    df_anac_group_atm = df_anac_group_atm.sort_values("DECOLAGENS", ascending=False)
    df_anac_group_atm = df_anac_group_atm.head(10)
    # criando o grafico pax
    fig_atm = px.bar(df_anac_group_atm, x="AERODROMO", y="DECOLAGENS", title="Ranking de aeródromos por movimentos - Top 10")
    fig_atm.update_traces(texttemplate='%{value}', textposition='outside')
    #col2.plotly_chart(fig_atm, use_container_width=True)
    fig_atm
    
elif filtro_graficos == "Carga Aérea":
    # # Título da página
    # st.subheader(":bar_chart: Ranking de Aeroportos Brasileiros")
    # st.markdown("*Fonte: Dados estatísticos publicados pela ANAC - Agência Nacional de Aviação Civil*")

    # st.markdown("#")
    st.markdown("""---""")
    
   
    # CARGO
    # preparando o grafico
    # layout dos graficos
    
    col1, col2 = st.columns(2)
           
    df_anac_group_cargo = df_anac.groupby("AERODROMO")["CARGA PAGA (KG)"].sum().reset_index()
    df_anac_group_cargo = df_anac_group_cargo.sort_values("CARGA PAGA (KG)", ascending=False)
    df_anac_group_cargo = df_anac_group_cargo.head(10)
    # criando o grafico pax
    fig_cargo = px.bar(df_anac_group_cargo, x="AERODROMO", y="CARGA PAGA (KG)", title="Ranking de aeródromos por carga aérea - Top 10")
    fig_cargo.update_traces(texttemplate='%{value}', textposition='outside')
    col1.plotly_chart(fig_cargo, use_container_width=True)
    
    
    # CORREIO
    # preparando o grafico
    df_anac_group_correio = df_anac.groupby("AERODROMO")["CORREIO (KG)"].sum().reset_index()
    df_anac_group_correio = df_anac_group_correio.sort_values("CORREIO (KG)", ascending=False)
    df_anac_group_correio = df_anac_group_correio.head(10)
    # criando o grafico pax
    fig_correio = px.bar(df_anac_group_correio, x="AERODROMO", y="CORREIO (KG)", title="Ranking de aeródromos por correio aéreo - Top 10")
    fig_correio.update_traces(texttemplate='%{value}', textposition='outside')
    col2.plotly_chart(fig_correio, use_container_width=True)
    
else:
    # # Título da página
    # st.subheader(":bar_chart: Evolução dos Aeroportos Brasileiros")
    # st.markdown("*Fonte: Dados estatísticos publicados pela ANAC - Agência Nacional de Aviação Civil*")

    # st.markdown("#")
    st.markdown("""---""")

    filtro_aeroportos = st.sidebar.selectbox("Aeroporto", df_anac["AERODROMO"].unique())
    filtro_tipo = st.sidebar.select_slider("Opções", ["Passageiros", "Aeronaves", "Carga Aérea"])

    if filtro_tipo == "Passageiros":
        
        col1, col2 = st.columns(2)
    
        df_anac_evo_pax = df_anac[df_anac["AERODROMO"] == filtro_aeroportos]
        df_anac_evo_pax = df_anac_evo_pax.groupby("MÊS")["PASSAGEIROS"].sum().reset_index()

        df_anac_evo_pax_y = df_anac[df_anac["AERODROMO"] == filtro_aeroportos]
        df_anac_evo_pax_y = df_anac_evo_pax_y.groupby("ANO")["PASSAGEIROS"].sum().reset_index()
           
        fig_evo_pax = px.bar(df_anac_evo_pax, x="MÊS", y="PASSAGEIROS", title=f"Evolução mensal de movimentação de passageiros - {filtro_aeroportos}/{filtro_ano}")
        fig_ev_ano = px.area(df_anac_evo_pax_y, x="ANO", y="PASSAGEIROS", title=f"Evolução anual de movimentação de passageiros - {filtro_aeroportos}")
        col2.plotly_chart(fig_evo_pax, use_container_width=True)
        col1.plotly_chart(fig_ev_ano, use_container_width=True)
    
    elif filtro_tipo == "Aeronaves": 
        
        col1, col2 = st.columns(2)
        
        df_anac_evo_act = df_anac[df_anac["AERODROMO"] == filtro_aeroportos]
        df_anac_evo_act = df_anac_evo_act.groupby("MÊS")["DECOLAGENS"].sum().reset_index()

        df_anac_evo_act_y = df_anac[df_anac["AERODROMO"] == filtro_aeroportos]
        df_anac_evo_act_y = df_anac_evo_act_y.groupby("ANO")["DECOLAGENS"].sum().reset_index()

        fig_evo_act_y = px.area(df_anac_evo_act_y, x="ANO", y="DECOLAGENS", title=f"Evolução anual de movimentação de aeronaves - {filtro_aeroportos}")
        fig_evo_act = px.bar(df_anac_evo_act, x="MÊS", y="DECOLAGENS", title=f"Evolução mensal de movimentação de aeronaves - {filtro_aeroportos}/{filtro_ano}")
        
        col1.plotly_chart(fig_evo_act_y, use_container_width=True)
        col2.plotly_chart(fig_evo_act, use_container_width=True)

    else: 
        
        col1, col2 = st.columns(2)
        
        df_anac_evo_cargo = df_anac[df_anac["AERODROMO"] == filtro_aeroportos]
        df_anac_evo_cargo = df_anac_evo_cargo.groupby("MÊS")["CARGA PAGA (KG)"].sum().reset_index()

        df_anac_evo_cargo_y = df_anac[df_anac["AERODROMO"] == filtro_aeroportos]
        df_anac_evo_cargo_y = df_anac_evo_cargo_y.groupby("ANO")["CARGA PAGA (KG)"].sum().reset_index()

        fig_evo_cargo_y = px.area(df_anac_evo_cargo_y, x="ANO", y="CARGA PAGA (KG)", title=f"Evolução anual de movimentação de carga - {filtro_aeroportos}")
        fig_evo_cargo = px.bar(df_anac_evo_cargo, x="MÊS", y="CARGA PAGA (KG)", title=f"Evolução mensal de movimentação de carga - {filtro_aeroportos}/{filtro_ano}")
        
        col1.plotly_chart(fig_evo_cargo_y, use_container_width=True)
        col2.plotly_chart(fig_evo_cargo, use_container_width=True)
    
  #

st.markdown("#")
st.markdown("""---""")
st.markdown("*Dados atualizados até 31 de dezembro de 2023*")
