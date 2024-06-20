from typing import Annotated

from fastapi import Form
from pydantic import BaseModel


class SImage(BaseModel):
    filename: Annotated[str, Form()]
    metadata: Annotated[str, Form()]
