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































    

    


       