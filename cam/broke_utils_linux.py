async def readUntilNewLine(reader, encoding='ascii') -> str:
    #sofar =[]
    idiotpython =[]
    #~~~~~~~~~~~~ whynot_plus_0 = bytearray()
    try:
        bt=b'1'
        while bt is not None:
            bt = await reader.read(1)
            if(bt==b'\n'):
                #await reader.read(1)
                if(len(idiotpython)<1):
                    return ""
                return "".join([i.decode(encoding) for i in idiotpython])# whynot_plus_0.decode(encoding)
            else:
                # apnika TypeError: 'bytes' object cannot be interpreted as an integer
                #sofar.append(bt+0)
                #~~~~~~~~~~~~ whynot_plus_0.append(bt)~
                idiotpython.append(bt)
    except Exception as ex:
        if(len(idiotpython)<1):
            return ""
        return "".join([i.decode(encoding) for i in idiotpython])# wwhynot_plus_0.decode(encoding)

async def readUntilSeperator(reader, sep: str, encoding='ascii') -> str:
    a=0
    la=len(sep)
    idiotpython =[]
    buf=[]
    #~~~~~~~~~~~~ whynot_plus_0 = bytearray()
    try:
        bt=b'1'
        while bt is not None:
            bt = await reader.read(1)
            if(a == 0):
                if(bt.decode(encoding)==sep[a]):
                    a=a+1
                    buf.append(bt)
                else:
                    idiotpython.append(bt)
            else:
                if(a==la-1 and bt.decode(encoding)==sep[a]):
                    return "".join([i.decode(encoding) for i in idiotpython])# whynot_plus_0.decode(encoding)
                else:
                    if(bt.decode(encoding)==sep[a]):
                        a=a+1
                        buf.append(bt)
                    else:
                        for i in buf:
                            idiotpython.append(i)
                        buf =[]
                        a=0
    except Exception as ex:
        if(len(idiotpython)<1):
            return ""
        return "".join([i.decode(encoding) for i in idiotpython])# wwhynot_plus_0.decode(encoding)

async def appendUntilSeperator(reader, sep: str, app_byt: bytes, encoding='ascii') -> bytearray:
    #immutablebytes_more_fun yahy I LOVE P{Y}!!!!1111 back to old shit.
    #more cool stuff: int is what, 32 bit length on 64 bit system no? 
    # ValueError("invalid literal for int() with base 10: b'\\xb8'") -> 184. less than 256 :D :D :D
    immutablebytes_more_fun = bytearray(app_byt)
    a=0
    la=len(sep)
    buf=[]
    #~~~~~~~~~~~~ whynot_plus_0 = bytearray()
    try:
        bt=b'1'
        while bt is not None:
            bt = await reader.read(1)
            if(a == 0):
                if(bt.decode(encoding)==sep[a] if bt < b'\x80' else False):
                    a=a+1
                    buf.append(bt)
                else:
                    immutablebytes_more_fun+=(bytearray(bt))
            else:
                if(a==la-1 and (bt.decode(encoding)==sep[a] if bt < b'\x80' else False)):
                    return immutablebytes_more_fun
                else:
                    if(bt.decode(encoding)==sep[a] if bt < b'\x80' else False):
                        a=a+1
                        buf.append(bt)
                    else:
                        for i in buf:
                            immutablebytes_more_fun+=(bytearray(i))
                        buf =[]
                        a=0
    except Exception as ex:
            return immutablebytes_more_fun

