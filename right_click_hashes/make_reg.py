import base64

REG_TEMPLATE = r'''Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\*\shell\calchashes]
@="Calculate MD5/SHA1"

[HKEY_CLASSES_ROOT\*\shell\calchashes\command]
@="\"C:\\Python27\\pythonw.exe\" \"-c\" \"exec 'B64SCRIPT_GOES_HERE'.decode('base64')\" \"%1\""

'''

script = file("hashes.py","rb").read()
b64script = base64.b64encode(script)
reg = REG_TEMPLATE.replace('B64SCRIPT_GOES_HERE', b64script)
file("right_click_hash.reg","wb").write(reg)
