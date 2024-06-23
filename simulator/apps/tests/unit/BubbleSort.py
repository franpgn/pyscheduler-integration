import unittest
import sys
import os

# Adiciona o diretório raiz do projeto ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../")))

from simulator.apps.BubbleSort import bubble_sort

class TestBubbleSort(unittest.TestCase):
    def test_sorted_array(self):
        arr = [1, 2, 3, 4, 5]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_reverse_sorted_array(self):
        arr = [5, 4, 3, 2, 1]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_unsorted_array(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        bubble_sort(arr)
        self.assertEqual(arr, [11, 12, 22, 25, 34, 64, 90])
    
    def test_array_with_duplicates(self):
        arr = [4, 2, 5, 2, 3, 1, 2]
        bubble_sort(arr)
        self.assertEqual(arr, [1, 2, 2, 2, 3, 4, 5])
    
    def test_empty_array(self):
        arr = []
        bubble_sort(arr)
        self.assertEqual(arr, [])

    def test_single_element_array(self):
        arr = [1]
        bubble_sort(arr)
        self.assertEqual(arr, [1])

    def test_large_numbers(self):
        arr = [12345, 67890, 23456, 98765, 34567, 87654]
        bubble_sort(arr)
        self.assertEqual(arr, [12345, 23456, 34567, 67890, 87654, 98765])
    
    def test_negative_numbers(self):
        arr = [-3, -1, -4, -2, 0, -5]
        bubble_sort(arr)
        self.assertEqual(arr, [-5, -4, -3, -2, -1, 0])
    
    def test_mixed_numbers(self):
        arr = [3, -1, 4, -2, 0, -5, 2]
        bubble_sort(arr)
        self.assertEqual(arr, [-5, -2, -1, 0, 2, 3, 4])
    
    def test_large_array(self):
        arr = list(range(1000, 0, -1))
        bubble_sort(arr)
        self.assertEqual(arr, list(range(1, 1001)))

if __name__ == "__main__":
    unittest.main()
