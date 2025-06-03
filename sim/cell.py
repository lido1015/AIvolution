class Cell:
    """
    Represents a single cell in the predator-prey environment grid.

    Attributes:
        terrain_type (str): Either "rock" (infertile) or "soil" (fertile).
        grass_amount (float): Amount of grass currently available (only if terrain_type == "soil").
        occupants (List[Animal]): List of Animal instances occupying this cell (max length = 2).
    """

    def __init__(self, terrain_type: str = "soil", initial_grass: float = 1.0):
        """
        Initialize a Cell.

        Args:
            terrain_type (str): Must be "rock" or "soil".
                - "rock": infertile; grass_amount is always 0.
                - "soil": fertile; grass can grow and be eaten.
            initial_grass (float): Starting grass amount (only used if terrain_type == "soil").
        """
        terrain_type = terrain_type.lower()
        if terrain_type not in {"rock", "soil"}:
            raise ValueError(f"Unsupported terrain_type '{terrain_type}'. Must be 'rock' or 'soil'.")

        self.terrain_type: str = terrain_type
        self.grass_amount: float = initial_grass if terrain_type == "soil" else 0.0
        self.occupants = []

    def is_fertile(self) -> bool:
        """
        Returns:
            bool: True if this cell is fertile ("soil"), False otherwise.
        """
        return self.terrain_type == "soil"

    def has_grass(self) -> bool:
        """
        Returns:
            bool: True if this cell has at least some grass (grass_amount > 0 and terrain_type == "soil"), False otherwise.
        """
        return self.is_fertile() and self.grass_amount > 0.0

    def consume_grass(self, amount: float) -> float:
        """
        A Prey can call this method to eat grass from the cell.

        Args:
            amount (float): Desired amount of grass to consume.

        Returns:
            float: The actual amount of grass consumed (min(self.grass_amount, amount)).
        
        Notes:
            - If terrain_type != "soil" or grass_amount <= 0, returns 0.0.
            - Decreases self.grass_amount by the consumed amount.
        """
        if not self.is_fertile() or self.grass_amount <= 0.0:
            return 0.0

        consumed = min(self.grass_amount, amount)
        self.grass_amount -= consumed
        return consumed

    def regenerate_grass(self, amount: float) -> None:
        """
        Regenerate grass in this cell.

        Args:
            amount (float): Amount of grass to add.
        
        Notes:
            - Only applies if terrain_type == "soil". Otherwise does nothing.
        """
        if self.is_fertile():
            self.grass_amount += amount

    def occupant_count(self) -> int:
        """
        Returns:
            int: Number of Animal instances currently occupying this cell (0, 1, or 2).
        """
        return len(self.occupants)

    def get_occupants(self) -> list:
        """
        Returns:
            List[Animal]: A (shallow) copy of the list of occupants in this cell.
        """
        return list(self.occupants)

    def can_add_animal(self) -> bool:
        """
        Returns:
            bool: True if another Animal can be placed in this cell (max 2 occupants), False otherwise.
        """
        return len(self.occupants) < 2

    def add_animal(self, animal) -> bool:
        """
        Place an Animal into this cell.

        Args:
            animal (Animal): The Animal instance to add.

        Returns:
            bool: True if the animal was successfully added; False if the cell already has 2 occupants.
        
        Side Effects:
            - If successful, assigns animal.position = this cell.
            - Does NOT perform any interaction logic (e.g., Predator eating Prey).
        """
        if not self.can_add_animal():
            return False

        self.occupants.append(animal)
        animal.position = self  # The Animal must have a 'position' attribute referring to this Cell.
        return True

    def remove_animal(self, animal) -> None:
        """
        Remove an Animal from this cell.

        Args:
            animal (Animal): The Animal instance to remove.
        
        Side Effects:
            - If the animal was present, removes it from occupants and sets animal.position = None.
        """
        if animal in self.occupants:
            self.occupants.remove(animal)
            animal.position = None

    def clear_occupants(self) -> None:
        """
        Remove all Animal occupants from this cell.

        Side Effects:
            - Empties the occupants list and sets each occupant's position = None.
        """
        for animal in self.occupants:
            animal.position = None
        self.occupants.clear()

    def __repr__(self) -> str:
        """
        String representation for debugging.

        Example:
            <Cell terrain='soil', grass=0.50, occupants=2>
        """
        return (
            f"<Cell terrain='{self.terrain_type}', "
            f"grass={self.grass_amount:.2f}, "
            f"occupants={len(self.occupants)}>"
        )




# class Cell:
#     """
#     Represents a single cell in the predator-prey environment grid.

