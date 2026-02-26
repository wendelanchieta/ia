# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import glob
from consolidar import gerar_documento_final
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pypdf import PdfReader
import re


# 1. IA LOCAL
local_llm = LLM(model="ollama/llama3", base_url="http://localhost:11434")

# FERRAMENTA DO ANALISTA (Lê a pasta toda)
class FerramentaLeituraGeral(BaseTool):
    name: str = "ler_todos_editais"
    description: str = "Lê todos os PDFs da pasta data para análise comparativa."

    def _run(self, **kwargs) -> str:
        arquivos = glob.glob(os.path.join(os.getcwd(), 'data', "*.pdf"))
        texto_total = ""
        for arq in arquivos:
            # Ignora o arquivo de erro para não poluir a análise comparativa
            if "PDF_TESTE_ERROS.pdf" in arq: continue
            reader = PdfReader(arq)
            texto_total += f"\n--- EDITAL: {os.path.basename(arq)} ---\n"
            for page in reader.pages:
                texto_total += page.extract_text() + "\n"
        return texto_total


# FERRAMENTA DO AUDITOR (Lê APENAS o arquivo de teste)
class FerramentaAuditoriaEspecifica(BaseTool):
    name: str = "ler_edital_auditoria"
    description: str = "Lê especificamente o arquivo PDF_TESTE_ERROS.pdf para auditoria detalhada."

    def _run(self, **kwargs) -> str:
        caminho = os.path.join(os.getcwd(), 'data', "PDF_TESTE_ERROS.pdf")
        if not os.path.exists(caminho):
            return "Erro: Arquivo PDF_TESTE_ERROS.pdf não encontrado na pasta data."

        reader = PdfReader(caminho)
        texto_edital = ""
        for page in reader.pages:
            texto_edital += page.extract_text() + "\n"
        return texto_edital


# Instanciando as duas
ferramenta_geral = FerramentaLeituraGeral()
ferramenta_auditoria = FerramentaAuditoriaEspecifica()

# 3. LISTA DE ARQUIVOS
arquivos = glob.glob("./data/*.pdf")
lista_formatada = "\n".join(arquivos)

# 4. AGENTES
analista = Agent(
    role='Analista Comparativo de Licitações',
    goal='Identificar padrões, métricas de produtividade e falhas em múltiplos editais históricos',
    backstory="""Você é um especialista em mineração de dados para o setor público. 
    Sua tarefa é ler todos os arquivos na pasta data, comparar as exigências 
    entre eles e destacar o que é padrão de mercado e o que é cláusula restritiva.
    Você é um robô de extração de dados. Você deve usar a ferramenta 
    de leitura para CADA UM dos arquivos da lista. Não tente adivinhar caminhos, 
    use apenas os caminhos completos que foram fornecidos.""",
    llm=local_llm,
    tools=[ferramenta_geral],
    verbose=True
)

consultor = Agent(
    role='Consultor de Governança Lei 14.133',
    goal='Sintetizar a melhor solução de compra baseada no histórico e na nova lei',
    backstory="""Você transforma dados brutos em estratégia jurídica. 
    Seu papel é filtrar as informações do analista e garantir que o novo 
    ETP siga rigorosamente o Art. 18 da Lei 14.133/2021, focando em eficácia.""",
    llm=local_llm,
    verbose=True
)

# AGENTE AUDITOR
auditor_fiscal = Agent(
    role='Auditor de Controle Externo Especializado em Logística',
    goal='Detectar erros críticos, ilegalidades e inconsistências matemáticas em editais de limpeza.',
    backstory="""Você é um auditor rigoroso com 20 anos de experiência em licitações. 
    Seu conhecimento é baseado na Lei 14.133/2021 e na Instrução Normativa SEGES/MP nº 05/2017. 
    Você não aceita desculpas e é extremamente detalhista com números. 
    Sua missão é impedir que editais com produtividades inexequíveis ou erros de cálculo 
    sejam publicados, evitando prejuízos ao erário.""",
    llm=local_llm,
    tools=[ferramenta_auditoria],
    verbose=True
)

