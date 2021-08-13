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


def parse(number: str) -> NumberInfo:
    res = NumberInfo()
    info = None

    # 非通知
    if number.startswith("184"):
        res.callerid_delivery = "withhold"
        res.parts.append("184")
        number = number[3:]
    # 通知
    elif number.startswith("186"):
        res.callerid_delivery = "provide"
        res.parts.append("186")
        number = number[3:]

    # 事業者指定番号
    if number.startswith("00"):
        prefix_len = 4
        if number.startswith("001"):
            prefix_len = 3
        elif number.startswith("002"):
            prefix_len = 5
        elif number.startswith("0091"):
            prefix_len = 6
        p = number[:prefix_len]
        if p in _data.CARRIER_SELECTORS:
            res.selected_carrier = NumberAndName(p, _data.CARRIER_SELECTORS[p])
            res.parts.append(p)
            number = number[prefix_len:]

    # 特番
    if number in _data.SPECIALS:
        sp = _data.SPECIALS[number]
        res.type = "特番:" + sp.get("d", "")
        res.parts = [number]
        return res

    prefix = ""
    len_number = len(number)
    for d in range(1, 6 + 1):
        prefix = number[0:d]
        info_cand = _data.PREFIXES.get(prefix)
        if info_cand:
            length = info_cand.get("l")
            if (length is None) or (length == len_number):
                info = info_cand

    if info:
        n1 = prefix[: info.get("f")]
        if n1:
            res.parts.append(n1)
        n2 = number[len(n1) : len(n1) + info.get("m", 0)]
        if n2:
            res.parts.append(n2)
        n3 = number[len(n1) + len(n2) :]
        if n3:
            res.parts.append(n3)

        message_area = info.get("a")
        if message_area:
            res.area_code = n1
            res.message_area = message_area
        print(info)
        res.type = info.get("t", "")

    else:
        if not number.startswith("0"):
            res.type = "国外"
        res.parts.append(number)

    return res
