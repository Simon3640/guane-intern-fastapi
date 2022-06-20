from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

#Se define el modelo perro
class Dog(BaseModel):
    name : str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="The name of the dog",
        example="Lulu"
    )
    picture : Optional[str] = Field(
        description="The picture of the dog",
        example="https://www.google.com/img/logo_lg.png"
    )
    is_adopted : bool = Field(
        ...,
        description="Is the dog adopted?",
        example=True
    )
    user_id : Optional[int] = Field(
        ...,
        description="The id of the user",
        example=1
    )
    created_date : Optional[datetime] = Field(
        description="The date the dog was created",
        example="2020-01-01T00:00:00.000Z"
    )

class responseDog(Dog):
    id : int = Field(
        ...,
        description="The id of the dog",
        example=1
    )