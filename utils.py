from scipy.sparse import coo_matrix
from sympy import diff
from sympy.abc import x,y
from sympy.polys import *
import os
import numpy as np
from itertools import cycle


def _poly_para_matriz(pol):
    """
    Transforma um polinômio sympy para uma matriz densa em formato de coordenadas
    :param pol: poliômio sympy
    :return: COOrdinate <numpy.float64>
    """
    graus_coefs = pol.as_poly().as_dict()

    coefs = np.asarray([u.evalf() for u in graus_coefs.values()], dtype=float)
    graus = list(graus_coefs.keys())

    gxs = [u[0] for u in graus]
    gys = [u[1] for u in graus]

    shape = max(gxs) + 1, max(gys) + 1

    matriz = coo_matrix((coefs, (gxs, gys)), shape)
    return matriz / np.sum(coefs)


def mapeia1ODE(a: Poly, p: Poly):
    """
    Cria um dicionário com os polinomios que representam numerador e denominador, e polinômio de Darboux
    :param a: corpo do conservado
    :param p: polinômio de Darboux
    """
    da_dx = diff(a, x)
    da_dy = diff(a, y)

    dp_dx = diff(p, x)
    dp_dy = diff(p, y)

    numerador   = factor(a * dp_dx + da_dx)
    denominador = factor(a * dp_dy + da_dy)

    mdc = gcd(numerador, denominador)

    numerador = (numerador / mdc).ratsimp().expand()
    denominador = (denominador / mdc).ratsimp().expand()

    g_p_x = p.degree(x)
    g_p_y = p.degree(y)

    g_a_x = a.degree(x)
    g_a_y = a.degree(y)

    return dict(num=_poly_para_matriz(numerador),
                den=_poly_para_matriz(denominador),
                p=_poly_para_matriz(p),

                g_p_x=g_p_x,
                g_p_y=g_p_y,

                g_num_x=degree(numerador, x),
                g_num_y=degree(numerador, y),

                g_den_x=degree(denominador, x),
                g_den_y=degree(denominador, y),

                g_a_x=g_a_x,
                g_a_y=g_a_y)


def pre_carrega_caminhos(base_path: str):
    return [{
                'key': filename.split('.', 2)[0],
                'caminho': os.path.join(dirpath, filename)
             }
            for (dirpath, dirs, files) in os.walk(base_path)
            for filename in files]


def gera_irredutives(base_path: str, random=True, ciclico=True):
    """
    Carrega polinômios na pasta em questão
    :param base_path:
    :return:
    """
    arquivos = pre_carrega_caminhos(base_path)

    if random:
        arquivos = np.random.choice(arquivos)

    if ciclico:
        arquivos = cycle(arquivos)

    for arquivo in arquivos:
        resultado = dict()
        resultado['key'] = arquivo['key']
        resultado['pol'] = np.load(arquivo['caminho'])[0]

        yield resultado


def infinitenumbers():
    count = 0
    while True:
        yield count
        count += 1
