from typing import Dict, Any, TypeAlias
from datetime import datetime
from uuid import UUID

JSONData: TypeAlias = Dict[
    str, str | int | bool | datetime | UUID
]
