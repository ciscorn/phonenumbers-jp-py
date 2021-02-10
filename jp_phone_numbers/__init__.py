from dataclasses import dataclass, field
from typing import List, Literal, Optional

from . import _data


@dataclass
class NumberAndName:
    number: str
    name: str


@dataclass
class NumberInfo:
    parts: List[str] = field(default_factory=list)
    type: str = "不明"
    area_code: Optional[str] = None
    message_area: Optional[str] = None
    selected_carrier: Optional[NumberAndName] = None
    callerid_delivery: Optional[Literal["withhold", "provide"]] = None


def parse(number: str):
    res = NumberInfo()
    info = None

    if number.startswith("184"):
        res.callerid_delivery = "withhold"
        res.parts.append("184")
        number = number[3:]
    elif number.startswith("186"):
        res.callerid_delivery = "provide"
        res.parts.append("186")
        number = number[3:]

    if number.startswith("00"):
        pl = 4
        if number.startswith("001"):
            pl = 3
        elif number.startswith("002"):
            pl = 5
        elif number.startswith("0091"):
            pl = 6
        p = number[:pl]
        if p in _data.CARRIER_SELECTORS:
            res.selected_carrier = NumberAndName(p, _data.CARRIER_SELECTORS[p])
            res.parts.append(p)
            number = number[pl:]

    prefix = ""
    for d in range(1, 6 + 1):
        prefix = number[0:d]
        cand = _data.PREFIXES.get(prefix)
        if cand:
            if number.startswith("0") or (len(number) == cand["f"]):
                info = cand
                break

    if info:
        n1 = prefix[: info["f"]]
        if n1:
            res.parts.append(n1)
        n2 = number[len(n1) : len(n1) + info["m"]]
        if n2:
            res.parts.append(n2)
        n3 = number[len(n1) + len(n2) :]
        if n3:
            res.parts.append(n3)

        ma = info.get("a")
        if ma:
            res.area_code = n1
            res.message_area = ma
        res.type = info["t"]

    else:
        if not number.startswith("0"):
            res.type = "国外"
        res.parts.append(number)

    return res
