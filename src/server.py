import mesa
from .agents import *
from .model import SimulationModel

def fox_hare_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Hare:
        portrayal["Shape"] = 'src/resources/hare.png'
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Fox:
        portrayal["Shape"] = 'src/resources/fox.png'
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Pheromone:
        value = max(0, min(1, agent.value))
        shades_of_yellow = [
            "#FFFF99",  # Light Yellow
            "#FFFF66",  # Pale Yellow
            "#FFFF00",  # Lemon Yellow
            "#FFD700",  # Canary Yellow / Gold Yellow
            "#FFFF00",  # Yellow
            "#FFD700",  # Gold Yellow / Canary Yellow
            "#DAA520",  # Goldenrod
            "#F4C430",  # Saffron Yellow
            "#FFBF00",  # Amber Yellow
            "#FFA500"   # Dark Yellow
        ]
        index = int(value * (len(shades_of_yellow) - 1))

        portrayal["Color"] = [shades_of_yellow[index]]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Sound:
        shades_of_blue = [
            "#063DFF",
            "#3763FF",
            "#6889FF",
            "#99AFFF",
            "#E2E8FE"
        ]
        portrayal["Color"] = [shades_of_blue[agent.r - 1]]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

canvas_element = mesa.visualization.CanvasGrid(fox_hare_portrayal, 20, 20, 500, 500)

model_params = {}

server = mesa.visualization.ModularServer(
    SimulationModel,
    visualization_elements=[canvas_element],
    name="Fox Hare Predation",
    model_params=model_params,
    port=8521
)
