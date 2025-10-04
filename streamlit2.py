import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ---- Configuration page Streamlit ----
st.set_page_config(
    page_title="Dashboard BI - TTMIK",
    page_icon="📊",
    layout="wide"
)

# ---- Titre ----
st.title("📊 Tableau de bord BI - Talk To Me In Korean (TTMIK)")
st.markdown("""
Ce tableau de bord permet de suivre les performances commerciales et d’apprentissage de **TTMIK** :  
- Chiffre d’affaires global  
- Fidélisation des abonnés  
- Progression des apprenants  
- Croissance des ventes de livres  
- Répartition des revenus
""")

# ---- Connexion à la base de données ----
conn = sqlite3.connect('TTMIK_BI.db')

# Chargement des tables
subscriptions = pd.read_sql("SELECT * FROM subscriptions", conn)
user_course_progress = pd.read_sql("SELECT * FROM user_course_progress", conn)
courses = pd.read_sql("SELECT * FROM courses", conn)
book_sales = pd.read_sql("SELECT * FROM book_sales", conn)
books = pd.read_sql("SELECT * FROM books", conn)
revenues = pd.read_sql("SELECT * FROM revenues", conn)
users = pd.read_sql("SELECT * FROM users", conn)

# ======================================================
#                CALCULS DES KPI
# ======================================================

# Taux de fidélisation des clients
total_abonnes = len(subscriptions)
abonnes_renouveles = subscriptions['renewed'].sum()
taux_fidelisation = (abonnes_renouveles / total_abonnes) * 100

# Taux de complétion des cours
merged_progress = user_course_progress.merge(courses, on="course_id")
merged_progress["completion_rate"] = (merged_progress["completed_lessons"] / merged_progress["total_lessons"]) * 100
taux_completion_moyen = merged_progress["completion_rate"].mean()

# Taux de croissance des ventes de livres (par format)
book_sales["sale_date"] = pd.to_datetime(book_sales["sale_date"])
book_sales["mois"] = book_sales["sale_date"].dt.to_period("M").astype(str)
ca_par_mois = book_sales.groupby("mois")["total_amount"].sum().reset_index()

if len(ca_par_mois) > 1:
    croissance_livres = ((ca_par_mois.iloc[-1, 1] - ca_par_mois.iloc[0, 1]) / ca_par_mois.iloc[0, 1]) * 100
else:
    croissance_livres = 0

# Part des revenus provenant des adhésions YouTube
revenu_total = revenues["amount"].sum()
revenu_youtube = revenues[revenues["source"] == "youtube_memberships"]["amount"].sum()
part_youtube = (revenu_youtube / revenu_total) * 100

# ======================================================
#               AFFICHAGE DES KPI 
# ======================================================

st.markdown("### 📈 Indicateurs globaux et BI")

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Chiffre d’affaires total", f"{revenu_total:,.0f} USD")
col2.metric("👥 Nombre d’apprenants", f"{len(users)}")
col3.metric("📚 Livres vendus (total)", f"{book_sales['quantity'].sum()}")
col4.metric("🧾 Abonnements actifs", f"{len(subscriptions)}")

st.markdown("---")

col5, col6, col7, col8 = st.columns(4)
col5.metric("🔁 Taux de fidélisation", f"{taux_fidelisation:.1f}%")
col6.metric("🎓 Taux moyen de complétion", f"{taux_completion_moyen:.1f}%")
col7.metric("📦 Croissance ventes livres", f"{croissance_livres:.1f}%")
col8.metric("▶️ Part revenus YouTube", f"{part_youtube:.1f}%")

# ======================================================
#                VISUALISATIONS 
# ======================================================

st.markdown("### 📊 Visualisations")

# CA mensuel (livres)
fig1, ax1 = plt.subplots(figsize=(6, 3))
ax1.plot(ca_par_mois["mois"], ca_par_mois["total_amount"], marker='o', color='#2ca02c')
ax1.set_title("Évolution mensuelle des ventes de livres")
ax1.set_xlabel("Mois")
ax1.set_ylabel("Montant (USD)")
st.pyplot(fig1)

# Répartition des revenus
revenus_source = revenues.groupby("source")["amount"].sum()
fig2, ax2 = plt.subplots(figsize=(4, 4))
ax2.pie(revenus_source, labels=revenus_source.index, autopct='%1.1f%%', startangle=90)
ax2.set_title("Répartition des revenus par source")
st.pyplot(fig2)

# Table détaillée (facultative)
with st.expander("📂 Voir les données détaillées"):
    st.write("### Abonnements")
    st.dataframe(subscriptions)
    st.write("### Progression des cours")
    st.dataframe(merged_progress[["user_id", "course_name", "completion_rate"]])
    st.write("### Ventes de livres")
    st.dataframe(book_sales)
    st.write("### Revenus")
    st.dataframe(revenues)

conn.close()
