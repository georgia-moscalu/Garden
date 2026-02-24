import bcrypt #protejare parole
import sqlite3 #lucram cu baze de date- stocam utilizatori


#DATABASE FUNCT
DB_FILE="garden.db"
def init_db(): #Creaza tabela de users
    conn=sqlite3.connect(DB_FILE) #daca nu exista file ul se creeaza
    cursor=conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
""")
    conn.commit()#salveaza schimbarile
    conn.close() #inchide conexiunea, lucram cu o conexiune odata

def get_user(email):
    #cautam un utilizator in baza de date dupa EMAIL
    conn=sqlite3.connect(DB_FILE)
    cursor=conn.cursor()
    cursor.execute("SELECT email, password_hash FROM users WHERE email = ?",(email,))
    user=cursor.fetchone() #returneaza prima linie care se potriveste
    conn.close()
    return user #returneaza text@gmail.com , "$23%3839"

def save_user(email,password_hash):
    try:
        conn=sqlite3.connect(DB_FILE) #deschide conexiunea
        cursor=conn.cursor()#creeaza cursor
        #insereaza noul utilizator
        cursor.execute(
            "INSERT INTO users (email,password_hash) VALUES(?,?)",
            (email,password_hash)
        )
        conn.commit() #save the changes
        conn.close()
        return True #totul ok
    except Exception as error:
        print(f"Eroare la salvare:{error}")
        return False

#FUNCTII PT PAROLA SIGURA
def hash_pwd(password):
    salt=bcrypt.gensalt(rounds=10)#genereaza salt-cuv aleatorii
    hashed=bcrypt.hashpw(password.encode(),salt)
    #encode->transforma string in bytes, bcrypt lucreaza bytes
    return hashed.decode('utf-8')

def check_pwd(password,hashed):
    return bcrypt.checkpw(password.encode(),hashed.encode())

#FUNCTII PT LOGIN & REGISTER

def login(email, password):
    init_db()
    if not email or not password:
        return{
            "success":False,
            "message":"Email si parola obligatorii!"
        }
    user=get_user(email)
    if not user:
        return{
            "success":False,
            "message": "Email nu a fost gasit!"
        }
    stored_email,password_hash=user
    if not check_pwd(password,password_hash):
        return {
            "success":False,
            "message":"Parola incorecta!"
        }
    return{
        "success":True,
    }
def register(email,password):
    init_db()
    if not email or "@" not in email:
        return{
            "success":False,
            "message":"Email invalid!"
        }
    if len(password)<6:
        return{
            "success":False,
            "message":"Parola trebuie sa contina minim 6 caractere"
        }
    existing_user=get_user(email)
    if existing_user:
        return{
            "success":False,
            "message":"Email deja inregistrat"
        }
    pwd_hash=hash_pwd(password)
    success=save_user(email,pwd_hash)
    if success:
        return{
            "success":True,
        }
    else:
        return{
            "success":False,
        }

