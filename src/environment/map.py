import random
import numpy as np
import os

current_dir = os.path.dirname(__file__)


def create_map() -> np.ndarray:
    """
    Reponsible for loading a file with map information. Each line in file represents each line
    in 20x20 grid, and each number represents which area is meadow ( for hares ) or forest ( for foxes) 
    It creates numpy array of size 20x20. 0 represents meadow and 1 represents forest.
    
    Returns:
        np.ndarray: Map with 0 and 1:
        - 0 represents meadow 
        - 1 represents forest.
    """
    with open(f"{current_dir}/layout.txt", "r") as f:
        map_vectors = np.zeros((20, 20))
        for x_axis, line in enumerate(f.readlines()):
            forest_areas = line.split(",")
            for y_axis in [int(i) for i in forest_areas]:
                map_vectors[x_axis][y_axis - 1] = 1
    return map_vectors


def add_food_to_map(
    map: np.ndarray, number_of_plants: int, number_of_fox_habitats: int, number_of_hare_habitats: int
) -> np.ndarray:
    """
    Add plants ( food for hares ), fox spawn points and hare spawn points to the map.
    It changes some 0 in array to 3 to create hare habitat, 0 to 2 to create plant
    and 1 to 4 to create fox habitat.

    Args:
        map (np.ndarray): Array of binary values.
        number_of_plants (int): Number of plant.
        number_of_fox_habitats (int): number of fox habitats.
        number_of_hare_habitats (int): Number of hare habitats.

    Returns:
        np.ndarray: Updated array with 0,1,2,3,4 values onlt.
    """
    size_of_forest = np.count_nonzero(map)
    size_of_meadow = (map.shape[0] * map.shape[1]) - size_of_forest
    fox_habitat_indexes = random.choices(range(size_of_forest), k=number_of_fox_habitats)
    hare_habitat_indexes = random.choices(range(size_of_meadow), k=number_of_hare_habitats)
    plant_indexes = random.choices(range(size_of_meadow), k=number_of_plants)
    updated_map = map.copy()
    hare_index = 0
    fox_index = 0
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i][j] == 0:
                if hare_index in hare_habitat_indexes:
                    updated_map[i][j] = 3
                elif hare_index in plant_indexes:
                    updated_map[i][j] = 2
                hare_index += 1
            elif map[i][j] == 1:
                if fox_index in fox_habitat_indexes:
                    updated_map[i][j] = 4
                fox_index += 1
    return updated_map
