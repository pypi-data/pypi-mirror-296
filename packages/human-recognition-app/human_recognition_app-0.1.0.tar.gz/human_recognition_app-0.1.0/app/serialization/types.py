from typing import Annotated

from pydantic import BeforeValidator

ShortFloat = Annotated[float, BeforeValidator(lambda x: round(x, 2))]
