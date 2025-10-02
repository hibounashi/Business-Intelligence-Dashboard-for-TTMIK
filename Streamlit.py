import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

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
selected_region = st.selectbox("Filtrer par région :", ["Toutes"] + regions)
df_filtered = df if selected_region == "Toutes" else df[df['region'] == selected_region]

# ---- KPI globaux ----
st.subheader("📈 Indicateurs globaux")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 CA total", f"{df_filtered['CA'].sum():,.0f} USD")
col2.metric("📦 Quantité vendue", f"{df_filtered['quantite'].sum()}")
col3.metric("👥 Nombre de clients", f"{df_filtered['client_id'].nunique()}")
top_prod = df_filtered.groupby('nom_produit')['CA'].sum().idxmax()
col4.metric("🏆 Meilleur produit", top_prod)

st.markdown("---")

# ---- Graphiques compacts ----
st.subheader("📊 Analyses visuelles")
# Container pour graphiques
with st.container():
    col1, col2 = st.columns(2)
    
    # CA par région
    ca_region = df_filtered.groupby('region')['CA'].sum()
    fig1, ax1 = plt.subplots(figsize=(4,3))
    ca_region.plot(kind='bar', color='#1f77b4', ax=ax1)
    ax1.set_title("CA par région")
    ax1.set_ylabel("USD")
    for i, v in enumerate(ca_region):
        ax1.text(i, v + 0.02*v, f"{v:,.0f}", ha='center', fontweight='bold')
    col1.pyplot(fig1)
    
    # Top produits
    top_produits = df_filtered.groupby('nom_produit')['CA'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(4,3))
    top_produits.plot(kind='bar', color='#ff7f0e', ax=ax2)
    ax2.set_title("Top produits CA")
    ax2.set_ylabel("USD")
    for i, v in enumerate(top_produits):
        ax2.text(i, v + 0.02*v, f"{v:,.0f}", ha='center', fontweight='bold')
    col2.pyplot(fig2)

# Evolution mensuelle
st.subheader("📅 Évolution mensuelle du CA")
ca_mois = df_filtered.groupby('mois_str')['CA'].sum()
fig3, ax3 = plt.subplots(figsize=(8,3))
ca_mois.plot(kind='line', marker='o', color='#2ca02c', ax=ax3)
ax3.set_ylabel("USD")
ax3.set_xlabel("Mois")
ax3.set_title("Évolution mensuelle du CA")
for i, v in enumerate(ca_mois):
    ax3.text(i, v + 0.02*v, f"{v:,.0f}", ha='center', fontweight='bold')
st.pyplot(fig3)

# ---- Données détaillées ----
with st.expander("📂 Voir les données détaillées"):
    st.dataframe(df_filtered)

conn.close()
