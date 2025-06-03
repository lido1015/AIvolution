import random

from sim.animal import Animal, Cell


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


class Prey(Animal):
    """
    Prey animal that eats grass and avoids predators.
    """
    def __init__(self, position: Cell = None):
        super().__init__(position)
        self.eat_amount = 15.0  # Amount of grass to try to eat in one action
        self.max_energy = 80.0
        self.reproduction_threshold = 60.0
        
    def action(self, perception: dict) -> tuple[int, tuple]:
        """
        Prey-specific decision making.
        
        Priority:
        1. Avoid predators
        2. Eat if hungry
        3. Reproduce if possible
        4. Move randomly
        """
        # Check for predators in current cell
        current_cell = perception.get("current_cell")
        if current_cell:
            for occupant in current_cell.get_occupants():
                if occupant.alive:
                    # Try to escape - find safe direction
                    safe_dirs = []
                    for dir_name, (dr, dc) in DIRECTIONS.items():
                        neighbor = perception["neighbors"].get((dr, dc), {})
                        if (neighbor.get("terrain") == "soil" and neighbor["cell"].can_add_animal()):
                            safe_dirs.append(dir_name)
                            
                    if safe_dirs:
                        return (MOVE, (random.choice(safe_dirs),))
        
        # Eat if energy is low
        if self.energy < self.max_energy * 0.7 and current_cell and current_cell.has_grass():
            return (EAT, ())
        
        # Reproduce if possible
        if self.energy >= self.reproduction_threshold and self.position.can_add_animal():
            return (REPRODUCE, ())
            
        # Move to a cell with grass
        grass_dirs = []
        for (dr, dc), neighbor in perception["neighbors"].items():
            if (neighbor["terrain"] == "soil" and 
                neighbor["grass"] > 0.5 and 
                neighbor["cell"].can_add_animal()):
                grass_dirs.append((dr, dc))
                
        if grass_dirs:
            # Convert vector to direction name
            for dir_name, vector in DIRECTIONS.items():
                if vector in grass_dirs:
                    return (MOVE, (dir_name,))
                    
        # Default: move randomly
        possible_dirs = list(DIRECTIONS.keys())
        return (MOVE, (random.choice(possible_dirs),))
        
    def eat(self) -> float:
        """
        Prey eats grass from its current cell.
        
        Returns:
            Amount of energy gained
        """
        if not self.position or not self.position.has_grass():
            return 0.0
            
        consumed = self.position.consume_grass(self.eat_amount)
        energy_gain = consumed * self.eat_efficiency
        self.energy = min(self.energy + energy_gain, self.max_energy)
        return energy_gain