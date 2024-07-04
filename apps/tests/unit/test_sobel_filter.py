import unittest
import numpy as np

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from apps.src.sobel_filter import sobel_filter


class TestSobelFilter(unittest.TestCase):

    def test_sobel_filter(self):
        # Definir a imagem de teste
        image = np.array([[10, 10, 10, 10, 10],
                          [10, 50, 50, 50, 10],
                          [10, 50, 100, 50, 10],
                          [10, 50, 50, 50, 10],
                          [10, 10, 10, 10, 10]])

        # Resultado esperado (a ser ajustado de acordo com a saída correta)
        expected_output = sobel_filter(image)

        # Obter o resultado da função
        result = sobel_filter(image)

        # Verificar se o resultado da função é igual ao esperado
        np.testing.assert_array_almost_equal(result, expected_output, decimal=5, err_msg="O filtro Sobel não produziu o resultado esperado")


if __name__ == '__main__':
    unittest.main()

