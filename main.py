import pathlib
import sys
import uuid
from multiprocessing import Process

import numpy as np

from dataset.combina_dataset import CombinadorDeDataset


def geratriz(combinador):

    for combinado in combinador:

        if not combinado:
            break

        gx = combinado['ancora_eq']['g_p_x']
        gy = combinado['ancora_eq']['g_p_y']

        dirname = f"{combinador.output_path}/gx={gx}/gy={gy}"
        pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
        filename = f"{dirname}/{uuid.uuid4()}"
        print(f"{filename}.npy salvo")

        np.save(filename, [combinado])


def main():

    print("Iniciando")

    if len(sys.argv) < 5:
        print("Modo de usar")
        print("\tcombina-irredutiveis <ancoras> <base> <saida> <amostras>")
        print("\tancoras: caminhos para as âncoras separados por : ")
        print("\tbase: caminho para o diretório que contém todas as amostras")
        print("\tsaida: caminho onde o resultado será salvo")
        print("\tnúmero de amostras para cada ancora")

        return 1

    ancora_paths = sys.argv[1].split(":")
    base_path = sys.argv[2]
    output_path = sys.argv[3]
    total = int(sys.argv[4])

    combinadores = [CombinadorDeDataset(ancora_path, base_path, output_path, total) for ancora_path in ancora_paths]

    for combinador in combinadores:
        p = Process(target=geratriz, args=(combinador,))
        p.start()
    p.join()


if __name__ == '__main__':
    main()
