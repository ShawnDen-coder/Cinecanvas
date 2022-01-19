import xml.etree.ElementTree as ET
from smpte_timecode import *
import zhconv

s = SMPTE()
s.fps = int(24)

class Compare():
    def __init__(self,file):
        self.root = ET.parse(file)
        self.timeline_start,self.timeline_rate =self._Gettimelinestart()
        s = SMPTE()
        s.fps = int(self.timeline_rate)


    def _Gettimelinestart(self):
        timeline_start = self.root.find("./sequence/timecode/string").text
        timeline_rate = self.root.find("./sequence/timecode/rate/timebase").text
        timeline_start = s.getframes(timeline_start)
        return [timeline_start,timeline_rate]


    def IsText(self,node):
        """判断根节点下是否有文本节点 bool 返回类型"""
        data = node.find("./effect/[effectid= 'Text']")
        data = data.find("./effectid").text
        return True if data == "Text" else False


    def GetText(self,node):
        """获取文本内容"""
        text_tag = node.find("./effect/parameter/[parameterid='str']")
        text_value = text_tag.find("./value")
        text_value.text = text_value.text.strip()
        return text_value.text

    def SetText(self,node,text):
        text_tag = node.find("./effect/parameter/[parameterid='str']")
        text_value = text_tag.find("./value")
        text_value.text = text
        return True if text_value.text == text else False


    def GetTextTimeCode(self,node):
        text_start = node.find("./start").text
        text_end = node.find("./end").text
        return [int(text_start), int(text_end)]


    def CheckCh(self,cn_str: str):
        for ch in cn_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def hant_2_hans(self,hant_str: str):
        return zhconv.convert(hant_str, 'zh-hans')

    def main(self):
        root_text = self.root.findall("./sequence/media/video/track/generatoritem")
        result = []
        for x in root_text:
            st = self.GetTextTimeCode(x)
            text = self.GetText(x)
            single = [[s.gettc(st[0]+self.timeline_start),s.gettc(st[1]+self.timeline_start)], text]
            single.append(True) if self.CheckCh(text) else single.append(False)
            result.append(single)
        return result





if __name__ == '__main__':
    int_ = Compare("../resource/btt/btt_R2_int.xml")
    data_int = int_.main()
    dom = Compare("../resource/btt/btt_R2_dom.xml")
    data_dom = dom.main()
    for INT in data_int:
        for DOM in data_dom:
            if INT[0] == DOM[0] and INT[-1] == DOM[-1]:
                if INT[-1]:
                    dalu = DOM[1].replace(" ","")
                    hk = INT[1].replace(" ","")

                    # print("{}".format(dalu==zhconv.convert(hk, 'zh-hans')))
                    if dalu != zhconv.convert(hk, 'zh-hans'):
                        print("{}------->{}------->{}".format(dalu,zhconv.convert(hk, 'zh-hans'),INT[1]))
