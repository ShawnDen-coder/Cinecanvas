import xml.etree.ElementTree as ET


ORIGIN_CN = {"horiz": 0, "vert": 0.390}
ORIGIN_EN = {"horiz": 0, "vert": 0.431}
STYLE = {"普通": "1", "粗体": "2", "斜体": "3", "粗体/斜体": "4"}


def IsFinalXml(root):
    global FINALXML
    appname = root.findall("./sequence/media/video/format/samplecharacteristics/"
                           "codec/appspecificdata/appname")
    if appname[0].text == "Final Cut Pro":
        FINALXML = True
    else:
        FINALXML = False


def IsText(node):
    """判断根节点下是否有文本节点 bool 返回类型"""
    data = node.find("./effect/[effectid= 'Text']")
    data = data.find("./effectid").text
    return True if data == "Text" else False


def GetText(node):
    """获取文本内容"""
    text_tag = node.find("./effect/parameter/[parameterid='str']")
    text_value = text_tag.find("./value")
    text_value.text = text_value.text.strip()
    return text_value.text


def SetFont(node, font):
    """设置文本字体"""
    font_tag = node.find("./effect/parameter/[parameterid='fontname']")
    font_value = font_tag.find("./value")
    font_value.text = font
    return font_value.text == font


def SetFontSize(node, size):
    """设置文本字体字号"""
    fontSize_tag = node.find("./effect/parameter/[parameterid='{}']".
                             format("fontsize" if FINALXML else "size"))
    fontSize_tag.find("./parameterid").text = "fontsize"
    fontSize_value = fontSize_tag.find("./value")
    fontSize_value.text = str(size)
    return fontSize_value.text == str(size)


def SetFontColor(node, color):
    """设置文本字体字号"""
    result = []
    fontcolor_tag = node.find("./effect/parameter/[parameterid='fontcolor']")
    fontcolor_value = fontcolor_tag.find("./value")
    for t in fontcolor_value:
        t.text = str(color)
        result.append(t.text == str(color))
    return result


def SetFontStyle(node, style="普通"):
    """{"普通": 1, "粗体": 2, "斜体": 3, "粗体/斜体": 4}"""
    fontStyle_tag = node.find("./effect/parameter/[parameterid='fontstyle']")
    fontStyle_value = fontStyle_tag.find("./value")
    fontStyle_value.text = STYLE[style]
    return fontStyle_value.text == STYLE[style]


def SetOrigin(node, origin: dict):
    """设置文本位置"""
    fontcolor_tag = node.find("./effect/parameter/[parameterid='origin']")
    fonthoriz_value = fontcolor_tag.find("./value/horiz")
    fontvert_value = fontcolor_tag.find("./value/vert")
    fonthoriz_value.text = str(origin['horiz'])
    fontvert_value.text = str(origin['vert'])
    return [fonthoriz_value.text == str(origin['horiz']),
            fontvert_value.text == str(origin['vert'])]


def CheckCh(cn_str: str):
    for ch in cn_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def main(file_path, cn_font="Source Han Sans CN", en_font="Arial", cn_font_size=12, en_font_size=10, font_style="普通"):
    root = ET.parse(file_path)
    IsFinalXml(root)
    text_root = root.findall("./sequence/media/video/track/generatoritem")
    for text_ob in text_root:
        if IsText(text_ob):
            # 判断这个节点下是否有文本节点
            if CheckCh(GetText(text_ob)):
                # 判断当前的这句台词中是否含有中文，如果有那么判断这个台词为中文文本
                SetFont(text_ob, cn_font)
                SetOrigin(text_ob, ORIGIN_CN)
                SetFontColor(text_ob, 255)
                SetFontSize(text_ob, str(cn_font_size))
                SetFontStyle(text_ob, font_style)
            else:
                SetFont(text_ob, en_font)
                SetOrigin(text_ob, ORIGIN_EN)
                SetFontColor(text_ob, 255)
                SetFontSize(text_ob, str(en_font_size))
                SetFontStyle(text_ob, font_style)
    return root


if __name__ == '__main__':
    file = "/Users/macintosh/Desktop/Final7/Test/_20220104_BTZDMT_REF_R3_CN&EN_.xml"
    x = main(file, cn_font="SimHei")
    x.write("/Users/macintosh/Desktop/Final7/final.xml", encoding="utf-8")
