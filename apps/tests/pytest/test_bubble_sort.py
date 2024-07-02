import sys
import os
import pytest

# Adiciona o diretório do projeto ao caminho do sistema
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

# Importa a função bubble_sort
from apps.src.bubble_sort import bubble_sort

# Funções de teste
def test_bubble_sort_empty():
    arr = []
    bubble_sort(arr)
    assert arr == []

def test_bubble_sort_single_element():
    arr = [1]
    bubble_sort(arr)
    assert arr == [1]

def test_bubble_sort_sorted():
    arr = [1, 2, 3, 4, 5]
    bubble_sort(arr)
    assert arr == [1, 2, 3, 4, 5]

def test_bubble_sort_unsorted():
    arr = [64, 34, 25, 12, 22, 11, 90]
    bubble_sort(arr)
    assert arr == [11, 12, 22, 25, 34, 64, 90]

def test_bubble_sort_duplicates():
    arr = [3, 3, 2, 1, 2]
    bubble_sort(arr)
    assert arr == [1, 2, 2, 3, 3]

def test_bubble_sort_negative_numbers():
    arr = [-2, -5, -45, -1, -34]
    bubble_sort(arr)
    assert arr == [-45, -34, -5, -2, -1]

def test_bubble_sort_mixed_numbers():
    arr = [12, -3, 7, 0, -8, 45, 2]
    bubble_sort(arr)
    assert arr == [-8, -3, 0, 2, 7, 12, 45]

def test_bubble_sort_large_numbers():
    arr = [1000, 20000, 300, 4000, 500, 60000, 7000]
    bubble_sort(arr)
    assert arr == [300, 500, 1000, 4000, 7000, 20000, 60000]

def test_bubble_sort_almost_sorted():
    arr = [1, 2, 3, 5, 4, 6, 7, 8, 9, 10]
    bubble_sort(arr)
    assert arr == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def test_bubble_sort_floats():
    arr = [1.1, 2.2, 0.5, 3.3, 2.1]
    bubble_sort(arr)
    assert arr == [0.5, 1.1, 2.1, 2.2, 3.3]

# Executa os testes se este arquivo for executado diretamente
if __name__ == "__main__":
    pytest.main(["apps/tests/pytest"])
