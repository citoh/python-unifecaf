# Leia todos os caracteres de uma string e retorne todos os 
# caracteres que não possuírem par. Por exemplo:
#     aabcc  => b
#     aabbccaafbbbaaacaa  => fc
#     aabbcc => None


def singleChars(text):
    if text == None: 
        return None
    
    if len(text) == 1:
        return text
    
    equals = 0
    singles = []
    for i, char in enumerate(text): 
        if(i + 1 < len(text)):
            if(char == text[i + 1]):
                equals += 1
            else:
                if(equals == 0):
                    singles.append(char)
                equals = 0
        else:
            if(equals == 0):
                    singles.append(char)
    
    if singles:
        return singles
    return None

text = 'aabbccaafbbbaaacaa'
print(singleChars(text))