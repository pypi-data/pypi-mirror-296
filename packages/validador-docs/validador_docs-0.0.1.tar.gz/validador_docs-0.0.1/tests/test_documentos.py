import pytest  

# Supondo que as funções estejam em um arquivo chamado documentos.py  
from validator_docs.validador import (  
    normalizar_dado,  
    identificar_documento,  
    calcular_dv_cpf,  
    calcular_dv_cnpj,  
    validar_cpf,  
    validar_cnpj,  
    formatar_cpf,  
    formatar_cnpj,  
    validar_doc,
    RANGE_CNPJ_DV_2,
    RANGE_CNPJ_DV_1,
    RANGE_CPF_DV_1,
    RANGE_CPF_DV_2,
)  

def test_normalizar_dado():  
    assert normalizar_dado('123.456.789-09') == '12345678909'  
    assert normalizar_dado(12345678909) == '12345678909'  
    with pytest.raises(ValueError):  
        normalizar_dado(123.45)  

def test_identificar_documento():  
    assert identificar_documento('123.456.789-09') == 'CPF'  
    assert identificar_documento('12.345.678/0001-95') == 'CNPJ'  
    with pytest.raises(ValueError):  
        identificar_documento('123456')  

def test_calcular_dv_cpf():  
    assert calcular_dv_cpf('123456789', range(10, 1, -1)) == 0  # 0 é o DV para o CPF fictício  
    assert calcular_dv_cpf('1234567890', range(11, 2, -1)) == 9  # 9 é o DV para o CPF fictício  

def test_calcular_dv_cnpj():  
    # Use exemplos válidos de CNPJ para os testes  
    assert calcular_dv_cnpj('12345678000195', RANGE_CNPJ_DV_1) == 9  # Exemplo de CNPJ fictício  
    assert calcular_dv_cnpj('12345678000195', RANGE_CNPJ_DV_2) == 5  # Exemplo de CNPJ fictício  

def test_validar_cpf():  
    assert validar_cpf('123.456.789-09')  # CPF fictício válido  
    assert not validar_cpf('123.456.789-00')  # CPF fictício inválido  

def test_validar_cnpj():  
    assert validar_cnpj('12.345.678/0001-95')  # CNPJ fictício válido  
    assert not validar_cnpj('12.345.678/0001-00')  # CNPJ fictício inválido  

def test_formatar_cpf():  
    assert formatar_cpf('12345678909') == '123.456.789-09'  

def test_formatar_cnpj():  
    assert formatar_cnpj('12345678000195') == '12.345.678/0001-95'  

def test_validar_doc():  
    assert validar_doc('123.456.789-09', formatado=True) == '123.456.789-09'
    assert validar_doc('12.345.678/0001-95', formatado=True) == '12.345.678/0001-95' 
    assert validar_doc('12345678909', formatado=True) == '123.456.789-09'
    assert validar_doc('12345678000195', formatado=True) == '12.345.678/0001-95' 
    assert validar_doc('12345678909') == '12345678909'
    assert validar_doc('12345678000195') == '12345678000195' 
    assert validar_doc(12345678909) == '12345678909'
    assert validar_doc(12345678000195) == '12345678000195'
    with pytest.raises(ValueError):  
        validar_doc('123.456.789-00')
    with pytest.raises(ValueError):  
        validar_doc('12.345.678/0001-00') 

# Executar os testes se este arquivo for chamado diretamente  
if __name__ == "__main__":  
    pytest.main()