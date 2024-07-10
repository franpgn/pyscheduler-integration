import sys
import os
from apps.src.disassemble import disassemble

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


def bubble_sort(arr):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                
if __name__ == "__main__":
    # Test
    arr = [64, 34, 25, 12, 17, 20, 1, 2, 39, 59, 23]
    bubble_sort(arr)
    print("Array ordenado:", arr)

    #Taking the bytecode
    print("\nInstruções bytecode da função bubble_sort:")
    disassemble(bubble_sort)
