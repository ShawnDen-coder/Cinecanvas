import xml.etree.ElementTree as ET

# class Canvars():
#     def __init__(self):
#         xml_head = ET.Element("xml version")


if __name__ == '__main__':
    xml_version = ET.Element("xml", {"versioon": "1.0", "encoding": "UTF-8"})
    SubtitleReel = ET.Element("SubtitleReel", {"xmlns": "http://www.smpte-ra.org/schemas/428-7/2010/DCST",
                                                   "xmlns:xs": "http://www.w3.org/2001/schema"})
    ID = ET.SubElement(SubtitleReel, "ID")
    ContentTitleText = ET.SubElement(SubtitleReel, "ContentTitleText")
    AnnotationText = ET.SubElement(SubtitleReel, "AnnotationText")
    IssueDate = ET.SubElement(SubtitleReel, "IssueDate")
    ReelNumber = ET.SubElement(SubtitleReel, "ReelNumber")
    Language = ET.SubElement(SubtitleReel, "Language")
    EditRate = ET.SubElement(SubtitleReel, "EditRate")
    TimeCodeRate = ET.SubElement(SubtitleReel, "TimeCodeRate")
    StartTime = ET.SubElement(SubtitleReel, "StartTime")
    LoadFont = ET.SubElement(SubtitleReel, "LoadFont",{"ID":""})
    SubtitleList = ET.SubElement(SubtitleReel, "SubtitleList")

    Font = ET.SubElement(SubtitleList, "Font")


    ET.dump(SubtitleReel)