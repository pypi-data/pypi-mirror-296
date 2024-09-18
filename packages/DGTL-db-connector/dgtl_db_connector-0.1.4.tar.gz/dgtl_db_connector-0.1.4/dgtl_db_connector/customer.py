from datetime import datetime

from .client import Client
from .model import Model


class Customer(Model):
    table_name = "customers"
    primary_key = "id"
    auto_id = False
    client = Client(table_name=table_name, index_name=primary_key)

    def __init__(self, **kwargs):
        super().__init__()
        self.id: str = kwargs.get('id')
        self.name: str = kwargs.get('name')
        self.sla_business_days: int = kwargs.get('sla_business_days')
        self.anonymize_after_days: int = kwargs.get('anonymize_after_days')
        self.archive_after_days: int = kwargs.get('archive_after_days')
        self.notification_emails: list = self.convert_json_list(kwargs.get('notification_emails'))
        
