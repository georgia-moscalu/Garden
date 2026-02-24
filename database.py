import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/Users/georgiamoscalu/Desktop/Gradina/gradina-cae54-firebase-adminsdk-fbsvc-ffe1e980c5.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def obtine_toate_plantele():
    lista_plante = []
    docs = db.collection("Gradina").stream()

    for doc in docs:
        date_planta = doc.to_dict()
        # Salvăm și ID-ul documentului (ne va ajuta când dăm click pe o plantă mai târziu)
        date_planta['id_document'] = doc.id
        lista_plante.append(date_planta)

    return lista_plante