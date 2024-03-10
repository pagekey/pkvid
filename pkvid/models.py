# eventually get rid of this module

from pydantic import BaseModel


class CartesianPair(BaseModel):
    x: float
    y: float
