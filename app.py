import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration et style css
st.set_page_config(page_title="FraudGuard ANONG", page_icon="🛡️", layout="wide")

# Initialisation du thème et autres variables de session
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'history' not in st.session_state:
    st.session_state.history = []

# Fonction pour changer de thème
def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# CSS dynamique
def apply_theme(theme):
    if theme == 'dark':
        bg, text, accent, card_bg, border = "#000000", "#FFFFFF", "#00f2ff", "#111111", "#333333"
        res_safe, res_fraud = "rgba(0, 242, 255, 0.1)", "rgba(255, 0, 85, 0.1)"
        border_safe, border_fraud = "#00f2ff", "#ff0055"
        table_color = "white"
        tab_text_color = "#FFFFFF"
        button_text_color = "#FFFFFF"
        metric_color = "#FFFFFF"
        input_bg = "#1a1a1a"
        input_text = "#FFFFFF"
    else:
        bg, text, accent, card_bg, border = "#FFFFFF", "#000000", "#1E3A8A", "#F0F2F6", "#DDDDDD"
        res_safe, res_fraud = "#D1FAE5", "#FEE2E2"
        border_safe, border_fraud = "#10B981", "#EF4444"
        table_color = "black"
        tab_text_color = "#000000"
        button_text_color = "#FFFFFF"
        metric_color = "#000000"
        input_bg = "#FFFFFF"
        input_text = "#000000"

    st.markdown(f"""
            <style>
                .stApp {{ 
                    background-color: {bg} !important; 
                    color: {text} !important; 
                }}

                [data-testid="stSidebar] {{ 
                    backgound-color: {card_bg} !important; 
                    border-right:1px solid {border} !important; 
                }}

                h1, h2, h3 {{ 
                    color: {text} !important; 
                }}

                p, span, label, div {{
                    color: {text} !important;
                }}
           
                .stTabs [data-baseweb="tab-list"] {{
                    gap: 8px;
                }}
                .stTabs [data-baseweb="tab-list"] button {{
                    background-color: transparent !important;
                    color: {tab_text_color} !important;
                }}
                .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
                    background-color: {accent} !important;
                    color: white !important;
                }}
                .stTabs [data-baseweb="tab-list"] button p {{
                    color: {tab_text_color} !important;
                }}
                .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p {{
                    color: white !important;
                }}
                .stTabs [data-baseweb="tab-panel"] {{
                    color: {text} !important;
                }}

                # Label des inputs
                label, [data-testid="stWidgetLabel"] {{
                    color: {text} !important;
                }}
                .stNumberInput label, .stNumberInput label p {{
                    color: {text} !important;
                }}
                .stTextInput label, .stTextInput label p {{
                    color: {text} !important;
                }}
                .stSelectBox label, .stSelectBox label p {{
                    color: {text} !important;
                }}
                input, select, textarea {{
                    background-color: {input_bg} !important;
                    color: {input_text} !important;
                }}
                .stNumberInput input {{
                    background-color: {input_bg} !important;
                    color: {input_text} !important;
                }}
                .stSelectbox select {{
                    background-color: {input_bg} !important;
                    color: {input_text} !important;
                }}
                
                /* CHECKBOXES  */
                .stCheckbox {{
                    color: {text} !important;
                }}
                .stCheckbox label {{
                    color: {text} !important;
                }}
                .stCheckbox label span {{
                    color: {text} !important;
                }}
                .stCheckbox label p {{
                    color: {text} !important;
                }}
                
                /* MÉTRIQUES */
                [data-testid="stMetricValue"] {{
                    color: {metric_color} !important;
                }}
                [data-testid="stMetricLabel"] {{
                    color: {metric_color} !important;
                }}
                [data-testid="stMetricDelta"] {{
                    color: {metric_color} !important;
                }}
                [data-testid="metric-container"] {{
                    background-color: {card_bg} !important;
                    border: 1px solid {border} !important;
                    padding: 15px !important;
                    border-radius: 10px !important;
                }}
                
                /* MARKDOWN dans les onglets */
                .stTabs [data-baseweb="tab-panel"] h4 {{
                    color: {text} !important;
                }}
                .stMarkdown {{
                    color: {text} !important;
                }}
                
                /* Cartes de prédiction */
                .res-card {{
                    padding: 30px !important;
                    border-radius: 15px !important;
                    text-align: center !important;
                    margin: 20px auto !important;
                    width: 70% !important;
                    border: 2px solid !important;
                }}
                .res-card h2, .res-card p {{
                    margin: 10px 0 !important;
                }}
                .res-safe {{ 
                    background-color: {res_safe} !important; 
                    border-color: {border_safe} !important; 
                }}
                .res-safe h2, .res-safe p {{ 
                    color: {border_safe} !important; 
                }}
                .res-fraud {{ 
                    background-color: {res_fraud} !important; 
                    border-color: {border_fraud} !important; 
                }}
                .res-fraud h2, .res-fraud p {{ 
                    color: {border_fraud} !important; 
                }}

                /* Bouton personnalisé */
                div.stButton > button:first-child {{
                    display: block !important;
                    background-color: {accent} !important;
                    margin: 0 auto !important;
                    color: {button_text_color} !important;
                    height: 3em !important;
                    width: 50% !important;
                    border-radius: 10px !important;
                    border: none !important;
                    transition: 0.3s !important;
                    font-weight: bold !important;
                }}
                div.stButton > button:first-child p {{
                    color: {button_text_color} !important;
                }}
                div.stButton > button:first-child:hover {{
                    opacity: 0.8 !important;
                    color: {button_text_color} !important;
                }}
                div.stButton > button:first-child:hover p {{
                    color: {button_text_color} !important;
                }}

                /* TABLEAU HISTORIQUE */
                .stTable {{
                    background-color: {card_bg} !important;
                    border-radius: 10px !important;
                    padding: 10px !important;
                }}
                .stTable table {{
                    color: {table_color} !important;
                    width: 100% !important;
                }}
                .stTable thead {{
                    background-color: {accent} !important;
                }}
                .stTable thead tr th {{
                    background-color: {accent} !important;
                    color: white !important;
                    padding: 10px !important;
                    font-weight: bold !important;
                    text-align: center !important;
                }}
                .stTable tbody tr td {{
                    color: {table_color} !important;
                    padding: 8px !important;
                    border-bottom: 1px solid {border} !important;
                    text-align: center !important;
                }}
                .stTable tbody tr:hover {{
                    background-color: {border} !important;
                }}
                
                /* Subheader */
                .stSubheader {{
                    color: {text} !important;
                }}
                
                /* Divider */
                hr {{
                    border-color: {border} !important;
                }}
                
                /* Spinner text */
                .stSpinner > div {{
                    color: {text} !important;
                }}
                
                /* Expander */
                .streamlit-expanderHeader {{
                    color: {text} !important;
                }}
            </style>
            """, unsafe_allow_html=True)

