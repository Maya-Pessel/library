import psycopg2
import streamlit as st
from entities.Members import Members
from datetime import date
import datetime

# conn = psycopg2.connect("dbname=library user=postgres")

# c = conn.cursor()


class Database:
    def __init__(self):
        self.conn = self.connect()
        self.cur = self.conn.cursor()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect("dbname=library user=postgres")

            # create a cursor
            cur = conn.cursor()

            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            cur.close()
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        self.cur.close()
        self.conn.close()

### CONNEXION A UN COMPTE ###
    def login(self, email: str, password: str):
        try:
            self.cur.execute("SELECT * FROM member WHERE email = %s AND password = %s", (email, password))
            member = Members(*self.cur.fetchone())            
            return member
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

### CREATION D'UN COMPTE ###
    def signup(self, name: str, email: str, password: str):
        try:
            self.cur.execute("INSERT INTO member (name, email, password) VALUES (%s, %s, %s) RETURNING memberId", (name, email, password))
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
            raise error

### AFFICHE LES LIVRES LES PLUS RECENTS ###
    def most_recent_book(self, rows):
        self.cur.execute("SELECT * FROM book ORDER BY date DESC LIMIT %s", (rows,))
        for row in self.cur.fetchall():
            st.write(f"Empruntez notre dernière sortie : {row[1]} de {row[2]} !")  
            print(row)   
        return self.cur.fetchall()

### VERIFIER SI LE MEMBRE EST ADMIN ###
    def is_admin(self, member):
        if st.session_state.member != None:
            self.cur.execute("SELECT role FROM member WHERE memberId = %s", (member.memberId,))
            role = self.cur.fetchone()[0]
            if role == 2:
                return True
            else:
                return False
        else:
            st.error("Vous n'êtes pas connecté")
    

### RENVOYER LA LISTE DES CATEGORIES ###
    def category(self):
        self.cur.execute("SELECT * FROM category")
        return [row[1] for row in self.cur.fetchall()]

### RENVOYER UNE LISTE DE LIVRES DISPONIBLES ###
    def book(self):
        # if quantity > 0
        self.cur.execute("SELECT name FROM book WHERE quantity > 0")
        return [row[0] for row in self.cur.fetchall()]

### FONCTION QUI RENVOIE LA LISTE DES LIVRES EMPRUNTES PAR UN MEMBRE ###
    def borrowed_book(self, member):
        # RECUPERER LE ISBN DU LIVRE
        self.cur.execute("SELECT isbn FROM borrow WHERE memberId = %s", (member,))

        # RECUPERER LES INFORMATIONS SUR L'EMPRUNT 
        self.cur.execute("SELECT book.name, borrow.date, borrow.estimatedDate FROM borrow INNER JOIN book ON borrow.isbn = book.isbn WHERE memberId = %s ORDER BY borrow.estimatedDate", (member,))
        return self.cur.fetchall()

### RECUPERER LE ID DE LA CATEGORIE A PARTIR DU NOM DE LA CATEGORIE ###
    def category_id(self, category):
        self.cur.execute("SELECT categoryId FROM category WHERE name = %s", (category,))
        return self.cur.fetchone()[0]

### RECUPERER LE ISBN DU LIVRE A PARTIR DU NOM DU LIVRE ###
    def book_id(self, book):
        self.cur.execute("SELECT isbn FROM book WHERE name = %s", (book,))
        return self.cur.fetchone()[0]

### BLOQUER UN MEMBRE SI IL A PLUS DE 3 LIVRES EMPRUTES OU SI IL EST EN RETARD SUR SES RENDUS ###
    def block_member(self, member, book):
        # VERIFIER SI LE MEMBRE A DEJA EMPRUNTE 3 LIVRES
        # self.cur.execute("SELECT COUNT(*) FROM borrow WHERE memberId = %s", (member.memberId,))
        # if self.cur.fetchone()[0] >= 3:
        #     st.error("Vous avez déjà 3 livres empruntés")
        #     return True
        member = st.session_state.member.memberId
        # VERIFIER SI LE MEMBRE EST EN RETARD SUR SES RENDUS ###
        print(member)
        self.cur.execute("SELECT * FROM borrow WHERE memberId = %s", (member,))
        today = date.today()

        for row in self.cur.fetchall():
            if today.strftime("%Y/%m/%d") < str(row[3]):
                st.error("Vous avez dépassé la date limite de retour")
                return True
        return False

