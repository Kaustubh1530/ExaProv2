def enc(edata):
   edata = list(edata)
   encdata = []
   for i in edata:
        asciiv = ord(i)
        encdata.append(chr(asciiv+5))
   eoutput = ''.join(encdata)
   return eoutput

def dec(ddata):
   ddata = list(ddata)
   decdata = []
   for i in ddata:
        asciiv = ord(i)
        decdata.append(chr(asciiv-5))
   doutput = ''.join(decdata)
   return doutput

