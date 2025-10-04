import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---- Configuration page Streamlit ----
st.set_page_config(
    page_title="Dashboard BI - Ventes TTMIK",
    page_icon="📊",
    layout="wide"
)

# ---- Titre ----
st.title("📊 Tableau de bord BI - Ventes TTMIK")

st.markdown("""
**À propos de TTMIK – Talk To Me In Korean**  
TTMIK est une entreprise éducative spécialisée dans l'apprentissage du coréen.  

Ce tableau de bord permet de suivre les performances commerciales :  
- Chiffre d’affaires total et par région  
- Produits les plus populaires  
- Évolution mensuelle des ventes
""")
st.markdown("---")

# ---- Connexion DB ----
conn = sqlite3.connect('ventes.db')
clients = pd.read_sql('SELECT * FROM clients', conn)
produits = pd.read_sql('SELECT * FROM produits', conn)
ventes = pd.read_sql('SELECT * FROM ventes', conn)

# ---- Fusion et calcul CA ----
df = ventes.merge(clients, left_on='client_id', right_on='id') \
           .merge(produits, left_on='produit_id', right_on='id', suffixes=('', '_produit'))
df['CA'] = df['prix'] * df['quantite']
df['date'] = pd.to_datetime(df['date'])
df['mois_str'] = df['date'].dt.to_period('M').astype(str)

# ---- Filtre région ----
regions = df['region'].unique().tolist()
selected_region = st.selectbox("🌍 Filtrer par région :", ["Toutes"] + regions)
df_filtered = df if selected_region == "Toutes" else df[df['region'] == selected_region]

# ======================================================
#                   KPI GLOBAUX
# ======================================================
st.subheader("📈 Indicateurs globaux")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 CA total", f"{df_filtered['CA'].sum():,.0f} USD")
col2.metric("📦 Quantité vendue", f"{df_filtered['quantite'].sum()}")
col3.metric("👥 Nombre de clients", f"{df_filtered['client_id'].nunique()}")
if not df_filtered.empty:
    top_prod = df_filtered.groupby('nom_produit')['CA'].sum().idxmax()
else:
    top_prod = "Aucun"
col4.metric("🏆 Meilleur produit", top_prod)

st.markdown("---")

# ======================================================
#              ANALYSES VISUELLES AVEC PLOTLY
# ======================================================
st.subheader("📊 Analyses visuelles")

# Palette visible en clair et sombre
custom_colors = ["#7b2ff7", "#5b7fff", "#4cc9f0", "#4895ef", "#80ffdb"]

col1, col2 = st.columns(2)

# ---- CA par région ----
ca_region = df_filtered.groupby('region')['CA'].sum().reset_index()
if not ca_region.empty:
    fig1 = px.bar(
        ca_region,
        x='region',
        y='CA',
        text='CA',
        title="💵 Chiffre d’affaires par région",
        color='region',
        color_discrete_sequence=custom_colors
    )
    fig1.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig1.update_layout(
        template="plotly_white",
        title_font=dict(size=18),
        font=dict(color="#3a0ca3", size=13),
        xaxis_title="Région",
        yaxis_title="Montant (USD)"
    )
    col1.plotly_chart(fig1, use_container_width=True)

# ---- Top produits ----
top_produits = df_filtered.groupby('nom_produit')['CA'].sum().sort_values(ascending=False).reset_index()
if not top_produits.empty:
    fig2 = px.bar(
        top_produits,
        x='nom_produit',
        y='CA',
        text='CA',
        title="🏆 Produits les plus rentables",
        color='nom_produit',
        color_discrete_sequence=custom_colors
    )
    fig2.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig2.update_layout(
        template="plotly_white",
        title_font=dict(size=18),
        font=dict(color="#3a0ca3", size=13),
        xaxis_title="Produit",
        yaxis_title="Montant (USD)"
    )
    col2.plotly_chart(fig2, use_container_width=True)

# ======================================================
#              ÉVOLUTION MENSUELLE DU CA
# ======================================================
st.subheader("📅 Évolution mensuelle du chiffre d’affaires")

ca_mois = df_filtered.groupby('mois_str')['CA'].sum().reset_index()
if not ca_mois.empty:
    fig3 = px.line(
        ca_mois,
        x='mois_str',
        y='CA',
        title="📈 Évolution mensuelle du CA",
        markers=True,
        color_discrete_sequence=["#7b2ff7"]
    )
    fig3.update_traces(line=dict(width=3))
    fig3.update_layout(
        template="plotly_white",
        title_font=dict(size=18),
        xaxis_title="Mois",
        yaxis_title="Montant (USD)",
        font=dict(color="#3a0ca3", size=13),
        hovermode="x unified"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ======================================================
#               PART DU CA PAR RÉGION (CERCLE)
# ======================================================
st.subheader("🧭 Répartition du CA par région (%)")

if not ca_region.empty:
    fig4 = px.pie(
        ca_region,
        names="region",
        values="CA",
        title="🌎 Répartition du chiffre d’affaires par région",
        color_discrete_sequence=custom_colors
    )
    fig4.update_traces(
        textinfo="percent+label",
        textfont_size=14,
        insidetextorientation="auto",
        textposition="inside",
        pull=[0.05]*len(ca_region),
        showlegend=True
    )
    fig4.update_layout(
        template="plotly_white",
        font=dict(color="#3a0ca3", size=13),
        title_font=dict(size=18)
    )
    st.plotly_chart(fig4, use_container_width=True)

# ======================================================
#              DONNÉES DÉTAILLÉES
# ======================================================
with st.expander("📂 Voir les données détaillées"):
    st.dataframe(df_filtered)

conn.close()
