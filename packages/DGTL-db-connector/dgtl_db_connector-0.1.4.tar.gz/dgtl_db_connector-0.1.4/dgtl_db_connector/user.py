from datetime import datetime

from .client import Client
from .customer import Customer
from .grader_pool import GraderPool
from .model import Model
from .role import Role


class User(Model):
    table_name = "users"
    primary_key = "username"
    auto_id = False
    client = Client(table_name=table_name, index_name=primary_key)

    def __init__(self, **kwargs):
        super().__init__()
        self.username: str = kwargs.get('username')
        self.role_ids: list = self.convert_json_list(kwargs.get('role_ids'))
        self.customer_ids: list = self.convert_json_list(kwargs.get('customer_ids'))
        self.grader_pool_ids: list = self.convert_json_list(kwargs.get('grader_pool_ids'))

    def customers(self) -> list[Customer]:
        return [Customer.find(customer) for customer in self.customer_ids]

    def roles(self) -> list[Role]:
        return [Role.find(role) for role in self.role_ids]
    
    def grader_pools(self) -> list[GraderPool]:
        return [GraderPool.find(grader_pool) for grader_pool in self.grader_pool_ids]



