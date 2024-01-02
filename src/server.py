import mesa
from .agents import *
from .model import SimulationModel
from .agents.fox_habitat import FoxHabitat
from .agents.hare_habitat import HareHabitat
from .agents.hare_food import HareFood

def fox_hare_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Hare:
        portrayal["Shape"] = 'src/resources/hare.png'
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Fox:
        portrayal["Shape"] = 'src/resources/fox.png'
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
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
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is HareFood and not agent.eaten:
        portrayal["Shape"] = "src/resources/plant.png"
        portrayal["scale"] = 0.9
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

    elif type(agent) is HareHabitat:
        portrayal["Shape"] = "src/resources/rabbit_hole.png"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = "purple"

    elif type(agent) is FoxHabitat:
        portrayal["Shape"] = "src/resources/fox_cave.png"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = "blue"
    
    return portrayal

canvas_element = mesa.visualization.CanvasGrid(fox_hare_portrayal, 20, 20, 500, 500)

model_params = {
    "title": mesa.visualization.StaticText("Parameters:"),
    "one_week": mesa.visualization.Slider(
        "One Week", 70, 1, 1000
    ),
    "initial_plant": mesa.visualization.Slider(
        "Initial Plant", 60, 1, 300
    ),
    "initial_fox": mesa.visualization.Slider(
        "Initial Fox Population", 1, 1, 300
    ),
    "initial_hare": mesa.visualization.Slider(
        "Initial Hare Population", 1, 1, 300
    ),
    "hare_lifetime": mesa.visualization.Slider(
        "Hare Lifetime", 200, 100, 300
    ),
    "hare_consumption": mesa.visualization.Slider(
        "Hare Consumption", 5, 1, 20
    ),
    "hare_speed": mesa.visualization.Slider(
        "Hare Speed", 2, 1, 5
    ),
    "hare_trace": mesa.visualization.Slider(
        "Hare Trace", 1, 0, 1, 0.01
    ),
    "hare_view_range": mesa.visualization.Slider(
        "Hare View Range", 5, 1, 100
    ),
    "hare_view_angle": mesa.visualization.Slider(
        "Hare View Angle", 350, 1, 360
    ),
    "hare_hearing_range": mesa.visualization.Slider(
        "Hare Hearing Range", 20, 1, 100
    ),
    "hare_sprint_speed": mesa.visualization.Slider(
        "Hare Sprint Speed", 4, 1, 5
    ),
    "hare_sprint_duration": mesa.visualization.Slider(
        "Hare Sprint Duration", 10, 1, 100
    ),
    "hare_sprint_cool_down": mesa.visualization.Slider(
        "Hare Sprint Cool Down", 20, 1, 100
    ),
    "hare_sprint_distance": mesa.visualization.Slider(
        "Hare Sprint Distance", 4, 1, 100
    ),
    "hare_no_movement_distance": mesa.visualization.Slider(
        "Hare No Movement Distance", 8, 1, 100
    ),
    "hare_no_movement_duration": mesa.visualization.Slider(
        "Hare No Movement Duration", 10, 1, 100
    ),
    "pheromone_evaporation_rate": mesa.visualization.Slider(
        "Pheromone Evaporation Rate", 0.4, 0, 1, 0.01
    ),
    "pheromone_diffusion_rate": mesa.visualization.Slider(
        "Pheromone Diffusion Rate", 0.1, 0, 1, 0.01
    ),
    "fox_lifetime": mesa.visualization.Slider(
        "Fox Lifetime", 160, 100, 300
    ),
    "fox_consumption": mesa.visualization.Slider(
        "Fox Consumption", 5, 1, 20
    ),
    "fox_speed": mesa.visualization.Slider(
        "Fox Speed", 6, 1, 5
    ),
    "fox_trace": mesa.visualization.Slider(
        "Fox Trace", 5, 0, 10, 1
    ),
    "fox_view_range": mesa.visualization.Slider(
        "Fox View Range", 6, 1, 100
    ),
    "fox_view_angle": mesa.visualization.Slider(
        "Fox View Angle", 135, 1, 360
    ),
    "fox_smelling_range": mesa.visualization.Slider(
        "Fox Smelling Range", 10, 1, 100
    ),
    "fox_attack_range": mesa.visualization.Slider(
        "Fox View Range", 3, 1, 100
    ),
}

server = mesa.visualization.ModularServer(
    SimulationModel,
    visualization_elements=[canvas_element],
    name="Fox Hare Predation",
    model_params=model_params,
    port=8521
)
