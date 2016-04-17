import alsaaudio
import audioop
   
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
inp.setchannels(1)
inp.setrate(16000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)

min_vol, max_vol = 100, 0
       
while True:
        l,data = inp.read()
        if l:
                vol = audioop.rms(data,2)
                if vol < min_vol:
                    min_vol = vol
                    print vol
                elif vol > max_vol:
                    max_vol = vol
                    print max_vol