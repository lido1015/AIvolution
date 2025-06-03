from abc import ABC, abstractmethod


class Environment(ABC):

    @abstractmethod
    def transform(self, action):
        """
        Transform the environment based on the action taken by an agent.

        Args:
            action: The action to be applied to the environment.

        Returns:
            The new state of the environment after the action is applied.
        """
        pass


class Agent(ABC):
    """
    Abstract base class for all agents.

    Methods:
        see(env): Observe the environment and return a perception.
        action(perception): Decide and return an action based on the perception.
    """

    @abstractmethod
    def see(self, env):
        """
        Observe the environment and return a perception.

        Args:
            env: The current state of the environment.

        Returns:
            A perception derived from the environment state.
        """
        pass
    
    @abstractmethod
    def action(self, perception):
        """
        Decide and return an action based on the perception.

        Args:
            perception: The agent's perception of the environment.

        Returns:
            The action to be performed.
        """
        pass





class DeductiveAgent(Agent):
    """
    Agent that selects actions based on a database of condition-action rules.

    Attributes:
        database (list): A list of (condition, action) tuples.

    Methods:
        next(perception): Placeholder for next step logic (not implemented).
        action(perception): Returns the action whose condition matches the perception.
    """

    def __init__(self) -> None:
        """
        Initialize the DeductiveAgent with an empty database.
        """
        self.database = []

    @abstractmethod
    def next(self, perception):
        """
        Placeholder for the next step logic.

        Args:
            perception: The agent's perception of the environment.

        Returns:    
            Update the agent's database.
        """
        pass
    
    def action(self, perception):
        """
        Select and return an action based on the perception.

        Args:
            perception: The agent's perception of the environment.

        Returns:
            The action to be performed, or None if no condition matches.
        """
        for condition, action in self.database:
            if condition(perception):
                return action(self, perception)
        return None
      


class BDIAgent(Agent):
    """
    An agent based on the Belief-Desire-Intention (BDI) architecture.

    The BDI agent maintains three main sets:
        - Beliefs: The agent's information about its environment.
        - Desires: The possible goals or states the agent may wish to achieve.
        - Intentions: The subset of desires the agent is currently committed to achieving.

    The BDI reasoning process involves the following components:
        - Belief Revision Function (beliefs_revision): Updates the agent's beliefs based on new perceptions and current beliefs.
        - Options Generation Function (generate_options): Determines the set of possible desires (options) available to the agent, based on its beliefs and current intentions. This function is responsible for planning and must ensure that generated options are consistent with the agent's beliefs and intentions, and can opportunistically adapt to changes in the environment.
        - Filtering Function (filter): Represents the agent's deliberation process, selecting which desires become intentions, based on current beliefs, desires, and intentions. This function ensures that intentions are valid, beneficial, and consistent, and may add new intentions or remove obsolete ones.
        - Execution Function (execute): Determines which action should be performed based on the intentions.

    The state of a BDI agent is a triple (B, D, I), where:
        - B ⊆ Bel: the current set of beliefs,
        - D ⊆ Des: the current set of desires,
        - I ⊆ Int: the current set of intentions.
    """

    def __init__(self) -> None:

        self.beliefs = {}
        self.desires = {}
        self.intentions = {}

    @abstractmethod
    def beliefs_revision(self, perception):
        """
        Belief Revision Function (brf): Updates the agent's beliefs.

        Given a new perception and the current set of beliefs, this function determines a new set of beliefs.

        Args:
            perception: The agent's perception of the environment.

        Returns:
            list: The updated set of beliefs.
        """
        pass
    
    @abstractmethod
    def generate_options(self):
        """
        Options Generation Function: Generates possible desires (options).

        Based on the current beliefs and intentions, this function determines the set of possible desires (options) available to the agent.
        It is responsible for planning and must ensure that generated options are consistent with the agent's beliefs and intentions, and can opportunistically adapt to changes in the environment.

        Returns:
            list: The set of possible desires.
        """
        pass
    
    @abstractmethod
    def filter(self):
        """
        Filtering Function: Selects intentions from desires.

        Represents the agent's deliberation process, selecting which desires become intentions, based on current beliefs, desires, and intentions.
        Ensures that intentions are valid, beneficial, and consistent, and may add new intentions or remove obsolete ones.

        Returns:
            list: The updated set of intentions.
        """
        pass
    
    @abstractmethod
    def execute(self):
        """
        Execution Function: Executes an action based on intentions.

        Returns:
            Any: The action to be performed.
        """
        pass
    
    def action(self, perception):
        """
        Performs the full BDI reasoning cycle.

        This method executes the following steps:
            1. Revises beliefs based on the new perception.
            2. Generates possible desires (options) based on updated beliefs and current intentions.
            3. Filters desires to update the set of intentions.
            4. Selects and executes an action based on current intentions.

        Args:
            perception: The agent's perception of the environment.

        Returns:
            Any: The action to be performed.
        """
        self.beliefs = self.beliefs_revision(perception)
        self.desires = self.generate_options()
        self.intentions = self.filter()
        return self.execute()