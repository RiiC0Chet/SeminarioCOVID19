# Trabajo realizado por
#  Jose Luis Rico Ramos y Miguel Tirado Guzmán,
# Basado en el trabajo de:
#   Cristina Aranda García-Torres
#   Paula Hernández Lozano

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



#importamos los datos del excel en el que tenemos los datos de chile generados siguiendo distribuciones normales con montecarlo
datos2 = pd.read_excel ('C:/Users/jlric/OneDrive - ugr.es/carrera/Cuarto año/Primer cuatri/ADE/EM/python/tutorial/SeminarioCOVID19/Montecarlo/DatosChile_montecarlo.xlsx', skiprows=5 , names= ['Ptdatos', 'Atdatos', 'RRtdatos', 'Cftdatos', 'Ydtdatos'])
#importamos los datos del excel en el que tenemos los datos de chile reales
datos = pd.read_excel ('C:/Users/jlric/OneDrive - ugr.es/carrera/Cuarto año/Primer cuatri/ADE/EM/python/tutorial/SeminarioCOVID19/Montecarlo/DatosChile.xlsx', skiprows=5 , names= ['Ptdatos', 'Atdatos', 'RRtdatos', 'Cftdatos', 'Ydtdatos'])
#importamos los datos del excel que hemos generado con nuestro código para tener los datos con los que realizar Montecarlo
datos_montecarlo = pd.read_excel ('C:/Users/jlric/OneDrive - ugr.es/carrera/Cuarto año/Primer cuatri/ADE/EM/python/tutorial/SeminarioCOVID19/Montecarlo/Final.xlsx', skiprows=0 , names= ['0', '1', '2', '3', '4', '5','6','7','8','9','real'])
#importamos los datos del excel de la simulación 1
datos_simulacion1 = pd.read_excel ('C:/Users/jlric/OneDrive - ugr.es/carrera/Cuarto año/Primer cuatri/ADE/EM/python/tutorial/SeminarioCOVID19/Montecarlo/Simulacion1.xlsx', skiprows=0 , names= ['0', '1', '2', '3', '4', '5','6','7','8','9','real'])
#importamos los datos del excel de la simulación 1
datos_simulacion2 = pd.read_excel ('C:/Users/jlric/OneDrive - ugr.es/carrera/Cuarto año/Primer cuatri/ADE/EM/python/tutorial/SeminarioCOVID19/Montecarlo/Simulacion2.xlsx', skiprows=0 , names= ['0', '1', '2', '3', '4', '5','6','7','8','9','real'])

#creamos las variables con los datos del excel de Chile
Pt_chile = datos['Ptdatos']
At_chile = datos['Atdatos']
RRt_chile = datos['RRtdatos']
Cft_chile = datos['Cftdatos']
Ydt_chile = datos['Ydtdatos']

#establecemos los valores de las variables que vamos a utilizar durante la ejecución del código
a0 = 1 #a0 > 0
a2 = 1 #a2 > 0
a1 = -0.1 #a1 < 0
a3 = -1 #a3 < 0
alpha = -0.1 #alpha < 0
n = 0.5 #entre 0 y 1
sigma_cuadrado = 1
beta = 1
L = 12
K = 12
gamma = 1
b0 = 1
b1 = 1
b2 = -0.1

# clase que engloba todo el tratamiento de los datos excel incluido los de montecarlo
class Schelling():
    # Este es el método que se ejecuta en la última linea del código
    def __init__(self):
        #calibrado
        self.dibujar()
        print("/nError cuadratico calibrado/n")
        print(self.error_cuadratico())
        #simulacion 1
        self.dibujar_simulacion1()
        print("/nError cuadratico simulación 1/n")
        print(self.error_simulacion1())
        #simulacion2
        self.dibujar_simulacion2()
        self.grafica_burbuja()
        print("/nError cuadratico simulación 2/n")
        print(self.error_simulacion2())

