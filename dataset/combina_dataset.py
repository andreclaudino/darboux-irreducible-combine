from utils import gera_irredutives
from utils import mapeia1ODE
import numpy as np


class CombinadorDeDataset:
    """
    Classe responsável por converter o dataset inteiro
    para um dado par de graus em contraste
    """

    def __init__(self,  ancora_path: str,
                        base_path: str,
                        output_path: str,
                        max_count=np.inf):

        self.ancoras = gera_irredutives(ancora_path)
        self.positivos = gera_irredutives(ancora_path)
        self.negativos = gera_irredutives(base_path, ancora_path)

        self.bases = gera_irredutives(base_path)
        self.output_path = output_path
        self.max_count = max_count
        self.count = 0

    def combina(self):
        """
        Coleta um polinômio aleatoriamente de uma das fontes de dados
        :return:
        """
        base = next(self.bases)

        ancora = next(self.ancoras)
        positivo = next(self.positivos)
        negativo = next(self.negativos)

        ancora_matriz = mapeia1ODE(base['pol'], ancora['pol'])
        positivo_matriz = mapeia1ODE(base['pol'], positivo['pol'])
        negativo_matriz = mapeia1ODE(base['pol'], negativo['pol'])

        if ancora['key'] == positivo['key'] or ancora['key'] == negativo['key'] or positivo['key'] == negativo['key']:
            raise Exception("keys são iguais")

        return dict(ancora_eq=ancora_matriz,
                    negativo_eq=negativo_matriz,
                    positivo_eq=positivo_matriz,

                    ancora_key=ancora['key'],
                    negativo_key=negativo['key'],
                    positivo_key=positivo['key'],

                    base_key=base['key'])

    def __iter__(self):
        return self

    def __next__(self):
        while self.count < self.max_count:
            self.count += 1
            return self.combina()




