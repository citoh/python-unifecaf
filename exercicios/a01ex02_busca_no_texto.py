# Busque no texto principal o valor digitado pelo usuário, 
# ao final retorne True se o valor for encontrado ou False 
# caso contrário. Deve ser analisado caractere por caractere. 
# Exemplo de entrada e saída:
#     Entrada do usuário: brasil
#     Texto: no brasil existem muitos lugares bonitos
#     Retorno experado: True


def searchText(text, search):
    idxSearch = 0
    foundChars = ''
    for char in text: 
        if(char == search[idxSearch]):
            foundChars += search[idxSearch]
            idxSearch += 1
            if(foundChars == search):
                return True
        else:
            idxSearch = 0
            foundChars = ''
    return False
        

search = 'brasil'
text = 'no brasil existem muitos lugares bonitos'
print(searchText(text, search))
