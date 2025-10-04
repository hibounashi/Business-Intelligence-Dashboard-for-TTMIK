import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Taux de fidélisation
total_abonnes = len(subscriptions)
abonnes_renouveles = subscriptions['renewed'].sum() if 'renewed' in subscriptions else 0
taux_fidelisation = (abonnes_renouveles / total_abonnes) * 100 if total_abonnes > 0 else 0

# Taux de complétion des cours
merged_progress = user_course_progress.merge(courses, on="course_id", how="left")
merged_progress["completion_rate"] = (merged_progress["completed_lessons"] / merged_progress["total_lessons"]) * 100
taux_completion_moyen = merged_progress["completion_rate"].mean()

# Taux de croissance des ventes de livres
book_sales["sale_date"] = pd.to_datetime(book_sales["sale_date"])
book_sales["mois"] = book_sales["sale_date"].dt.to_period("M").astype(str)
ca_par_mois = book_sales.groupby("mois")["total_amount"].sum().reset_index()

if len(ca_par_mois) > 1:
    croissance_livres = ((ca_par_mois.iloc[-1, 1] - ca_par_mois.iloc[0, 1]) / ca_par_mois.iloc[0, 1]) * 100
else:
    croissance_livres = 0

# Part des revenus YouTube
revenu_total = revenues["amount"].sum()
revenu_youtube = revenues[revenues["source"] == "youtube_memberships"]["amount"].sum() if "youtube_memberships" in revenues["source"].values else 0
part_youtube = (revenu_youtube / revenu_total) * 100 if revenu_total > 0 else 0

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
#                VISUALISATIONS AVEC PLOTLY
# ======================================================

st.markdown("### 📊 Visualisations")

# Palette de couleurs lisible en clair et sombre
custom_colors = ["#7b2ff7", "#5b7fff", "#80d0c7", "#c77dff", "#9d4edd"]

# ---- Évolution mensuelle des ventes de livres ----
if not ca_par_mois.empty:
    fig1 = px.line(
        ca_par_mois,
        x="mois",
        y="total_amount",
        title="📅 Évolution mensuelle des ventes de livres",
        markers=True,
        color_discrete_sequence=["#7b2ff7"]
    )
    fig1.update_traces(line=dict(width=3))
    fig1.update_layout(
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        title_font=dict(size=18),
        xaxis_title="Mois",
        yaxis_title="Montant (USD)",
        font=dict(color="#3a0ca3", size=13),
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)

# ---- Répartition des revenus ----
if not revenues.empty:
    revenus_source = revenues.groupby("source")["amount"].sum().reset_index()
    fig2 = px.pie(
        revenus_source,
        names="source",
        values="amount",
        title="💡 Répartition des revenus par source",
        color_discrete_sequence=custom_colors
    )
    fig2.update_traces(
        textinfo="percent+label",
        textfont_size=14,
        insidetextorientation="auto",
        textposition="inside",
        pull=[0.05]*len(revenus_source),
        showlegend=True
    )
    fig2.update_layout(
        template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
        title_font=dict(size=18),
        font=dict(color="#3a0ca3", size=13)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ======================================================
#                TABLES DÉTAILLÉES
# ======================================================

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
