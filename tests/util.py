# -*- coding: utf-8 -*-
# FIXME: Refactor this to `mqttwarn.testing.util`.
from dataclasses import dataclass
from typing import Dict, Union, List

@dataclass
class ProcessorItem:
    """
    A surrogate processor item for feeding into service handlers.
    """

    service: str = None
    target: str = None
    config: Dict = None
    addrs: List[str] = None
    priority: int = None
    topic: str = None
    title: str = None
    message: Union[str, bytes] = None
    data: Dict = None
