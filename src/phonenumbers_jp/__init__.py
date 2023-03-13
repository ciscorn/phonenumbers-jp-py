from . import _data
from .types import NumberAndName, NumberInfo


def parse(number: str) -> NumberInfo:
    res = NumberInfo()

    # 非通知・通知
    if number.startswith("184"):
        res.callerid_delivery = "withhold"
        res.parts.append("184")
        number = number[3:]
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
            res.specified_carrier = NumberAndName(p, _data.CARRIER_SELECTORS[p])
            res.parts.append(p)
            number = number[prefix_len:]

    prefix = ""
    len_number = len(number)
    prefix_data = None
    for d in range(1, 6 + 1):
        prefix = number[0:d]
        data_cand = _data.PREFIXES.get(prefix)
        if data_cand:
            length = data_cand.get("l")
            if (length is None) or (length == len_number):
                prefix_data = data_cand

    if prefix_data:
        n1 = prefix[: prefix_data.get("f")]
        if n1:
            res.parts.append(n1)
        n2 = number[len(n1) : len(n1) + prefix_data.get("m", 0)]
        if n2:
            res.parts.append(n2)
        n3 = number[len(n1) + len(n2) :]
        if n3:
            res.parts.append(n3)

        if message_area := prefix_data.get("a"):
            res.message_area = NumberAndName(number=n1, name=message_area)
        res.type = prefix_data.get("t")
        res.subtype = prefix_data.get("st")

    else:
        if not number.startswith("0"):
            res.type = "国外"
        res.parts.append(number)

    return res
