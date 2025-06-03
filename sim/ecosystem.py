import random

from sim.base import Environment
from sim.cell import Cell
from sim.animal import Animal
from sim.predator import Predator
from sim.prey import Prey    

# Constants for actions
MOVE = 0
EAT = 1
REPRODUCE = 2

# Directions for movement
DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}


class Ecosystem(Environment):
    """
    Manages the environment grid and animal interactions.
    
    Attributes:
        map (List[List[Cell]]): 2D grid of cells
        size (int): Grid size
        grass_regrowth_rate (float): Amount of grass regrown per step
    """
    
    def __init__(self, size: int, 
                 grass_regrowth_rate: float = 0.1,
                 rock_density: float = 0.2):
        
        self.size = size
        self.grass_regrowth_rate = grass_regrowth_rate
        
        # Initialize grid
        self.map = []
        for _ in range(size):
            row = []
            for _ in range(size):
                # Randomly place rocks
                if random.random() < rock_density:
                    cell = Cell("rock")
                else:
                    cell = Cell("soil", initial_grass=random.uniform(0.5, 1.0))
                cell.map_reference = self.map  # Give cells access to the grid
                row.append(cell)
            self.map.append(row)
    
    def transform(self, animal: Animal, action: tuple[int, tuple]) -> tuple[bool, list]:
        """
        Apply an animal's action to the ecosystem.
        
        Args:
            animal: The animal performing the action
            action: Tuple (action_id, args)
            
        Returns:
            Tuple: (alive_status, new_offspring)
        """
        action, args = action
        

        if action == MOVE:
            direction = args[0]
            animal.move(direction)
            return (animal.alive, [])
            
        elif action == EAT:
            # Predator eating requires a prey argument
            if isinstance(animal, Predator) and len(args) > 0 and isinstance(args[0], Prey):
                energy_gained = animal.eat(args[0])
                return (animal.alive, [])
            else:
                energy_gained = animal.eat()
                return (animal.alive, [])
                
        elif action == REPRODUCE:
            success = animal.reproduce()
            if success:
                # Return the last added occupant as offspring
                return (animal.alive, [animal.position.occupants[-1]])
            return (animal.alive, [])
            
        return (animal.alive, [])
    
    def regenerate_grass(self):
        """
        Regenerate grass in all soil cells.
        """
        for row in self.map:
            for cell in row:
                if cell.terrain_type == "soil":
                    cell.regenerate_grass(self.grass_regrowth_rate)