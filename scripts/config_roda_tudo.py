import glob
import sys

diretorio = r"C:\Users\nathan\Documents\projetos\project_data\scripts"  # Insira o caminho para o diretório onde estão os arquivos
log_file = "log.txt"  # Nome do arquivo de log

# Encontra todos os arquivos que começam com 'df_' no diretório especificado
arquivos = glob.glob(diretorio + "/df_*.py")
total_arquivos = len(arquivos)
print(arquivos)
# Executa cada arquivo encontrado e registra as informações no log
with open(log_file, "w") as f:
    for i, arquivo in enumerate(arquivos):
        try:
            exec(open(arquivo).read())  # Python 3
            # execfile(arquivo)  # Python 2
            f.write(f"Arquivo executado com sucesso: {arquivo}\n")
        except Exception as e:
            f.write(f"Erro ao executar o arquivo {arquivo}: {e}\n")
        
        # Atualiza a barra de progresso
        progresso = (i + 1) / total_arquivos * 100
        barra = "#" * int(progresso // 2) + "-" * int(50 - progresso // 2)
        sys.stdout.write(f"\rProgresso: [{barra}] {progresso:.2f}%")
        sys.stdout.flush()
