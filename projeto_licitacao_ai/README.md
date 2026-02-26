<figure>
  <img src="https://github.com/wendelanchieta/python/blob/master/img/python_banner_image.png" alt="cabecalho-readme-python" height="100" align="middle">
</figure>

[![Email](https://img.shields.io/badge/email-wendelanchieta%40gmail.com-blue)](mailto:wendelanchieta@gmail.com)
[![Python](https://img.shields.io/badge/python-blue)](#)

# Agentes de IA para análise de editais de licitação

>O código implementa um fluxo de automação para análise de editais de licitação, extração de dados de PDFs, comparação de métricas e auditoria legal, utilizando agentes de IA especializados e RAG (Retrieval-Augmented Generation ou Geração Aumentada por Recuperação).
	
## Contexto

>Gerir compras públicas no Brasil já era uma arte; com a Lei nº 14.133/2021 (Nova Lei de Licitações), tornou-se uma ciência de alta precisão que exige planejamento, gestão de riscos e uma conformidade rigorosa.

>Essa implementação se propõe a resolver:<br/>
>1. Evitar o "Control+C / Control+V" cego: O agente de IA lê o PDF antigo, mas o segundo agente (Consultor Lei) é obrigado a "criticar" esse conteúdo sob a ótica da nova lei.
>2. Memória Institucional: Muitas vezes, o servidor que fez a licitação passada saiu do órgão. A IA recupera o conhecimento técnico depositado nos arquivos do departamento.
>3. Justificativa de Preços: Ao ler editais anteriores e compará-los com o mercado atual, você gera uma trilha de auditoria robusta para justificar o preço estimado, uma das maiores causas de punição pelos Tribunais de Contas.

>`Nota de Segurança:` Lembre-se que, ao usar APIs de nuvem (como OpenAI), é importante não subir PDFs que contenham dados sigilosos ou sensíveis, a menos que você esteja usando uma instância privada (como Azure OpenAI ou servidores locais via Ollama).
	
### IA Agêntica (Agentic AI)	
><b>O que é Agentic AI?</b><br/> (A Diferença entre Ferramenta e Agente) Imagine a IA tradicional (como o `ChatGPT` comum) como uma enciclopédia rápida: você faz uma pergunta, ela responde. Já a IA `Agêntica` é como um analista técnico autônomo.Ela não apenas "sabe" coisas; ela executa fluxos de trabalho. Um agente tem capacidade de raciocínio, planejamento e, principalmente, iniciativa para usar ferramentas (consultar o PNCP, ler editais, comparar planilhas) para atingir um objetivo que você definiu.

### O que é crewAI?

>CrewAI é um framework de orquestração multiagente de código aberto criado por João Moura. Esse framework baseado em Python aproveita a colaboração da inteligência artificial (IA) ao orquestrar agentes autônomos que desempenham papéis específicos e trabalham juntos como uma equipe (crew) para completar tarefas. O objetivo do crewAI é fornecer uma base sólida para automatizar fluxos de trabalho multiagentes.
<br/>Fonte: [O que é crewAI?](https://www.ibm.com/br-pt/think/topics/crew-ai)

### O que é RAG?

>`RAG (Retrieval-Augmented Generation ou Geração Aumentada por Recuperação)` é uma técnica de IA que conecta `Grandes Modelos de Linguagem (LLMs)` a fontes de dados externas confiáveis. Isso permite que a IA acesse informações atualizadas, proprietárias ou específicas, reduzindo "alucinações" e melhorando a precisão sem precisar retreinar o modelo. Esse processo otimiza a saída de um grande modelo de linguagem, de forma que ele faça referência a uma base de conhecimento confiável fora das suas fontes de dados de treinamento antes de gerar uma resposta. Grandes modelos de linguagem (LLMs) são treinados em grandes volumes de dados e usam bilhões de parâmetros para gerar resultados originais para tarefas como responder a perguntas, traduzir idiomas e concluir frases. A RAG estende os já poderosos recursos dos LLMs para domínios específicos ou para a base de conhecimento interna de uma organização sem a necessidade de treinar novamente o modelo. É uma abordagem econômica para melhorar a produção do LLM, de forma que ele permaneça relevante, preciso e útil em vários contextos.
<br/>Fonte: [O que é RAG (geração aumentada via recuperação)?](https://aws.amazon.com/pt/what-is/retrieval-augmented-generation)

## O está implementado?

>O código implementa um fluxo de automação para análise de editais de licitação, extração de dados de PDFs, comparação de métricas e auditoria legal, utilizando agentes de IA especializados.<br>Este script simula 3 agentes: um `Especialista em Normas` (que garante o cumprimento da Lei 14.133), um `Analista de Mercado` (que busca preços e soluções) e `Auditor de Controle Externo` (Especializado em Logística).

### Estrutura:

>projeto_licitacao_ai/<br/>
>├── data/&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&nbsp;# Coloque aqui seus PDFs de editais antigos<br/>
>├── .env&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&nbsp;&nbsp;# Arquivo para chaves de API (não compartilhe!)<br/>
>├── requirements.txt&nbsp;# Lista de bibliotecas para instalar<br/>
>├── consolidar.py&ensp;&ensp;&ensp;# Gera o arquivo com o relatório final em `.docx` <br/>
>└── main.py&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;# O script principal que executa os agentes<br/>

> #### Lista de agentes:
>
> - Especialista em Normas (`que garante o cumprimento da Lei 14.133`)
> - Analista de Mercado (`que busca preços e soluções`) 
> - Auditor de Controle Externo (`Especializado em Logística`)
>
>  <br/>**Obs:** o código ainda está em *desenvolvimento*.

<img src="https://github.com/wendelanchieta/ia/blob/master/img/ai_agent_vs_agentic_ai.gif">