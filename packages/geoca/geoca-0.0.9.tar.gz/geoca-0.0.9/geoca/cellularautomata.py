"""
Description:
The cellularautomata module implements a cellularautomata model for analyzing the distribution of population and other resources within a study area based on grid data.
"""

import random

# Get coordinates of neighbors in eight directions
def get_neighbors(row_now, col_now, data_list, direction_num=4):
    """
    Get neighboring valid coordinates given a row and column index in a 2D data list.

    Args:
        row_now (int): The current row index.
        col_now (int): The current column index.
        data_list (list): A 2D array representing the data converted from raster data.
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.

    Returns:
        list: A list of neighboring valid coordinates.
    """

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if direction_num == 8:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    neighbors = []
    for dr, dc in directions:
        new_row, new_col = row_now + dr, col_now + dc
        if 0 <= new_row < len(data_list) and 0 <= new_col < len(data_list[0]) and data_list[new_row][new_col] is not None:
            neighbors.append((new_row, new_col))
    return neighbors

# Migrate population function
def migrate_population_focus(data_list, population, direction_num=4, proportion=1):
    """
    The population is focused towards the most suitable nearby migration areas based on the raster pixel values.

    Args:
        data_list (list): A 2D array converted from a raster of environmental data.
        population (list): A 2D array converted from the initial population count of each pixel.
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.
        proportion (float): The proportion of population to migrate (default: 1). The proportion ranges from 0 to 1, with a proportion of 1 for complete migration and 0.5 for 50 percent migration.

    Returns:
        list: A 2D list representing the new population distribution after migration.
    """
    new_population = [[0 for _ in range(len(data_list[0]))] for _ in range(len(data_list))]
    
    for row in range(len(data_list)):
        for col in range(len(data_list[0])):
            if not data_list[row][col]:
                continue  # Skip invalid regions
            neighbors = get_neighbors(row, col, data_list, direction_num)
            if not neighbors:
                continue  # Skip if no valid neighbors
            
            max_value = max([data_list[r][c] for r, c in neighbors])
            highest_neighbors = [(r, c) for r, c in neighbors if data_list[r][c] == max_value]

            target_row, target_col = random.choice(highest_neighbors)
            
            if not population[row][col]:
                continue  # Skip invalid regions
            migrated_population = int(population[row][col] * proportion)
            
            new_population[target_row][target_col] += migrated_population
            new_population[row][col] += population[row][col] - migrated_population
    
    return new_population

# Migrate population function
def migrate_population_disperse(data_list, population, direction_num=4, proportion=[0.5, 0.25, 0.15, 0.05]):
    """
    The population is dispersed and migrates to the neighborhood based on the raster pixel values.

    Args:
        data_list (list): A 2D array converted from a raster of environmental data.
        population (list): A 2D array converted from the initial population count of each pixel.
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.
        proportion (list): A list of the proportion of the population that migrated to each neighboring pixel, ordered from highest to lowest suitability for migration. The proportion ranges from 0 to 1, with a proportion of 1 for complete migration and 0.5 for 50 percent migration.

    Returns:
        list: A 2D list representing the new population distribution after migration.
    """
    new_population = [[0 for _ in range(len(data_list[0]))] for _ in range(len(data_list))]
    
    for row in range(len(data_list)):
        for col in range(len(data_list[0])):
            if not data_list[row][col]:
                continue  # Skip invalid regions
            neighbors = get_neighbors(row, col, data_list, direction_num)
            if not neighbors:
                continue  # Skip if no valid neighbors
            
            # Sort neighbors based on the pixel value, in descending order
            sorted_neighbors = sorted(neighbors, key=lambda n: data_list[n[0]][n[1]], reverse=True)

            migrated_population = 0
            if not population[row][col]:
                continue  # Skip invalid regions
            
            # Distribute the population based on the given proportions
            for i in range(min(len(sorted_neighbors), len(proportion)-1)):
                target_row, target_col = sorted_neighbors[i]
                distributed_value = population[row][col] * proportion[i]
                new_population[target_row][target_col] += int(distributed_value)
                # new_population[target_row][target_col] += int(population[row][col] * proportion[i])
                migrated_population += new_population[target_row][target_col]
            
            # Remaining population stays
            if migrated_population < population[row][col]:
                new_population[row][col] += population[row][col] - migrated_population
    
    return new_population

