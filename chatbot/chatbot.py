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
import re
import time
#import tensorflow as tf
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()

# Pré-processamento dos dados

# Importacao dos dados de linhas
#linhas = open('/home/wendel/ambdes/projetosgit/ia/chatbot/recursos/movie-lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
#linhas = open('E:/ambdes/ProjetosGIT/ia/chatbot/recursos/movie-lines.txt').read().split('\n')
linhas = open('C:/ambdes/ProjetosGit/ia/chatbot/recursos/movie-lines.txt').read().split('\n')
# Importacao dos dados de Conversas
#conversas = open('/home/wendel/ambdes/projetosgit/ia/chatbot/recursos/movie-conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')
#conversas = open('E:/ambdes/ProjetosGIT/ia/chatbot/recursos/movie-conversations.txt').read().split('\n')
conversas = open('C:/ambdes/ProjetosGit/ia/chatbot/recursos/movie-conversations.txt').read().split('\n')
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

# Remoção de palavras não frequentes e tokenização (dois dicionários)
limite = 20
perguntas_palavras_int = {}
numero_palavra = 0
for palavra, contagem in palavras_contagem.items():
    if contagem >= limite:
        perguntas_palavras_int[palavra] = numero_palavra
        numero_palavra += 1

respostas_palavras_int = {}
numero_palavra = 0
for palavra, contagem in palavras_contagem.items():
    if contagem >= limite:
        respostas_palavras_int[palavra] = numero_palavra
        numero_palavra += 1

# Adição de tokens no dicionário
tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']        

for token in tokens:
    perguntas_palavras_int[token] = len(perguntas_palavras_int) + 1

for token in tokens:
    respostas_palavras_int[token] = len(respostas_palavras_int) + 1

# Criação do dicionário inverso com o dicionário de respostas
respostas_int_palavras = {p_i: p for p, p_i in respostas_palavras_int.items()}

# Adição do token final de string <EOS> para o final de cada resposta
for i in range(len(respostas_limpas)):
    respostas_limpas[i] += ' <EOS>'

# Tradução de todas as perguntas e respostas para inteiros 
# Substituição das palavras menos frequentes para <OUT>   
perguntas_para_int = []
for pergunta in perguntas_limpas:
    ints = []
    for palavra in pergunta.split():
        if palavra not in perguntas_palavras_int:
            ints.append(perguntas_palavras_int['<OUT>'])
        else:
            ints.append(perguntas_palavras_int[palavra])
    perguntas_para_int.append(ints)            
    
respostas_para_int = []
for resposta in respostas_limpas:
    ints = []
    for palavra in resposta.split():
        if palavra not in respostas_palavras_int:
            ints.append(respostas_palavras_int['<OUT>'])
        else:
            ints.append(respostas_palavras_int[palavra])
    respostas_para_int.append(ints)            

# Ordenação das perguntas e respostas pelo tamanho das perguntas    
perguntas_limpas_ordenadas = []
respostas_limpas_ordenadas = []
for tamanho in range(1,25 + 1):
    for i in enumerate(perguntas_para_int):
        if len(i[1]) == tamanho:
            perguntas_limpas_ordenadas.append(perguntas_para_int[i[0]])
            respostas_limpas_ordenadas.append(respostas_para_int[i[0]])

# Construção do modelo Seq2Seq
# Criação de placeholders para as entradas e saidas
# [64, 25]
# olá <PAD> <PAD> <PAD> <PAD>
# olá tudo bem <PAD> <PAD>
# olá tudo bem e você 
# [3, 5]            
def entradas_modelo():
    entradas = tf.placeholder(tf.int32, [None, None], name='entradas')
    saidas = tf.placeholder(tf.int32, [None, None], name='saidas')           
    lr = tf.placeholder(tf.float32, name='learning_rate')
    keep_prob = tf.placeholder(tf.float32, name='keep_prob')
    return entradas, saidas, lr, keep_prob

