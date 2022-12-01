# create a add book page

import streamlit as st
from Database import Database


db = Database()


if st.session_state.member != None and st.session_state.member.role == 2:
    st.title("Ajouter un livre")

    name = st.text_input("Nom du livre")

    author = st.text_input("Auteur")

    date = st.date_input("Date de sortie")

    quantity = st.slider("Quantité", 1, 10)

    # category field who show a list of category and return the id of the category
    category = st.selectbox("Catégorie", db.category())




    if st.button("Ajouter"):
        db.add_book(name, author, date, category, quantity)
        st.success("Le livre a été ajouté")
else:
    st.title("Vous n'êtes pas connecté ou vous n'avez pas le role d'administrateur")
    st.info("Veuillez vous connecter a un compte administrateur pour ajouter un livre")