# Migrate time function
def migrate_time(data_list, cost_list):
    """
    Calculate the migration time based on the cost path raster and the environment raster.

    Args:
        data_list (list): A 2D array converted from a raster of environmental data.
        cost_list (list): A 2D array converted from the cost path raster.

    Returns:
        tuple: A tuple containing the cumulative migration time, the number of iterations, and a list of environment raster values corresponding to the cost path raster.
    """
    iteration_count = 0  # Initialize the iteration counter
    migration_time = 0  # Initialize migration time
    positions_data_list = []  # Initialize the list of environment raster values corresponding to cost paths
    
    # In ArcGIS Pro, each least-cost path is assigned a value when encountered in the scanning process.
    # The ending cell on the original source raster of a cost path receives 1, the first path receives 3.

    # Find initial position (cost path raster pixel value = 1)
    initial_positions = []
    for r in range(len(cost_list)):
        for c in range(len(cost_list[0])):
            if cost_list[r][c] == 1:
                initial_positions.append((r, c))
                positions_data_list.append(data_list[r][c])

    if len(initial_positions) != 1:
        # Finds more than one or zero initial positions, exits the loop
        raise RuntimeError("Error: The cost path raster should have and only have one initial position.")
    
    for initial_row, initial_col in initial_positions:
        while True:
            # Get cost path raster coordinates in eight directions around the initial position
            neighbors = get_neighbors(initial_row, initial_col, cost_list, 8)
            # Get the elements in the eight coordinates that have a cost path raster pixel value of 3
            threes = [(r, c) for r, c in neighbors if cost_list[r][c] == 3]

            iteration_count += 1    # Iterative counter accumulation
            
            # If the threes list has only one value, the program runs normally
            if len(threes) == 1:
                # Calculate migration time
                target_row, target_col = threes[0]
                migration_diff = data_list[initial_row][initial_col] - data_list[target_row][target_col]
                migration_time += migration_diff + 30

                # Adding environmental raster values for locations corresponding to cost paths
                positions_data_list.append(data_list[target_row][target_col])
                
                # Update cost path list element values so that computed pixels are not subsequently re-read
                cost_list[target_row][target_col] = 5
                
                # Update initial position
                initial_row, initial_col = target_row, target_col
            if len(threes) == 0:
                # If no element with value 3 is found, exit the loop
                print("Cost path raster traversal is complete.")
                break
            elif len(threes) > 1:
                # Finds more than one element with a value of 3 and exits the loop
                raise RuntimeError("Error: multiple cost path raster values exist around the initial position.")
    
    return migration_time, iteration_count, positions_data_list

def run_iterations_num(iterations, data_list, population_num=10, direction_num=4, type_migration="focus", migration_proportion=1):
    """
    Running a cellular automata using a uniform initial population count to simulate population migration based on a raster of environmental data.

    Args:
        iterations (int): The number of iterations to run the simulation.
        data_list (list): A 2D array converted from a raster of environmental data.
        population_num (int): The initial population count at each pixel (default: 10).
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.
        type_migration (str): The type of migration to use, either "focus" or "disperse" (default: "focus").
        migration_proportion (float or list): The proportion of population to migrate (default: 1). The proportion ranges from 0 to 1, with a proportion of 1 for complete migration and 0.5 for 50 percent migration.

    Returns:
        list: A 2D list representing the population distribution after running the simulation.
    """
    population = [[population_num for _ in range(len(data_list[0]))] for _ in range(len(data_list))]

    for i in range(iterations):
        if type_migration == "focus":
            population = migrate_population_focus(data_list, population, direction_num, migration_proportion)
        elif type_migration == "disperse":
            population = migrate_population_disperse(data_list, population, direction_num, migration_proportion)
        print(f"Iteration {i + 1} is complete.")

    return population

def run_iterations_pop(iterations, data_list, population_list, direction_num=4, type_migration="focus", migration_proportion=1):
    """
    Running a cellular automata using an initial population size raster to simulate population migration based on a raster of environmental data.

    Args:
        iterations (int): The number of iterations to run the simulation.
        data_list (list): A 2D array converted from a raster of environmental data.
        population_list (list): A 2D array converted from an initial population size raster.
        direction_num (int): The number of migration directions (default: 4). Only two values, 4 and 8, are allowed; if any other value is entered, it is recognized as the default 4 direction.
        type_migration (str): The type of migration to use, either "focus" or "disperse" (default: "focus").
        migration_proportion (float or list): The proportion of population to migrate (default: 1). The proportion ranges from 0 to 1, with a proportion of 1 for complete migration and 0.5 for 50 percent migration.

    Returns:
        list: A 2D list representing the population distribution after running the simulation.
    """

    for i in range(iterations):
        if type_migration == "focus":
            population_list = migrate_population_focus(data_list, population_list, direction_num, migration_proportion)
        elif type_migration == "disperse":
            population_list = migrate_population_disperse(data_list, population_list, direction_num, migration_proportion)
        print(f"Iteration {i + 1} is complete.")

    return population_list
