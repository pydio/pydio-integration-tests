import json

base = "/Users/thomas/Pydio/tests/anothersync"

a = {'/àòt copy1/ypSfEXDxIppOtmuKfeA.png': 1459344647.433858, '/ipcBpmEgN ': 1459344647.43396, '/àòt copy1/LòErlògàR.png': 1459344647.434465, '/àòt copy1/BvSwe OQGc copy0.png': 1459344647.433957, '/àòt copy1/cFQwt.png': 1459344647.433862, '/lolà/DBt': 1459344647.434521, '/àòt copy1/mDQhLRzEro.png': 1459344647.434242, '/àòt copy1/CPIIrqy  fnLXS.pydio1.png': 1459344647.434182, '/àòt copy1/sLDgYBuCl.png': 1459344647.433933, '/àòt copy1/wùçRyKcAg.png': 1459344647.434662, '/àòt copy1/oçàOàXBçtòwtsAR.png': 1459344647.434469, '/àòt copy1/DQeEHYPqlf.png': 1459344647.433816, '/àòt copy1/àCàlWKbAùOxd.png': 1459344647.434482, '/àòt copy1/HlHòwoTMTKBDC.png': 1459344647.434576, '/gEOp copy1': 1459344647.434033, '/àòt copy1/lnegLAyGBEv.png': 1459344647.434332, '/àòt copy1/cjM.pydio1.png': 1459344647.434274, '/oSòUFNyi copy1': 1459344647.434336, '/àòt copy1/KisVeaeMmysfmDvKS.png': 1459344647.433822, '/àòt copy1/VXBYdUyoògGKC.png': 1459344647.434012, '/àòt copy1/CPIIrqy  fnLXS.png': 1459344647.43411, '/àòt copy1/gRuHfyVòwWèOJsgtlC.png': 1459344647.433898, '/gEOp copy1/çEwciggNjWWej.bmp': 1459344647.433868, '/àòt copy1/gyUxfNFkI.png': 1459344647.434353, '/àòt copy1/CkZOrpvèxIS.png': 1459344647.434896, '/àòt copy1/NçMWpIyZPtGjZVè.png': 1459344647.433758, '/àòt copy1/DQeEHYPqlf copy0.png': 1459344647.433847, '/àòt copy1/càcà.tiff': 1459344647.43442, '/àòt copy1': 1459344647.433671, '/Dùr': 1459344647.433713, '/àòt copy1/eKEpGFFnz.png': 1459344647.434545, '/àòt copy1/crOEévàefBx.png': 1459344647.434759, '/àòt copy1/nmMirYCxrVqçcph.png': 1459344647.434401, '/àòt copy1/jSypTGltcwW.png': 1459344647.434526, '/àòt0': 1459344647.434302, '/àòt copy1/ITHaNèzàQ.png': 1459344647.434621, '/àòt copy1/WyZufxIlò.png': 1459344647.433691, '/àòt copy1/KckLCHykrx.png': 1459344647.43364, '/lolà': 1459344647.434821, '/àòt copy1/nài HDçFD.png': 1459344647.43443}

logfile = 'test_interactive.log.json'

with open(logfile, 'r') as f:
    if f.readline()[0] != "{":
        print("You have to manually edit " + logfile)
    else:
        f.seek(0)
        log = json.load(f)
        for k in a.keys():
            try:
                log[base+k]
                print(log[base+k])
            except KeyError:
                for p in log.keys():
                    if str(log[p]).find(k) > -1:
                        print(k + " " + log[p])
                logstr = str(log)
                startpos = logstr.find(k)
                if startpos > -1:
                    start = logstr.rfind('{', 0, startpos)
                    end = max(logstr.find(']', startpos), logstr.find('}', startpos))
                    if start != -1 and end != -1:
                        print(k + " (" + str(startpos)+ ") is in " + logstr[start:end])
                    else:
                        print(k + " (" + str(startpos)+ ") is in " + logstr[startpos-20:end+10])
        print("Done")

