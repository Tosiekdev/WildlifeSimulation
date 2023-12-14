from typing import Any

import mesa


class SimulationModel(mesa.Model):
    """Application base model"""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
