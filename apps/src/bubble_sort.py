import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from apps.src.disassemble import disassemble

def bubble_sort():
    arr = [64, 34, 25, 12, 17, 20, 1, 2, 39, 59, 23]
    n = len(arr)
    i = 0
    while i < n:
        j = 0
        while j < n - i - 1:
            if arr[j] > arr[j + 1]:
                # Swap the elements
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
            j += 1
        i += 1
    return arr

                
if __name__ == "__main__":
    # Test


    print("Array ordenado:", bubble_sort())

    #Taking the bytecode
    print("\nInstruções bytecode da função bubble_sort:")
    disassemble(bubble_sort.__code__)
