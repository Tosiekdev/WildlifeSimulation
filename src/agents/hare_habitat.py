import mesa


class HareHabitat(mesa.Agent):
    """
    Class representing hare habitat area.
    
    """
    def __init__(self, model):
        super().__init__(model.next_id(), model)
