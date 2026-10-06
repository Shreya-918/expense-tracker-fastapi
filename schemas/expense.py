from typing import Annotated
from pydantic import BaseModel, Field, field_validator

class ExpenseRequest(BaseModel):
    title:Annotated[str,Field(...,description="title of expense",min_length=1,max_length=200)]
    amount:Annotated[float,Field(...,description="Amount of the expense")]
    description:Annotated[str,Field(...,description="description of expense",nullable=True)]
    show:Annotated[bool,Field(...,description="Wheather the expense should be shown")]
    
class ExpenseResponse(BaseModel):

    id: Annotated[int,Field(..., description="The ID of the expense")]
    title: Annotated[str,Field(..., description="The title of Expense")]
    amount: Annotated[float,Field(..., description="Amount of the expense")]
    description: Annotated[str,Field(..., description="The description of the expense")]
    show: Annotated[bool,Field(..., description="Whether the expense should be shown")]
    created_at: Annotated[str,Field(..., description="The creation date of the expense")]

    @field_validator("created_at", mode="before")
    @classmethod
    def convert_datetime_to_string(cls, value):
        return value.isoformat() if value else None

    model_config={
        "from_attributes":True
    }

class ExpenseUpdate(BaseModel):
    title: Annotated[str | None, Field( default=None,description="The title of the expense")]
    description: Annotated[str | None, Field(default=None,description="The description of the expense")]
    amount: Annotated[float | None, Field( default=None,description="The amount of the expense")]