################################################################################### FÓRMULAS SOBRE EL MERCADO DE VIVIENDAS EN CHILE ##############################################
    #metemos en un vector (ft) los valores del valor fundamental de los precios de la vivienda. Teniendo un valor para cada mes
    def Ft(self):
        ft = []
        for mes_actual in range( Pt_chile.size) :
            ft.append(self.calcular_valor_fundamental_precios_vivienda(mes_actual))
        return ft

    #calculamos el valor de la demanda de los consumidores para el mes que le pasemos como parámetro
    #Ecuación 1 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_demanda_consumidores(mes_actual):
        dct1 = a0 + a1 * Pt_chile[mes_actual] + a2 * Ydt_chile[mes_actual] + a3 * RRt_chile[mes_actual]
        return dct1
    
    #calculamos las expectativas de ganancia esperadas de los inversores fundamentalistas para el mes que le pasemos como parámetro
    #Ecuación 3 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_ganancias_esperadas_inversores_fundamentalistas_Rt1(self,mes_actual):
        Et_fundamentalistas_Rt1= alpha * (Pt_chile[mes_actual] - self.calcular_valor_fundamental_precios_vivienda(mes_actual)) #diferencia entre precio de un periodo y su valor fundamental en el presente
        return Et_fundamentalistas_Rt1

    #calculamos la demanda de los inversores fundamentalistas para el mes que le pasemos como parámetro
    #Ecuación 4 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_demanda_inversores_fundamentalistas_t1(self,mes_actual):
        dft1= ((1) / (n * sigma_cuadrado)) * self.calcular_ganancias_esperadas_inversores_fundamentalistas_Rt1(mes_actual)
        return dft1
   
    #Calculamos el valor de g, que es el valor de la tasa de crecimiento de las rentas. Asumimos que es el promedio del crecimiento mensual de los índices de precios de los arriendos
    def  calcular_g(self):
        suma = 0
        for i in range(At_chile.size - 1):
            suma += At_chile[i+1] - At_chile[i]

        g= suma/ (At_chile.size - 1)
        return g

    #Calculamos el valor fundamental de la vivienda en cada periodo
    #Ecuación 6 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_valor_fundamental_precios_vivienda(self,mes_actual):
        Fvt = ((1 + self.calcular_g()) * At_chile[mes_actual] ) / (At_chile[mes_actual] / Pt_chile[mes_actual])
        return Fvt


    #Calculamos el valor de las ganancias esperadas por los inversores psicológicos para el mes actual
    #Ecuación 8 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_ganancias_esperadas_inversores_psicologicos_Rt1(self,mes_actual):
        suma = 0
        for i in range(L) :
            suma += (Pt_chile[mes_actual -i ]-Pt_chile[mes_actual-i -1])
        Et_psicologicos_Rt1= suma * beta
        return Et_psicologicos_Rt1

    #Calculamos el valor de la demanda de los inversores psicológicos para el mes actual
    #Ecuación 9 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_demanda_inversores_psicologicos_t1(self, mes_actual):
        dpt1 = ((1) / (n * sigma_cuadrado)) * self.calcular_ganancias_esperadas_inversores_psicologicos_Rt1(mes_actual)
        return dpt1

    #Calculamos el valor de los errores de predicción de los inversores fundamentalistas para el mes actual
    #Ecuación 13 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_errores_prediccion_fundamentalistas(self,mes_actual):
        eft = 0
        for i in range(K) :
            eft += abs( alpha * (Pt_chile[mes_actual - i] - self.calcular_valor_fundamental_precios_vivienda(mes_actual-i)) - (Pt_chile[mes_actual +1]-Pt_chile[mes_actual]))
        return eft

    #Calculamos el valor de los errores de predicción de los inversores psicológicos para el mes actual
    #Ecuación 14 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_errores_prediccion_psicologicos(self, mes_actual):
        est = 0
        for i in range(K) :
            est += abs(self.calcular_ganancias_esperadas_inversores_psicologicos_Rt1(mes_actual- i+1) - (Pt_chile[mes_actual-i +1]-Pt_chile[mes_actual-i]))
        return est


    #Calculamos el valor de Wt para el mes actual. Siendo Wt el peso relativo que tienen los fundamentalistas en el periodo t.
    #   Tendremos un valor de Wt entre 0 y 1
    #Ecuación 12 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_Wt(self,mes_actual):
        Wt= 1 / (1 + exp(gamma * ((self.calcular_errores_prediccion_fundamentalistas(mes_actual) - self.calcular_errores_prediccion_psicologicos(mes_actual)) / (self.calcular_errores_prediccion_fundamentalistas(mes_actual) + self.calcular_errores_prediccion_psicologicos(mes_actual)))))
        return Wt

    #Calculamos la demanda de los inversores (psicológicos y fundamentalistas) para el mes actual habiendo tenido en cuenta el peso que tienen cada uno (Wt)
    def  calcular_demanda_inversores_t1(self,mes_actual):
        demanda_inversores=self.calcular_Wt(mes_actual) * self.calcular_demanda_inversores_fundamentalistas_t1(mes_actual) + (1 - self.calcular_Wt(mes_actual)) * self.calcular_demanda_inversores_psicologicos_t1(mes_actual)
        return demanda_inversores

    #Calculamos la demanda total de vivienda (compuesta por la demanda de consumidores y la demanda de los inversores) para el mes actual
    #Ecuación 15 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_demanda_t1(self,mes_actual):
        dTt1= self.calcular_demanda_consumidores(mes_actual) + self.calcular_demanda_inversores_t1(mes_actual)
        return dTt1

    #Calculamos el costo promedio de la construcción (sumatoria del costo real de construcción para cada mes entre el número de meses que hay)
    def  calcular_costo_promedio_construccion(self):
        Cf=np.sum(Cft_chile)/Cft_chile.size
        return Cf

    #Calculamos el valor de la oferta de los constructores para el mes actual
    #Ecuación 17 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def  calcular_oferta_constructores(self,mes_actual):
        oferta_t1=b0 + b1 * Pt_chile[mes_actual] + b2 * Cft_chile[mes_actual]
        return oferta_t1

    #Calculamos el ruido blanco, no lo hemos borrado por si en un futuro tuviesemos que cambiar su valor por alguno distinto a 0
    def  calcular_ruido_blanco(self):
        ruido = 0
        return ruido

    #Calculamos el valor del retorno esperado de invertir en un período dado
    #Ecuación 22 del documento "Estudiantes Price Bubbles in a Multi Agent INvestor Sistem"
    def calcular_retorno_esperada_inversion(self,mes_actual):
        Rt1 = (a0 - b0) + (a1 - b1) * Pt_chile[mes_actual] + a2 * Ydt_chile[mes_actual]  + a3 * RRt_chile[mes_actual] + b2 * Cft_chile[mes_actual] + self.calcular_Wt(mes_actual) * (float(alpha) * (Pt_chile[mes_actual] - self.calcular_valor_fundamental_precios_vivienda(mes_actual))) + (1 - self.calcular_Wt(mes_actual))*self.calcular_ganancias_esperadas_inversores_psicologicos_Rt1(mes_actual) + self.calcular_ruido_blanco()
        return Rt1

