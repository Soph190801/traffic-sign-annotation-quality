from dataclasses import dataclass
from typing import List
from typing import Literal, Dict, Union, TypedDict, Optional

Severity = Literal["error", "warning"]

@dataclass
class ErrorsContext:
    severity: Severity
    message: Optional[str] = None

@dataclass
class TruncationConfig:
    threshold: int # Distance (in px) to consider a box close to the edge
    attributeName: str # Name of the truncation attribute (e.g., "truncation")
    truncationValues: List[str] # Values that indicate an object is truncated

@dataclass
class AttributeConditionConfig:
    labels: List[str] # Labels to apply the rule to
    attributes: Dict[str, Union[str, int, float]] # Expected attribute values
    shouldMatchAttributes: bool = True # If True, will flag if attributes don't match

@dataclass
class MaxSizeConfig:
    maxWidth: Optional[int] = 10**100 # Maximum allowed width
    maxHeight: Optional[int] = 10**100 # Maximum allowed height
