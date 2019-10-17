# -*- coding: utf-8 -*-
"""
Construção de Chatbot implementado com o modelo Seq2Seq 
de Processamento de Linguagem Natural, 
utilizando Redes Neurais Recorrentes.

Created on Wed Oct 16 14:29:59 2019

@author: wendel.anchieta
"""

#!pip install tensorflow
import numpy as np
import tensorflow as tf
import re
import time

# Pré-processamento dos dados

# Importacao dos dados de linhas
linhas = open('/home/wendel/ambdes/projetosgit/ia/chatbot/recursos/movie-lines.txt', encoding='utf-8', errors='ignore').read().split('\n')

# Importacao dos dados de Conversas
conversas = open('/home/wendel/ambdes/projetosgit/ia/chatbot/recursos/movie-conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

# Criação de um dicionário para mapear cada linha com seu ID
# Olá! - Olá!
# Tudo bem? - Tudo!
# Eu também!

# Olá! - Olá!
# Olá! - Tudo bem?
# Tudo bem? - Tudo
# Tudo - Eu também!

id_para_linha = {}

for linha in linhas:
    _linha = linha.split(' +++$+++ ')
    if len(_linha) == 5:
        #print(_linha)
        id_para_linha[_linha[0]] = _linha[4]
        
# Criação de uma lista com todas as conversas
conversas_id = []
# -1 impede do laço for trazer o ultimo resultado
for conversa in conversas[:-1]:
    #print(conversa)
    _conversa = conversa.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
    #print(_conversa)
    conversas_id.append(_conversa.split(','))
    
# Separacao das perguntas e respostas
# 194 - 195 - 196 - 197

# 194 - 195
# 195 - 196
# 196 - 197

perguntas = []
respostas = []
for conversa in conversas_id:
    #print(conversa)
    #print('******')
    for i in range(len(conversa)-1):
        #print(i)
        perguntas.append(id_para_linha[conversa[i]])
        respostas.append(id_para_linha[conversa[i+1]])

def limpa_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"i'm", "i am", texto)
    texto = re.sub(r"i ' m", "i am", texto)
    texto = re.sub(r"he's", "he is", texto)
    texto = re.sub(r"he ' s", "he is", texto)
    texto = re.sub(r"she's", "she is", texto)
    texto = re.sub(r"she ' s", "she is", texto)
    texto = re.sub(r"that's", "that is", texto)
    texto = re.sub(r"that ' s", "that is", texto)
    texto = re.sub(r"what's", "what is", texto)
    texto = re.sub(r"what ' s", "what is", texto)
    texto = re.sub(r"where's", "where is", texto)
    texto = re.sub(r"where ' s", "where is", texto)
    texto = re.sub(r"\'ll", " will", texto)
    texto = re.sub(r"\ ' ll", " will", texto)
    texto = re.sub(r"\'ve", " have", texto)
    texto = re.sub(r"\ ' ve", " have", texto)
    texto = re.sub(r"\'re", " are", texto)
    texto = re.sub(r"\ ' re", " are", texto)
    texto = re.sub(r"\'d", " would", texto)
    texto = re.sub(r"\ ' d", " would", texto)
    texto = re.sub(r"won't", "will not", texto)
    texto = re.sub(r"won ' t", "will not", texto)
    texto = re.sub(r"can't", "cannot", texto)
    texto = re.sub(r"can ' t", "cannot", texto)
    texto = re.sub(r"don ' t", "don't", texto)
    texto = re.sub(r"[-()#/@;:<>~{}~+=.|,%?¨]", "", texto)
    texto = re.sub(r"  ", " ", texto)
    return texto

# Limpeza das perguntas
perguntas_limpas = []
for pergunta in perguntas:
    perguntas_limpas.append(limpa_texto(pergunta))    

# Limpeza das respostas
respostas_limpas = []    
for resposta in respostas:
    respostas_limpas.append(limpa_texto(resposta))    

# Criação de um dicionário que mapeia cada palavra e o número de ocorrências NLTK
palavras_contagem = {}
for pergunta in perguntas_limpas:
    for palavra in pergunta.split():
        if palavra not in palavras_contagem:
            palavras_contagem[palavra] = 1
        else:
            palavras_contagem[palavra] += 1

for resposta in respostas_limpas:
    for palavra in resposta.split():
        if palavra not in palavras_contagem:
            palavras_contagem[palavra] = 1
        else:
            palavras_contagem[palavra] += 1






















    

    


       