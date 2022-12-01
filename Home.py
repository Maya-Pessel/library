import streamlit as st
from Database import Database
from typing import List
from streamlit_searchbox import st_searchbox
import pandas as pd


db = Database()



if 'member' not in st.session_state:
    st.session_state.member = None

st.set_page_config(
    layout="wide",
)

if st.session_state.member != None:
    st.title("Bonjour " + st.session_state.member.name + " !")
    most_recent_book = db.most_recent_book(1)
    
    # AFFICHER LES LIVRES PAR CATEGORIE
    st.subheader("Livres par catégorie")
    st.write("Cliquez sur une catégorie pour voir les livres de cette catégorie")
    category = st.selectbox("Catégorie", db.category())
    st.write("Vous avez sélectionné la catégorie " + category)

    df = pd.DataFrame(
    db.display_books_by_cat(category),
    columns=("Titre", "Auteur", "Date de publication", "Catégorie"))

    st.dataframe(df, width=1000, )
    
    # search = st.text_input("Rechercher un livre", key="search")
    # ff = pd.DataFrame(
    # db.display_books(st.session_state.search),
    # columns=("Titre", "Auteur", "Date de publication", "Catégorie"))

    # st.dataframe(df, width=1000, )




else:
    st.title("Bibliothèque")

    login, signup = st.tabs(["Connexion", "Inscription"])

    # Login
    with login:
        st.header("Se connecter")
        login_name = st.text_input('Email')
        login_password = st.text_input('Password', type="password")

        if st.button('Se connecter'):
            member = db.login(login_name, login_password)
            if member:
                st.session_state.member = member
                st.success("Vous êtes connecté")
                st.experimental_rerun()
            else:
                st.error("La connexion a échoué")

    # Inscription
    with signup:
        st.header("S'inscrire")

        inscription_name = st.text_input('Nom*')
        inscription_email = st.text_input('Email*')
        inscription_password = st.text_input('Password*', type="password")

        if st.button('S\'inscrire'):
            try:
                db.signup(inscription_name, inscription_email, inscription_password)
                st.success("Vous êtes inscrit")
                st.info("Vous pouvez vous connecter")
            except:
                st.error("Erreur lors de l'inscription")
                st.info("Veuillez réessayer")
                
