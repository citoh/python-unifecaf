import sys

output = "ALOCAÇÃO BASE EM BYTES ---------------------------------\n"

types = {
    "int": 0,
    "float": 0.0,
    "bool": True,
    "str": "",
    "list": [],
    "tuple": (),
    "dict": {},
    "set": set(),
    "NoneType": None,
}

for name, value in types.items():
    output += f"{name:<8} ->  {sys.getsizeof(value)} bytes\n"

output += "\n"
output += "TESTE A SUA VARIÁVEL -----------------------------------\n"

x = 1
output += f"Valor: {x}\n"
output += f"Tipo: {type(x).__name__}\n"
output += f"Bytes usados: {sys.getsizeof(x)}\n"
output += "\n"

# Imprime na tela o que temos na memória RAM (variável output)
print(output)

# Salvando em arquivo o que temos na memória RAM (variável output)
with open("a1_variaveis/a1_variaveis_dados.txt", "w", encoding="utf-8") as file:
    file.write(output)