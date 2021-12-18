import xml.etree.ElementTree as ET


class Canvars():
    def __init__(self):
        self._xml_version = ET.Element("xml", {"version": "1.0", "encoding": "UTF-8"})
        self.SubtitleReel = ET.Element("SubtitleReel", {"xmlns": "http://www.smpte-ra.org/schemas/428-7/2010/DCST",
                                                        "xmlns:xs": "http://www.w3.org/2001/schema"})
        self.double_subtitle = False
        self.double_font = False
        self._SubtitleReel_main()
        self._subtitle_attrib = {"SpotNumber": "0", "TimeIn": "00:00:00:00", "TimeOut": "00:00:00:00","FadeUpTime": "00:00:00:00", "FadeDownTime": "00:00:00:00"}
        self.text_attrib = {"Hposition": "0.0", "Halign": "center", "Valign": "bottom", "Vposition": "0.0",
                            "Direction": "ltr"}
        self.effect_attrib = {"ID": "SimHei", "Color": "FFFFFFFF", "Weight": "normal", "Size": "36", "Effect": "shadow",
                              "EffectColor": "FF000000", "AspectAdjust": "1.00"}
        self.SubtitleList = ET.SubElement(self.SubtitleReel, "SubtitleList")

    def __str__(self):
        return "{}".format(ET.dump(self.SubtitleReel))

    def _SubtitleReel_main(self):
        "为SubtitleReel下增加节点"
        self.ID = ET.SubElement(self.SubtitleReel, "ID")
        self.ContentTitleText = ET.SubElement(self.SubtitleReel, "ContentTitleText")
        self.AnnotationText = ET.SubElement(self.SubtitleReel, "AnnotationText")
        self.IssueDate = ET.SubElement(self.SubtitleReel, "IssueDate")
        self.ReelNumber = ET.SubElement(self.SubtitleReel, "ReelNumber")
        self.Language = ET.SubElement(self.SubtitleReel, "Language")
        self.EditRate = ET.SubElement(self.SubtitleReel, "EditRate")
        self.TimeCodeRate = ET.SubElement(self.SubtitleReel, "TimeCodeRate")
        self.StartTime = ET.SubElement(self.SubtitleReel, "StartTime")
        self.LoadFont = ET.SubElement(self.SubtitleReel, "LoadFont", {"ID": ""})

    def subtitle_info(self,textinfo:list):
        self.subtitle = ET.SubElement(self.SubtitleList, "subtitle", self._subtitle_attrib)
        self.subtitle.attrib[]
        if self.double_subtitle:
            self.Text = ET.SubElement(self.subtitle,"Text",self.text_attrib)
            if self.double_font:
                self.subtitle2 = ET.SubElement(self.subtitle, "subtitle", self._subtitle_attrib)
                self.Text2 = ET.SubElement(self.subtitle2, "Text", self.text_attrib)
        else:
            for text in textinfo[-1]:
                ET.SubElement(self.subtitle,"Text",)


if __name__ == '__main__':
    print(Canvars())
