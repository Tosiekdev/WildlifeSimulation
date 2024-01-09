import random
import numpy as np
import os

current_dir = os.path.dirname(__file__)


def create_map(model_height: int, model_width: int) -> np.ndarray:
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
    ratio_x = model_width / map_vectors.shape[0]
    ratio_y = model_height / map_vectors.shape[1]
    map = np.repeat(np.repeat(map_vectors, ratio_y, axis=0), ratio_x, axis=1)
    return map


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
        np.ndarray: Updated array with 0,1,2,3,4 values only.
    """
    updated_map = map.copy()
    meadow_indexes = np.where(updated_map == 0)
    forest_indexes = np.where(updated_map == 1)
    meadow_size = meadow_indexes[0].size
    forest_size = forest_indexes[0].size
    
    plant_indexes = np.random.choice(meadow_size, size=number_of_plants, replace=False)
    hare_habitat_indexes = np.random.choice(meadow_size, size=number_of_hare_habitats, replace=False)
    fox_habitat_indexes = np.random.choice(forest_size, size=number_of_fox_habitats, replace=False)
    are_fox_habitats_close = True
    while are_fox_habitats_close:
        are_fox_habitats_close = False
        for i in fox_habitat_indexes:
            for j in fox_habitat_indexes[1:]:
                if np.abs(i-j) <= 50:
                    are_fox_habitats_close = True
                    break
        if are_fox_habitats_close:
            fox_habitat_indexes = np.random.choice(forest_size, size=number_of_fox_habitats, replace=False)
            break
    
    are_hares_habitats_close = True
    while not are_hares_habitats_close:
        are_hares_habitats_close = False
        for i in hare_habitat_indexes:
            for j in hare_habitat_indexes[1:]:
                if np.abs(i-j) <= 50:
                    are_hares_habitats_close = True
                    break
        if are_hares_habitats_close:
            hare_habitat_indexes = np.random.choice(forest_size, size=number_of_hare_habitats, replace=False)
            break
    


    updated_map[meadow_indexes[0][hare_habitat_indexes], meadow_indexes[1][hare_habitat_indexes]] = 3
    updated_map[meadow_indexes[0][plant_indexes], meadow_indexes[1][plant_indexes]] = 2
    updated_map[forest_indexes[0][fox_habitat_indexes], forest_indexes[1][fox_habitat_indexes]] = 4

    return updated_map
