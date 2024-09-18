from datetime import datetime

from .client import Client
from .model import Model


class GraderPool(Model):
    table_name = "grader_pools"
    primary_key = "id"
    auto_id = True
    client = Client(table_name=table_name, index_name=primary_key)

    def __init__(self, **kwargs):
        super().__init__()
        self.id: str = kwargs.get('id')
        self.name: str = kwargs.get('name')
        