##################################################################### CALIBRADO ####################################################################
    #Esta función es para realizar el calibrado
    #Esta función nos crea un archivo de excel llamado Rtv.xlsx en el que calculamos Rtv para el calibrado
    def calibrado(self):
        Rt_total = []
        libro = xlsxwriter.Workbook('Rtv.xlsx')
        hoja = libro.add_worksheet()
        
        row = 0
        col = 2
        hoja.write(row,col, 'Rtv_'+str(col))
        row +=1
        for i in range(Pt_chile.size-1):
            Rtv = self.calcular_retorno_esperada_inversion(i)
            Rt_total.append( Rtv )

        for dato in (Rt_total):
            hoja.write(row, col, dato)
            row += 1

        libro.close()

        return Rt_total

    #Esta función nos dibuja las 10 muestras de Montecarlo junto con la muestra real indicando el nombre de los ejes y con una leyenda indicando que color representa cada muestra
    def dibujar(self):
        plt.title('Calibrado con Montecarlo')
        plt.plot(datos_montecarlo['0'],label="Muestra 1")
        plt.plot(datos_montecarlo['1'],label="Muestra 2")
        plt.plot(datos_montecarlo['2'],label="Muestra 3")
        plt.plot(datos_montecarlo['3'],label="Muestra 4")
        plt.plot(datos_montecarlo['4'],label="Muestra 5")
        plt.plot(datos_montecarlo['5'],label="Muestra 6")
        plt.plot(datos_montecarlo['6'],label="Muestra 7")
        plt.plot(datos_montecarlo['7'],label="Muestra 8")
        plt.plot(datos_montecarlo['8'],label="Muestra 9")
        plt.plot(datos_montecarlo['9'],label="Muestra 10")
        plt.plot(datos_montecarlo['real'],linewidth=3.5,label="Muestra real")
        plt.legend(loc='upper left')
        plt.xlabel('Tiempo(meses)')
        plt.ylabel('Retorno esperado inversión')
        plt.show()


    #Esta función calcula el error cuadrático medio de las 10 muestras de Montecarlo en comparación con la muestra real
    def error_cuadratico(self):
        mse=[]
        
        for i in range(10):
            mco = sm.OLS(datos_montecarlo['real'],sm.add_constant(datos_montecarlo[str(i)])).fit()
            mse.append(mco.rsquared)
            """
            mse1 = (np.square(datos_montecarlo[str(i)] - datos_montecarlo['real'])).mean()
            print(mse1)
            mse.append( mse1)
            """
        return mse
