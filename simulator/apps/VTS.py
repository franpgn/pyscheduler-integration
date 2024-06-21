import dis
def VTS1(palavra1, palavra2):
    # Inicializa dois dicionários para contar a frequência de cada letra
    contagem1 = {}
    contagem2 = {}
    
    # Conta a frequência de cada letra na primeira palavra
    for letra in palavra1:
        if letra in contagem1:
            contagem1[letra] += 1
        else:
            contagem1[letra] = 1
    
    # Conta a frequência de cada letra na segunda palavra
    for letra in palavra2:
        if letra in contagem2:
            contagem2[letra] += 1
        else:
            contagem2[letra] = 1
    
    # Compara os dois dicionários de frequência
    return contagem1 == contagem2

print(list(dis.get_instructions(VTS1)))