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


def add_food_to_map(map, number_of_plants, number_of_hare_habitats, number_of_fox_habitats):
    """
    Places plants, hare habitats and fox habitats on the map.

    Args:
        map (np.ndarray): Map to place habitats on.
        number_of_plants (int): Number of plants to place.
        number_of_hare_habitats (int): Number of hare habitats to place.
        number_of_fox_habitats (int): Number of fox habitats to place.

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
        fox_habitat_positions = forest_indexes[0][fox_habitat_indexes], forest_indexes[1][fox_habitat_indexes]
        for i in range(len(fox_habitat_positions[0])):
            for j in range(i + 1, len(fox_habitat_positions[0])):
                if np.sqrt((fox_habitat_positions[0][i] - fox_habitat_positions[0][j]) ** 2 +
                           (fox_habitat_positions[1][i] - fox_habitat_positions[1][j]) ** 2) <= 20:
                    are_fox_habitats_close = True
                    break
        if are_fox_habitats_close:
            fox_habitat_indexes = np.random.choice(forest_size, size=number_of_fox_habitats, replace=False)

    are_hares_habitats_close = True
    while are_hares_habitats_close:
        are_hares_habitats_close = False
        hare_habitat_positions = meadow_indexes[0][hare_habitat_indexes], meadow_indexes[1][hare_habitat_indexes]
        for i in range(len(hare_habitat_positions[0])):
            for j in range(i + 1, len(hare_habitat_positions[0])):
                if np.sqrt((hare_habitat_positions[0][i] - hare_habitat_positions[0][j]) ** 2 +
                           (hare_habitat_positions[1][i] - hare_habitat_positions[1][j]) ** 2) <= 5:
                    are_hares_habitats_close = True
                    break
        if are_hares_habitats_close:
            hare_habitat_indexes = np.random.choice(meadow_size, size=number_of_hare_habitats, replace=False)
    


    updated_map[meadow_indexes[0][plant_indexes], meadow_indexes[1][plant_indexes]] = 2
    updated_map[meadow_indexes[0][hare_habitat_indexes], meadow_indexes[1][hare_habitat_indexes]] = 3
    updated_map[forest_indexes[0][fox_habitat_indexes], forest_indexes[1][fox_habitat_indexes]] = 4

    return updated_map
