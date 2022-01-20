import xml.etree.ElementTree as ET
from smpte_timecode import *
import zhconv,csv

s = SMPTE()
s.fps = int(24)


class Compare():
    def __init__(self, frame_rate, timeline_start):

        s = SMPTE()
        s.fps = int(frame_rate)
        self.timeline_start = s.getframes(timeline_start)

    def IsText(self, node):
        """判断根节点下是否有文本节点 bool 返回类型"""
        data = node.find("./effect/[effectid= 'Text']")
        data = data.find("./effectid").text
        return True if data == "Text" else False

    def GetText(self, node):
        """获取文本内容"""
        text_tag = node.find("./effect/parameter/[parameterid='str']")
        text_value = text_tag.find("./value")
        text_value.text = text_value.text.strip()
        return text_value.text

    def SetText(self, node, text):
        text_tag = node.find("./effect/parameter/[parameterid='str']")
        text_value = text_tag.find("./value")
        text_value.text = text
        return True if text_value.text == text else False

    def GetTextTimeCode(self, node):
        text_start = node.find("./start").text
        text_end = node.find("./end").text
        return [int(text_start), int(text_end)]

    def CheckCh(self, cn_str: str):
        for ch in cn_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def hant_2_hans(self, hant_str: str):
        return zhconv.convert(hant_str, 'zh-hans')

    def InsterSpace(self, fan, jian):
        fan = list(fan)
        jian = list(jian)
        num = 0
        for i in jian:
            if i.isspace():
                fan.insert(num, " ")
            num += 1
        return "".join(fan)

    def Pase(self, file):
        root = ET.parse(file)
        root_text = root.findall("./sequence/media/video/track/generatoritem")
        result = []
        for x in root_text:
            st = self.GetTextTimeCode(x)
            text = self.GetText(x)
            single = [[s.gettc(st[0] + self.timeline_start), s.gettc(st[1] + self.timeline_start)], text]
            single.append(True) if self.CheckCh(text) else single.append(False)
            result.append(single)
        return result

    def SearchHans(self, fan_text_list, jian_hans_list: list):
        text_time_code, text, iscn = fan_text_list
        for hans in jian_hans_list:
            if text_time_code in hans and iscn == hans[-1]:
                return hans

    def User(self, text_list):
        print("\n未找到当前对白简体版本\n"
              "{}\t{}\t{}\n".format(text_list[0], text_list[1], text_list[2]))
        while True:
            select = input("请手动指定当前对白（P 跳过）：")
            if select != 'P':
                return select
            else:
                break
        return None

    def Edit(self, fan_list, jian_hans_xml):
        jian_list = self.Pase(jian_hans_xml)
        data = []
        for x in jian_list:
            if fan_list[0] in x and fan_list[-1] == x[-1]:
                data.extend(x)
        if fan_list[-1]:
            if 0 < len(data) <= 3:
                if fan_list[1] == data[1]:
                    return None
                elif self.hant_2_hans(fan_list[1].replace(" ", "")) == data[1].replace(" ", ""):
                    text = self.InsterSpace(fan_list[1].replace(" ", ""), data[1])
                    if " " not in text:
                        return None
                    return text
                else:
                    self.User(fan_list)
            else:
                self.User(fan_list)
        else:
            if "-" in fan_list[1]:
                en_list = list(fan_list[1])
                num = 0
                for x in en_list:
                    if x == "-" and en_list[num - 1].isspace():
                        en_list[num - 1] = "    "
                    num += 1
                return "".join(en_list)


    def Main(self, xml_file, jian_hans_xml, mark_log):
        root = ET.parse(xml_file)
        root_text = root.findall("./sequence/media/video/track/generatoritem")

        header = ["In","Out","After Text","Before Text","State"]
        log_list = []
        for x in root_text:
            time = self.GetTextTimeCode(x)
            text = self.GetText(x)
            fan_data = [[s.gettc(time[0] + self.timeline_start), s.gettc(time[1] + self.timeline_start)], text,
                        self.CheckCh(text)]
            space_text = self.Edit(fan_data, jian_hans_xml)
            if space_text != None:
                stat = self.SetText(x, space_text)
                log_list.append([fan_data[0][0],fan_data[0][1],space_text,fan_data[1],stat])
        with open(mark_log,"w") as file:
            csv_file = csv.writer(file)
            csv_file.writerow(header)
            csv_file.writerows(log_list)




if __name__ == '__main__':
    Compare(frame_rate=24, timeline_start="00:00:00:00").Main(
        "/Users/macintosh/PycharmProjects/Cinecanvas/resource/btt/btt_R2_int.xml",
        "/Users/macintosh/PycharmProjects/Cinecanvas/resource/btt/btt_R2_dom.xml",
        "/Users/macintosh/PycharmProjects/Cinecanvas/resource/btt/log_text.csv")
