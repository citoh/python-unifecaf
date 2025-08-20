# RESOLVIDO !!
# Busque no texto principal o valor digitado pelo usuário, 
# ao final retorne True se o valor for encontrado ou False 
# caso contrário. Deve ser analisado caractere por caractere. 
# Exemplo de entrada e saída:
#     Entrada do usuário: brasil
#     Texto: no brasil existem muitos lugares bonitos
#     Retorno experado: True


def buscaTexto(texto, termo):
    idxTermo = 0
    caracteresEncontrados = ''
    for char in texto: 
        if(char == termo[idxTermo]):
            caracteresEncontrados += termo[idxTermo]
            idxTermo += 1
            if(caracteresEncontrados == termo):
                return True
        else:
            idxTermo = 0
            caracteresEncontrados = ''
    return False
        

termo = 'brasil'
texto = 'no brasil existem muitos lugares bonitos'
print(buscaTexto(texto, termo))
