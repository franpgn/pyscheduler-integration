import dis

def bubble_sort(arr):
    n = len(arr)
    # Percorre todos os elementos do array
    for i in range(n):
        # Últimos i elementos já estão no lugar correto
        for j in range(0, n-i-1):
            # Troca se o elemento encontrado for maior do que o próximo
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Exemplo de uso
arr = [64, 34, 25, 12, 17, 20, 1, 2, 39, 59, 23]
bubble_sort(arr)
print("Array ordenado:", arr)

# Descompilando a função bubble_sort para mostrar os bytecodes
print("\nInstruções bytecode da função bubble_sort:")
dis.dis(bubble_sort)

