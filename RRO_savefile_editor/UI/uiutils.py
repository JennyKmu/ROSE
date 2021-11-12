# class ANSI(object):
#     import os
#     isPowerShell = len(os.getenv('PSModulePath', '').split(os.pathsep)) >= 3
#
#     def __init__(self, code):
#

NeedSecondByteWin = [
    b'\xe0',
    b'\x00',
]

KeyTranslatorWin = {
    b"\xe0H":b"KEY_UP",
    b"\xe0M":b"KEY_RIGHT",
    b"\xe0P":b"KEY_DOWN",
    b"\xe0K":b"KEY_LEFT",
    b"\xe0I":b"PAGE_UP",
    b"\xe0Q":b"PAGE_DOWN",
    b"\r":b"RETURN",
    b"\x08":b"BACKSPACE",
    b"\x1b":b"ESCAPE",
    b"\x03":b"CTRL_C",
    b"\x04":b"CTRL_D"
}


NeedSecondByteUnix = [
    b'\x1b',
]

NeedFourthByteUnix = [
    b'\x1b[5',
    b'\x1b[6',
]

KeyTranslatorUnix = {
    b"\x1b[A":b"KEY_UP",
    b"\x1b[B":b"KEY_DOWN",
    b"\x1b[C":b"KEY_RIGHT",
    b"\x1b[D":b"KEY_LEFT",
    b"\x1b[6~":b"PAGE_DOWN",
    b"\x1b[5~":b"PAGE_UP",
    b"\x1b":b"ESCAPE",
    b"\r":b"RETURN",
    b"\x03":b"CTRL_C",
    b"\x04":b"CTRL_D"
}

### From StackOverflow:
# https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-a-script-from-the-termina
# vvvvv
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen. From http://code.activestate.com/recipes/134892/"""
    def __init__(self):
        try:
            self._impl = _GetchWindows()
        except ImportError:
            try:
                self._impl = _GetchMacCarbon()
            except(AttributeError, ImportError):
                self._impl = _GetchUnix()

    def __call__(self): return self._impl()

    @property
    def impl(self):
        return self._impl



class _GetchUnix:
    def __init__(self):
        import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

    def __call__(self, _chekmorebytes=True):
        # print("_GetchUnix")
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch in NeedSecondByteUnix and _chekmorebytes:
                #~ while True:
                  #~ chb = self(_chekmorebytes=False)
                  #~ print(repr(chb))
                  #~ if chb != '' and chb is not None:
                    #~ ch += chb
                ch2 = self(_chekmorebytes=False)
                if ch2 != '':
                    ch3 = self(_chekmorebytes=False)
                    ch = ch + ch2 + ch3
                    if ch in NeedFourthByteUnix:
                      ch4 = self(_chekmorebytes=False)
                      ch += ch4
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def translate(self, b):
        try:
            r = KeyTranslatorUnix[b]
            if r == b"CTRL_C":
                raise KeyboardInterrupt
            if r == b"CTRL_D":
                raise SystemExit
            return r
        except KeyError:
            return b


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self, _checkmorebytes=True):
        # print("_GetchWindows")
        import msvcrt
        r = msvcrt.getch()
        if r in NeedSecondByteWin and  _checkmorebytes == True:
            r = r + msvcrt.getch()

        return r

    def translate(self, b):
        try:
            r = KeyTranslatorWin[b]
            if r == b"CTRL_C":
                raise KeyboardInterrupt
            if r == b"CTRL_D":
                raise SystemExit
            return r
        except KeyError:
            return b


class _GetchMacCarbon:
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.  The
    page http://www.mactech.com/macintosh-c/chap02-1.html was
    very helpful in figuring out how to do this.
    """
    def __init__(self):
        import Carbon
        Carbon.Evt #see if it has this (in Unix, it doesn't)

    def __call__(self):
        # print("_GetchMacCarbon")
        import Carbon
        if Carbon.Evt.EventAvail(0x0008)[0]==0: # 0x0008 is the keyDownMask
            return ''
        else:
            #
            # The event contains the following info:
            # (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            #
            # The message (msg) contains the ASCII char which is
            # extracted with the 0x000000FF charCodeMask; this
            # number is converted to an ASCII character with chr() and
            # returned
            #
            (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)



# Adapted below by Jenny
def getKey():
    inkey = _Getch().impl
    # import sys
    # for i in range(sys.maxsize):
    while True:
        k = inkey()
        k = inkey.translate(k)
        if k!='': break

    return k
#^^^^


if __name__ == "__main__":
    while True:
        print(repr(getKey()))
