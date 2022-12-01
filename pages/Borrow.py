
import streamlit as st
from Database import Database
import pandas as pd

db = Database()

if st.session_state.member != None:
    # borrow page
    st.title("Emprunter un livre")

    # select a book

    memberId = st.session_state.member.memberId

    book = st.selectbox("Livre", db.book())

    # borrow button

    if st.button("Emprunter"):
        db.borrow_book(memberId, book)
        

    # print the list of book borrowed

    df = pd.DataFrame(
    db.borrowed_book(memberId),
    columns=("Titre du livre", "Date de l'emprunt", "Date du rendu"))

    st.title("Liste des livres empruntés")
    st.dataframe(df, width=1000, )


    if st.button("DELETE"):
        db.delete_all()
        st.success("Tout a été supprimé")

    if st.button("ADD"):
        db.add_books()


    if st.button("show"):
        db.show_borrowed_books()
        st.success("Tout a été affiché")

else:
    st.title("Vous n'êtes pas connecté")
    st.info("Veuillez vous connecter pour emprunter un livre")