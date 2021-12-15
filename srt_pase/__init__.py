import pysrt

def ms_trans(timecode:str,fps:[float,int]):
    mstimecode = timecode.split(",")
    mstimecode[-1] = "{:0>2d}".format(int(int(mstimecode[-1])/1000*fps))
    print(int(mstimecode[-1])/1000)
    result = ":".join(mstimecode)
    print(result)

if __name__ == '__main__':
    data = pysrt.open("/Users/denghui/PycharmProjects/Cinecanvas/resource/IMAX.srt")
    test = data[0].end
    ms_trans("00:01:59,083",24)