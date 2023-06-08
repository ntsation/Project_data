import os
import sys

def gerar_arquivo_python(pasta, nome_arquivo, codigo):
    caminho_pasta = os.path.abspath(pasta)
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
    with open(caminho_arquivo, 'w', encoding= 'utf-8') as arquivo:
        arquivo.write(codigo)
    print(f'O arquivo {nome_arquivo} foi gerado com sucesso na pasta {caminho_pasta}!')

# Define o caminho padrão da pasta
caminho_pasta_padrao = r'C:\\Users\\nathan\\Documents\\projetos\\project_data\\scripts\\'  # Substitua pelo caminho desejado

# Verifica se o nome do arquivo foi fornecido corretamente
if len(sys.argv) < 2:
    print("Uso: python nome_do_script.py nome_do_arquivo")
else:
    nome_arquivo = sys.argv[1]
    codigo = '''
import csv
import pyodbc
import pandas as pd
from config_sql import server, database, driver
import os
import logging
import re

# Configuração do arquivo CSV
csv_file = r'C:\\Users\\nathan\\Documents\\projetos\\project_data\\source\\datasets' # Substitua pelo caminho desejado

# Obter o diretório do arquivo CSV
csv_directory = os.path.dirname(csv_file)

# Obter o nome do arquivo CSV sem a extensão
table_name = os.path.splitext(os.path.basename(csv_file))[0]

# Configuração do arquivo de log
log_file = os.path.join(csv_directory, 'log.txt')

# Configuração do logger
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Conexão com o banco de dados
try:
    conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
    logging.info('Conexão com o banco de dados estabelecida com sucesso.')
except pyodbc.Error as e:
    logging.error('Erro ao estabelecer a conexão com o banco de dados: ' + str(e))

# Criação do cursor
cursor = conn.cursor()

# Leitura do arquivo CSV usando o pandas
try:
    df = pd.read_csv(csv_file)
    logging.info('Arquivo CSV lido com sucesso.')
except pd.errors.EmptyDataError:
    logging.error('Erro ao ler o arquivo CSV: arquivo vazio.')
    exit()
except pd.errors.ParserError as e:
    logging.error('Erro ao ler o arquivo CSV: ' + str(e))
    exit()
except FileNotFoundError:
    logging.error('Erro ao ler o arquivo CSV: arquivo não encontrado.')
    exit()

# Limpar os nomes das colunas do arquivo CSV
clean_column_names = [re.sub(r'\W+', '_', col.strip()) for col in df.columns]

# Atualizar os nomes das colunas no dataframe
df.columns = clean_column_names

# Obtém os nomes das colunas do arquivo CSV
column_names = df.columns.tolist()

# Criação da tabela no banco de dados com as colunas inferidas
columns_definition = ', '.join('{} VARCHAR(MAX)'.format(col) for col in column_names)
create_table_query = 'CREATE TABLE {} ({})'.format(table_name, columns_definition)

# Executa a query de criação da tabela
try:
    cursor = conn.cursor()
    cursor.execute(create_table_query)
    cursor.commit()
    logging.info('Tabela criada com sucesso.')
except pyodbc.Error as e:
    logging.error('Erro ao criar tabela no banco de dados: ' + str(e))

# Insere os dados do arquivo CSV na tabela
for row in df.itertuples(index=False):
    values = [str(value) for value in row]
    insert_query = 'INSERT INTO {} VALUES ({})'.format(table_name, ', '.join(['?'] * len(column_names)))

    try:
        cursor.execute(insert_query, values)
    except pyodbc.Error as e:
        logging.error('Erro ao inserir dados na tabela: ' + str(e))
        exit()

# Confirma as alterações no banco de dados
try:
    conn.commit()
    logging.info('Dados inseridos com sucesso no banco de dados.')
except pyodbc.Error as e:
    logging.error('Erro ao confirmar as alterações no banco de dados: ' + str(e))

# Fecha a conexão com o banco de dados
conn.close()
logging.info('Conexão com o banco de dados encerrada.')

# Fecha o arquivo de log
logging.shutdown()

'''
    gerar_arquivo_python(caminho_pasta_padrao, nome_arquivo, codigo)
