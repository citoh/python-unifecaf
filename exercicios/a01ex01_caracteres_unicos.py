# RESOLVIDO !!
# Leia todos os caracteres de uma string e retorne todos os 
# caracteres únicos. Por exemplo:
#     aabcc  => b
#     aabbccaafbbbaaacaa  => fc
#     aabbcc => None

<<<<<<< Updated upstream

def caractaresUnicos(texto):
    if texto == None: 
        return None
    
    if len(texto) == 1:
        return texto
    
    iguais = 0
    unicos = []
    for i, caracter in enumerate(texto): 
        if(i + 1 < len(texto)):
            if(caracter == texto[i + 1]):
                iguais += 1
            else:
                if(iguais == 0):
                    unicos.append(caracter)
                iguais = 0
        else:
            if(iguais == 0):
                    unicos.append(caracter)
    
    if unicos:
        return unicos
    return None

texto = 'aabbccaafbbbaaacaa'
print(caractaresUnicos(texto))
=======
text = 'aabbccaafbbbaaacaa'
equals = 0
uniqueChars = []
for i, char in enumerate(text):
    if (i + 1 < len(text)):
        if (char == text[i+1]):
            equals += 1
        else:
            if(equals == 0):
                uniqueChars.append(char)
            equals = 0
    else:
        if(equals == 0):
            uniqueChars.append(char)

print(uniqueChars)     
>>>>>>> Stashed changes