# 5. TAREFAS
tarefa_extracao = Task(
    description=f"""
    1. Chame a ferramenta 'leitor_pdf_especializado'. 
    Ela retornará o texto de todos os editais na pasta data.
    2. Sua única tarefa é analisar esse texto e extrair produtividade m² e valores.
    3. Liste as diferentes metodologias de medição de serviço de limpeza encontradas.
    4. Identifique a produtividade média (m² por servente) adotada.
    5. Verifique se houve exigência de amostras ou vistoria técnica.""",
    expected_output="Relatório comparativo destacando as melhores práticas e riscos encontrados nos documentos.",
    agent=analista,
    output_file="relatorio_analista.md"
)

tarefa_etp = Task(
    description="""Com base no relatório comparativo, redija a seção de 'Levantamento de Mercado' 
    e 'Justificativa de Quantitativos' para um NOVO ETP de limpeza. 
    Adapte os termos técnicos para a nomenclatura da Lei 14.133/2021.""",
    expected_output="Minuta técnica do ETP em formato Markdown, pronta para revisão humana.",
    agent=consultor,
    output_file="relatorio_consultor.md"
)

# TAREFA DE AUDITORIA
tarefa_auditoria_critica = Task(
    description="""USE A FERRAMENTA 'ler_edital_auditoria' para obter o conteúdo do arquivo.
    Não tente ler outros arquivos. Foque exclusivamente nos dados retornados por esta ferramenta. 
    Você deve confrontar o texto do edital com os seguintes parâmetros LEGAIS:

    1. PRODUTIVIDADE: Segundo a IN 05/2017, a produtividade de referência para limpeza interna 
       é de 600m² a 800m². Qualquer valor ACIMA disso deve ser apontado como 'Inexequível'.
    2. MATEMÁTICA: Multiplique o valor do posto pelo número de postos e verifique se o total 
       anual bate com o 'Valor Global Estimado'. Aponte divergências centavo por centavo.
    3. QUALIFICAÇÃO FINANCEIRA: A Lei 14.133/21 limita o Patrimônio Líquido a no máximo 10% 
       do valor estimado. Aponte se o edital estiver exigindo mais.
    4. GARANTIA DE PROPOSTA: O limite legal é de 1%. Valores superiores são ilegais.
    5. LEGISLAÇÃO: Verifique se o edital cita leis revogadas (como a 8.666/93).

    Se encontrar erros, use o cabeçalho '🔴 ALERTA DE ILEGALIDADE'. 
    Se encontrar erros de cálculo, use '🧮 ERRO ARITMÉTICO'.""",
    expected_output="""Um relatório de auditoria estruturado em: 
    - Item analisado;
    - Trecho encontrado no edital;
    - Base legal violada;
    - Recomendação de correção.""",
    agent=auditor_fiscal,
    output_file="relatorio_auditoria_teste.md"
)

# 6. EQUIPE
equipe = Crew(
    agents=[analista, consultor, auditor_fiscal],
    tasks=[tarefa_extracao, tarefa_etp, tarefa_auditoria_critica],
    process=Process.sequential,
    cache=True # Evita gastos repetidos de API com o mesmo PDF
)

if __name__ == "__main__":
    # Limpa chave OpenAI para garantir 100% local
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    print("### Iniciando Processamento de Múltiplos Editais ###")
    resultado = equipe.kickoff()
    print("\n\n################################################")
    print("## PROPOSTA DE ETP BASEADA EM DADOS HISTÓRICOS ##")
    print("################################################\n")
    print(resultado)
    gerar_documento_final()
    print("\nO PARECER_TECNICO_FINAL_MCTI.docx final foi gerado.")
    print("\nProcesso concluído! O arquivo 'relatorio_auditoria_teste.md' foi gerado.")