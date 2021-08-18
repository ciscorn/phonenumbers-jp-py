import phonenumbers_jp


def test_parse_kotei():
    info = phonenumbers_jp.parse("0344445555")
    assert info.type == "固定"
    assert info.parts == ["03", "4444", "5555"]
    assert info.message_area is not None
    assert info.message_area.number == "03"
    assert info.message_area.name == "東京"
    assert info.selected_carrier is None

    info = phonenumbers_jp.parse("0344445555")
    assert info.type == "固定"
    assert info.parts == ["03", "4444", "5555"]
    assert info.message_area is not None
    assert info.message_area.number == "03"
    assert info.message_area.name == "東京"

    info = phonenumbers_jp.parse("0344445555")
    assert info.type == "固定"
    assert info.parts == ["03", "4444", "5555"]
    assert info.message_area is not None
    assert info.message_area.number == "03"
    assert info.message_area.name == "東京"

    info = phonenumbers_jp.parse("0997223333")
    assert info.type == "固定"
    assert info.parts == ["0997", "22", "3333"]
    assert info.message_area is not None
    assert info.message_area.number == "0997"
    assert info.message_area.name == "種子島"

    info = phonenumbers_jp.parse("0997998888")
    assert info.type == "固定"
    assert info.parts == ["0997", "99", "8888"]
    assert info.message_area is not None
    assert info.message_area.number == "0997"
    assert info.message_area.name == "徳之島"


def test_parse_mobile():
    info = phonenumbers_jp.parse("09011112222")
    assert info.type == "携帯"
    assert info.parts == ["090", "1111", "2222"]
    assert info.message_area is None


def test_parse_freedial():
    info = phonenumbers_jp.parse("0120123456")
    assert info.type == "フリーダイヤル"
    assert info.parts == ["0120", "123", "456"]
    assert info.callerid_delivery is None
    assert info.message_area is None

    info = phonenumbers_jp.parse("08001112222")
    assert info.type == "フリーダイヤル"
    assert info.parts == ["0800", "111", "2222"]
    assert info.callerid_delivery is None
    assert info.message_area is None


def test_parse_m2m():
    info = phonenumbers_jp.parse("02011122222")
    assert info.type == "M2M"
    assert info.parts == ["020", "111", "22222"]
    assert info.callerid_delivery is None
    assert info.message_area is None


def test_parse_184_186():
    info = phonenumbers_jp.parse("1840355556666")
    assert info.callerid_delivery == "withhold"
    assert info.parts == ["184", "03", "5555", "6666"]
    assert info.message_area is not None
    assert info.message_area.number == "03"

    info = phonenumbers_jp.parse("1860355556666")
    assert info.callerid_delivery == "provide"
    assert info.parts == ["186", "03", "5555", "6666"]
    assert info.message_area is not None
    assert info.message_area.number == "03"


def test_parse_carrier_selector():
    info = phonenumbers_jp.parse("00330355556666")
    assert info.callerid_delivery is None
    assert info.parts == ["0033", "03", "5555", "6666"]
    assert info.message_area is not None
    assert info.message_area.number == "03"

    info = phonenumbers_jp.parse("0010355556666")
    assert info.callerid_delivery is None
    assert info.parts == ["001", "03", "5555", "6666"]
    assert info.message_area is not None
    assert info.message_area.number == "03"

    # not designated
    info = phonenumbers_jp.parse("00210355556666")
    assert info.parts == ["00210355556666"]

    info = phonenumbers_jp.parse("0091300355556666")
    assert info.callerid_delivery is None
    assert info.parts == ["009130", "03", "5555", "6666"]
    assert info.message_area is not None
    assert info.message_area.number == "03"


def test_parse_184_and_carrier():
    info = phonenumbers_jp.parse("18400330355556666")
    assert info.callerid_delivery == "withhold"
    assert info.parts == ["184", "0033", "03", "5555", "6666"]
    assert info.message_area is not None
    assert info.message_area.number == "03"


def test_parse_tokuban():
    info = phonenumbers_jp.parse("110")
    assert info.type == "特番"
    assert info.subtype == "警察機関への緊急通報"


def test_parse_international():
    info = phonenumbers_jp.parse("01081355554444")
    assert info.type == "国際電話"
    assert info.message_area is None
    assert info.parts == ["010", "81355554444"]


def test_parse_international2():
    info = phonenumbers_jp.parse("12024558888")
    assert info.type == "国外"
    assert info.message_area is None
    assert info.parts == ["12024558888"]
