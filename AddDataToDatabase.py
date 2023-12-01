import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from FireBaseIniciar import inicializar_firebase
from datetime import datetime


# Chame a função para inicializar o Firebase
inicializar_firebase()


# Referencia ao nó 'Alunos' no banco de dados
ref = db.reference('Alunos')

def adicionar_aluno(RM, nome, curso, ano_inicio, sexo, idade ):
    ultima_presenca_fixa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Valor fixo para última presença
    total_frequencia_fixo = 0
    aluno_data = {
        "name": nome,
        "curso": curso,
        "comecou_ano": int(ano_inicio),
        "total_frequencia": int(total_frequencia_fixo),
        "sexo": sexo,
        "idade": int(idade),
        "ultima_presencia": ultima_presenca_fixa
    }

    ref.child(RM).set(aluno_data)
    print(f"Aluno {nome} adicionado ao banco de dados.")

#Dados dos alunos a seremm inseridos no banco de dados
data = {
    "169083":
        {
             "name": "Matheus Frizzi",
             "curso": "Desenvolvedor de sistemas",
             "comecou_ano": 2022,
             "total_frequencia" : 10,
             "sexo" : "M",
             "idade": 18,
             "ultima_presencia": "2023-11-09 00:53:22"
        },


}
# Inserçao dos dados dos alunos no banco de dados
for key,value in data.items():
    ref.child(key).set(value)

