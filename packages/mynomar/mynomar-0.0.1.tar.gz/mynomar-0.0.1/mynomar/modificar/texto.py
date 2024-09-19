def caixa_baixa(texto):
	"""
	Converte todo o texto para letras minúsculas.
	
	Args:
		texto (str): O texto original.
	
	Returns:
		str: O texto todo em letras minúsculas.
	"""
	return texto.lower()


def caixa_alta(texto):
	"""
	Converte todo o texto para letras maiúsculas.
	
	Args:
		texto (str): O texto original.
	
	Returns:
		str: O texto todo em letras maiúsculas.
	"""
	return texto.upper()


def caixa_capital(texto):
	"""
	Capitaliza o texto, deixando a primeira letra em maiúscula e as outras em minúsculas.
	
	Args:
		texto (str): O texto original.
	
	Returns:
		str: O texto capitalizado.
	"""
	return texto.capitalize()