### AJOUTER UN LIVRE A LA BIBLIOTHEQUE ###
    def add_book(self, name, author, date, category, quantity):
            member = st.session_state.member
            print("this is the member", member)

            # SI LE MEMBRE EST ADMIN
            if self.is_admin(member):
                try:
                    # RECUPERER L'ID DE LA CATEGORIE
                    categoryId = self.category_id(category)
                    # AJOUTER LE LIVRE A LA BDD
                    self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", (name, author, date, categoryId, quantity))
                    self.conn.commit()
                    st.success("Le livre a été ajouté")
                    self.cur.execute("SELECT * FROM book")
                    for row in self.cur.fetchall():
                        print(row)
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                    self.conn.rollback()
                    raise error
            else:
                st.error("Vous n'avez pas les droits pour ajouter un livre")
                print("this is the member", member)

### EMPRUNTER UN LIVRE ###
    def borrow_book(self, member, book):
        # VERIFIER SI LE MEMBRE EST BLOQUE
        if self.block_member(member, book) == False:
            try:
                # RECUPERER LE ISBN DU LIVRE
                isbn = self.book_id(book)

                # CHECK LA QUANTITE DE LIVRE
                self.cur.execute("SELECT quantity FROM book WHERE isbn = %s", (isbn,))
                quantity = self.cur.fetchone()[0]

                # SI LE LIVRE A UNE QUANTITE SUPERIEUR A 0
                if quantity > 0:
                    self.cur.execute("INSERT INTO borrow (memberId, isbn, date, estimatedDate) VALUES (%s, %s, %s, %s)", (member, isbn, datetime.date.today(), datetime.date.today() + datetime.timedelta(days=30)))            
                    self.conn.commit()
                    st.success("Le livre a été emprunté")
                    # AUGMENTER LA QUANTITE DE LIVRE
                    self.cur.execute("UPDATE book SET quantity = quantity - 1 WHERE isbn = %s", (isbn,))
                    self.conn.commit()
                else:
                    st.error("Le livre n'est pas disponible")
    
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                self.conn.rollback()
                raise error
        else:
            st.error("Vous ne pouvez pas emprunter de livre")
            print("BLOCKED")

### RENDRE UN LIVRE ###
    def return_book(self, member, book):
        # RECUPERER L'ID DU LIVRE
        member = st.session_state.member.memberId
        # RECUPERER LE ISBN DU LIVRE
        isbn = self.book_id(book)
        # RECUPERER LE ID DE L'EMPRUNT
        self.cur.execute("SELECT borrowId FROM borrow WHERE memberId = %s AND isbn = %s", (member, isbn))
        borrowId = self.cur.fetchone()[0]
        # SUPPRIMER L'EMPRUNT
        self.cur.execute("DELETE FROM borrow WHERE borrowId = %s", (borrowId,))
        self.conn.commit()
        st.success("Le livre a été rendu")
        # AUGMENTER LA QUANTITE DE LIVRE
        self.cur.execute("UPDATE book SET quantity = quantity + 1 WHERE isbn = %s", (isbn,))
        self.conn.commit()

### AFFICHER LES LIVRES ET LES TRIER PAR CATEGORIE ###
    def display_books_by_cat(self, category):
        # RECUPERER L'ID DE LA CATEGORIE
        categoryId = self.category_id(category)
        # USE THE CATEGORY ID FUNCTION TO SHOW TEH CATEGORY NAME
        # RECUPERER LES LIVRES DE LA CATEGORIE
        self.cur.execute("SELECT book.name, book.author, book.date, category.name FROM book INNER JOIN category ON book.category = category.categoryId WHERE category.categoryId = %s", (categoryId,))
        return self.cur.fetchall()

### AFFICHER LES LIVRES ET LES filtrer PAR NOM, AUTEUR, DATE, CATEGORIE, WHERE LIKE ###
    def display_books(self, search):
        # RECUPERER LES LIVRES DE LA CATEGORIE
        self.cur.execute("SELECT book.name, book.author, book.date, category.name FROM book INNER JOIN category ON book.category = category.categoryId WHERE book.name LIKE '%%' AND book.author LIKE '%%' AND category.name LIKE '%%'", (search, search, search, search))
        print("search", search)
        return self.cur.fetchall()


# DELETE ALL BOOKS AND ALL BOOKS BORROWED
    def delete_all(self):
        self.cur.execute("DELETE FROM borrow")
        self.cur.execute("DELETE FROM book")
        self.conn.commit()

# ADD NEW BOOKS
    def add_books(self):
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter 2", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter 3", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter 4", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter 5", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter 6", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter 7", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter 8", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.cur.execute("INSERT INTO book (name, author, date, category, quantity) VALUES (%s, %s, %s, %s, %s)", ("Harry Potter 9", "J.K Rowling", datetime.datetime.now(), 1, 2))
        self.conn.commit()

#  show borrowed books
    def show_borrowed_books(self):
        self.cur.execute("SELECT * FROM book")
        for row in self.cur.fetchall():
            print(row)
