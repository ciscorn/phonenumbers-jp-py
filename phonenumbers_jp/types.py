from dataclasses import dataclass, field
from typing import List, Literal, Optional

NumberTypes = Literal[
    "特番",
    "固定",
    "携帯",
    "IP",
    "M2M",
    "国際電話",
    "国外",
    "フリーダイヤル",
    "FMC",
    "ポケベル",
    "災害募金サービス",
    "ナビダイヤル",
]


@dataclass
class NumberAndName:
    number: str
    name: str


@dataclass
class NumberInfo:
    parts: List[str] = field(default_factory=list)
    type: Optional[NumberTypes] = None
    subtype: Optional[str] = None
    message_area: Optional[NumberAndName] = None
    specified_carrier: Optional[NumberAndName] = None
    callerid_delivery: Optional[Literal["withhold", "provide"]] = None
