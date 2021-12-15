
import pysrt
from smpte_timecode import *
import pandas as pd

s = SMPTE()


def ms_trans(timecode: str, fps: [float, int]):

    timecode = timecode.replace(",", ":")
    H, M, S, MS = timecode.split(":")
    Timecode_S = 3600 * int(H) + 60 * int(M) + int(S)
    Timecode_MS = (int(MS) / 1000) / (1/fps)
    s.gettc(fps)
    return s.gettc((Timecode_S * 24) + Timecode_MS)



if __name__ == '__main__':
    data = pysrt.open("/Users/macintosh/PycharmProjects/Cinecanvas/resource/IMAX.srt")
    csvfile = "/Users/macintosh/PycharmProjects/Cinecanvas/srt_pase/test.csv"

    xy = []
    for x in data:
        # t = "{}--->{}---->{}---->{}".format(x.index, ms_trans(str(x.start), 24), ms_trans(str(x.end), 24), x.text)
        xy.append([x.index, ms_trans(str(x.start), 24), ms_trans(str(x.end), 24), x.text])

    final = pd.DataFrame(xy,columns=["index","start","end","sub"])
    final.to_csv(csvfile,encoding="utf-8")