def validar_campos_obrigatorios(campos):
    return all(campos)

def validar_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False