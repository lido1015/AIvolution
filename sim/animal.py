from abc import ABC, abstractmethod
from dataclasses import dataclass
import random


from sim.base import BDIAgent
from sim.cell import Cell


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


class Animal:
    """
    Base class for all animals in the ecosystem. Implements basic BDI architecture.
    
    Attributes:
        position (Cell): The current cell the animal occupies
        alive (bool): Whether the animal is alive
        energy (float): Current energy level
        max_energy (float): Maximum energy capacity
        move_cost (float): Energy cost for moving
        eat_efficiency (float): Efficiency in consuming food
        reproduction_threshold (float): Energy level required for reproduction
        reproduction_cost (float): Energy cost for reproduction
    """
    
    def __init__(self, position: Cell = None):
        self.position = position
        self.alive = True
        self.energy = 50.0
        self.max_energy = 100.0
        self.move_cost = 2.0
        self.eat_efficiency = 0.7
        self.reproduction_threshold = 80.0
        self.reproduction_cost = 40.0
        
    def see(self, grid: list[list[Cell]]) -> dict:
        """
        Generate perception of the environment based on the agent's position.
        
        Args:
            grid: The ecosystem grid
            
        Returns:
            Dictionary containing perceived information about the environment
        """
        if not self.position or not self.alive:
            return {}
        
        # Find current position in grid
        current_row, current_col = None, None
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell is self.position:
                    current_row, current_col = r, c
                    break
            if current_row is not None:
                break
                
        if current_row is None:
            return {}
        
        # Perceive immediate neighborhood (3x3 area centered on current cell)
        perception = {
            "current_cell": self.position,
            "neighbors": {},
            "self_energy": self.energy
        }
        
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                r, c = current_row + dr, current_col + dc
                if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                    neighbor = grid[r][c]
                    perception["neighbors"][(dr, dc)] = {
                        "cell": neighbor,
                        "terrain": neighbor.terrain_type,
                        "grass": neighbor.grass_amount if neighbor.is_fertile() else 0.0,
                        "occupants": neighbor.get_occupants()
                    }
                    
        return perception
    
    def action(self, perception: dict) -> tuple[int, tuple]:
        """
        Base action decision method. To be overridden by subclasses.
        
        Args:
            perception: Dictionary containing environmental information
            
        Returns:
            Tuple: (action_id, arguments)
        """
        # Default behavior: move randomly if possible
        possible_dirs = list(DIRECTIONS.keys())
        return (MOVE, (random.choice(possible_dirs),))
    
    def move(self, direction: str) -> bool:
        """
        Attempt to move in the specified direction.
        
        Args:
            direction: Direction to move ('UP', 'DOWN', 'LEFT', 'RIGHT')
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self.alive or self.energy < self.move_cost:
            return False
            
        if self.position is None:
            return False
            
        # Find current position in ecosystem grid
        current_row, current_col = None, None
        for r, row in enumerate(self.position.map_reference):
            for c, cell in enumerate(row):
                if cell is self.position:
                    current_row, current_col = r, c
                    break
            if current_row is not None:
                break
                
        if current_row is None:
            return False
            
        # Calculate new position
        dx, dy = DIRECTIONS[direction]
        new_row, new_col = current_row + dx, current_col + dy
        
        # Check if new position is valid
        if (0 <= new_row < len(self.position.map_reference) and 
            0 <= new_col < len(self.position.map_reference[0])):
            
            new_cell = self.position.map_reference[new_row][new_col]
            
            # Can only move to soil cells that aren't full
            if new_cell.terrain_type == "rock" or not new_cell.can_add_animal():
                return False
                
            # Move to new cell
            self.position.remove_animal(self)
            new_cell.add_animal(self)
            self.energy -= self.move_cost
            return True
            
        return False
        
    def eat(self) -> float:
        """
        Attempt to eat. Returns amount of energy gained.
        
        Returns:
            Amount of energy gained from eating
        """
        # Base method - to be overridden by subclasses
        return 0.0
        
    def reproduce(self) -> bool:
        """
        Attempt to reproduce. Returns True if successful.
        
        Returns:
            True if reproduction was successful, False otherwise
        """
        if (not self.alive or 
            self.energy < self.reproduction_threshold or 
            self.position is None or 
            not self.position.can_add_animal()):
            return False
            
        # Create offspring
        offspring = self.__class__(self.position)
        offspring.energy = self.energy / 2
        self.energy -= self.reproduction_cost
        
        # Add offspring to current cell
        return self.position.add_animal(offspring)
    
    def step(self, perception: dict) -> tuple[bool, list]:
        """
        Execute one step of the animal's lifecycle.
        
        Args:
            perception: Environmental perception
            
        Returns:
            Tuple: (alive_status, new_offspring)
        """
        action_id, args = self.action(perception)
        new_offspring = []
        
        if not self.alive:
            return (False, [])
            
        # Handle energy depletion
        if self.energy <= 0:
            self.alive = False
            if self.position:
                self.position.remove_animal(self)
            return (False, [])
            
        # Execute action
        if action_id == MOVE:
            self.move(*args)
        elif action_id == EAT:
            self.eat()
        elif action_id == REPRODUCE:
            if self.reproduce():
                # Offspring added to cell, but we need to return it for tracking
                new_offspring = [self.position.occupants[-1]]
                
        return (self.alive, new_offspring)




# @dataclass
# class Perception:
#     """"""
#     position: tuple[int, int]
#     close_plants: list[tuple[int, int]]
#     close_preys: list[tuple[int, int]]
#     close_predators: list[tuple[int, int]]    

# @dataclass
# class Genotype:
#     speed: int
#     size: int
#     strength: int
#     vision: int
#     reproduction_rate: float


# # Desires
# HUNGER = 1
# LIBIDO = 2


# # Intentions




# class Animal(ABC, BDIAgent):

        

#     def __init__(self, genotype: Genotype):
#         super().__init__()

#         self.speed = genotype.speed
#         self.size = genotype.size
#         self.strength = genotype.strength   
#         self.vision = genotype.vision
#         self.reproduction_rate = genotype.reproduction_rate

#         self.energy = 100

#         self.intentions = {

#         }


#     def see(self, env) -> Perception:

#         position = env.get_agent_position(self)
#         close_plants = env.get_close_plants(position, self.genotype.vision)
#         close_preys = env.get_close_preys(position, self.genotype.vision)
#         close_predators = env.get_close_predators(position, self.genotype.vision)

#         return Perception(
#             position=position,
#             close_plants=close_plants,
#             close_preys=close_preys,
#             close_predators=close_predators
#         )
        


