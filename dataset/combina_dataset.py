from utils import gera_irredutives, infinitenumbers
from utils import mapeia1ODE
import numpy as np
import os
from concurrent import futures


class CombinaDataset:
    """
    Classe responsável por converter o dataset inteiro
    para um dado par de graus em contraste
    """

    def __init__(self,  ancora_path: str,
                        contraste_path: str,
                        base_path: str,
                        output_path: str,
                        total='infinity'):

        self.ancoras = gera_irredutives(ancora_path)
        self.positivos = gera_irredutives(ancora_path)
        self.negativos = gera_irredutives(contraste_path)

        self.bases = gera_irredutives(base_path)
        self.output_path = output_path
        self.range = infinitenumbers() if total == 'infinity' else np.arange(0, total)

    def combina(self, _):
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

        return dict(ancora_eq=ancora_matriz,
                    negativo_eq=negativo_matriz,
                    positivo_eq=positivo_matriz,

                    ancora_key=ancora['key'],
                    negativo_key=negativo['key'],
                    positivo_key=positivo['key'],

                    base_key=base['key'])

    def processa(self):
        with futures.ProcessPoolExecutor() as executor:
            for combinado in executor.map(self.combina, range):
                np.save(os.path.join(self.output_path, hash(combinado)), [combinado])




