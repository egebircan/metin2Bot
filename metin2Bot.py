import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

#constants
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
X = 0x2D
H = 0x23
ALT = 0x38
TAB = 0x0F
CTRL = 0x1D
SPACE = 0x39

NP_1 = 0x4f
NP_2 = 0x50
NP_4 = 0x4B
NP_6 = 0x4D
NP_8 = 0x48

AIR_BLADE_COOLDOWN = 60

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


#functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002,
                        0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ToggleHorse():
    PressKey(CTRL)
    time.sleep(0.2)
    PressKey(H)
    time.sleep(0.2)
    ReleaseKey(H)
    ReleaseKey(CTRL)
    time.sleep(1)

def AirBlade():
    PressKey(NP_1)
    time.sleep(0.2)
    ReleaseKey(NP_1)
    time.sleep(3)

def ChangeWindow():
    PressKey(ALT)
    time.sleep(0.2)
    PressKey(TAB)
    time.sleep(0.2)
    ReleaseKey(TAB)
    ReleaseKey(ALT)
    time.sleep(1)

def BotInit():
    ChangeWindow()
    AirBlade()
    ToggleHorse()
    

#program
BotInit()
startTime = time.time()       
while True:
    PressKey(X)
    PressKey(SPACE)
    time.sleep(0.2)

    timeDiff = time.time() - startTime
    if timeDiff >= AIR_BLADE_COOLDOWN:
        ToggleHorse()
        AirBlade()
        ToggleHorse()
        startTime = time.time()

