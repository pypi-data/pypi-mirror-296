import boto3

from .client import Client
from .customer import Customer
from .model import EncryptedString, Model


class GraderPool(Model):
    table_name = "grader_pools"
    primary_key = "id"
    auto_id = True
    client = Client(table_name=table_name, index_name=primary_key)

    def __init__(self, **kwargs):
        super().__init__()
        self.id: str = kwargs.get('id')
        self.name: str = kwargs.get('name')
        self.customer_id: str = kwargs.get('customer_id')
        self.price: int|None = kwargs.get('price')
        self.sla_business_days: int|None = kwargs.get('sla_business_days')
        self.cardiologs_key: EncryptedString|None = EncryptedString(encrypted_value=kwargs.get('cardiologs_key')) if kwargs.get('cardiologs_key') else None
            

    def customer(self) -> Customer:
        return Customer.find(self.customer_id)

    def get_cardiologs_key(self) -> str:
        if self.cardiologs_key:
            return self.cardiologs_key.decrypted_value
        else:
            return self.__get_cardiologs_key_from_ssm()
        
    def __get_cardiologs_key_from_ssm(self):
        ssm_client = boto3.client('ssm')
        parameter_name = '/cardiologs/DGTL_Health_api_key'
        return ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)['Parameter']['Value']
\

