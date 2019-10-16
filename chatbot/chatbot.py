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
linhas = open('E:/ambdes/ProjetosGIT/ia/chatbot/recursos/movie-lines.txt').read().split('\n')

# Importacao dos dados de Conversas
conversas = open('E:/ambdes/ProjetosGIT/ia/chatbot/recursos/movie-conversations.txt').read().split('\n')

# Criação de um dicionário para mapear cada linha com seu ID
id_para_linha = {}
for linha in linhas:
    _linha = linha.split(' +++$+++ ')
    if len(_linha) == 5:
        #print(_linha)
        id_para_linha[_linha[0]] = _linha[4]