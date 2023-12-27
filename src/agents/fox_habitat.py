import mesa


class FoxHabitat(mesa.Agent):
    """
    Class representing fox habitat area.
        
    """
    def __init__(self, model):
        super().__init__(model.next_id(), model)
