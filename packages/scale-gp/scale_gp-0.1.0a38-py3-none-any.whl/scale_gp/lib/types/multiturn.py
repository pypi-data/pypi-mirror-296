from typing import Any, Dict, List, Union, Optional

from src.scale_gp import BaseModel
from src.scale_gp.types.evaluation_datasets import FlexibleMessage


class MultiturnTestCaseSchema(BaseModel):
    messages: FlexibleMessage
    turns: Optional[List[int]]
    expected_messages: Optional[FlexibleMessage]
    other_inputs: Optional[Union[str, float, Dict[str, Any]]] = None
    other_expected: Optional[Union[str, float, Dict[str, Any]]] = None
