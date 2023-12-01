import firebase_admin
from firebase_admin import credentials

def inicializar_firebase():
    # Verificar se o app do Firebase já foi inicializado
    if not firebase_admin._apps:
        # Se não foi inicializado, então inicialize
        cred = credentials.Certificate("serviceAccountKey.json")#Chave
        firebase_admin.initialize_app(cred, {

        'databaseURL': "https://reconhecimentofacialbd-default-rtdb.firebaseio.com/",
        'storageBucket': "reconhecimentofacialbd.appspot.com"
        })

# Chame a função para inicializar o Firebase
inicializar_firebase()
