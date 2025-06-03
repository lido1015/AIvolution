import random

from sim.cell import Cell
from sim.animal import Animal
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


class Predator(Animal):
    """
    Predator animal that hunts prey.
    """
    def __init__(self, position: Cell = None):
        super().__init__(position)
        self.attack_cost = 5.0
        self.attack_damage = 25.0
        self.max_energy = 120.0
        self.reproduction_threshold = 90.0
        
    def action(self, perception: dict) -> tuple[int, tuple]:
        """
        Predator-specific decision making.
        
        Priority:
        1. Hunt prey in current cell
        2. Hunt prey in adjacent cells
        3. Eat if energy low
        4. Reproduce if possible
        5. Move randomly
        """
        # Hunt in current cell
        current_cell = perception.get("current_cell")
        if current_cell:
            for occupant in current_cell.get_occupants():
                if isinstance(occupant, Prey) and occupant.alive:
                    return (EAT, (occupant,))
        
        # Hunt in adjacent cells
        prey_dirs = []
        for (dr, dc), neighbor in perception["neighbors"].items():
            if any(isinstance(occ, Prey) for occ in neighbor.get("occupants", [])):
                # Convert vector to direction name
                for dir_name, vector in DIRECTIONS.items():
                    if vector == (dr, dc):
                        prey_dirs.append(dir_name)
                        break
                        
        if prey_dirs:
            return (MOVE, (random.choice(prey_dirs),))
            
        # Eat if energy is low
        if self.energy < self.max_energy * 0.6:
            # Look for prey in neighborhood
            for v, neighbor in perception["neighbors"].items():
                for occupant in neighbor.get("occupants", []):
                    if isinstance(occupant, Prey) and occupant.alive:
                        # Convert vector to direction name
                        for dir_name, vector in DIRECTIONS.items():
                            if vector == v:
                                return (MOVE, (dir_name,))
        
        # Reproduce if possible
        if self.energy >= self.reproduction_threshold and self.position.can_add_animal():
            return (REPRODUCE, ())
            
        # Default: move randomly
        possible_dirs = list(DIRECTIONS.keys())
        return (MOVE, (random.choice(possible_dirs),))
        
    def eat(self, prey: Prey) -> float:
        """
        Predator eats a prey.
        
        Args:
            prey: The prey to eat
            
        Returns:
            Amount of energy gained
        """
        if not self.alive or not prey.alive or self.position != prey.position:
            return 0.0
            
        # Attack prey
        self.energy -= self.attack_cost
        if self.energy <= 0:
            self.alive = False
            return 0.0
            
        # Damage prey
        prey.energy -= self.attack_damage
        if prey.energy <= 0:
            prey.alive = False
            self.position.remove_animal(prey)
            energy_gain = prey.max_energy * self.eat_efficiency
            self.energy = min(self.energy + energy_gain, self.max_energy)
            return energy_gain
            
        return 0.0
