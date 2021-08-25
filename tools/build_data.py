from typing import Any, Dict

import black
import pandas
import requests

BASE_URL = "https://www.soumu.go.jp/main_content/"
KOTEI_FILES = [
    "000697543.xls",
    "000697544.xls",
    "000697545.xls",
    "000697546.xls",
    "000697548.xls",
    "000697549.xls",
    "000697550.xls",
    "000697551.xls",
    "000697552.xls",
]
PROVIDERS_FILE = "000697542.xlsx"


providers = {}
source = []

res = requests.get(BASE_URL + PROVIDERS_FILE)
df = pandas.read_excel(res.content, skiprows=7)
for (_, row) in df.iterrows():
    a = row["番号"]
    for n in range(0, 10):
        b = row[chr(n + 65296)]
        if b != "-" and isinstance(b, str):
            number = a + str(n)
            name = b
            name = name.replace("ＫＤＤＩ", "KDDI")
            name = name.replace("ＮＴＴ", "NTT")
            providers[number] = name


for path in KOTEI_FILES:
    url = BASE_URL + path
    print(url)
    res = requests.get(BASE_URL + path)
    df = pandas.read_excel(res.content, skiprows=1)
    for (_, row) in df.iterrows():
        b1 = "0" + str(row["市外局番"])
        r = {
            "b": "0" + str(row["番号"]),
            "b1": b1,
            "area": row["MA"],
            "m": 6 - len(b1),
            "l": 10,
            "type": "固定",
        }
        source.append(r)

source.extend(
    [
        {"b": "050", "b1": "050", "m": 4, "l": 11, "type": "IP"},
        {"b": "0600", "b1": "0600", "m": 3, "type": "FMC"},
        {"b": "0120", "b1": "0120", "m": 3, "l": 10, "type": "フリーダイヤル"},
        {"b": "0800", "b1": "0800", "m": 3, "l": 11, "type": "フリーダイヤル"},
        {"b": "0204", "b1": "0204", "m": 3, "l": 11, "type": "ポケベル"},
        {"b": "0990", "b1": "0990", "m": 3, "l": 10, "type": "災害募金サービス"},
        {"b": "0570", "b1": "0570", "m": 3, "l": 10, "type": "ナビダイヤル"},
        {"b": "010", "b1": "010", "m": 0, "type": "国際電話"},
    ]
)


def add_tokuban(number, desc):
    source.append(
        {
            "b": number,
            "b1": number,
            "m": 0,
            "l": 3,
            "type": "特番",
            "st": f"{desc}",
        }
    )


add_tokuban("100", "オペレータ経由呼接続")
add_tokuban("102", "非常・緊急扱い通話")
add_tokuban("104", "番号案内")
add_tokuban("106", "オペレータ経由呼接続")
add_tokuban("108", "呼接続に関する付加的な処理")
add_tokuban("110", "警察機関への緊急通報")
add_tokuban("111", "試験")
add_tokuban("112", "共同相互通話")
add_tokuban("113", "故障受付")
add_tokuban("114", "話中調べ")
add_tokuban("115", "電報受付")
add_tokuban("116", "営業・料金案内")
add_tokuban("117", "時報")
add_tokuban("118", "海上保安機関への緊急通報")
add_tokuban("119", "消防機関への緊急通報")
add_tokuban("122", "固定優先接続の解除")
add_tokuban("131", "通話料分計")
add_tokuban("134", "サービス条件設定")
add_tokuban("135", "サービス条件設定")
add_tokuban("136", "発信番号電話通知サービス応用")
add_tokuban("140", "サービス条件設定")
add_tokuban("141", "留守番電話")
add_tokuban("142", "着信転送")
add_tokuban("143", "ドライブモード")
add_tokuban("144", "迷惑電話対応")
add_tokuban("145", "話し中時対応")
add_tokuban("146", "特定者向け情報の蓄積・再生")
add_tokuban("147", "発信番号電話通知サービス応用")
add_tokuban("148", "通知要請")
add_tokuban("149", "サービス条件設定")
add_tokuban("151", "営業・料金案内")
add_tokuban("154", "サービス条件設定")
add_tokuban("157", "営業・料金案内")
add_tokuban("158", "サービス条件設定")
add_tokuban("159", "サービス条件設定")
add_tokuban("161", "特定者向け情報の蓄積・再生")
add_tokuban("162", "特定者向け情報の蓄積・再生")
add_tokuban("164", "端末切り替え")
add_tokuban("165", "メール送受信")
add_tokuban("171", "災害用伝言ダイヤル")
add_tokuban("177", "天気予報")
add_tokuban("178", "呼接続に関する付加的な処理")
add_tokuban("179", "呼接続に関する付加的な処理")
add_tokuban("181", "ローミング")
add_tokuban("184", "発信者番号通知拒否")
add_tokuban("186", "発信者番号通知")
add_tokuban("188", "消費生活相談受付")
add_tokuban("189", "児童虐待通告・児童相談受付")


# 携帯
for k in [7, 8, 9]:
    for i in range(1, 9 + 1):
        source.append(
            {
                "b": f"0{k}0{i}",
                "b1": f"0{k}0",
                "m": 4,
                "l": 11,
                "type": "携帯",
            }
        )

# M2M
for i in [1, 2, 3, 5, 6, 7, 8, 9]:
    source.append(
        {
            "b": f"020{i}",
            "b1": "020",
            "m": 3,
            "l": 11,
            "type": "M2M",
        }
    )

closeset = {}
openset = source


for prefix_len in range(1, 6 + 1):
    counter: Dict[str, Any] = {}
    for r in openset:
        prefix = r["b"][0:prefix_len]
        if len(prefix) < prefix_len:
            raise RuntimeError("cannot distinguish")
        if prefix not in counter:
            counter[prefix] = {}

        key = (r["b1"], r.get("type"), r.get("area"))
        if key not in counter[prefix]:
            counter[prefix][key] = []
        counter[prefix][key].append(r)

    openset = []
    for (prefix, values) in counter.items():
        if len(values) == 1:
            r = list(values.values())[0][0]
            closeset[prefix] = {
                "f": len(r["b1"]),
                "m": r["m"],
                "t": r["type"],
                "l": r.get("l"),
            }
            if area := r.get("area"):
                closeset[prefix]["a"] = area
            if st := r.get("st"):
                closeset[prefix]["st"] = st
        else:
            for records in values.values():
                openset.extend(records)

assert len(openset) == 0


code = ["# This code was automatically generated by tools/build_data.py\n"]

code.append(
    """
from typing import Dict, TypedDict, Optional
from .types import NumberTypes


class _PrefixData(TypedDict, total=False):
    f: int            # length of the first part
    m: int            # length of the second part
    l: Optional[int]  # total length
    t: NumberTypes    # number type
    st: str           # subtype
    a: str            # message area name

"""
)

code.append("PREFIXES: Dict[str, _PrefixData] = {\n")
code.append(",\n".join(repr(k) + ": " + repr(v) for (k, v) in closeset.items()))
code.append("\n}\n\n")

code.append("CARRIER_SELECTORS: Dict[str, str] = ")
code.append(repr(providers))
body = "".join(code)
body = black.format_str(body, mode=black.Mode())

with open("phonenumbers_jp/_data.py", "w", encoding="utf-8") as f:
    f.write(body)
