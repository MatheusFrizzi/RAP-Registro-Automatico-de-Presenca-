import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from FireBaseIniciar import inicializar_firebase

def GerarCodificado():


    # Chame a função para inicializar o Firebase
    inicializar_firebase()

    # Diretorio  contendo imgens dos estudantes
    folderPath = 'Imagens'
    PathList = os.listdir(folderPath)

    #Lista oata armazenar imagens e IDs dos estudantes
    ListaAlunos = []
    AlunosRm = []


    #Envia as imagens para o firebase Storage e armazena as informaçoes dos estudantes
    for path in PathList:
        #Adiciona a imagem à lista
        ListaAlunos.append(cv2.imread(os.path.join(folderPath,path)))

        # extrai o ID do estudante a partir do nome do arquivo
        AlunosRm.append(os.path.splitext(path)[0])


        #Faz upload da imagem para o firebase Storage
        fileName = f'{folderPath}/{path}'
        bucket = storage.bucket()
        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)


    #Função para codificar as imagens faciais
    def encotrarCodigo(ListaImagens):
        CodifcarLista = []
        for img in ListaImagens:
            #converte a imagem para o formato RGB(necessário para a face_recognition)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


            face_locations = face_recognition.face_locations(img)
        
            if face_locations:
   

            #codifica a face na imagem
              Codificar = face_recognition.face_encodings(img)[0]
              CodifcarLista.append(Codificar)
            else:
              # se nenhum rosto for encontrado, adicione None à lista para indicar a ausência de rosto
             CodifcarLista.append(None)
             
        return CodifcarLista



    print("Codificando ...."),

    EncontrarLista = encotrarCodigo(ListaAlunos)

    print(EncontrarLista)

    #Combina as listas de condificações faciais e IDs dos estudantes
    EncontrarListacomRM = [EncontrarLista, AlunosRm]

    #Exibe mensagem de conclusão
    print("Codificação completa")

    #Salva as informações no arquivo pickle
    arquivo = open("ArquivoCodificado.p", 'wb')
    pickle.dump(EncontrarListacomRM, arquivo)
    arquivo.close()
    print("Arquivo Salvo")



#Se quiser rodar o codigo sem ter que mexer no formulario e so chamar o funçao no final do coidgo
#Mas quando for utilizar com o formulario retire a linha ou comente a linha
#GerarCodificado()