apply_theme(st.session_state.theme)

# Chargement du modèle et du scaler
@st.cache_resource
def load_assets():
    m = pickle.load(open('svm_model.pkl', 'rb'))
    s = pickle.load(open('scaler.pkl', 'rb'))
    return m, s

try:
   model, scaler = load_assets() 
except Exception as e:
    st.error(f"Fichiers svm ou scaler introuvables : {e}")

# Logique des modals
@st.dialog("Résultat de l'analyse")
def show_prediction_modal(pred, amount):
    if pred == 1:
        st.error(f"⚠️ Alerte fraude confirmée pour {amount}")
        st.write("Le comportement financier viole les règles de sécurité.")
    else:
        st.success(f"✅ Transaction de {amount} validée")
        st.write("Les flux de capitaux sont cohérents avec l'historique utilisateur.")
    if st.button("Fermer"):
        st.rerun()

# Barre latérale
with st.sidebar:
    st.markdown(f"## 🛡️ FraudGuard ANONG {'Dark' if st.session_state.theme == 'dark' else 'Light'}")
    st.button("🌓 Switch Theme", on_click=toggle_theme)
    st.divider()
    menu = ['Home', 'Prediction', 'Analysis']
    choice = st.sidebar.selectbox('Navigation', menu)

# Logique des pages
# Page d'accueil
if choice == 'Home':
    st.markdown(f"<h1 style='text-align: center;'>Bienvenue sur FraudGuard <span style='color: #00f2ff;'>de ANONG</span> </h1>", unsafe_allow_html=True)
    col_img, col_txt = st.columns([1, 1.5])
    with col_img:
        st.image('https://cdn-icons-png.flaticon.com/512/2092/2092663.png', width=250)
    with col_txt:
        st.write(f"""
                 ### Sécurité bancaire
                 Notre système utilise un modèle de pointe pour détecter les tentatives de fraude financière
                 **Points clés :**
                 - Analyse des anomalies de solde
                 - Détection par analyse rapide
                 - Taux de précision 98%
              """)
