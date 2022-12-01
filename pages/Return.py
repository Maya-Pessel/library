
import streamlit as st
from Database import Database


db = Database()

# for each book borrowed, the user can return it by clicking on the button
if st.session_state.member != None:
    # if the borrow table is not empty
    if db.borrowed_book(st.session_state.member.memberId):
        member = st.session_state.member.memberId
        # POUR CHAQUE LIVRE EMPRUNTÉ, L'UTILISATEUR PEUT LE RENDRE EN CLIQUANT SUR LE BOUTON
        for book in db.borrowed_book(st.session_state.member.memberId):
            # RENDRE UN LIVRE
            if st.button("Rendre " + book[0]):
                db.return_book(member, book[0])
                st.experimental_rerun()
    else:
        st.title("Vous n'avez pas de livre emprunté")
else:
    st.title("Vous n'êtes pas connecté")
    st.info("Veuillez vous connecter pour rendre un livre")

