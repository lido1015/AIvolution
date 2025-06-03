import random

from sim.ecosystem import Ecosystem
from sim.prey import Prey
from sim.predator import Predator


class Simulation:
    """
    Manages the simulation workflow and parameters.
    
    Attributes:
        ecosystem (Ecosystem): The environment
        animals (List[Animal]): All animals in the simulation
        max_steps (int): Maximum number of steps to run
        current_step (int): Current step number
    """
    
    def __init__(self, size: int = 20, height: int = 20, 
                 initial_prey: int = 20, initial_predators: int = 5,
                 max_steps: int = 1000, **params):
        self.ecosystem = Ecosystem(size, **params)
        self.animals = []
        self.max_steps = max_steps
        self.current_step = 0
        
        # Initialize animals
        self._initialize_animals(initial_prey, initial_predators)
        
    def _initialize_animals(self, prey_count: int, predator_count: int):
        """Place initial animals in the ecosystem."""
        # Place prey
        for _ in range(prey_count):
            placed = False
            while not placed:
                r = random.randint(0, self.ecosystem.size - 1)
                c = random.randint(0, self.ecosystem.size - 1)
                cell = self.ecosystem.map[r][c]
                if cell.terrain_type != "rock" and cell.can_add_animal():
                    prey = Prey(cell)
                    cell.add_animal(prey)
                    self.animals.append(prey)
                    placed = True
                    
        # Place predators
        for _ in range(predator_count):
            placed = False
            while not placed:
                r = random.randint(0, self.ecosystem.size - 1)
                c = random.randint(0, self.ecosystem.size - 1)
                cell = self.ecosystem.map[r][c]
                if cell.terrain_type != "rock" and cell.can_add_animal():
                    predator = Predator(cell)
                    cell.add_animal(predator)
                    self.animals.append(predator)
                    placed = True
    
    def next_step(self):
        """Advance the simulation by one step."""
        if self.current_step >= self.max_steps:
            return False
            
        # Phase 1: Gather perceptions and decide actions
        actions = []
        for animal in self.animals:
            if animal.alive:
                perception = animal.see(self.ecosystem.map)
                action = animal.action(perception)
                actions.append((animal, action))
        
        # Phase 2: Execute actions
        new_animals = []
        dead_animals = []
        
        # Execute predator actions first
        for animal, action in actions:
            if isinstance(animal, Predator) and animal.alive:
                alive, offspring = self.ecosystem.transform(animal, action)
                if not alive:
                    dead_animals.append(animal)
                new_animals.extend(offspring)
        
        # Then execute prey actions
        for animal, action in actions:
            if isinstance(animal, Prey) and animal.alive:
                alive, offspring = self.ecosystem.transform(animal, action)
                if not alive:
                    dead_animals.append(animal)
                new_animals.extend(offspring)
        
        # Update animal list
        self.animals = [a for a in self.animals if a.alive and a not in dead_animals]
        self.animals.extend(new_animals)
        
        # Regenerate grass
        self.ecosystem.regenerate_grass()
        
        # Update stats
        self.current_step += 1
        return True
    
    def run(self, steps: int = None):
        """Run the simulation for a given number of steps."""
        steps = steps or self.max_steps
        for _ in range(steps):
            if not self.next_step():
                break
    
    def get_population_counts(self):
        """Return current population counts."""
        prey = sum(1 for a in self.animals if isinstance(a, Prey) and a.alive)
        predators = sum(1 for a in self.animals if isinstance(a, Predator) and a.alive)
        return prey, predators