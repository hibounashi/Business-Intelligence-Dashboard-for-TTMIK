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

# ---- Titre et présentation de l'entreprise ----
st.title("📊 Tableau de bord BI - Ventes TTMIK")

st.markdown("""
**À propos de TTMIK – Talk To Me In Korean**  
TTMIK est une entreprise éducative internationale spécialisée dans l'apprentissage du coréen.  
Elle propose des cours en ligne, des livres, des vidéos et du matériel pédagogique pour tous les niveaux, du débutant à l’avancé.  

Ce tableau de bord permet de suivre les performances commerciales de TTMIK en temps réel, y compris :  
- Le chiffre d’affaires total et par région  
- Les produits les plus populaires  
- L’évolution mensuelle des ventes  

**Site officiel :** [https://www.ttmik.com](https://www.ttmik.com)
""")

st.markdown("---")


# ---- Connexion à la base SQLite ----
conn = sqlite3.connect('ventes.db')

# Chargement des tables
clients = pd.read_sql('SELECT * FROM clients', conn)
produits = pd.read_sql('SELECT * FROM produits', conn)
ventes = pd.read_sql('SELECT * FROM ventes', conn)

# Fusion des tables
df = ventes.merge(clients, left_on='client_id', right_on='id', suffixes=('', '_client')) \
           .merge(produits, left_on='produit_id', right_on='id', suffixes=('', '_produit'))

# Calcul du CA
df['CA'] = df['prix'] * df['quantite']

# Conversion date
df['date'] = pd.to_datetime(df['date'])
df['mois_str'] = df['date'].dt.to_period('M').astype(str)

# ---- Filtre interactif par région ----
regions = df['region'].unique().tolist()
selected_region = st.selectbox("Filtrer par région :", ["Toutes"] + regions)

if selected_region != "Toutes":
    df_filtered = df[df['region'] == selected_region]
else:
    df_filtered = df

st.markdown("---")

# ---- KPI globaux ----
st.subheader("📈 Indicateurs globaux")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Chiffre d’affaires total", f"{df_filtered['CA'].sum():,.2f} USD")
col2.metric("📦 Quantité totale vendue", f"{df_filtered['quantite'].sum()}")
col3.metric("👥 Nombre de clients", f"{df_filtered['client_id'].nunique()}")
# Meilleur produit correct
top_prod = df_filtered.groupby('nom_produit')['CA'].sum().idxmax()
col4.metric("🏆 Meilleur produit", top_prod)

st.markdown("---")

# ---- CA par région ----
st.subheader("🌍 Chiffre d’affaires par région")
ca_region = df_filtered.groupby('region')['CA'].sum()
fig, ax = plt.subplots(figsize=(6,4))
ca_region.plot(kind='bar', color='#1f77b4', ax=ax)
ax.set_ylabel("CA (USD)")
ax.set_xlabel("Région")
ax.set_title("Chiffre d’affaires par région")
for i, v in enumerate(ca_region):
    ax.text(i, v + 0.05*v, f"{v:,.0f}", ha='center', fontweight='bold')
st.pyplot(fig)

st.markdown("---")

# ---- Top produits par CA ----
st.subheader("🏆 Top produits par CA")
top_produits = df_filtered.groupby('nom_produit')['CA'].sum().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(6,4))
top_produits.plot(kind='bar', color='#ff7f0e', ax=ax2)
ax2.set_ylabel("CA (USD)")
ax2.set_xlabel("Produit")
ax2.set_title("Top produits par chiffre d’affaires")
for i, v in enumerate(top_produits):
    ax2.text(i, v + 0.05*v, f"{v:,.0f}", ha='center', fontweight='bold')
st.pyplot(fig2)

st.markdown("---")

# ---- Évolution mensuelle du CA ----
st.subheader("📅 Évolution mensuelle du CA")
ca_mois = df_filtered.groupby('mois_str')['CA'].sum()
fig3, ax3 = plt.subplots(figsize=(8,4))
ca_mois.plot(kind='line', marker='o', color='#2ca02c', ax=ax3)
ax3.set_ylabel("CA (USD)")
ax3.set_xlabel("Mois")
ax3.set_title("Évolution mensuelle du chiffre d’affaires")
for i, v in enumerate(ca_mois):
    ax3.text(i, v + 0.05*v, f"{v:,.0f}", ha='center', fontweight='bold')
st.pyplot(fig3)

st.markdown("---")

# ---- Affichage des données brutes (optionnel) ----
with st.expander("📂 Voir les données détaillées"):
    st.dataframe(df_filtered)

# ---- Fermeture de la connexion ----
conn.close()
