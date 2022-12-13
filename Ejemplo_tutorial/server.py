from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from Ejemplo_tutorial.model import MoneyModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule


NUMBER_OF_CELLS = 20

SIZE_OF_CANVAS_IN_PIXELS_X = 800
SIZE_OF_CANVAS_IN_PIXELS_Y = 800

NO_CONTAGIADO = 0
CEPA_LEVE = 1
CEPA_MEDIA = 2
CEPA_AGRESIVA =3


simulation_params = {
    
    "number_of_agents": UserSettableParameter(
        "slider",
        "Numero de ciudadanos",
        50, #default
        10, #min
        200,#max
        1,  #step
        description="Escoge el numero de agentes a implementar",
    ),
    
    "porcentaje_libre_movimiento": UserSettableParameter(
        "slider",
        "Porcentaje de agentes con libertad de movimiento",
        50, #default
        0,  #min
        100, #max
        1,  #step
        description="Escoge el porcentaje de poblacion que iniciara la simulacion en cuarentena",
    ),
    
    "contagios_iniciales": UserSettableParameter(
        "slider",
        "porcentaje de poblacion inicialmente contagiada",
        50,
        0,
        100,
        1,
        description="Escoge el porcentaje de poblacion que empezara la simulacion contagiada",
    ),
    
    "capacidad_sanidad": UserSettableParameter(
        "slider",
        "Capacidad de atención de sanidad",
        50,
        0,
        100,
        1,
        description="Escoge el límite de poblacion al que puede atender la sanidad",
    ),
    "cepa_covid": UserSettableParameter(
        "choice", 
        "Tipo de cepa", 
        value="1", # default lo ponemos a 1 para poder hacer la conversion a int, el 1 seria de tipo Cepa leve
        choices=["Cepa leve", "Cepa media", "Cepa agresiva"]),
    
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
}


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                "Filled": "true",
                "r": 0.5}
    
    if agent.tipo_contagio == NO_CONTAGIADO:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        
    return portrayal

grid = CanvasGrid(agent_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)

chart = ChartModule([
                    {"Label": "Healthy Agents","Color": "Green"},
                    {"Label": "Non Healthy AGents", "Color": "Red"},
                    {"Label": "Dead AGents", "Color": "Black"}],
                    data_collector_name='datacollector_currents')

server = ModularServer(MoneyModel,
                    [grid, chart],
                    "Money Model",
                    model_params=simulation_params)

server.port = 8521
                    # The default
server.launch()
