# TRABAJO REALIZADO POR:
#   Jose Luis Rico Ramos
#   Miguel Tirado Guzmán
#
from mesa import Model
from SeminarioCovid.agents import CovidAgent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import  numpy as np
# imports para la generacion normal de la edad
import scipy.stats as ss
import numpy as np
import random

# Creacion de variables globales 

NO_CONTAGIADO = 0
CEPA_LEVE = 1
CEPA_MEDIA = 2
CEPA_AGRESIVA = 3

LIBRE_MOVIMIENTO = 0
NO_MOVILIDAD = 1
class CovidModel(Model):
    "A model with some number of agents."

    def __init__(self, number_of_agents,porcentaje_libre_movimiento,capacidad_sanidad,contagios_iniciales,cepa_covid, width, height):
        
        # Inicializamos las variables de estado del modelo
        self.num_agents = number_of_agents
        self.porcentaje_libre_movimiento = porcentaje_libre_movimiento/100
        self.capacidad_sanidad = capacidad_sanidad
        self.cepa_covid = cepa_covid
        self.arr_agents = []
        self.running = True
        # Cambiamos a tipo de variable entera en funcion de la cepa para poder operar mejor
        if(cepa_covid == "Cepa leve"):
            self.cepa_covid = CEPA_LEVE
        elif(cepa_covid == "Cepa media"):
            self.cepa_covid = CEPA_MEDIA
        elif(cepa_covid == "Cepa agresiva"):
            self.cepa_covid = CEPA_AGRESIVA
        
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.contagios_iniciales = contagios_iniciales
        self.contagiados = contagios_iniciales
        self.no_contagiados = number_of_agents - contagios_iniciales
        self.n_fallecidos = 0
        # Calculamos la barrera poblacional inicialmente contagiada
        barrera_contagios_inicial = (contagios_iniciales/100)*number_of_agents
        
        media = 0
        nums = 0

        # Cantidad de agentes con libertad de movimiento
        cantidad_agentes_movimiento = round(number_of_agents*self.porcentaje_libre_movimiento)

        # Creamos todos los agentes, a los cuales les vamos a asignar una edad en funcion de una distribucion normal
        # ademas en funcion de la poblacion inicialmente contagiada, comenzaran con covid o no
        for i in range(self.num_agents):
            
            nums = 0
            for j in range(10):
                nums += random.randint(1, 10)
            
            nums -= 10
            media += nums
            
            # Evaluamos en funcion de la generacion si inician contagiados o no
            if(i > barrera_contagios_inicial):
                if(cantidad_agentes_movimiento>0):
                    a = CovidAgent(i, self, tipo_contagio=NO_CONTAGIADO ,edad=nums,cepa_covid=self.cepa_covid, movimiento=LIBRE_MOVIMIENTO)
                    cantidad_agentes_movimiento-=1
                else:
                    a = CovidAgent(i, self, tipo_contagio=NO_CONTAGIADO ,edad=nums,cepa_covid=self.cepa_covid, movimiento=NO_MOVILIDAD)
            else:
                if(cantidad_agentes_movimiento>0):
                    a = CovidAgent(i, self, tipo_contagio=self.cepa_covid ,edad=nums,cepa_covid=self.cepa_covid, movimiento=LIBRE_MOVIMIENTO)
                    cantidad_agentes_movimiento-=1
                else:
                    a = CovidAgent(i, self, tipo_contagio=self.cepa_covid ,edad=nums,cepa_covid=self.cepa_covid, movimiento=NO_MOVILIDAD)
            
            self.arr_agents=np.append(self.arr_agents, a)
            self.schedule.add(a)

            # Añadir el agente en una posicion aleatoria
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                
                if(self.grid.is_cell_empty((x,y)) == True):
                    self.grid.place_agent(a, (x, y) )
                    break
            
            self.datacollector_currents = DataCollector({
            "Healthy Agents": MoneyModel.current_healthy_agents,
            "Non Healthy AGents": MoneyModel.current_non_healthy_agents,
            "Dead AGents": MoneyModel.current_dead_agents,})
    
    def step(self):
        "Avanzamos el modelo en una iteracion."
        self.schedule.step()
        self.datacollector_currents.collect(self)

    #Calculo de la capacidad neta efectiva de la sanidad (La capacidad de acoger a mas enfermos)
    def capacidad_neta(self):
        sum=0
        for i in range(self.num_agents):
            if(self.arr_agents[i].tipo_contagio != NO_CONTAGIADO):
                sum+=1
        capacidad_efectiva = self.capacidad_sanidad/100 - (sum/self.num_agents)
        return capacidad_efectiva
    
    #Funcion para comprobar cuantos agentes sanos hay
    @staticmethod
    def current_healthy_agents(model) -> int:
        return sum([1 for agent in model.schedule.agents if agent.tipo_contagio == 0])
    
    #Funcion para comprobar cuantos agentes enfermos hay
    @staticmethod
    def current_non_healthy_agents(model) -> int:
        return sum([1 for agent in model. schedule. agents if agent.tipo_contagio != 0])

    #Funcion para comprobar cuantos fallecidos hay
    @staticmethod
    def current_dead_agents(model) -> int:
        return model.n_fallecidos