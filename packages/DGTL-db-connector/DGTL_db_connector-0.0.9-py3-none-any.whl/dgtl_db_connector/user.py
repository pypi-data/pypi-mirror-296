from datetime import datetime

from .client import Client
from .customer import Customer
from .model import Model
from .role import Role


class User(Model):
    table_name = "users"
    primary_key = "email"
    auto_id = False
    client = Client(table_name=table_name, index_name=primary_key)

    def __init__(self, **kwargs):
        super().__init__()
        self.email: str = kwargs.get('email')
        self.role_ids: list = self.convert_json(kwargs.get('role_ids'))
        self.customer_ids: list = self.convert_json(kwargs.get('customer_ids'))
        self.grader_pool_ids: list = self.convert_json(kwargs.get('grader_pool_ids'))

    def customers(self) -> list[Customer]:
        return [Customer(uuid=customer) for customer in self.customer_ids]

    def roles(self) -> list[Role]:
        return [Role(uuid=role) for role in self.role_ids]



