# TRABAJO REALIZADO POR:
#   Jose Luis Rico Ramos
#   Miguel Tirado Guzmán
#
# Basado en el trabajo de:
#   Cristina Aranda García-Torres
#   Paula Hernández Lozano

#ESTE ARCHIVO PUEDE TENER MENOR EXTENSION QUE EL ORIGINAL YA QUE EL CALIBRADO
# LO REALIZAMOS EN EL ARCHIVO montecarlo.py

from montecarlo import Montecarlo

#libreria matemática
import math
from math import exp
# Este módulo provee acceso a algunas variables usadas o mantenidas por el intérprete y a funciones que interactúan fuertemente con el intérprete. Siempre está disponible.
import sys
# El módulo os nos permite acceder a funcionalidades dependientes del Sistema Operativo.
import os
# La biblioteca random contiene una serie de funciones relacionadas con los valores aleatorios. El listado completo de funciones de esta biblioteca se describe en el manual de Python.
import random
from random import randint
# NumPy es un paquete de Python que significa “Numerical Python”, es la librería principal para la informática científica, proporciona potentes estructuras de datos, implementando matrices y matrices multidimensionales.
import numpy as np
# Pandas es una librería de Python especializada en el manejo y análisis de estructuras de datos.
import pandas as pd
# genera gráficos según tus deseos.
import matplotlib.pyplot as plt 
# El módulo xlsxwriter se utiliza principalmente para generar tablas de Excel, insertar datos, insertar iconos y otras operaciones de tabla.
import xlsxwriter
# Este proporciona funciones para la estimación de muchos modelos estadísticos
import statsmodels.api as sm

#importamos los datos del excel de la simulación
datos_simulacion1 = pd.read_excel ('ArchivoSimulacion.xlsx', skiprows=1 , names= ['Contagios Simulacion 1', 'Contagios Simulacion 2', 'Contagios Simulacion 3', 'Contagios Simulacion 4', 'Contagios Simulacion 5', 'Contagios Simulacion 6','Contagios Simulacion 7','Contagios Simulacion 8','Contagios Simulacion 9','Contagios Simulacion 10','Contagios reales'])

# clase que engloba todo el tratamiento de los datos excel incluido los de montecarlo
class Schelling():
    # Este es el método que se ejecuta en la última linea del código
    def __init__(self):
        #simulacion 1
        self.dibujar_simulacion1()

    #Dibujamos los resultados de la simulacion 1
    def dibujar_simulacion1(self):
        plt.title('Simulación 1')
        plt.plot(datos_simulacion1['Contagios Simulacion 1'],label="Simulacion 1")
        plt.plot(datos_simulacion1['Contagios Simulacion 2'],label="Simulacion 2")
        plt.plot(datos_simulacion1['Contagios Simulacion 3'],label="Simulacion 3")
        plt.plot(datos_simulacion1['Contagios Simulacion 4'],label="Simulacion 4")
        plt.plot(datos_simulacion1['Contagios Simulacion 5'],label="Simulacion 5")
        plt.plot(datos_simulacion1['Contagios Simulacion 6'],label="Simulacion 6")
        plt.plot(datos_simulacion1['Contagios Simulacion 7'],label="Simulacion 7")
        plt.plot(datos_simulacion1['Contagios Simulacion 8'],label="Simulacion 8")
        plt.plot(datos_simulacion1['Contagios Simulacion 9'],label="Simulacion 9")
        plt.plot(datos_simulacion1['Contagios Simulacion 10'],label="Simulacion 10")
        plt.plot(datos_simulacion1['Contagios reales'],linewidth=3.5,label="Simulacion real")
        plt.legend(loc='upper left')
        plt.xlabel('Iteracion')
        plt.ylabel('Numero contagios')
        plt.show()
    

ejecutar = Schelling()














