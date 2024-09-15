from .base.base_model import BaseModel
from .base.parent_model import ParentModel
from pydantic import Field
from typing import List
from enum import Enum
from .item import Item


class HeightEnum(str, Enum):
    compact = "compact"
    xsmall= "xsmall"
    small = "small"
    medium = "medium"
    large = "large"
    xlarge = "xlarge"
    xxlarge = 'xxlarge'


class Row(BaseModel, ParentModel):
    """
    Rows are the horizontal component of the dashboard grid and house 1 to many [Items](./Item/).

    !!! tip
        You can set the height of a row using the `height` attribute on a row
        
        ??? information "Row Height Options in Pixels"

            | Height | Pixels |
            |------------|-------|
            | compact | wrapped |
            | xsmall | 128 |
            | small | 256 |
            | medium | 396 |
            | large | 512 |
            | xlarge | 768 |
            | xxlarge | 1024 |
    """

    def id(self):
        return f"Row - {','.join(list(map(lambda i: i.id(), self.items)))}"

    height: HeightEnum = Field(
        HeightEnum.medium, description="Sets the height of the row."
    )
    items: List[Item] = Field(
        None,
        description="A list of items containing tables, charts or markdown. Items are placed in the row in the order that they are listed from left to right.",
    )

    def child_items(self):
        return self.items
