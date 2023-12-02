import gzip
from io import StringIO, BytesIO
import data1

# https://stackoverflow.com/q/69714533/435878
# function author: Fumanchu3000
# https://stackoverflow.com/users/8245737/fumanchu3000
# no changes where made.
def string_to_bytes(input_str: str) -> bytes:
    """
        Read the given string, encode it in utf-8, gzip compress
        the data and return it as a byte array.
    """
    bio = BytesIO()
    bio.write(input_str.encode("utf-8"))
    bio.seek(0)
    stream = BytesIO()
    compressor = gzip.GzipFile(fileobj=stream, mode='w')
    while True:  # until EOF
        chunk = bio.read(8192)
        if not chunk:  # EOF?
            compressor.close()
            return stream.getvalue()
        compressor.write(chunk)
        
# as this function has no link to other functions whatsoever,
# it is not built upon them
# therefore not required to be by-sa 4.0
def bytes_to_4string(in_by: bytes) -> str:
    cnt = 0
    #outstr = [(("0x"+i.hex()+" ", print(cnt)), cnt=cnt+1) for i in in_by]
    #outstr = [("0x"+i.hex()+" ", cnt=cnt+1) for i in in_by]
    #iter = in_by.iterbytes()
    #outstr = ["0x"+i.hex()+(" " if n%16==0 else "\n") for i, n in enumerate(iter) in iter]
    #outstr = [(hex(n) if n>0xF else hex(n).replace("x", "x0")).upper()+("\n" if i%16==0 and i!=0 else " ") for i, n in enumerate(in_by)]
    outstr = [(f" 0x{n:X},\n" if n>0xF else f" 0x{n:X},\n".replace("x", "x0")) if (i+1)%16==0 else (f" 0x{n:X}," if n>0xF else f" 0x{n:X},".replace("x", "x0")) for i, n in enumerate(in_by)]
    #outstr[0::16] = 
    outstr[len(outstr)-1] = outstr[len(outstr)-1].replace(",","")
    #print("".join(outstr))
    return "".join(outstr)

# https://stackoverflow.com/q/69714533/435878
# function author: Fumanchu3000
# https://stackoverflow.com/users/8245737/fumanchu3000
# no changes where made.
def bytes_to_string(input_bytes: bytes) -> str:
    """
        Decompress the given byte array (which must be valid
        compressed gzip data) and return the decoded text (utf-8).
    """
    bio = BytesIO()
    stream = BytesIO(input_bytes)
    decompressor = gzip.GzipFile(fileobj=stream, mode='r')
    while True:  # until EOF
        chunk = decompressor.read(8192)
        if not chunk:
            decompressor.close()
            bio.seek(0)
            return bio.read().decode("utf-8")
        bio.write(chunk)
    return None


""" #deflate
f = open("../temp/01.h", "w", encoding='utf8')
f.write(bytes_to_4string(data1.ig))
f.close()
fil = open("../temp/01.html", "w", encoding='utf8')
fil.write(bytes_to_string(data1.ig))
fil.close()
"""

""" #inflate
"""
fr = open("../temp/01.html", "r", encoding="utf-8")
f = open("../temp/01.h", "w", encoding='utf8')
f.write(bytes_to_4string(string_to_bytes(fr.read())))
f.close()
fr.close()
#print(a)
