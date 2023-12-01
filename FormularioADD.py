from AddDataToDatabase import adicionar_aluno
from GeradorCodigos import GerarCodificado
import cv2
import os
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk


def coletar_dados_aluno():
    #Mostra Quais Informaçoes ele quuuer
    def capturar_dados():
        RM = entrada_RM.get()
        nome = entrada_nome.get()
        curso = entrada_curso.get()
        ano_inicio = entrada_ano.get()
        sexo = entrada_sexo.get()
        idade = entrada_idade.get()

        adicionar_aluno(RM, nome, curso, ano_inicio, sexo, idade)


        #Parte que liga a webcam
        reconhecimento_rosto = mp.solutions.face_detection
        reconhecedor_rosto = reconhecimento_rosto.FaceDetection()

        cap = cv2.VideoCapture(0)
        while True:
            validacao, frame = cap.read()
            if not validacao:
                break

            imagem = frame
            rgb_imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
            resultado = reconhecedor_rosto.process(rgb_imagem)

            if resultado.detections:
                for deteccao_rosto in resultado.detections:
                    confianca = deteccao_rosto.score[0]
                    if confianca > 0.95:
                        # Se a confiança for maior que 0.8, você pode imprimir ou realizar alguma ação aqui
                        print(f"Confiança de detecção: {confianca}")

            cv2.imshow("Rostos na sua webcam", imagem)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        #Cria uma imagen .png com o RM do aluno na pasta Imagens, se a pasta não existir ele cria
        img_name = f"{RM}.png"
        cv2.imwrite(img_name, imagem)
        if not os.path.exists("Imagens"):
            os.makedirs("Imagens")
        os.replace(img_name, os.path.join("Imagens", img_name))

    #Abre uma interface para Colocar as informaçoes
    root = tk.Tk()
    root.title("Adiocionar Dados do Aluno")

    
    def fechar_janela():
     root.destroy()  
     
    path_to_icon = 'E:\ReconhecimentoFacialBD\Resources\Icone.ico'

    # Definindo o tamanho da janela
    largura_janela = 400
    altura_janela = 350

    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    x = (largura_tela / 2) - (largura_janela / 2)
    y = (altura_tela / 2) - (altura_janela / 2)

    root.geometry(f"{largura_janela}x{altura_janela}+{int(x)}+{int(y)}")


    root.iconbitmap(path_to_icon)
    # Rótulos e caixas de texto
    rotulo_RM = tk.Label(root, text="RM do aluno:")
    rotulo_RM.pack()
    entrada_RM = tk.Entry(root)
    entrada_RM.pack()

    rotulo_nome = tk.Label(root, text="Nome do aluno:")
    rotulo_nome.pack()
    entrada_nome = tk.Entry(root)
    entrada_nome.pack()

    rotulo_curso = tk.Label(root, text="Curso do aluno:")
    rotulo_curso.pack()
    entrada_curso = tk.Entry(root)
    entrada_curso.pack()

    rotulo_ano = tk.Label(root, text="Ano de início do curso:")
    rotulo_ano.pack()
    entrada_ano = tk.Entry(root)
    entrada_ano.pack()

    rotulo_sexo = tk.Label(root, text="Sexo do aluno:")
    rotulo_sexo.pack()
    entrada_sexo = tk.Entry(root)
    entrada_sexo.pack()

    rotulo_idade = tk.Label(root, text="Idade do aluno:")
    rotulo_idade.pack()
    entrada_idade = tk.Entry(root)
    entrada_idade.pack()

    #Chama a funcao coletar_dados_aluno onde coleta os dados e coloca no banco de dados
    btn_capturar = tk.Button(root, text="Capturar Rosto do Aluno", command=capturar_dados)
    btn_capturar.pack()
    btn_capturar.pack(pady=5) 

    #Chama a funcao GerarCodificado Onde criar o ArquivoCodificado.p
    btn_capturar = tk.Button(root, text="Finalizar Registro", command=GerarCodificado)
    btn_capturar.pack()
    btn_capturar.pack(pady=5) 

    btn_fechar = tk.Button(root, text="Fechar", command=fechar_janela)
    btn_fechar.pack(pady=5)  # Espaçamento entre os botões


    root.mainloop()



# Coletando dados do aluno
coletar_dados_aluno()

# Chama a função para gerar o código de reconhecimento facial
GerarCodificado()



