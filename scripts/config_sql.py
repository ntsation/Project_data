# config.py

server = 'DESKTOP-IO738LM'
database = 'project_data'
driver = '{ODBC Driver 17 for SQL Server}'

try:
    from config_sql import server, database, driver
    print("Arquivo config.py importado com sucesso.")
except ImportError:
    print("Erro ao importar o arquivo config.py. Verifique se o arquivo existe e está configurado corretamente.")