#     Attributes:
#         terrain_type (str): Either "rock" (infertile) or "soil" (fertile).
#         grass_amount (float): Amount of grass currently available (only if terrain_type == "soil").
#         occupants (List[Animal]): List of Animal instances occupying this cell (max length = 2).
#     """

#     def __init__(self, terrain_type: str = "soil", initial_grass: float = 1.0):
#         """
#         Initialize a Cell.

#         Args:
#             terrain_type (str): Must be "rock" or "soil".
#                 - "rock": infertile; grass_amount is always 0.
#                 - "soil": fertile; grass can grow and be eaten.
#             initial_grass (float): Starting grass amount (only used if terrain_type == "soil").
#         """
#         terrain_type = terrain_type.lower()
#         if terrain_type not in {"rock", "soil"}:
#             raise ValueError(f"Unsupported terrain_type '{terrain_type}'. Must be 'rock' or 'soil'.")

#         self.terrain_type: str = terrain_type
#         self.grass_amount: float = initial_grass if terrain_type == "soil" else 0.0
#         self.occupants = []

#     def is_fertile(self) -> bool:
#         """
#         Returns:
#             bool: True if this cell is fertile ("soil"), False otherwise.
#         """
#         return self.terrain_type == "soil"

#     def has_grass(self) -> bool:
#         """
#         Returns:
#             bool: True if this cell has at least some grass (grass_amount > 0 and terrain_type == "soil"), False otherwise.
#         """
#         return self.is_fertile() and self.grass_amount > 0.0

#     def consume_grass(self, amount: float) -> float:
#         """
#         A Prey can call this method to eat grass from the cell.

#         Args:
#             amount (float): Desired amount of grass to consume.

#         Returns:
#             float: The actual amount of grass consumed (min(self.grass_amount, amount)).
        
#         Notes:
#             - If terrain_type != "soil" or grass_amount <= 0, returns 0.0.
#             - Decreases self.grass_amount by the consumed amount.
#         """
#         if not self.is_fertile() or self.grass_amount <= 0.0:
#             return 0.0

#         consumed = min(self.grass_amount, amount)
#         self.grass_amount -= consumed
#         return consumed

#     def regenerate_grass(self, amount: float) -> None:
#         """
#         Regenerate grass in this cell.

#         Args:
#             amount (float): Amount of grass to add.
        
#         Notes:
#             - Only applies if terrain_type == "soil". Otherwise does nothing.
#         """
#         if self.is_fertile():
#             self.grass_amount += amount

#     def occupant_count(self) -> int:
#         """
#         Returns:
#             int: Number of Animal instances currently occupying this cell (0, 1, or 2).
#         """
#         return len(self.occupants)

#     def get_occupants(self) -> list:
#         """
#         Returns:
#             List[Animal]: A (shallow) copy of the list of occupants in this cell.
#         """
#         return list(self.occupants)

#     def can_add_animal(self) -> bool:
#         """
#         Returns:
#             bool: True if another Animal can be placed in this cell (max 2 occupants), False otherwise.
#         """
#         return len(self.occupants) < 2

#     def add_animal(self, animal) -> bool:
#         """
#         Place an Animal into this cell.

#         Args:
#             animal (Animal): The Animal instance to add.

#         Returns:
#             bool: True if the animal was successfully added; False if the cell already has 2 occupants.
        
#         Side Effects:
#             - If successful, assigns animal.position = this cell.
#             - Does NOT perform any interaction logic (e.g., Predator eating Prey).
#         """
#         if not self.can_add_animal():
#             return False

#         self.occupants.append(animal)
#         animal.position = self  # The Animal must have a 'position' attribute referring to this Cell.
#         return True

#     def remove_animal(self, animal) -> None:
#         """
#         Remove an Animal from this cell.

#         Args:
#             animal (Animal): The Animal instance to remove.
        
#         Side Effects:
#             - If the animal was present, removes it from occupants and sets animal.position = None.
#         """
#         if animal in self.occupants:
#             self.occupants.remove(animal)
#             animal.position = None

#     def clear_occupants(self) -> None:
#         """
#         Remove all Animal occupants from this cell.

#         Side Effects:
#             - Empties the occupants list and sets each occupant's position = None.
#         """
#         for animal in self.occupants:
#             animal.position = None
#         self.occupants.clear()

#     def __repr__(self) -> str:
#         """
#         String representation for debugging.

#         Example:
#             <Cell terrain='soil', grass=0.50, occupants=2>
#         """
#         return (
#             f"<Cell terrain='{self.terrain_type}', "
#             f"grass={self.grass_amount:.2f}, "
#             f"occupants={len(self.occupants)}>"
#         )