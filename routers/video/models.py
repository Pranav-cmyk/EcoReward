from pydantic import BaseModel
from enum import Enum
from typing import List

class WasteCategory(str, Enum):
    DRY = "Dry Waste"
    WET = "Wet Waste"
    MIXED = "Mixed Waste"

class AnalysisResult(BaseModel):
    validVideo: bool
    category: WasteCategory
    estimatedWeight: str
    points: int
    items: List[str]

