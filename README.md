# phonenumbers-jp-py

![Test](https://github.com/ciscorn/phonenumbers-jp-py/actions/workflows/test.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/ciscorn/phonenumbers-jp-py/branch/main/graph/badge.svg)](https://codecov.io/gh/ciscorn/phonenumbers-jp-py)
[![pypi package](https://img.shields.io/pypi/v/phonenumbers-jp?color=%2334D058&label=pypi%20package)](https://pypi.org/project/phonenumbers-jp)

Get attribute information from Japanese domestic phone numbers.

日本国内の電話番号から、種別や市外局番などの情報を取得します。

License: MIT

## Installation

```bash
pip3 install phonenumbers-jp -U
```

## Examples

```python
>>> phonenumbers_jp.parse("0311111111")
NumberInfo(parts=['03', '1111', '1111'], type='固定', subtype=None, message_area=NumberAndName(number='03', name='東京'), specified_carrier=None, callerid_delivery=None)

>>> phonenumbers_jp.parse("0992000000")
NumberInfo(parts=['099', '200', '0000'], type='固定', subtype=None, message_area=NumberAndName(number='099', name='鹿児島'), specified_carrier=None, callerid_delivery=None)

>>> phonenumbers_jp.parse("1840992000000")
NumberInfo(parts=['184', '099', '200', '0000'], type='固定', subtype=None, message_area=NumberAndName(number='099', name='鹿児島'), specified_carrier=None, callerid_delivery='withhold')

>>> phonenumbers_jp.parse("09011112222")
NumberInfo(parts=['090', '1111', '2222'], type='携帯', subtype=None, message_area=None, specified_carrier=None, callerid_delivery=None)

>>> phonenumbers_jp.parse("117")
NumberInfo(parts=['117'], type='特番', subtype='時報', message_area=None, specified_carrier=None, callerid_delivery=None)

>>> phonenumbers_jp.parse("05012345678")
NumberInfo(parts=['050', '1234', '5678'], type='IP', subtype=None, message_area=None, specified_carrier=None, callerid_delivery=None)

>>> phonenumbers_jp.parse("00630111111111")
NumberInfo(parts=['0063', '011', '111', '1111'], type='固定', subtype=None, message_area=NumberAndName(number='011', name='札幌'), specified_carrier=NumberAndName(number='0063', name='ソフトバンク株式会社'), callerid_delivery=None)

>>> phonenumbers_jp.parse("0120444444")
NumberInfo(parts=['0120', '444', '444'], type='フリーダイヤル', subtype=None, message_area=None, specified_carrier=None, callerid_delivery=None)
```

## API

```python
NumberTypes = Literal[
    "特番", "固定", "携帯", "IP", "M2M", "国際電話", "国外",
    "フリーダイヤル", "FMC", "ポケベル", "災害募金サービス", "ナビダイヤル"
]

@dataclass
class NumberAndName:
    number: str
    name: str

@dataclass
class NumberInfo:
    parts: List[str] = field(default_factory=list)  # 分解された電話番号
    type: Optional[NumberTypes] = None  # 種別
    subtype: Optional[str] = None  # 特番の内容
    message_area: Optional[NumberAndName] = None  # メッセージエリア (市外局番)
    specified_carrier: Optional[NumberAndName] = None  # 事業者指定番号
    callerid_delivery: Optional[Literal["withhold", "provide"]] = None  # 非通知・通知

def parse(number: str) -> NumberInfo:
    ...
```
