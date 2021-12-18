import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from datetime import datetime
from srt_pase import srt_pase
import uuid


class Canvars():
    def __init__(self):
        self.SubtitleReel = ET.Element("SubtitleReel", {"xmlns": "http://www.smpte-ra.org/schemas/428-7/2010/DCST",
                                                        "xmlns:xs": "http://www.w3.org/2001/schema"})
        self.double_font = []

        self._subtitle_attrib = {"SpotNumber": "0", "TimeIn": "00:00:00:00", "TimeOut": "00:00:00:00",
                                 "FadeUpTime": "00:00:00:00", "FadeDownTime": "00:00:00:00"}
        self.text_attrib = {"Hposition": "0.0", "Halign": "center", "Valign": "bottom", "Vposition": "0.0",
                            "Direction": "ltr"}
        self.effect_attrib = {"ID": "SimHei", "Color": "FFFFFFFF", "Weight": "normal", "Size": "37", "Effect": "shadow",
                              "EffectColor": "FF000000", "AspectAdjust": "1.00"}

    def creat_main(self):
        "为SubtitleReel下增加节点"
        self.ID = ET.SubElement(self.SubtitleReel, "ID")
        self.ContentTitleText = ET.SubElement(self.SubtitleReel, "ContentTitleText")
        self.AnnotationText = ET.SubElement(self.SubtitleReel, "AnnotationText")
        self.IssueDate = ET.SubElement(self.SubtitleReel, "IssueDate")
        self.IssueDate.text = str(datetime.now())
        self.ReelNumber = ET.SubElement(self.SubtitleReel, "ReelNumber")
        self.Language = ET.SubElement(self.SubtitleReel, "Language")
        self.EditRate = ET.SubElement(self.SubtitleReel, "EditRate")
        self.TimeCodeRate = ET.SubElement(self.SubtitleReel, "TimeCodeRate")
        self.StartTime = ET.SubElement(self.SubtitleReel, "StartTime")
        self.StartTime.text = "00:00:00:00"
        for font in self.double_font:
            self.LoadFont = ET.SubElement(self.SubtitleReel, "LoadFont", {"ID": font})
            self.LoadFont.text = str(uuid.uuid4())
        self.SubtitleList = ET.SubElement(self.SubtitleReel, "SubtitleList")
        self.effect_attrib.update({"ID": self.double_font[0]})
        self.mainFont = ET.SubElement(self.SubtitleList, "Font", self.effect_attrib)

    def add_subtitle(self, text_info: list):
        text_list = text_info[-1]
        if text_list:
            subtitle = ET.SubElement(self.mainFont, "subtitle", self._subtitle_attrib)
            subtitle.attrib.update({"SpotNumber": str(text_info[0]), "TimeIn": text_info[1], "TimeOut": text_info[2]})
            for text in text_list:
                if text_list.index(text) >= 1 and len(self.double_font) > 1:
                    child_font_node = ET.SubElement(subtitle, "Font", self.effect_attrib)
                    child_font_node.attrib.update({"ID": self.double_font[1]})
                    Text = ET.SubElement(child_font_node, "Text", self.text_attrib)
                    Text.text = text
                else:
                    Text = ET.SubElement(subtitle, "Text", self.text_attrib)
                    Text.text = text


def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


if __name__ == '__main__':
    srt_list = srt_pase("/Users/denghui/PycharmProjects/Cinecanvas/resource/IMAX.srt")
    xml_ob = Canvars()
    xml_ob.double_font = ["test1", "test5"]
    xml_ob.creat_main()
    for text in srt_list:
        xml_ob.add_subtitle(text)
    print(prettify(xml_ob.SubtitleReel))
