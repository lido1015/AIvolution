class Agent:

    def see(self, environment_state):
        raise NotImplementedError()
    
    def action(self, perception):
        raise NotImplementedError()


class DeductiveAgent(Agent):

    def __init__(self) -> None:
        self.database = []

    def next(self, perception):
        raise NotImplementedError()
    
    def action(self, perception):
        for condition, action in self.database:
            if condition(perception):
                return action(self, perception)
        return None        
    

class ProactiveAgent(Agent):

    def __init__(self) -> None:
        self.beliefs = []

    def beliefs_revision(self, perception):
        raise NotImplementedError()
    
    def generate_options(self):
        raise NotImplementedError()
    
    def filter(self, options):
        raise NotImplementedError()
    
    def action(self, perception):
        self.beliefs = self.beliefs_revision(perception)
        options = self.generate_options()
        return filter(options)