# Pré-processamento das saidas (alvos)
# [batch_size, 1] = [64, 1] 
# 0 - SOS (8830)
# 1 - SOS (8830)   
def preprocessamento_saidas(saidas, palavra_para_int, batch_size):
    esquerda = tf.fill([batch_size,1], palavra_para_int['<SOS>'])
    direita = tf.strided_slice(saidas, [0,0], [batch_size, -1], strides = [1,1])
    saidas_preprocessadas = tf.concat([esquerda,direita], 1)
    return saidas_preprocessadas

# criação da camada RNN do codificador
# tf.VERSION
def rnn_codificador(rnn_entradas, rnn_tamanho, numero_camadas, keep_prob, tamanho_sequencia):
    lstm = tf.contrib.rnn.LSTMCell(rnn_tamanho)
    lstm_dropout = tf.contrib.rnn.DropoutWrapper(lstm, input_keep_prob = keep_prob)
    encoder_celula = tf.contrib.rnn.MultiRNNCell([lstm_dropout] * numero_camadas)
    _, encoder_estado = tf.nn.bidirectional_dynamic_rnn(cell_fw = encoder_celula,
                                                     cell_bw = encoder_celula,
                                                     sequence_lenght = tamanho_sequencia,
                                                     inputs = rnn_entradas,
                                                     dtype = tf.float32)
    return encoder_estado

# Decodificação da base de treinamento
def decodifica_base_treinamento(encoder_estado, decodificador_celula, 
                                decodificador_embedded_entrada, tamanho_sequencia, 
                                decodificador_escopo, funcao_saida, 
                                keep_prob, batch_size):
    estados_atencao = tf.zeros([batch_size, 1, decodificador_celula.output_size])
    attention_keys, attention_values, attention_score_function, attention_construct_function = tf.contrib.seq2seq.prepare_attention(estados_atencao,
                                                                                                                                    attention_option = 'bahdanau',
                                                                                                                                    num_units = decodificador_celula.output_size)
    funcao_decodificador_treinamento = tf.contrib.seq2seq.attention_decoder_fn_train(encoder_estado[0],
                                                                                     attention_keys, 
                                                                                     attention_values, 
                                                                                     attention_score_function, 
                                                                                     attention_construct_function,
                                                                                     name = 'attn_dec_train')
    decodificador_saida, _, _ = tf.contrib.seq2seq.dynamic_rnn_decoder(decodificador_celula, 
                                                                       funcao_decodificador_treinamento,
                                                                       decodificador_embedded_entrada,
                                                                       tamanho_sequencia,
                                                                       scope = decodificador_escopo)
    decodificador_saida_dropout = tf.nn.dropout(decodificador_saida, keep_prob)
    return funcao_saida(decodificador_saida_dropout)

# Decodificação da base de teste/validacao
def decodifica_base_teste(encoder_estado, decodificador_celula, 
                          decodificador_embedding_matrix, sos_id, eos_id, tamanho_maximo,
                          numero_palavras, decodificador_escopo, funcao_saida,
                          keep_prob, batch_size):
                          
    estados_atencao = tf.zeros([batch_size, 1, decodificador_celula.output_size])
    attention_keys, attention_values, attention_score_function, attention_construct_function = tf.contrib.seq2seq.prepare_attention(estados_atencao,
                                                                                                                                    attention_option = 'bahdanau',
                                                                                                                                    num_units = decodificador_celula.output_size)
    funcao_decodificador_teste = tf.contrib.seq2seq.attention_decoder_fn_inference(funcao_saida,
                                                                                   encoder_estado[0],
                                                                                   attention_keys, 
                                                                                   attention_values, 
                                                                                   attention_score_function, 
                                                                                   attention_construct_function,
                                                                                   decodificador_embedding_matrix,
                                                                                   sos_id,
                                                                                   eos_id,
                                                                                   tamanho_maximo,
                                                                                   numero_palavras,
                                                                                   name = 'attn_dec_inf')
    
    previsoes_teste, _, _ = tf.contrib.seq2seq.dynamic_rnn_decoder(decodificador_celula, 
                                                                   funcao_decodificador_teste,
                                                                   scope = decodificador_escopo)
    
    return previsoes_teste

