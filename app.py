from flask import Flask, render_template, jsonify
import random
import time
import csv
from datetime import datetime

app = Flask(__name__)

# Lista global para armazenar nomes já sorteados
nomes_sorteados = []

# Função para ler os consultores do CSV (email e nome)
def ler_consultores(arquivo):
    consultores = []
    with open(arquivo, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile)
        next(leitor)  # Pula o cabeçalho (email,nome)
        for linha in leitor:
            consultores.append({'email': linha[0], 'nome': linha[1]})  # Armazena email e nome
    return consultores

# Rota principal para exibir a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para realizar o sorteio
@app.route('/sortear', methods=['GET'])
def sortear():
    global nomes_sorteados
    
    # Define a seed com base no timestamp atual
    timestamp = int(datetime.now().timestamp())
    random.seed(timestamp)
    
    # Lê os consultores do CSV
    consultores = ler_consultores('consultores.csv')
    
    # Remove os nomes já sorteados da lista de candidatos
    candidatos = [consultor for consultor in consultores if consultor['nome'] not in nomes_sorteados]
    
    # Se não houver mais candidatos, reinicia a lista de sorteados
    if not candidatos:
        nomes_sorteados = []
        candidatos = consultores.copy()
    
    # Realiza o sorteio
    vencedor = random.choice(candidatos)
    
    # Adiciona o nome do vencedor à lista de sorteados
    nomes_sorteados.append(vencedor['nome'])
    
    # Simula o atraso de 5 segundos
    time.sleep(5)
    
    # Retorna tanto o nome quanto o email
    return jsonify({'vencedor': vencedor['nome'], 'email': vencedor['email']})

if __name__ == '__main__':
    app.run(debug=True)