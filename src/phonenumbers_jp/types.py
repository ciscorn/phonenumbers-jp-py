from dataclasses import dataclass, field
from typing import List, Literal, Optional

NumberType = Literal[
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
    "テレドーム",
]


@dataclass
class NumberAndName:
    number: str
    name: str


@dataclass
class NumberInfo:
    parts: List[str] = field(default_factory=list)
    type: Optional[NumberType] = None
    subtype: Optional[str] = None
    message_area: Optional[NumberAndName] = None
    specified_carrier: Optional[NumberAndName] = None
    callerid_delivery: Optional[Literal["withhold", "provide"]] = None
