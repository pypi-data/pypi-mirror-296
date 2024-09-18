from typing import Dict, TypeAlias
from datetime import datetime
from uuid import UUID

JSONData: TypeAlias = Dict[str, str | int | bool | datetime | UUID]
