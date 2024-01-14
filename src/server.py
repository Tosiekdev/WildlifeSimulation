import mesa

from .agents.vaccine_factory import Vaccine
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
            "#0000FF",
            "#0000CC",
            "#000099",
            "#336699",
            "#3399FF",
            "#66B2FF",
            "#99CCFF",
            "#CCE5FF",
            "#66A3FF",
            "#0066CC"
        ]
        portrayal["Color"] = [shades_of_blue[min(9, agent.r-1)]]
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

    elif type(agent) is FoxHabitat:
        portrayal["Shape"] = "src/resources/fox_cave.png"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    
    elif type(agent) is Vaccine:
        portrayal["Shape"] = "src/resources/vaccine.png"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        
    return portrayal

canvas_element = mesa.visualization.CanvasGrid(fox_hare_portrayal, 40, 40, 520, 520)

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
    "initial_number_of_hares_habitats": mesa.visualization.Slider(
            "Initial Number of Hares Habitats", 3, 1, 300
    ),
    "initial_number_of_foxes_habitats": mesa.visualization.Slider(
            "Initial Number of Foxes Habitats", 3, 1, 300
    ),
    "food_amount": mesa.visualization.Slider(
        "Initial Food Amount", 25, 1, 300
    ),
    "food_frequency": mesa.visualization.Slider(
        "Initial Food Frequency", 10, 1, 300
    ),
    "fox_mating_season": mesa.visualization.Slider(
        "Initial Fox Mating Season", 365, 1, 1000
    ),
    "fox_min_mating_range": mesa.visualization.Slider(
        "Initial Fox Min Mating Range", 1, 1, 100
    ),
    "fox_max_mating_range": mesa.visualization.Slider(
        "Initial Fox Max Mating Range", 11, 1, 100
    ),
    "hare_mating_season": mesa.visualization.Slider(
        "Initial Hare Mating Season", 100, 1, 1000
    ),
    "hare_min_mating_range": mesa.visualization.Slider(
        "Initial Hare Min Mating Range", 3, 1, 100
    ),
    "hare_max_mating_range": mesa.visualization.Slider(
        "Initial Hare Max Mating Range", 5, 1, 100
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
    "food_lifetime": mesa.visualization.Slider(
        "Food Lifetime", 350, 100, 1000
    ),
    "fox_lifetime": mesa.visualization.Slider(
        "Fox Lifetime", 160, 100, 300
    ),
    "fox_consumption": mesa.visualization.Slider(
        "Fox Consumption", 5, 1, 20
    ),
    "fox_speed": mesa.visualization.Slider(
        "Fox Speed", 2, 1, 5
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
        "Fox Attack Range", 3, 1, 100
    ),
    "fox_sprint_speed": mesa.visualization.Slider(
        "Fox Sprint Speed", 3, 1, 5
    ),
    "fox_sneak_speed": mesa.visualization.Slider(
        "Fox Sneak Speed", 1, 1, 5
    ),
    "vaccine_amount": mesa.visualization.Slider(
        "Vaccine Amount", 10, 1, 100
    ),
    "vaccine_frequency": mesa.visualization.Slider(
        "Vaccine Frequency", 100, 1, 100
    ),
    "vaccine_lifetime": mesa.visualization.Slider(
        "Vaccine LifeTime", 50, 1, 100
    ),
    "vaccine_effectiveness": mesa.visualization.Slider(
        "Vaccine Effectiveness", 15, 0, 1, 0.01
    ),
}

server = mesa.visualization.ModularServer(
    SimulationModel,
    visualization_elements=[canvas_element],
    name="Fox Hare Predation",
    model_params=model_params,
    port=8521
)
