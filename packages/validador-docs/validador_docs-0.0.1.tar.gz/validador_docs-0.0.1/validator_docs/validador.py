import re

RANGE_CPF_DV_1 = range(10, 1, -1)
RANGE_CPF_DV_2 = range(11, 2, -1)
RANGE_CNPJ_DV_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
RANGE_CNPJ_DV_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

def normalizar_dado(dado: str | int):
    """
    Remove todos os caracteres que não são dígitos e verifica se é um número válido
    """
    if isinstance(dado, str):
        return re.sub(r'\D', '', dado)
    elif isinstance(dado, int):
        return str(dado)
    else:
        raise ValueError("O dado deve ser uma string ou um número.")

def identificar_documento(dado: str | int):
    """
    Identifica se o dado é CPF ou CNPJ com base na quantidade de dígitos.
    CPF tem 11 digitos
    CNPJ tem 14 digitos
    """
    dado_limpo = normalizar_dado(dado)
    if len(dado_limpo) == 11:
        return 'CPF'
    elif len(dado_limpo) == 14:
        return 'CNPJ'
    else:
        raise ValueError("Dado inválido: Não foi possivel identificar o tipo de dado. CPF: 11 digitos, CNPJ 14 digitos")
    
def calcular_dv_cpf(cpf, peso):
    """
    Calcula o digito verificador do CPF
    
    parametros: CPF - str | int
                peso: digito verificador 1: range(10, 1, -1)
                peso: digito verificador 2: range(11, 2, -1)
                
    retorna -> digito verificador
    """
    soma = sum(int(cpf[i]) * peso for i, peso in enumerate(peso))
    resto = (soma * 10) % 11
    return 0 if resto == 10 else resto

def calcular_dv_cnpj(cnpj, pesos):
    """ 
    Calcula o dígito verificador do CNPJ.  
    
    parâmetros: CNPJ - str | int  
                pesos: lista de pesos a serem utilizados no cálculo do dígito verificador,   
                       onde a lista deve ter um comprimento adequado dependendo da posição   
                       do dígito verificador sendo calculado.  
    
    retorna -> dígito verificador  
    """
    soma = sum(int(cnpj[i]) * pesos[i % len(pesos)] for i in range(len(pesos)))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto

def validar_cpf(cpf: str) -> bool:
    """
    Valida um cpf verificando os dígitos verificadores
    """
    cpf = normalizar_dado(cpf)
    if len(cpf) != 11:
        return False
    
    primeiro_dv = calcular_dv_cpf(cpf, RANGE_CPF_DV_1)
    segundo_dv = calcular_dv_cpf(cpf, RANGE_CPF_DV_2)
    
    return cpf[-2:] == f'{primeiro_dv}{segundo_dv}'

def validar_cnpj(cnpj: str) -> bool:
    """
    Valida um CNPJ verificando os dígitos verificadores.
    """
    cnpj = normalizar_dado(cnpj)

    if len(cnpj) != 14:
        return False

    primeiro_dv = calcular_dv_cnpj(cnpj[:-2], RANGE_CNPJ_DV_1)
    segundo_dv = calcular_dv_cnpj(cnpj[:-1], RANGE_CNPJ_DV_2)

    return cnpj[-2:] == f'{primeiro_dv}{segundo_dv}'

def formatar_cpf(cpf):
    """
    Formata o CPF para o padrão XXX.XXX.XXX-XX
    """
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_cnpj(cnpj):
    """
    Formata o CNPJ para o padrão XX.XXX.XXX/XXXX-XX
    """
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def validar_doc(dado, formatado = False):
    """
    Valida se o dado informado é um CPF ou CNPJ e verifica sua validade.
    Retorna o CPF/CNPJ formatado se for válido em formato String, ou uma exceção se for inválido.
    """
    tipo = identificar_documento(dado)
    dado_validado = ''
    
    if tipo == 'CPF':
        if validar_cpf(dado):
            dado_validado = normalizar_dado(dado)
            if formatado:
                dado_validado = formatar_cpf(dado_validado)
        else:
            raise ValueError("CPF inválido.")
    elif tipo == 'CNPJ':
        if validar_cnpj(dado):
            dado_validado = normalizar_dado(dado)
            if formatado:
                dado_validado = formatar_cnpj(dado_validado)
        else:
            raise ValueError("CNPJ inválido")
        
    return dado_validado
