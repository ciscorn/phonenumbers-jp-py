from dataclasses import dataclass, field
from typing import List, Literal, Optional

NumberTypes = Literal[
    "不明",
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
    type: NumberTypes = "不明"
    subtype: Optional[str] = None
    message_area: Optional[NumberAndName] = None
    selected_carrier: Optional[NumberAndName] = None
    callerid_delivery: Optional[Literal["withhold", "provide"]] = None