# Page prédiction
elif choice == 'Prediction':
    st.markdown("## Analyse de Transaction")
    # Formulaire avec onglets pour plus de propreté
    tab1, tab2 = st.tabs(["📊 Paramètres Transaction", "🏦 Détails des Comptes"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            step = st.number_input('Heure de la transaction (Step)',1, 744, 24)
            trans_type = st.selectbox('Type de transaction', ['CASH_OUT', 'TRANSFER', 'PAYMENT', 'CASH_IN', 'DEBIT'])
        with col2:
            amount = st.number_input('Montant de la transaction ($)', 0.0, 50000000.0, 1500.0)
    with tab2:
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### Expéditeur")
            old_orig = st.number_input('Solde Initial (Orig)', 0.0, 50000000.0, 5000.0)
            new_orig = st.number_input('Solde Final (Orig)', 0.0, 50000000.0, 3000.0)
        with col4:
            st.markdown("#### Destinataire")
            old_dest = st.number_input('Solde Initial (Dest)', 0.0, 50000000.0, 5000.0)
            new_dest = st.number_input('Solde Final (Dest)', 0.0, 50000000.0, 3000.0)
    # Encodage et prédiction
    # Valeurs exactes issues du nettoyage
    type_dict = {
        'TRANSFER': 0.292707,
        'CASH_OUT': 0.310970,
        'PAYMENT': 0.275782,
        'DEBIT': 0.019481,
        'CASH_IN': 0.101059
    }
    type_enc = type_dict.get(trans_type)
    if st.button('🔍 Lancer le diagnostic'):
        with st.spinner('Analyse'):
            time.sleep(1)
            # calcul des variables d'erreur
            error_orig = old_orig - amount - new_orig
            error_dest = old_dest + amount - new_dest
            # Création du dataframe avec l'ordre strict du notebook
            input_data = pd.DataFrame([{
                'step': float(step),
                'amount': float(amount),
                'errorBalanceDest': float(error_dest),
                'errorBalanceOrig': float(error_orig),
                'type_encode': float(type_enc)
            }])
            # Scaling et prédiction 
            try:
                # les colonnes doivent être dans l'ordre attendu par le scaler
                input_data = input_data[['step', 'amount', 'errorBalanceDest', 'errorBalanceOrig', 'type_encode']]
                # normalisation
                input_scaled = scaler.transform(input_data)
                # prédiction finale
                prediction = model.predict(input_scaled)[0]

                # Enregistrement dans l'historique des analyses
                new_entry = {
                    "Heure": step, "Montant": amount, "Type": trans_type,
                    "Résultat": "🔴 FRAUDE" if prediction == 1 else "🟢 SAIN"
                }
                st.session_state.history.append(new_entry)
                if len(st.session_state.history) > 5:
                    st.session_state.history.pop(0)
                st.session_state['last_pred'] = prediction
                # affichage du modal avec le résultat
                show_prediction_modal(prediction, amount)

                # Affichage des résultats sur la page
                st.divider()
                if 'last_pred' in st.session_state:
                    if st.session_state['last_pred'] == 1:
                        st.markdown(f'<div class="res-card res-fraud"><h2>⚠️ ALERTE FRAUDE DETECTEE</h2><p> Une fraude de type {trans_type}  d\'un montant de {amount} a été détectée.</p></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="res-card res-safe"><h2>✅ TRANSACTION VALIDEE</h2><p> La transaction d\'un montant de {amount} ne présente aucun risque majeur.</p></div>', unsafe_allow_html=True)
                
                # TABLEAU HISTORIQUE DES 5 DERNIERES ANALYSES
                if st.session_state.history:
                    st.divider()
                    st.subheader("📜 Historique des 5 dernières analyses")
                    history_df = pd.DataFrame(st.session_state.history[::-1]) #inverser pour voir la dernière analyse en haut
                    st.table(history_df)

            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {e}")
elif choice == 'Analysis':
    st.markdown("<h1 class='title-text'>Analyse des Données d'Entraînement</h1>", unsafe_allow_html=True)

    # 1. Chargement des données
    @st.cache_data
    def get_analysis_data():
        df = pd.read_csv('clean_fraud.csv')
        return df
    
    data_ana = get_analysis_data()

    # style des graphiques selon le thème
    plt_theme ='dark_background' if st.session_state.theme == 'dark' else 'default'
    chart_color = '#00f2ff' if st.session_state.theme == 'dark' else '#1E3A8A'

    # 2. KPI
    col1, col2, col3 = st.columns(3)
    total_trans = len(data_ana)
    fraud_count = int(data_ana['isFraud'].sum())
    fraud_rate = (fraud_count / total_trans) * 100

    with col1:
        st.metric("Total transactions", f"{total_trans:,}")
    with col2:
        st.metric("Cas de fraude", f"{fraud_count:,}", delta_color="inverse")
    with col3:
        st.metric("Taux de fraude", f"{fraud_rate:.2f}%")
    st.divider()

    # 3. Graphiques
    # Répartition horaire
    cola, colb = st.columns(2)

    with cola:
        st.subheader("⏰ Analyse horaire des fraudes")
        # Paramétrage forcé des couleurs Matplotlib
        plt.rcParams.update({
            'text.color': 'white' if st.session_state.theme == 'dark' else 'black',
            'axes.labelcolor': 'white' if st.session_state.theme == 'dark' else 'black',
            'xtick.color': 'white' if st.session_state.theme == 'dark' else 'black',
            'ytick.color': 'white' if st.session_state.theme == 'dark' else 'black'
        })
        # On regarde où les fraudes se concentrent sur l'axe step
        fig, ax1 = plt.subplots(facecolor='none')
        plt.style.use(plt_theme)
        sns.histplot(data_ana[data_ana['isFraud']==1]['step'], bins=50, color='#ff0055', ax=ax1, kde=True)
        ax1.set_title("Pics de fraude par heure (step)", color='grey')
        st.pyplot(fig)
        st.write("Ce graphique permet de repérer les périodes critiques où les fraudeurs sont les plus actifs.")

    # Répartition des types de transaction
    with colb:
        st.subheader("⚖️ Répartition des types de transactions")
        # On montre quels types de transaction sont les plus risqués
        fig2, ax2 = plt.subplots(facecolor='none')
        sns.countplot(data=data_ana, x='isFraud', palette=['#00f2ff', '#ff0055'], ax=ax2)
        ax2.set_xticklabels(['Légitime', 'Fraude'])
        st.pyplot(fig2)
        st.write("Volume total des transactions par classe dans le jeu d'entrainement.")
    
    # Légitimité de notre modèle
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.subheader("⚖️ Équilibre des Classes")
        fig, ax = plt.subplots()
        # On remplace 0/1 par des labels pour le graphique
        labels = ['Légitime', 'Fraude']
        sizes = data_ana['isFraud'].value_counts()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#10B981', '#EF4444'])
        ax.axis('equal')
        st.pyplot(fig)
        st.write("Le dataset a été équilibré ) 50/50 pour optimiser l'apprentissage")
    with row1_col2:
        st.subheader("💰 Distribution des Montants")
        fig, ax= plt.subplots()
        # on utilise une échelle log car les montants varient énormément
        sns.boxplot(x='isFraud', y='amount', data=data_ana, palette=['#10B981', '#EF4444'])
        ax.set_xticklabels(['Légitime', 'Fraude'])
        ax.set_yscale('log') # aide à la lisibilité
        st.pyplot(fig)
        st.write("Note: l'échelle est logarithmique. Les fraudes concernent des montants élevés.")
        st.divider()
    
    # 4. Analyse des variables d'erreur
    st.subheader("🔍 Impact des anomalies de solde (ErrorBalance)")
    col_err1, col_err2 = st.columns(2)

    with col_err1:
        fig, ax = plt.subplots()
        sns.kdeplot(data=data_ana, x='errorBalanceOrig', hue='isFraud', fill=True, palette=['#10B981', '#EF4444'])
        plt.title("Anomalie solde expéditeur")
        st.pyplot(fig)
    with col_err2:
        fig, ax = plt.subplots()
        sns.kdeplot(data=data_ana, x='errorBalanceDest', hue='isFraud', fill=True, palette=['#10B981', '#EF4444'])
        plt.title("Anomalie solde destinataire")
        st.pyplot(fig)
    st.write("On remarque que pour les fraudes (rouge), l'erreur de solde n'est pas centré sur 0, ce qui confirme que l'argent 'apparaît' ou 'disparaît' anormalement.")

    # 5. Matrice de corrélation
    if st.checkbox("Afficher la matrice de corrélation"):
        st.subheader("🔗 Corrélation entre variables")
        fig, ax = plt.subplots(figsize=(10,6))
        sns.heatmap(data_ana.corr(), annot=True, cmap='RdBu_r', center=0)
        st.pyplot(fig)