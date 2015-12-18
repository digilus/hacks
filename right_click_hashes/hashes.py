# Under MIT License
# win32_unicode_argv snippet by Craig McQueen based on ActiveState:
# http://stackoverflow.com/questions/846850/read-unicode-characters-from-command-line-arguments-in-python-2-x-on-windows
# Retrieved 2015-12-19
import sys
MB_SETFOREGROUND = 0x10000
from ctypes import POINTER, byref, cdll, c_int, windll
from ctypes.wintypes import LPCWSTR, LPWSTR
import hashlib

BLOCK_SIZE = 0x100000

def win32_unicode_argv():
    """Uses shell32.GetCommandLineArgvW to get sys.argv as a list of Unicode
    strings.

    Versions 2.x of Python don't support Unicode in sys.argv on
    Windows, with the underlying Windows API instead replacing multi-byte
    characters with '?'.
    """


    GetCommandLineW = cdll.kernel32.GetCommandLineW
    GetCommandLineW.argtypes = []
    GetCommandLineW.restype = LPCWSTR

    CommandLineToArgvW = windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.argtypes = [LPCWSTR, POINTER(c_int)]
    CommandLineToArgvW.restype = POINTER(LPWSTR)

    cmd = GetCommandLineW()
    argc = c_int(0)
    argv = CommandLineToArgvW(cmd, byref(argc))
    if argc.value > 0:
        # Remove Python executable and commands if present
        start = argc.value - len(sys.argv)
        return [argv[i] for i in
                xrange(start, argc.value)]

sys.argv = win32_unicode_argv()

filename = sys.argv[1]
md5 = hashlib.md5()
sha = hashlib.sha1()
infile = file(filename, "rb")
block = infile.read(BLOCK_SIZE)
while block != '':
    md5.update(block)
    sha.update(block)
    block = infile.read(BLOCK_SIZE)
    
msg = u'''%s
MD5: %s
SHA1: %s
''' % (filename, md5.hexdigest(), sha.hexdigest())

windll.user32.MessageBoxW(0, msg, filename, MB_SETFOREGROUND)