########################################################################### SIMULACION 1 #####################################################################################################
    #Repetimos el proceso como en el calibrado pero ahora para la simulación 1
    #Nuestra simulación 1 consiste en igualar Wt a 1. Siendo Wt el peso relativo que tienen los fundamentalistas en el periodo t. 
    #Lo que significaría que no existen inversores psicológicos
    def simulacion1(self, mes_actual):
        Rt1 = (a0 - b0) + (a1 - b1) * Pt_chile[mes_actual] + a2 * Ydt_chile[mes_actual]  + a3 * RRt_chile[mes_actual] + b2 * Cft_chile[mes_actual] + 1 * (float(alpha) * (Pt_chile[mes_actual] - self.calcular_valor_fundamental_precios_vivienda(mes_actual))) + (1 - 1)*self.calcular_ganancias_esperadas_inversores_psicologicos_Rt1(mes_actual) + self.calcular_ruido_blanco()
        return Rt1 

    def bucle_simulacion1(self):
        Rt_total = []
        libro = xlsxwriter.Workbook('Temporal.xlsx')
        hoja = libro.add_worksheet()
        
        row = 0
        col = 8
        hoja.write(row,col, 'Rtv_'+str(col))
        row +=1
        for i in range(Pt_chile.size-1):
            Rtv = self.simulacion1(i)
            Rt_total.append( Rtv )

        for dato in (Rt_total):
            hoja.write(row, col, dato)
            row += 1

        libro.close()

        return Rt_total

    #Dibujamos los resultados de la simulacion 1
    def dibujar_simulacion1(self):
        plt.title('Simulación 1')
        plt.plot(datos_simulacion1['0'],label="Muestra 1")
        plt.plot(datos_simulacion1['1'],label="Muestra 2")
        plt.plot(datos_simulacion1['2'],label="Muestra 3")
        plt.plot(datos_simulacion1['3'],label="Muestra 4")
        plt.plot(datos_simulacion1['4'],label="Muestra 5")
        plt.plot(datos_simulacion1['5'],label="Muestra 6")
        plt.plot(datos_simulacion1['6'],label="Muestra 7")
        plt.plot(datos_simulacion1['7'],label="Muestra 8")
        plt.plot(datos_simulacion1['8'],label="Muestra 9")
        plt.plot(datos_simulacion1['9'],label="Muestra 10")
        plt.plot(datos_simulacion1['real'],linewidth=3.5,label="Muestra real")
        plt.legend(loc='upper left')
        plt.xlabel('Tiempo(meses)')
        plt.ylabel('Retorno esperado inversión')
        plt.show()
    
    #Calculamos el error cuadrático medio de la simulación 1. De cada muestra con respecto a la real
    def error_simulacion1(self):
        mse=[]
        
        for i in range(10):
            mco = sm.OLS(datos_simulacion1['real'],sm.add_constant(datos_simulacion1[str(i)])).fit()
            mse.append(mco.rsquared)
            """
            mse1 = (np.square(datos_montecarlo[str(i)] - datos_montecarlo['real'])).mean()
            print(mse1)
            mse.append( mse1)
            """
        return mse

