from datetime import datetime
from dataclasses import dataclass


@dataclass
class Sale:
    Retailer_code: int
    Product_number: int
    Order_method_code: int
    Date: datetime
    Quantity: int
    Unit_price: float
    Unit_sale_price: float

    def __hash__(self):
        return hash(self.Product_number)
