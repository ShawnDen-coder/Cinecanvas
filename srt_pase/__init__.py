import pysrt
from smpte_timecode import *

s = SMPTE()


def ms_trans(timecode: str, fps: [float, int]):
    timecode = timecode.replace(",", ":")
    H, M, S, MS = timecode.split(":")
    Timecode_S = 3600 * int(H) + 60 * int(M) + int(S)
    Timecode_MS = (int(MS) / 1000) / (1 / fps)
    s.gettc(fps)
    return s.gettc((Timecode_S * 24) + Timecode_MS)


def srt_pase(srt_file):
    data = pysrt.open(srt_file)
    result = []
    for x in data:
        result.append([x.index, ms_trans(str(x.start), 24), ms_trans(str(x.end), 24), x.text.split("\n")])
    return result


if __name__ == '__main__':
    x = srt_pase("/Users/denghui/PycharmProjects/Cinecanvas/resource/IMAX.srt")
    print(x)