# Criação da RNN do decodificador
def rnn_decodificador(decodificador_embedded_entrada, decodificador_embeddings_matrix,
                      codificador_estado, numero_palavras, tamanho_sequencia, rnn_tamanho,
                      numero_camadas, palavra_para_int, keep_prob, batch_size):
    with tf.variable_scope("decodificador") as decodificador_escopo:
        lstm = tf.contrib.rnn.LSTMCell(rnn_tamanho)
        lstm_dropout = tf.contrib.rnn.DropoutWrapper(lstm, input_keep_prob = keep_prob)
        decodificador_celula = tf.contrib.rnn.MultiRNNCell([lstm_dropout] * numero_camadas)
        pesos = tf.truncated_normal_initializer(stddev = 0.1)
        biases = tf.zeros_initializer()
        funcao_saida = lambda x: tf.contrib.layers.fully_connected(x, numero_palavras,
                                                                   None,
                                                                   scope = decodificador_escopo,
                                                                   weights_initializer = pesos,
                                                                   biases_initializer = biases)
        previsoes_treinamento = decodifica_base_treinamento(codificador_estado,
                                                            decodificador_embedded_entrada,
                                                            tamanho_sequencia,
                                                            decodificador_escopo,
                                                            funcao_saida,
                                                            keep_prob,
                                                            batch_size)
        decodificador_escopo.reuse_variables()
        privisoes_teste = decodifica_base_teste(codificador_estado,
                                                decodificador_celula,
                                                decodificador_embeddings_matrix,
                                                palavra_para_int['<SOS>'],
                                                palavra_para_int['<EOS>'],
                                                tamanho_sequencia - 1,
                                                numero_palavras,
                                                decodificador_escopo,
                                                funcao_saida,
                                                keep_prob,
                                                batch_size)
        return previsoes_treinamento, privisoes_teste

# Criação do modelo Seq2Seq
def modelo_seq2seq(entradas, saidas, keep_prob, batch_size, tamanho_sequencia,
                   numero_palavras_respostas, numero_palavras_perguntas, 
                   tamanho_codificador_embeddings, tamanho_decodificador_embeddings,
                   rnn_tamanho, numero_camadas, perguntas_palavras_int):
    
    codificador_embedded_entrada = tf.contrib.layers.embed_sequence(entradas,
                                                                    numero_palavras_respostas + 1,
                                                                    tamanho_codificador_embeddings,
                                                                    initializer = tf.random_uniform_initializer(0,1))
    codificador_estado = rnn_codificador(codificador_embedded_entrada,
                                         rnn_tamanho, numero_camadas,
                                         keep_prob, tamanho_sequencia)
    
    saidas_preprocessadas = preprocessamento_saidas(saidas, perguntas_palavras_int, batch_size)
    
    decodificador_embeddings_matrix = tf.Variable(tf.random_uniform([numero_palavras_perguntas + 1,
                                                                     tamanho_decodificador_embeddings],0, 1))
    decodificador_embedded_entradas =  tf.nn.embedding_lookup(decodificador_embeddings_matrix,
                                                              saidas_preprocessadas)
    previsoes_treinamento, privisoes_teste = rnn_decodificador(decodificador_embedded_entrada,
                                                               decodificador_embeddings_matrix,
                                                               codificador_estado,
                                                               numero_palavras_perguntas,
                                                               rnn_tamanho, 
                                                               numero_camadas,
                                                               perguntas_palavras_int,
                                                               keep_prob,
                                                               batch_size)
    return previsoes_treinamento, privisoes_teste
            
# -Treinamento do modelo Seq2Seq -
# Configuração dos hiperparâmetros
epocas = 100
batch_size = 64 
rnn_tamanho = 512
numero_camadas = 3
tamanho_codificador_embeddings = 512
tamanho_decodificador_embeddings = 512
learning_rate = 0.01
learning_rate_decaimento = 0.9
min_learning_rate = 0.0001
probabilidade_dropout = 0.5

# Definição da seção
tf.reset_default_graph()
session = tf.InteractiveSession()


    
    
    
    
    
    