########################################################################### SIMULACION 2 #####################################################################################################
    # Repetimos el proceso como en el calibrado pero ahora para la simulación 2
    # Calcular el retorno esperado de la inversión para situaciones de burbuja inmobiliaria, es decir, con una diferencia entre el indice de precios y el precio fundamental de la vivienda mayor que 10
    def simulacion2(self,mes_actual,burbuja):
        Rt1 = (a0 - b0) + (a1 - b1) * Pt_chile[mes_actual] + a2 * Ydt_chile[mes_actual]  + a3 * RRt_chile[mes_actual] + b2 * Cft_chile[mes_actual] + self.calcular_Wt(mes_actual) * (float(alpha) * (burbuja)) + (1 - self.calcular_Wt(mes_actual))*self.calcular_ganancias_esperadas_inversores_psicologicos_Rt1(mes_actual) + self.calcular_ruido_blanco()
        return Rt1
        
    # Genera el retorno esperado de la inversion con las condiciones de la simulación 2 para cada muestra
    def bucle_simulacion2(self):
        Rt_total = []
        libro = xlsxwriter.Workbook('Temporal.xlsx')
        hoja = libro.add_worksheet()
        
        row = 0
        col = 9
        hoja.write(row,col, 'Rtv_'+str(col))
        row +=1
        for i in range(Pt_chile.size-1):
            burbuja = randint(10,1000)
            Rtv = self.simulacion2(i,burbuja)
            Rt_total.append( Rtv )

        for dato in (Rt_total):
            hoja.write(row, col, dato)
            row += 1

        libro.close()

        return Rt_total

    # Calculamos el valor aleatori oentre 10 y 1000 que hemos generado para cada mes de la muestra con los datos reales/originales
    def despejar_burbuja(self,mes_actual):
        burbuja = (datos_simulacion2['real'][mes_actual] - (a0 - b0) - (a1 - b1) * Pt_chile[mes_actual] - a2 * Ydt_chile[mes_actual]  - a3 * RRt_chile[mes_actual] - b2 * Cft_chile[mes_actual]  - (1 - self.calcular_Wt(mes_actual))*self.calcular_ganancias_esperadas_inversores_psicologicos_Rt1(mes_actual) - self.calcular_ruido_blanco()) / (self.calcular_Wt(mes_actual) * float(alpha))
        return burbuja

    # Dibujamos una grafica que compare los valores de la burbuja con los del retorno esperado de la inversion para la muestra real. A más burbuja, menos retorno.
    def grafica_burbuja(self):
        burbuja = []
        for i in range(Pt_chile.size-1):
            burbuja.append(self.despejar_burbuja(i))
        plt.plot(datos_simulacion2['real'], label="Muestra real")
        plt.plot(burbuja, label='Burbuja')

        plt.legend(loc='upper left')
        plt.xlabel('Tiempo(meses)')
        plt.ylabel('Retorno esperado inversión/Valor de la burbuja inmobiliaria')
        plt.title('Comparación burbuja con retorno esperado inversión')
        plt.show()
    #Dibujamos los resultados de la simulacion 2
    def dibujar_simulacion2(self):
        plt.title('Simulación 2')
        plt.plot(datos_simulacion2['0'],label="Muestra 1")
        plt.plot(datos_simulacion2['1'],label="Muestra 2")
        plt.plot(datos_simulacion2['2'],label="Muestra 3")
        plt.plot(datos_simulacion2['3'],label="Muestra 4")
        plt.plot(datos_simulacion2['4'],label="Muestra 5")
        plt.plot(datos_simulacion2['5'],label="Muestra 6")
        plt.plot(datos_simulacion2['6'],label="Muestra 7")
        plt.plot(datos_simulacion2['7'],label="Muestra 8")
        plt.plot(datos_simulacion2['8'],label="Muestra 9")
        plt.plot(datos_simulacion2['9'],label="Muestra 10")
        plt.plot(datos_simulacion2['real'],linewidth=3.5,label="Muestra real")
        plt.legend(loc='upper left')
        plt.xlabel('Tiempo(meses)')
        plt.ylabel('Retorno esperado inversión')
        plt.show()
    
    #Calculamos el error cuadrático medio de la simulación 2. De cada muestra con respecto a la real
    def error_simulacion2(self):
        mse=[]
        
        for i in range(10):
            mco = sm.OLS(datos_simulacion2['real'],sm.add_constant(datos_simulacion2[str(i)])).fit()
            mse.append(mco.rsquared)
            """
            mse1 = (np.square(datos_montecarlo[str(i)] - datos_montecarlo['real'])).mean()
            print(mse1)
            mse.append( mse1)
            """
        return mse

    


ejecutar = Schelling()














