import os
import pickle
import cv2
import face_recognition
import cvzone
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

#Bibliotecas Usadas, estou utilizando python em sua versão 3.11


# - Cmake
# - dlib
# - Face-Recognition
# - CVZone
# - NumPy
# - OpenCV
# - Firebase Admin
# - Datetime
# - Os
# - Pickle


#Configuraçao do FireBase
cred = credentials.Certificate("serviceAccountKey.json")#Chave
firebase_admin.initialize_app(cred, {

    'databaseURL': "https://reconhecimentofacialbd-default-rtdb.firebaseio.com/",
    'storageBucket': "reconhecimentofacialbd.appspot.com"
    })

bucket = storage.bucket()


#Configuração da webcam

cap = cv2.VideoCapture(1)
# Resoluçao da webcam
cap.set(3,640) #Horizontal
cap.set(4, 480) #Vertical

# le uma imagem para ser usada como fundo
imgBackground = cv2.imread('Resources/background.png')

# importando as imagens para um array (lista)
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
ListaImagem = []


for path in modePathList:
    ListaImagem.append(cv2.imread(os.path.join(folderModePath,path)))



   # Carregando o arquivoCodificado
print("Descodificando ....")

arquivo = open('ArquivoCodificado.p','rb')
EncontrarListacomRM = pickle.load(arquivo)
arquivo.close()
EncontrarLista, AlunosRm = EncontrarListacomRM


print("Descodificando Completa")


contador = 0
RM = -1
ImagemAluno = []
Alunos_Escaneados =[]
IDReconhecidos = []
Reconhecedor = 0
y_offset = 60
Reconhecimento = 0.95



AlunosInfo = db.reference(f'Alunos/{RM}').get()

while True:
    success, img = cap.read()

    # Diminui a imagem
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Pega os dados do rosto que estão guardados
    RostoFrame = face_recognition.face_locations(imgS)
    CodificadoFrame = face_recognition.face_encodings(imgS, RostoFrame)

    # Deixando a webcam junto com a imagem
    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414]

    if RostoFrame:
        for CodigosRostos, RostoMapeado in zip(CodificadoFrame, RostoFrame):
            RostoParecido = face_recognition.compare_faces(EncontrarLista, CodigosRostos)
            DistanciaRosto = face_recognition.face_distance(EncontrarLista, CodigosRostos)

            EncontrarIndex = np.argmin(DistanciaRosto)
            precisao = (1 - DistanciaRosto[EncontrarIndex]) * 100
           # print("EncontrarIndex", EncontrarIndex)

            if RostoParecido[EncontrarIndex]:
             #   print("Rosto Reconhecido")
             #   print(AlunosRm[EncontrarIndex])
                y1, x2, y2, x1 = RostoMapeado
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                RM = AlunosRm[EncontrarIndex]
                
              

        if contador != 0:
          # Fazendo o Download dos dados dos alunos
          
          if contador == 1:
            AlunosInfo = db.reference(f'Alunos/{RM}').get()
            print(AlunosInfo)

            #coletando a imagem do Storage
            blob = bucket.get_blob(f'Imagens/{RM}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
           

            
            #Autalizando presença
            datetimeObject = datetime.strptime(AlunosInfo['ultima_presencia'],"%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
            print(secondsElapsed)
            if secondsElapsed > 30 and precisao >= Reconhecimento:
                if EncontrarIndex not in IDReconhecidos:
                    ref = db.reference(f'Alunos/{RM}')
                    AlunosInfo['total_frequencia'] +=1
                    ref.child('total_frequencia').set(AlunosInfo['total_frequencia'])
                    ref.child('ultima_presencia').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                     #Escrevendo Info dos Alunos
                    Alunos_Escaneados.append({
                    "RM": RM,
                    "Nome": AlunosInfo['name'],
                    "Curso": AlunosInfo['curso'],
                    "total_frequencia": AlunosInfo['total_frequencia'],
                    "ultima_presencia": AlunosInfo['ultima_presencia'],
                    "idade": AlunosInfo['idade']
                })
                if contador == 0 :
                    contador = 1 
                  
    
                for aluno in Alunos_Escaneados:
                   cv2.putText(imgBackground, f"RM:{aluno['RM']} - Aluno: {aluno['Nome']} - Frequencia: {aluno['total_frequencia']} Ultima-Presencia: {aluno['ultima_presencia']}",  (820, y_offset),
                     cv2.FONT_HERSHEY_TRIPLEX  , 0.5, (50, 50, 50), 1)
            
                y_offset += 20
                
                Alunos_Escaneados =[]
            else:
              
                contador = 0 
            


        contador += 1

        if contador>=20:
             contador = 0
     
             AlunosInfo = []
  
            
    else:
       
        contador = 0

    # Mostrando a imagem de fundo
    cv2.imshow("ChamadaAutomatica", imgBackground)
    cv2.waitKey(1)
    
    # ESC # garante que o código vai ser pausado ao apertar ESC (código 27) e que o código vai esperar 5 milisegundos a cada leitura da webcam
    
    if cv2.waitKey(5) == 27: 
        break
        