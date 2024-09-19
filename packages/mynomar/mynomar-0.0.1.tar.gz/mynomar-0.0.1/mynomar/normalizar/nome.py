import re
import os
from ..modificar import texto

def arquivo(nome_arquivo: str, caixa: str = '', caracteres_permitidos: str = "_-.") -> str:
	"""
	Normaliza o nome de um arquivo removendo caracteres especiais e espaços.
	
	Args:
		nome_arquivo (str): O nome do arquivo original.
		caracteres_permitidos (str): Lista de caracteres permitidos além de caracteres alfanuméricos.
	
	Returns:
		str: O nome do arquivo normalizado.
	"""
	
	# Separa o nome do arquivo da sua extensão
	nome, extensao = os.path.splitext(nome_arquivo)

	# Substitui espaços por sublinhados
	nome = nome.replace(' ', '_')

	# Remove caracteres que não são alfanuméricos ou permitidos
	nome = re.sub(rf'[^\w{re.escape(caracteres_permitidos)}]', '', nome)

	# Junta o nome e a extensão de volta
	arquivo_normalizado = f"{nome}{extensao}"

	resultado = arquivo_normalizado

	match caixa.lower():
		case 'alta': 
			resultado = texto.caixa_alta(arquivo_normalizado)
		case 'baixa':
			resultado = texto.caixa_baixa(arquivo_normalizado)
		case 'capital':
			resultado = texto.caixa_capital(arquivo_normalizado)
		case _:
			pass

	return resultado



def pasta(caminho: str, caixa: str = '', caracteres_permitidos: str = "_-.") -> None:
	"""
	Normaliza todos os arquivos em um diretório, renomeando-os.

	Args:
		caminho (str): Caminho do diretório.
		caracteres_permitidos (str): Lista de caracteres permitidos além de caracteres alfanuméricos.
	"""
	for nome_arquivo in os.listdir(caminho):
		caminho_antigo = os.path.join(caminho, nome_arquivo)
		
		# Ignorar diretórios
		if os.path.isdir(caminho_antigo):
			continue
		
		novo_arquivo = arquivo(nome_arquivo, caixa, caracteres_permitidos)
		caminho_novo = os.path.join(caminho, novo_arquivo)

		# Renomeia o arquivo se o nome mudou
		if caminho_antigo != caminho_novo:
			os.rename(caminho_antigo, caminho_novo)
			print(f"Renomeado: {caminho_antigo} -> {caminho_novo}")
