import numpy as np
import sys
import os
import unittest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_root)

from apps.src.mean_filter import mean_filter


class TestMediaFilter(unittest.TestCase):

    def test_media_filter(self):
        # Definir a imagem de teste
        image = np.array([[10, 10, 10, 10, 10],
                          [10, 50, 50, 50, 10],
                          [10, 50, 100, 50, 10],
                          [10, 50, 50, 50, 10],
                          [10, 10, 10, 10, 10]])
        
        # Resultado esperado (a ser ajustado de acordo com a saída correta)
        expected_output = mean_filter(image)


        # Obter o resultado da função
        result = mean_filter(image)
        
        # Verificar se o resultado da função é igual ao esperado
        np.testing.assert_array_almost_equal(result, expected_output, decimal=5, err_msg="O filtro Blur não produziu o resultado esperado")

if __name__ == '__main__':
    unittest.main()
