cimport cython
cimport numpy as np
from cython.operator cimport dereference as deref, preincrement as inc
from exceptdrucker import errwrite
from itertools import chain, islice
from libc.math cimport sqrt, abs
from libc.stdlib cimport srand, rand
from libc.time cimport time as ctime
from libcpp.algorithm cimport for_each
from string import printable
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libcpp.utility cimport pair
from libcpp.vector cimport vector
from tempfile import NamedTemporaryFile
from time import time
import ctypes
import cython
import numpy as np
import os
import regex as re
import subprocess
import sys
import unicodedata
import struct
np.import_array()
sru=subprocess.run
cdef str structformat='qqHHI'
structsize=struct.calcsize(structformat)
struckt_pack=struct.Struct(structformat).pack
ctypedef pair[unsigned int,unsigned int] mypair
ctypedef vector[mypair] myvector
_func_cache=[]
config_settings=sys.modules[__name__]
config_settings.debug_enabled=True
srand(ctime(NULL))
ctypedef unordered_map[string, unsigned short] key_dict
cdef key_dict all_linux_key_events = {
    "KEY_RESERVED": 0,
    "KEY_ESC": 1,
    "KEY_1": 2,
    "KEY_2": 3,
    "KEY_3": 4,
    "KEY_4": 5,
    "KEY_5": 6,
    "KEY_6": 7,
    "KEY_7": 8,
    "KEY_8": 9,
    "KEY_9": 10,
    "KEY_0": 11,
    "KEY_MINUS": 12,
    "KEY_EQUAL": 13,
    "KEY_BACKSPACE": 14,
    "KEY_TAB": 15,
    "KEY_Q": 16,
    "KEY_W": 17,
    "KEY_E": 18,
    "KEY_R": 19,
    "KEY_T": 20,
    "KEY_Y": 21,
    "KEY_U": 22,
    "KEY_I": 23,
    "KEY_O": 24,
    "KEY_P": 25,
    "KEY_LEFTBRACE": 26,
    "KEY_RIGHTBRACE": 27,
    "KEY_ENTER": 28,
    "KEY_LEFTCTRL": 29,
    "KEY_A": 30,
    "KEY_S": 31,
    "KEY_D": 32,
    "KEY_F": 33,
    "KEY_G": 34,
    "KEY_H": 35,
    "KEY_J": 36,
    "KEY_K": 37,
    "KEY_L": 38,
    "KEY_SEMICOLON": 39,
    "KEY_APOSTROPHE": 40,
    "KEY_GRAVE": 41,
    "KEY_LEFTSHIFT": 42,
    "KEY_BACKSLASH": 43,
    "KEY_Z": 44,
    "KEY_X": 45,
    "KEY_C": 46,
    "KEY_V": 47,
    "KEY_B": 48,
    "KEY_N": 49,
    "KEY_M": 50,
    "KEY_COMMA": 51,
    "KEY_DOT": 52,
    "KEY_SLASH": 53,
    "KEY_RIGHTSHIFT": 54,
    "KEY_KPASTERISK": 55,
    "KEY_LEFTALT": 56,
    "KEY_SPACE": 57,
    "KEY_CAPSLOCK": 58,
    "KEY_F1": 59,
    "KEY_F2": 60,
    "KEY_F3": 61,
    "KEY_F4": 62,
    "KEY_F5": 63,
    "KEY_F6": 64,
    "KEY_F7": 65,
    "KEY_F8": 66,
    "KEY_F9": 67,
    "KEY_F10": 68,
    "KEY_NUMLOCK": 69,
    "KEY_SCROLLLOCK": 70,
    "KEY_KP7": 71,
    "KEY_KP8": 72,
    "KEY_KP9": 73,
    "KEY_KPMINUS": 74,
    "KEY_KP4": 75,
    "KEY_KP5": 76,
    "KEY_KP6": 77,
    "KEY_KPPLUS": 78,
    "KEY_KP1": 79,
    "KEY_KP2": 80,
    "KEY_KP3": 81,
    "KEY_KP0": 82,
    "KEY_KPDOT": 83,
    "KEY_ZENKAKUHANKAKU": 85,
    "KEY_102ND": 86,
    "KEY_F11": 87,
    "KEY_F12": 88,
    "KEY_RO": 89,
    "KEY_KATAKANA": 90,
    "KEY_HIRAGANA": 91,
    "KEY_HENKAN": 92,
    "KEY_KATAKANAHIRAGANA": 93,
    "KEY_MUHENKAN": 94,
    "KEY_KPJPCOMMA": 95,
    "KEY_KPENTER": 96,
    "KEY_RIGHTCTRL": 97,
    "KEY_KPSLASH": 98,
    "KEY_SYSRQ": 99,
    "KEY_RIGHTALT": 100,
    "KEY_LINEFEED": 101,
    "KEY_HOME": 102,
    "KEY_UP": 103,
    "KEY_PAGEUP": 104,
    "KEY_LEFT": 105,
    "KEY_RIGHT": 106,
    "KEY_END": 107,
    "KEY_DOWN": 108,
    "KEY_PAGEDOWN": 109,
    "KEY_INSERT": 110,
    "KEY_DELETE": 111,
    "KEY_MACRO": 112,
    "KEY_MUTE": 113,
    "KEY_VOLUMEDOWN": 114,
    "KEY_VOLUMEUP": 115,
    "KEY_POWER": 116,
    "KEY_KPEQUAL": 117,
    "KEY_KPPLUSMINUS": 118,
    "KEY_PAUSE": 119,
    "KEY_SCALE": 120,
    "KEY_KPCOMMA": 121,
    "KEY_HANGEUL": 122,
    "KEY_HANGUEL": 122,
    "KEY_HANJA": 123,
    "KEY_YEN": 124,
    "KEY_LEFTMETA": 125,
    "KEY_RIGHTMETA": 126,
    "KEY_COMPOSE": 127,
    "KEY_STOP": 128,
    "KEY_AGAIN": 129,
    "KEY_PROPS": 130,
    "KEY_UNDO": 131,
    "KEY_FRONT": 132,
    "KEY_COPY": 133,
    "KEY_OPEN": 134,
    "KEY_PASTE": 135,
    "KEY_FIND": 136,
    "KEY_CUT": 137,
    "KEY_HELP": 138,
    "KEY_MENU": 139,
    "KEY_CALC": 140,
    "KEY_SETUP": 141,
    "KEY_SLEEP": 142,
    "KEY_WAKEUP": 143,
    "KEY_FILE": 144,
    "KEY_SENDFILE": 145,
    "KEY_DELETEFILE": 146,
    "KEY_XFER": 147,
    "KEY_PROG1": 148,
    "KEY_PROG2": 149,
    "KEY_WWW": 150,
    "KEY_MSDOS": 151,
    "KEY_COFFEE": 152,
    "KEY_SCREENLOCK": 152,
    "KEY_ROTATE_DISPLAY": 153,
    "KEY_DIRECTION": 153,
    "KEY_CYCLEWINDOWS": 154,
    "KEY_MAIL": 155,
    "KEY_BOOKMARKS": 156,
    "KEY_COMPUTER": 157,
    "KEY_BACK": 158,
    "KEY_FORWARD": 159,
    "KEY_CLOSECD": 160,
    "KEY_EJECTCD": 161,
    "KEY_EJECTCLOSECD": 162,
    "KEY_NEXTSONG": 163,
    "KEY_PLAYPAUSE": 164,
    "KEY_PREVIOUSSONG": 165,
    "KEY_STOPCD": 166,
    "KEY_RECORD": 167,
    "KEY_REWIND": 168,
    "KEY_PHONE": 169,
    "KEY_ISO": 170,
    "KEY_CONFIG": 171,
    "KEY_HOMEPAGE": 172,
    "KEY_REFRESH": 173,
    "KEY_EXIT": 174,
    "KEY_MOVE": 175,
    "KEY_EDIT": 176,
    "KEY_SCROLLUP": 177,
    "KEY_SCROLLDOWN": 178,
    "KEY_KPLEFTPAREN": 179,
    "KEY_KPRIGHTPAREN": 180,
    "KEY_NEW": 181,
    "KEY_REDO": 182,
    "KEY_F13": 183,
    "KEY_F14": 184,
    "KEY_F15": 185,
    "KEY_F16": 186,
    "KEY_F17": 187,
    "KEY_F18": 188,
    "KEY_F19": 189,
    "KEY_F20": 190,
    "KEY_F21": 191,
    "KEY_F22": 192,
    "KEY_F23": 193,
    "KEY_F24": 194,
    "KEY_PLAYCD": 200,
    "KEY_PAUSECD": 201,
    "KEY_PROG3": 202,
    "KEY_PROG4": 203,
    "KEY_ALL_APPLICATIONS": 204,
    "KEY_DASHBOARD": 204,
    "KEY_SUSPEND": 205,
    "KEY_CLOSE": 206,
    "KEY_PLAY": 207,
    "KEY_FASTFORWARD": 208,
    "KEY_BASSBOOST": 209,
    "KEY_PRINT": 210,
    "KEY_HP": 211,
    "KEY_CAMERA": 212,
    "KEY_SOUND": 213,
    "KEY_QUESTION": 214,
    "KEY_EMAIL": 215,
    "KEY_CHAT": 216,
    "KEY_SEARCH": 217,
    "KEY_CONNECT": 218,
    "KEY_FINANCE": 219,
    "KEY_SPORT": 220,
    "KEY_SHOP": 221,
    "KEY_ALTERASE": 222,
    "KEY_CANCEL": 223,
    "KEY_BRIGHTNESSDOWN": 224,
    "KEY_BRIGHTNESSUP": 225,
    "KEY_MEDIA": 226,
    "KEY_SWITCHVIDEOMODE": 227,
    "KEY_KBDILLUMTOGGLE": 228,
    "KEY_KBDILLUMDOWN": 229,
    "KEY_KBDILLUMUP": 230,
    "KEY_SEND": 231,
    "KEY_REPLY": 232,
    "KEY_FORWARDMAIL": 233,
    "KEY_SAVE": 234,
    "KEY_DOCUMENTS": 235,
    "KEY_BATTERY": 236,
    "KEY_BLUETOOTH": 237,
    "KEY_WLAN": 238,
    "KEY_UWB": 239,
    "KEY_UNKNOWN": 240,
    "KEY_VIDEO_NEXT": 241,
    "KEY_VIDEO_PREV": 242,
    "KEY_BRIGHTNESS_CYCLE": 243,
    "KEY_BRIGHTNESS_AUTO": 244,
    "KEY_BRIGHTNESS_ZERO": 244,
    "KEY_DISPLAY_OFF": 245,
    "KEY_WWAN": 246,
    "KEY_WIMAX": 246,
    "KEY_RFKILL": 247,
    "KEY_MICMUTE": 248,
    "BTN_MISC": 0x100,
    "BTN_0": 0x100,
    "BTN_1": 0x101,
    "BTN_2": 0x102,
    "BTN_3": 0x103,
    "BTN_4": 0x104,
    "BTN_5": 0x105,
    "BTN_6": 0x106,
    "BTN_7": 0x107,
    "BTN_8": 0x108,
    "BTN_9": 0x109,
    "BTN_MOUSE": 0x110,
    "BTN_LEFT": 0x110,
    "BTN_RIGHT": 0x111,
    "BTN_MIDDLE": 0x112,
    "BTN_SIDE": 0x113,
    "BTN_EXTRA": 0x114,
    "BTN_FORWARD": 0x115,
    "BTN_BACK": 0x116,
    "BTN_TASK": 0x117,
    "BTN_JOYSTICK": 0x120,
    "BTN_TRIGGER": 0x120,
    "BTN_THUMB": 0x121,
    "BTN_THUMB2": 0x122,
    "BTN_TOP": 0x123,
    "BTN_TOP2": 0x124,
    "BTN_PINKIE": 0x125,
    "BTN_BASE": 0x126,
    "BTN_BASE2": 0x127,
    "BTN_BASE3": 0x128,
    "BTN_BASE4": 0x129,
    "BTN_BASE5": 0x12A,
    "BTN_BASE6": 0x12B,
    "BTN_DEAD": 0x12F,
    "BTN_GAMEPAD": 0x130,
    "BTN_SOUTH": 0x130,
    "BTN_A": 0x130,
    "BTN_EAST": 0x131,
    "BTN_B": 0x131,
    "BTN_C": 0x132,
    "BTN_NORTH": 0x133,
    "BTN_X": 0x133,
    "BTN_WEST": 0x134,
    "BTN_Y": 0x134,
    "BTN_Z": 0x135,
    "BTN_TL": 0x136,
    "BTN_TR": 0x137,
    "BTN_TL2": 0x138,
    "BTN_TR2": 0x139,
    "BTN_SELECT": 0x13A,
    "BTN_START": 0x13B,
    "BTN_MODE": 0x13C,
    "BTN_THUMBL": 0x13D,
    "BTN_THUMBR": 0x13E,
    "BTN_DIGI": 0x140,
    "BTN_TOOL_PEN": 0x140,
    "BTN_TOOL_RUBBER": 0x141,
    "BTN_TOOL_BRUSH": 0x142,
    "BTN_TOOL_PENCIL": 0x143,
    "BTN_TOOL_AIRBRUSH": 0x144,
    "BTN_TOOL_FINGER": 0x145,
    "BTN_TOOL_MOUSE": 0x146,
    "BTN_TOOL_LENS": 0x147,
    "BTN_TOOL_QUINTTAP": 0x148,
    "BTN_STYLUS3": 0x149,
    "BTN_TOUCH": 0x14A,
    "BTN_STYLUS": 0x14B,
    "BTN_STYLUS2": 0x14C,
    "BTN_TOOL_DOUBLETAP": 0x14D,
    "BTN_TOOL_TRIPLETAP": 0x14E,
    "BTN_TOOL_QUADTAP": 0x14F,
    "BTN_WHEEL": 0x150,
    "BTN_GEAR_DOWN": 0x150,
    "BTN_GEAR_UP": 0x151,
    "KEY_OK": 0x160,
    "KEY_SELECT": 0x161,
    "KEY_GOTO": 0x162,
    "KEY_CLEAR": 0x163,
    "KEY_POWER2": 0x164,
    "KEY_OPTION": 0x165,
    "KEY_INFO": 0x166,
    "KEY_TIME": 0x167,
    "KEY_VENDOR": 0x168,
    "KEY_ARCHIVE": 0x169,
    "KEY_PROGRAM": 0x16A,
    "KEY_CHANNEL": 0x16B,
    "KEY_FAVORITES": 0x16C,
    "KEY_EPG": 0x16D,
    "KEY_PVR": 0x16E,
    "KEY_MHP": 0x16F,
    "KEY_LANGUAGE": 0x170,
    "KEY_TITLE": 0x171,
    "KEY_SUBTITLE": 0x172,
    "KEY_ANGLE": 0x173,
    "KEY_ZOOM": 0x174,
    "KEY_MODE": 0x175,
    "KEY_KEYBOARD": 0x176,
    "KEY_SCREEN": 0x177,
    "KEY_PC": 0x178,
    "KEY_TV": 0x179,
    "KEY_TV2": 0x17A,
    "KEY_VCR": 0x17B,
    "KEY_VCR2": 0x17C,
    "KEY_SAT": 0x17D,
    "KEY_SAT2": 0x17E,
    "KEY_CD": 0x17F,
    "KEY_TAPE": 0x180,
    "KEY_RADIO": 0x181,
    "KEY_TUNER": 0x182,
    "KEY_PLAYER": 0x183,
    "KEY_TEXT": 0x184,
    "KEY_DVD": 0x185,
    "KEY_AUX": 0x186,
    "KEY_MP3": 0x187,
    "KEY_AUDIO": 0x188,
    "KEY_VIDEO": 0x189,
    "KEY_DIRECTORY": 0x18A,
    "KEY_LIST": 0x18B,
    "KEY_MEMO": 0x18C,
    "KEY_CALENDAR": 0x18D,
    "KEY_RED": 0x18E,
    "KEY_GREEN": 0x18F,
    "KEY_YELLOW": 0x190,
    "KEY_BLUE": 0x191,
    "KEY_CHANNELUP": 0x192,
    "KEY_CHANNELDOWN": 0x193,
    "KEY_FIRST": 0x194,
    "KEY_LAST": 0x195,
    "KEY_AB": 0x196,
    "KEY_NEXT": 0x197,
    "KEY_RESTART": 0x198,
    "KEY_SLOW": 0x199,
    "KEY_SHUFFLE": 0x19A,
    "KEY_BREAK": 0x19B,
    "KEY_PREVIOUS": 0x19C,
    "KEY_DIGITS": 0x19D,
    "KEY_TEEN": 0x19E,
    "KEY_TWEN": 0x19F,
    "KEY_VIDEOPHONE": 0x1A0,
    "KEY_GAMES": 0x1A1,
    "KEY_ZOOMIN": 0x1A2,
    "KEY_ZOOMOUT": 0x1A3,
    "KEY_ZOOMRESET": 0x1A4,
    "KEY_WORDPROCESSOR": 0x1A5,
    "KEY_EDITOR": 0x1A6,
    "KEY_SPREADSHEET": 0x1A7,
    "KEY_GRAPHICSEDITOR": 0x1A8,
    "KEY_PRESENTATION": 0x1A9,
    "KEY_DATABASE": 0x1AA,
    "KEY_NEWS": 0x1AB,
    "KEY_VOICEMAIL": 0x1AC,
    "KEY_ADDRESSBOOK": 0x1AD,
    "KEY_MESSENGER": 0x1AE,
    "KEY_DISPLAYTOGGLE": 0x1AF,
    "KEY_BRIGHTNESS_TOGGLE": 0x1AF,
    "KEY_SPELLCHECK": 0x1B0,
    "KEY_LOGOFF": 0x1B1,
    "KEY_DOLLAR": 0x1B2,
    "KEY_EURO": 0x1B3,
    "KEY_FRAMEBACK": 0x1B4,
    "KEY_FRAMEFORWARD": 0x1B5,
    "KEY_CONTEXT_MENU": 0x1B6,
    "KEY_MEDIA_REPEAT": 0x1B7,
    "KEY_10CHANNELSUP": 0x1B8,
    "KEY_10CHANNELSDOWN": 0x1B9,
    "KEY_IMAGES": 0x1BA,
    "KEY_DEL_EOL": 0x1C0,
    "KEY_DEL_EOS": 0x1C1,
    "KEY_INS_LINE": 0x1C2,
    "KEY_DEL_LINE": 0x1C3,
    "KEY_FN": 0x1D0,
    "KEY_FN_ESC": 0x1D1,
    "KEY_FN_F1": 0x1D2,
    "KEY_FN_F2": 0x1D3,
    "KEY_FN_F3": 0x1D4,
    "KEY_FN_F4": 0x1D5,
    "KEY_FN_F5": 0x1D6,
    "KEY_FN_F6": 0x1D7,
    "KEY_FN_F7": 0x1D8,
    "KEY_FN_F8": 0x1D9,
    "KEY_FN_F9": 0x1DA,
    "KEY_FN_F10": 0x1DB,
    "KEY_FN_F11": 0x1DC,
    "KEY_FN_F12": 0x1DD,
    "KEY_FN_1": 0x1DE,
    "KEY_FN_2": 0x1DF,
    "KEY_FN_D": 0x1E0,
    "KEY_FN_E": 0x1E1,
    "KEY_FN_F": 0x1E2,
    "KEY_FN_S": 0x1E3,
    "KEY_FN_B": 0x1E4,
    "KEY_BRL_DOT1": 0x1F1,
    "KEY_BRL_DOT2": 0x1F2,
    "KEY_BRL_DOT3": 0x1F3,
    "KEY_BRL_DOT4": 0x1F4,
    "KEY_BRL_DOT5": 0x1F5,
    "KEY_BRL_DOT6": 0x1F6,
    "KEY_BRL_DOT7": 0x1F7,
    "KEY_BRL_DOT8": 0x1F8,
    "KEY_BRL_DOT9": 0x1F9,
    "KEY_BRL_DOT10": 0x1FA,
    "KEY_NUMERIC_0": 0x200,
    "KEY_NUMERIC_1": 0x201,
    "KEY_NUMERIC_2": 0x202,
    "KEY_NUMERIC_3": 0x203,
    "KEY_NUMERIC_4": 0x204,
    "KEY_NUMERIC_5": 0x205,
    "KEY_NUMERIC_6": 0x206,
    "KEY_NUMERIC_7": 0x207,
    "KEY_NUMERIC_8": 0x208,
    "KEY_NUMERIC_9": 0x209,
    "KEY_NUMERIC_STAR": 0x20A,
    "KEY_NUMERIC_POUND": 0x20B,
    "KEY_NUMERIC_A": 0x20C,
    "KEY_NUMERIC_B": 0x20D,
    "KEY_NUMERIC_C": 0x20E,
    "KEY_NUMERIC_D": 0x20F,
    "KEY_CAMERA_FOCUS": 0x210,
    "KEY_WPS_BUTTON": 0x211,
    "KEY_TOUCHPAD_TOGGLE": 0x212,
    "KEY_TOUCHPAD_ON": 0x213,
    "KEY_TOUCHPAD_OFF": 0x214,
    "KEY_CAMERA_ZOOMIN": 0x215,
    "KEY_CAMERA_ZOOMOUT": 0x216,
    "KEY_CAMERA_UP": 0x217,
    "KEY_CAMERA_DOWN": 0x218,
    "KEY_CAMERA_LEFT": 0x219,
    "KEY_CAMERA_RIGHT": 0x21A,
    "KEY_ATTENDANT_ON": 0x21B,
    "KEY_ATTENDANT_OFF": 0x21C,
    "KEY_ATTENDANT_TOGGLE": 0x21D,
    "KEY_LIGHTS_TOGGLE": 0x21E,
    "BTN_DPAD_UP": 0x220,
    "BTN_DPAD_DOWN": 0x221,
    "BTN_DPAD_LEFT": 0x222,
    "BTN_DPAD_RIGHT": 0x223,
    "KEY_ALS_TOGGLE": 0x230,
    "KEY_ROTATE_LOCK_TOGGLE": 0x231,
    "KEY_BUTTONCONFIG": 0x240,
    "KEY_TASKMANAGER": 0x241,
    "KEY_JOURNAL": 0x242,
    "KEY_CONTROLPANEL": 0x243,
    "KEY_APPSELECT": 0x244,
    "KEY_SCREENSAVER": 0x245,
    "KEY_VOICECOMMAND": 0x246,
    "KEY_ASSISTANT": 0x247,
    "KEY_BRIGHTNESS_MIN": 0x250,
    "KEY_BRIGHTNESS_MAX": 0x251,
    "KEY_KBDINPUTASSIST_PREV": 0x260,
    "KEY_KBDINPUTASSIST_NEXT": 0x261,
    "KEY_KBDINPUTASSIST_PREVGROUP": 0x262,
    "KEY_KBDINPUTASSIST_NEXTGROUP": 0x263,
    "KEY_KBDINPUTASSIST_ACCEPT": 0x264,
    "KEY_KBDINPUTASSIST_CANCEL": 0x265,
    "KEY_RIGHT_UP": 0x266,
    "KEY_RIGHT_DOWN": 0x267,
    "KEY_LEFT_UP": 0x268,
    "KEY_LEFT_DOWN": 0x269,
    "KEY_ROOT_MENU": 0x26A,
    "KEY_MEDIA_TOP_MENU": 0x26B,
    "KEY_NUMERIC_11": 0x26C,
    "KEY_NUMERIC_12": 0x26D,
    "KEY_AUDIO_DESC": 0x26E,
    "KEY_3D_MODE": 0x26F,
    "KEY_NEXT_FAVORITE": 0x270,
    "KEY_STOP_RECORD": 0x271,
    "KEY_PAUSE_RECORD": 0x272,
    "KEY_VOD": 0x273,
    "KEY_UNMUTE": 0x274,
    "KEY_FASTREVERSE": 0x275,
    "KEY_SLOWREVERSE": 0x276,
    "KEY_DATA": 0x277,
    "KEY_ONSCREEN_KEYBOARD": 0x278,
    "BTN_TRIGGER_HAPPY": 0x2C0,
    "BTN_TRIGGER_HAPPY1": 0x2C0,
    "BTN_TRIGGER_HAPPY2": 0x2C1,
    "BTN_TRIGGER_HAPPY3": 0x2C2,
    "BTN_TRIGGER_HAPPY4": 0x2C3,
    "BTN_TRIGGER_HAPPY5": 0x2C4,
    "BTN_TRIGGER_HAPPY6": 0x2C5,
    "BTN_TRIGGER_HAPPY7": 0x2C6,
    "BTN_TRIGGER_HAPPY8": 0x2C7,
    "BTN_TRIGGER_HAPPY9": 0x2C8,
    "BTN_TRIGGER_HAPPY10": 0x2C9,
    "BTN_TRIGGER_HAPPY11": 0x2CA,
    "BTN_TRIGGER_HAPPY12": 0x2CB,
    "BTN_TRIGGER_HAPPY13": 0x2CC,
    "BTN_TRIGGER_HAPPY14": 0x2CD,
    "BTN_TRIGGER_HAPPY15": 0x2CE,
    "BTN_TRIGGER_HAPPY16": 0x2CF,
    "BTN_TRIGGER_HAPPY17": 0x2D0,
    "BTN_TRIGGER_HAPPY18": 0x2D1,
    "BTN_TRIGGER_HAPPY19": 0x2D2,
    "BTN_TRIGGER_HAPPY20": 0x2D3,
    "BTN_TRIGGER_HAPPY21": 0x2D4,
    "BTN_TRIGGER_HAPPY22": 0x2D5,
    "BTN_TRIGGER_HAPPY23": 0x2D6,
    "BTN_TRIGGER_HAPPY24": 0x2D7,
    "BTN_TRIGGER_HAPPY25": 0x2D8,
    "BTN_TRIGGER_HAPPY26": 0x2D9,
    "BTN_TRIGGER_HAPPY27": 0x2DA,
    "BTN_TRIGGER_HAPPY28": 0x2DB,
    "BTN_TRIGGER_HAPPY29": 0x2DC,
    "BTN_TRIGGER_HAPPY30": 0x2DD,
    "BTN_TRIGGER_HAPPY31": 0x2DE,
    "BTN_TRIGGER_HAPPY32": 0x2DF,
    "BTN_TRIGGER_HAPPY33": 0x2E0,
    "BTN_TRIGGER_HAPPY34": 0x2E1,
    "BTN_TRIGGER_HAPPY35": 0x2E2,
    "BTN_TRIGGER_HAPPY36": 0x2E3,
    "BTN_TRIGGER_HAPPY37": 0x2E4,
    "BTN_TRIGGER_HAPPY38": 0x2E5,
    "BTN_TRIGGER_HAPPY39": 0x2E6,
    "BTN_TRIGGER_HAPPY40": 0x2E7,
}
ctypedef key_dict.iterator key_dict_iter
cdef dict[dict] letter_tmp_dict={}
ctypedef string MY_DATA_TYPE_KEY
ctypedef string MY_DATA_TYPE_VALUE
MY_DATA_TYPE_C_TYPES_KEY=ctypes.c_char_p
MY_DATA_TYPE_C_TYPES_VALUE=ctypes.c_char_p
MY_DATA_TYPE_PY_KEY=type(bytes)
MY_DATA_TYPE_PY_VALUE=type(bytes)
MY_DATA_TYPE_STR_KEY='B'
MY_DATA_TYPE_STR_VALUE='B'
ctypedef unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE] MY_UNORDERED_MAP
ctypedef unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator MY_UNORDERED_MAP_ITER
ctypedef pair[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE] ipair
ctypedef void (*pure_c_function)(ipair)
ctypedef void (*pure_c_pyfunction)(ipair)
ctypedef void (*pure_c_function_nogil)(ipair) noexcept nogil

CUSTOM_DTYPE_PY = np.dtype([
    ('a0', "q"),
    ('b0', "q"),
    ('c0', "H"),
    ('d0', "H"),
    ('e0', "I"),
], align=False)
CUSTOM_DTYPE_PY_ALIGNED = np.dtype([
            ('a0', "q"),
            ('b0', "q"),
            ('c0', "H"),
            ('d0', "H"),
            ('e0', "I"),
        ], align=True)
cdef:
    np.dtype CUSTOM_DTYPE = np.dtype([
        ('a0', "q"),
        ('b0', "q"),
        ('c0', "H"),
        ('d0', "H"),
        ('e0', "I"),
    ], align=False)

cdef packed struct custom_dtype_struct:
    long long   a0
    long long   b0
    unsigned short c0
    unsigned short d0
    unsigned int   e0

ctypedef fused arraylikepy:
    list
    tuple

cdef dict[str,tuple[str]] std_key_mapping_dict = {
    " ": ("KEY_SPACE",),
    "!": (
        "KEY_LEFTSHIFT",
        "KEY_1",
    ),
    "'": ("KEY_APOSTROPHE",),
    '"': (
        "KEY_LEFTSHIFT",
        "KEY_APOSTROPHE",
    ),
    "#": (
        "KEY_LEFTSHIFT",
        "KEY_3",
    ),
    "$": (
        "KEY_LEFTSHIFT",
        "KEY_4",
    ),
    "%": (
        "KEY_LEFTSHIFT",
        "KEY_5",
    ),
    "&": (
        "KEY_LEFTSHIFT",
        "KEY_7",
    ),
    "(": (
        "KEY_LEFTSHIFT",
        "KEY_9",
    ),
    ")": (
        "KEY_LEFTSHIFT",
        "KEY_0",
    ),
    "*": (
        "KEY_LEFTSHIFT",
        "KEY_8",
    ),
    "+": ("KEY_KPPLUS",),
    ",": ("KEY_COMMA",),
    "-": ("KEY_MINUS",),
    ".": ("KEY_DOT",),
    "/": ("KEY_SLASH",),
    "0": ("KEY_0",),
    "1": ("KEY_1",),
    "2": ("KEY_2",),
    "3": ("KEY_3",),
    "4": ("KEY_4",),
    "5": ("KEY_5",),
    "6": ("KEY_6",),
    "7": ("KEY_7",),
    "8": ("KEY_8",),
    "9": ("KEY_9",),
    ":": (
        "KEY_LEFTSHIFT",
        "KEY_SEMICOLON",
    ),
    ";": ("KEY_SEMICOLON",),
    "<": (
        "KEY_LEFTSHIFT",
        "KEY_COMMA",
    ),
    "=": ("KEY_EQUAL",),
    ">": (
        "KEY_LEFTSHIFT",
        "KEY_DOT",
    ),
    "?": ("KEY_QUESTION",),
    "@": (
        "KEY_LEFTSHIFT",
        "KEY_2",
    ),
    "A": (
        "KEY_LEFTSHIFT",
        "KEY_A",
    ),
    "B": (
        "KEY_LEFTSHIFT",
        "KEY_B",
    ),
    "C": (
        "KEY_LEFTSHIFT",
        "KEY_C",
    ),
    "D": (
        "KEY_LEFTSHIFT",
        "KEY_D",
    ),
    "E": (
        "KEY_LEFTSHIFT",
        "KEY_E",
    ),
    "F": (
        "KEY_LEFTSHIFT",
        "KEY_F",
    ),
    "G": (
        "KEY_LEFTSHIFT",
        "KEY_G",
    ),
    "H": (
        "KEY_LEFTSHIFT",
        "KEY_H",
    ),
    "I": (
        "KEY_LEFTSHIFT",
        "KEY_I",
    ),
    "J": (
        "KEY_LEFTSHIFT",
        "KEY_J",
    ),
    "K": (
        "KEY_LEFTSHIFT",
        "KEY_K",
    ),
    "L": (
        "KEY_LEFTSHIFT",
        "KEY_L",
    ),
    "M": (
        "KEY_LEFTSHIFT",
        "KEY_M",
    ),
    "N": (
        "KEY_LEFTSHIFT",
        "KEY_N",
    ),
    "O": (
        "KEY_LEFTSHIFT",
        "KEY_O",
    ),
    "P": (
        "KEY_LEFTSHIFT",
        "KEY_P",
    ),
    "Q": (
        "KEY_LEFTSHIFT",
        "KEY_Q",
    ),
    "R": (
        "KEY_LEFTSHIFT",
        "KEY_R",
    ),
    "S": (
        "KEY_LEFTSHIFT",
        "KEY_S",
    ),
    "T": (
        "KEY_LEFTSHIFT",
        "KEY_T",
    ),
    "U": (
        "KEY_LEFTSHIFT",
        "KEY_U",
    ),
    "V": (
        "KEY_LEFTSHIFT",
        "KEY_V",
    ),
    "W": (
        "KEY_LEFTSHIFT",
        "KEY_W",
    ),
    "X": (
        "KEY_LEFTSHIFT",
        "KEY_X",
    ),
    "Y": (
        "KEY_LEFTSHIFT",
        "KEY_Y",
    ),
    "Z": (
        "KEY_LEFTSHIFT",
        "KEY_Z",
    ),
    "[": ("KEY_LEFTBRACE",),
    "\n": ("KEY_ENTER",),
    "\t": ("KEY_TAB",),
    "]": ("KEY_RIGHTBRACE",),
    "^": (
        "KEY_LEFTSHIFT",
        "KEY_6",
    ),
    "_": (
        "KEY_LEFTSHIFT",
        "KEY_MINUS",
    ),
    "`": ("KEY_GRAVE",),
    "a": ("KEY_A",),
    "b": ("KEY_B",),
    "c": ("KEY_C",),
    "d": ("KEY_D",),
    "e": ("KEY_E",),
    "f": ("KEY_F",),
    "g": ("KEY_G",),
    "h": ("KEY_H",),
    "i": ("KEY_I",),
    "j": ("KEY_J",),
    "k": ("KEY_K",),
    "l": ("KEY_L",),
    "m": ("KEY_M",),
    "n": ("KEY_N",),
    "o": ("KEY_O",),
    "p": ("KEY_P",),
    "q": ("KEY_Q",),
    "r": ("KEY_R",),
    "s": ("KEY_S",),
    "t": ("KEY_T",),
    "u": ("KEY_U",),
    "v": ("KEY_V",),
    "w": ("KEY_W",),
    "x": ("KEY_X",),
    "y": ("KEY_Y",),
    "z": ("KEY_Z",),
    "{": (
        "KEY_LEFTSHIFT",
        "KEY_LEFTBRACE",
    ),
    "}": (
        "KEY_LEFTSHIFT",
        "KEY_RIGHTBRACE",
    ),
    "|": (
        "KEY_LEFTSHIFT",
        "KEY_BACKSLASH",
    ),
    "~": (
        "KEY_LEFTSHIFT",
        "KEY_GRAVE",
    ),
    "ç": (
        "KEY_LEFTALT",
        "KEY_C",
    ),
    "Ç": (
        "KEY_LEFTALT",
        "KEY_LEFTSHIFT",
        "KEY_C",
    ),
    "ß": (
        "KEY_LEFTALT",
        "KEY_S",
    ),
    "ẞ": (
        "KEY_LEFTSHIFT",
        "KEY_LEFTALT",
        "KEY_S",
    ),
    "ctrl": (
        "KEY_LEFTCTRL",
    ),
    "alt": (
        "KEY_LEFTALT",
    ),
    "shift": (
        "KEY_LEFTSHIFT",
    ),
}

#cdef:

cpdef add_key_combinations():
    cdef:
        key_dict_iter  begin = all_linux_key_events.begin()
        key_dict_iter  end = all_linux_key_events.end()
        str k1, key_suffix
        list keynamelist
    while (begin!=end):
        k1=deref(begin).first
        inc(begin)
        if k1.startswith('KEY_'):
            keynamelist=k1.split('_',maxsplit=1)
            if len(keynamelist)<2:
                continue
            key_suffix=keynamelist[1].lower()
            std_key_mapping_dict[f'ctrl+{key_suffix}']= ("KEY_LEFTCTRL", k1,)
            std_key_mapping_dict[f'shift+{key_suffix}']= ("KEY_LEFTSHIFT", k1,)
            std_key_mapping_dict[f'alt+{key_suffix}']= ("KEY_LEFTALT", k1,)
            std_key_mapping_dict[f'ctrl+alt+shift+{key_suffix}']= ("KEY_LEFTCTRL","KEY_LEFTALT","KEY_LEFTSHIFT", k1,)
            std_key_mapping_dict[f'ctrl+alt+{key_suffix}']= ("KEY_LEFTCTRL","KEY_LEFTALT", k1,)

add_key_combinations()

def create_temp_memdisk(
    subprocess_shell,
    str memdisk_path="/media/ramdisk",
    str memdisk_size="128M",
    str su_exe="su",
    **kwargs,
):
    cdef:
        str remountcmd
    remountcmd = (
        R"""
    SUEXEFILE
    check_if_mounted() {
        mountcheckervalue=0
        mountchecker="$(mount -v | grep -v 'rw' | grep 'ro' | awk 'BEGIN{FS="[\\(]+";}{print $2}' | awk 'BEGIN{FS="[\\),]+";}{if ($1 ~ /^ro$/){ print 1;exit}}')"
        echo -e "$mountchecker"
        mountcheckervalue=$((mountcheckervalue + mountchecker))
        return "$mountcheckervalue"
    }

    modr() {

        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat1
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount --all -o remount,rw -t ext4
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o remount,rw
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o remount,rw /;
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o rw&&remount /
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o rw;remount /
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount -o remount,rw /
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount --all -o remount,rw -t vfat
        else
            return 0
        fi
        if ! check_if_mounted; then
            getprop --help >/dev/null;su -c 'mount -o remount,rw /;'
        else
            return 0
        fi
        if ! check_if_mounted; then
            mount -o remount,rw /;
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -v | grep "^/" | grep -v '\\(rw,' | grep '\\(ro' | awk '{print "mount -o rw,remount " $1 " " $3}' | tr '\n' '\0' | xargs -0 -n1 su -c
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -v | grep "^/" | grep -v '\\(rw,' | grep '\\(ro' | awk '{print "mount -o rw,remount " $1 " " $3}' | su -c sh
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -v | grep "^/" | grep -v '\\(rw,' | grep '\\(ro' | awk '{system("mount -o rw,remount " $1 " " $3)}'
        else
            return 0
        fi

        if ! check_if_mounted; then
            su -c 'mount -v | grep -E "^/" | awk '\''{print "mount -o rw,remount " $1 " " $3}'\''' | tr '\n' '\0' | xargs -0 -n1 su -c
        else
            return 0
        fi

        if ! check_if_mounted; then
            mount -Ev | grep -Ev 'nodev' | grep -Ev '/proc' | grep -v '\\(rw,' | awk 'BEGIN{FS="([[:space:]]+(on|type)[[:space:]]+)|([[:space:]]+\\()"}{print "mount -o rw,remount " $1 " " $2}' | xargs -n5 | su -c
        else
            return 0
        fi

        if ! check_if_mounted; then
            su -c 'mount -v | grep -E "^/" | awk '\''{print "mount -o rw,remount " $1 " " $3}'\''' | sh su -c
        else
            return 0
        fi

        if ! check_if_mounted; then
            getprop --help >/dev/null;su -c 'mount -v | grep -E "^/" | awk '\''{print "mount -o rw,remount " $1 " " $3}'\''' | tr '\n' '\0' | xargs -0 -n1 | su -c sh
        else
            return 0
        fi
    return 1
    }
    if [ ! -e "MYMEMDISKPATH" ]; then
        if ! modr 2>/dev/null; then
            echo -e "FALSEFALSEFALSE"
        else
            echo -e "TRUETRUETRUE"
        fi
        mkdir -p MYMEMDISKPATH
        mount -t tmpfs -o size=SIZEOFMYMEMDISK tmpfs MYMEMDISKPATH
    fi

    """.replace("MYMEMDISKPATH", memdisk_path)
        .replace("SUEXEFILE", su_exe)
        .replace("SIZEOFMYMEMDISK", str(memdisk_size))
    )

    try:
        return sru(subprocess_shell,**{**{'env':os.environ,'cwd':os.getcwd(),'shell':True,'capture_output':False},**kwargs},input=remountcmd.encode(),)
    except Exception:
        if config_settings.debug_enabled:
            errwrite()


cpdef size_t convert_to_c_function(object fu):
    CMPFUNC = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
    cmp_func = CMPFUNC(fu)
    _func_cache.append(cmp_func)
    return ctypes.addressof(cmp_func)

cpdef size_t convert_to_c_pyfunction(object fu):
    CMPFUNC = ctypes.PYFUNCTYPE(None, ctypes.c_void_p)
    cmp_func = CMPFUNC(fu)
    _func_cache.append(cmp_func)
    return ctypes.addressof(cmp_func)

cpdef vector[MY_DATA_TYPE_KEY]  _getiter_key(i):
    cdef:
        vector[MY_DATA_TYPE_KEY] keyvec
        Py_ssize_t iterloop
    if not isinstance(i,(str,bytes)):
        try:
            for iterloop in range(len(i)):
                keyvec.push_back(i[iterloop])
        except Exception:
            keyvec.push_back(i)
    else:
        keyvec.push_back(i)
    return keyvec

cpdef vector[MY_DATA_TYPE_VALUE]  _getiter_val(i):
    cdef:
        vector[MY_DATA_TYPE_VALUE] keyvec
        Py_ssize_t iterloop
    if not isinstance(i,(str,bytes)):
        try:
            for iterloop in range(len(i)):
                keyvec.push_back(i[iterloop])
        except Exception:
            keyvec.push_back(i)
    else:
        keyvec.push_back(i)
    return keyvec


cdef class CppUMap:
    cdef MY_UNORDERED_MAP v

    def __init__(self,*args,**kwargs):
        if len(args)>0:
            self.v.reserve(len(args[0]))
            for k,v in args[0].items():
                try:
                    self.v[k]=v
                except Exception:
                    self.v[<string>k.encode()] = v


    cpdef print_data(self):
        for k,v in self.sorted().items():
            print(f'{str(k).ljust(30)}\t:\t{ascii(v)}')

    def __str__(self):
        self.print_data()
        return ""

    def __len__(self):
        return self.v.size()

    def __getitem__(self, key):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  it
        if isinstance(key,str):
            key=key.encode()
        it = self.v.find(key)
        if it == self.v.end():
            newkey="".join(lookup(key.decode('utf-8','ignore'), case_sens = True, replace="", add_to_printable = "")["suggested"]).encode()
            it = self.v.find(newkey)
            if it == self.v.end():
                raise KeyError(f'{key} not found')
            return deref(it).second
        return deref(it).second

    cpdef getitems(self,i):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE] resultmap = {}
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_KEY] keyvec = _getiter_key(i)
            vector[MY_DATA_TYPE_KEY].iterator vec_begin=keyvec.begin()
            vector[MY_DATA_TYPE_KEY].iterator vec_end=keyvec.end()
        with nogil:
            while (vec_begin!=vec_end):
                while (begin!=end):

                    if deref(begin).first == deref(vec_begin):
                        resultmap[deref(begin).first]=deref(begin).second
                        break
                    else:
                        inc(begin)
                begin = self.v.begin()
                end = self.v.end()
                inc(vec_begin)
        return resultmap

    def __setitem__(self, key, value):
        try:
            self.v[key] = value
        except Exception:
            self.v[<string>key.encode()] = value

    cpdef void set_np(self, np.ndarray keys, np.ndarray values):
        cdef:
            Py_ssize_t key_array_len=keys.shape[0]
            Py_ssize_t indi
        for indi in range(key_array_len):
            try:
                self.v[keys[indi]]=values[indi]
            except Exception:
                self.v[<string>keys[indi].encode()] = values[indi]
    cpdef void set_tuple_list(self,list[tuple] keys_values):
        cdef:
            Py_ssize_t key_array_len=len(keys_values)
            Py_ssize_t indi
        for indi in range(key_array_len):
            self.v[keys_values[indi][0]]=keys_values[indi][1]

    cpdef get(self, key, default=None):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  it
        if isinstance(key,str):
            key=key.encode()
        it = self.v.find(key)
        if it == self.v.end():
            return default
        return deref(it).second


    def __repr__(self):
        return self.__str__()


    def __delitem__(self, i):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_KEY] keyvec = _getiter_key(i)
            vector[MY_DATA_TYPE_KEY].iterator vec_begin=keyvec.begin()
            vector[MY_DATA_TYPE_KEY].iterator vec_end=keyvec.end()
        with nogil:
            while (vec_begin!=vec_end):
                while (begin!=end):

                    if deref(begin).first == deref(vec_begin):
                        begin=self.v.erase(begin)
                        break
                    else:
                        inc(begin)
                begin = self.v.begin()
                end = self.v.end()
                inc(vec_begin)
    cpdef del_by_values(self, i):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_VALUE] keyvec = _getiter_val(i)
            vector[MY_DATA_TYPE_VALUE].iterator vec_begin=keyvec.begin()
            vector[MY_DATA_TYPE_VALUE].iterator vec_end=keyvec.end()
            Py_ssize_t iterloop
        with nogil:
            while (vec_begin!=vec_end):
                while (begin!=end):
                    if deref(begin).second == deref(vec_begin):
                        begin=self.v.erase(begin)
                    else:
                        inc(begin)
                begin = self.v.begin()
                end = self.v.end()
                inc(vec_begin)

    cpdef del_by_key_and_value(self, list[tuple] i):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_KEY] keyvec
            vector[MY_DATA_TYPE_KEY].iterator key_vec_begin
            vector[MY_DATA_TYPE_KEY].iterator key_vec_end
            vector[MY_DATA_TYPE_VALUE] valvec
            vector[MY_DATA_TYPE_VALUE].iterator val_vec_begin
            vector[MY_DATA_TYPE_VALUE].iterator val_vec_end
            Py_ssize_t iterloop
        for iterloop in range(len(i)):
            keyvec.push_back(i[iterloop][0])
            valvec.push_back(i[iterloop][1])
        key_vec_begin=keyvec.begin()
        key_vec_end=keyvec.end()
        val_vec_begin=valvec.begin()
        val_vec_end=valvec.end()
        with nogil:
            while (key_vec_begin!=key_vec_end) and (val_vec_begin!=val_vec_end):
                while (begin!=end):
                    if (deref(begin).first == deref(key_vec_begin)) and (deref(begin).second == deref(val_vec_begin)):
                        begin=self.v.erase(begin)
                    else:
                        inc(begin)
                begin = self.v.begin()
                end = self.v.end()
                inc(key_vec_begin)
                inc(val_vec_begin)

    cpdef dict sorted(self,key=None,bint reverse=False):
        return {k1:v1 for k1,v1 in sorted(dict(self.v).items(),key=key,reverse=reverse)}

    def __iter__(self):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
        while (begin!=end):
            yield deref(begin).first
            inc(begin)
    cpdef keys(self):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_KEY] resultvector
        resultvector.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                resultvector.push_back(deref(begin).first)
                inc(begin)
        return resultvector
    cpdef values(self):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[MY_DATA_TYPE_VALUE] resultvector
        resultvector.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                resultvector.push_back(deref(begin).second)
                inc(begin)
        return resultvector
    cpdef items(self):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            vector[ipair] resultvector
        resultvector.reserve(self.v.size())
        with nogil:
            while (begin!=end):
                resultvector.push_back(ipair(deref(begin).first, deref(begin).second))
                inc(begin)
        return resultvector

    cpdef dict to_dict(self):
        return dict(self.v)

    cpdef pop(self, i):
        x = self.__getitem__(i)
        self.__delitem__(i)
        return x

    cpdef void update(self,object other):
        for k,v in other.items():
            try:
                self.v[k] = v
            except Exception:
                self.v[<string>k.encode()] = v

    cpdef copy(self):
        newclass=self.__class__()
        newclass.update(self.v)
        return newclass

    cpdef void append(self, MY_DATA_TYPE_KEY key, MY_DATA_TYPE_VALUE value):
        self.v.insert(ipair(key,value))

    cpdef list apply_function(self,object fu):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            list results=[]
        while (begin!=end):
            results.append(fu(deref(begin).first,deref(begin).second))
            inc(begin)
        return results

    cpdef void apply_as_c_function(self,object function):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            size_t fu=convert_to_c_function(function)
            pure_c_function cfu = (<pure_c_function*>fu)[0]
        for_each(begin,end,cfu)

    cpdef void apply_as_c_function_nogil(self,object function):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            size_t fu=convert_to_c_function(function)
            pure_c_function cfu = (<pure_c_function_nogil*>fu)[0]
        for_each(begin,end,cfu)

    cpdef void apply_as_c_pyfunction(self,object function):
        cdef:
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  begin = self.v.begin()
            unordered_map[MY_DATA_TYPE_KEY,MY_DATA_TYPE_VALUE].iterator  end = self.v.end()
            size_t fu=convert_to_c_pyfunction(function)
            pure_c_pyfunction cfu = (<pure_c_pyfunction*>fu)[0]
        for_each(begin,end,cfu)


cpdef dict lookup(
    str l, bint case_sens = True, str replace="", str add_to_printable = ""
):
    cdef:
        list v
        bint is_printable_letter, is_printable,is_capital
        str sug,stri_pri
    foundletter=letter_tmp_dict.get((l,case_sens,replace,add_to_printable), None)
    if foundletter:
        return foundletter
    v = sorted(unicodedata.name(l).split(), key=len)
    sug = replace
    stri_pri = printable + add_to_printable.upper()
    is_printable_letter = v[0] in stri_pri
    is_printable = l in stri_pri
    is_capital = "CAPITAL" in v
    if is_printable_letter:
        sug = v[0]

        if case_sens:
            if not is_capital:
                sug = v[0].lower()
    elif is_printable:
        sug = l
    letter_tmp_dict[(l,case_sens,replace,add_to_printable)] = {
        "all_data": v,
        "is_printable_letter": is_printable_letter,
        "is_printable": is_printable,
        "is_capital": is_capital,
        "suggested": sug,
    }
    return letter_tmp_dict[(l,case_sens,replace,add_to_printable)]

cpdef generate_keystrokes_dict():
    cdef:
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray= np.zeros(6,dtype=CUSTOM_DTYPE_PY)
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray1=np.zeros(3,dtype=CUSTOM_DTYPE_PY)
        custom_dtype_struct[:] s
        custom_dtype_struct[:] s1
        dict[str,bytes] resultmap = {}
        dict[str,bytes] resultmap_press = {}
        dict[str,bytes] resultmap_release = {}
        key_dict.iterator  begin = all_linux_key_events.begin()
        key_dict.iterator  end = all_linux_key_events.end()
        Py_ssize_t c=0
        Py_ssize_t c1=0
        long random_number1=(rand() % 99999) + (3 * 100000)
        long random_number2=(rand() % 99999) + (4 * 100000)
        long tstamp=int(time())
        int aligned_array_itemsize
    s=struarray
    s1=struarray1
    aligned_array_itemsize=struarray.astype(CUSTOM_DTYPE_PY_ALIGNED).itemsize
    while (begin!=end):
        random_number1=(rand() % 99999) + (3 * 100000)
        random_number2=(rand() % 99999) + (4 * 100000)
        c=0
        (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number1, 4, 4, <unsigned int>deref(begin).second)
        c+=1
        (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number1, 1, deref(begin).second, 1)
        c+=1
        (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number1, 0, 0, 0)
        c+=1
        c1=0
        (s1[c1].a0, s1[c1].b0, s1[c1].c0, s1[c1].d0, s1[c1].e0)=(tstamp, random_number1, 4, 4, <unsigned int>deref(begin).second)
        c1+=1
        (s1[c1].a0, s1[c1].b0, s1[c1].c0, s1[c1].d0, s1[c1].e0)=(tstamp, random_number1, 1, deref(begin).second, 1)
        c1+=1
        (s1[c1].a0, s1[c1].b0, s1[c1].c0, s1[c1].d0, s1[c1].e0)=(tstamp, random_number1, 0, 0, 0)
        resultmap_press[deref(begin).first] =b"".join(struarray1.astype(CUSTOM_DTYPE_PY_ALIGNED).view(f'V{aligned_array_itemsize}'))
        c1=0
        (s1[c1].a0, s1[c1].b0, s1[c1].c0, s1[c1].d0, s1[c1].e0)=(tstamp, random_number2, 4, 4,  <unsigned int> deref(begin).second)
        c1+=1
        (s1[c1].a0, s1[c1].b0, s1[c1].c0, s1[c1].d0, s1[c1].e0)=(tstamp, random_number2, 1, deref(begin).second, 0)
        c1+=1
        (s1[c1].a0, s1[c1].b0, s1[c1].c0, s1[c1].d0, s1[c1].e0)=(tstamp, random_number2, 0, 0, 0)
        resultmap_release[deref(begin).first] =b"".join(struarray1.astype(CUSTOM_DTYPE_PY_ALIGNED).view(f'V{aligned_array_itemsize}'))
        (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number2, 4, 4,  <unsigned int>deref(begin).second)
        c+=1
        (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number2, 1, deref(begin).second, 0)
        c+=1
        (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number2, 0, 0, 0)
        resultmap[deref(begin).first] =b"".join(struarray.astype(CUSTOM_DTYPE_PY_ALIGNED).view(f'V{aligned_array_itemsize}'))
        inc(begin)
    return resultmap,resultmap_press,resultmap_release


cpdef tuple[dict] generate_mnouse_commands():
    cdef:
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray= np.zeros(4,dtype=CUSTOM_DTYPE_PY)
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray1=np.zeros(2,dtype=CUSTOM_DTYPE_PY)
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray2=np.zeros(2,dtype=CUSTOM_DTYPE_PY)
        custom_dtype_struct[:] s,s1,s2,s3,s4,s5
        dict[str,bytes] resultmap = {}
        dict[str,bytes] resultmap_press = {}
        dict[str,bytes] resultmap_release = {}
        bytes r1,r2,r3
        long random_number1=(rand() % 99999) + (3 * 100000)
        long random_number2=(rand() % 99999) + (4 * 100000)
        long tstamp=int(time())
        dict mouse_commands={
        'BTN_MOUSE': [(tstamp, random_number2, 1, 0x110, 1), (tstamp, random_number2, 0, 0, 0), (tstamp, random_number1, 1, 0x110, 0),(tstamp, random_number1, 0, 0, 0),],
        'BTN_RIGHT':[(tstamp, random_number2, 1, 0x111, 1), (tstamp, random_number2, 0, 0, 0), (tstamp, random_number1, 1, 0x111, 0),(tstamp, random_number1, 0, 0, 0),],
        'BTN_MIDDLE':[(tstamp, random_number2, 1, 0x112, 1), (tstamp, random_number2, 0, 0, 0), (tstamp, random_number1, 1, 0x112, 0),(tstamp, random_number1, 0, 0, 0),],
        'BTN_SIDE':[(tstamp, random_number2, 1, 0x113, 1), (tstamp, random_number2, 0, 0, 0), (tstamp, random_number1, 1, 0x113, 0),(tstamp, random_number1, 0, 0, 0),],
        'BTN_EXTRA':[(tstamp, random_number2, 1, 0x114, 1), (tstamp, random_number2, 0, 0, 0), (tstamp, random_number1, 1, 0x114, 0),(tstamp, random_number1, 0, 0, 0),],
        'SCROLL_DOWN':[(tstamp, random_number1, 2, 8, 4294967295),(tstamp, random_number1, 0, 0, 0),(tstamp, random_number1, 2, 8, 4294967295),(tstamp, random_number1, 0, 0, 0)],
        'SCROLL_UP':[(tstamp, random_number2, 2, 8, 1),(tstamp, random_number2, 0, 0, 0),(tstamp, random_number2, 2, 8, 1),(tstamp, random_number2, 0, 0, 0)],
        }
        Py_ssize_t c=0
        Py_ssize_t c1=0
        Py_ssize_t c2=0
        int aligned_array_itemsize

    s=struarray
    s1=struarray1
    s2=struarray2
    aligned_array_itemsize=struarray.astype(CUSTOM_DTYPE_PY_ALIGNED).itemsize
    for key,item in mouse_commands.items():
        if len(item)==4:
            c=0
            c1=0
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0) = item[0]
            (s1[c1].a0, s1[c1].b0, s1[c1].c0, s1[c1].d0, s1[c1].e0) = item[0]
            c1+=1
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0) = item[1]
            (s1[c1].a0, s1[c1].b0, s1[c1].c0, s1[c1].d0, s1[c1].e0) = item[1]
            c+=1
            c2=0
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0) = item[2]
            (s2[c2].a0, s2[c2].b0, s2[c2].c0, s2[c2].d0, s2[c2].e0)  = item[2]
            c+=1
            c2+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0) = item[3]
            (s2[c2].a0, s2[c2].b0, s2[c2].c0, s2[c2].d0, s2[c2].e0)  = item[3]
            r1=b"".join(struarray1.astype(CUSTOM_DTYPE_PY_ALIGNED).view(f'V{aligned_array_itemsize}'))
            r2=b"".join(struarray2.astype(CUSTOM_DTYPE_PY_ALIGNED).view(f'V{aligned_array_itemsize}'))
            r3=b"".join(struarray.astype(CUSTOM_DTYPE_PY_ALIGNED).view(f'V{aligned_array_itemsize}'))
            resultmap_press[key.encode()] =r1+r1
            resultmap_release[key.encode()] =r2+r2
            resultmap[key.encode()] =r3+r3

    return resultmap,resultmap_press,resultmap_release

def _get_current_mouse_position(
    object shellcmd="sh",
    str su_exe="su",
    str device="/dev/input/event5",
    str getevent="getevent",
    **kwargs,
):
    cdef:
        bytes cmd2execute
        object p
    if su_exe:
        cmd2execute=f"{su_exe}\n{getevent} -lp {device}".encode("utf-8")
    else:
        cmd2execute=f"{getevent} -lp {device}".encode("utf-8")
    p = subprocess.run(
        shellcmd,
        input=cmd2execute,
        capture_output=True,
        **{**{"shell":True,'env':os.environ,'cwd':os.getcwd()},**kwargs,}
    )
    return p.stdout, p.stderr, p.returncode

def get_current_mouse_screen_position(
    object shellcmd="sh",
    str su_exe="su",
    str device="/dev/input/event5",
    str getevent="getevent",
    int screen_width=720,
    int screen_height=1280,
    bytes regex_for_coords=rb"_([XY])\b\s+[^\d]+(\d+)[^\d].*max\s+(\d+)",
    **kwargs,
):
    cdef:
        object mstdout, mstderr, mreturncode
        list regex_results
        Py_ssize_t xcoordnow = 0
        Py_ssize_t ycoordnow = 0
        list x_ycoords
    mstdout, mstderr, mreturncode = _get_current_mouse_position(
        shellcmd=shellcmd, su_exe=su_exe, device=device, getevent=getevent, **kwargs
    )
    regex_results = re.findall(regex_for_coords, mstdout)

    if regex_results:
        x_ycoords = sorted(regex_results)
        if len(x_ycoords) > 1:
            try:
                if len(x_ycoords[0]) > 2:
                    xcoordnow = int(
                        int(x_ycoords[0][1]) / int(x_ycoords[0][2]) * screen_width
                    )

                if len(x_ycoords[1]) > 2:
                    ycoordnow = int(
                        int(x_ycoords[1][1]) / int(x_ycoords[1][2]) * screen_height
                    )
            except Exception as e:
                if config_settings.debug_enabled:
                    errwrite()
        else:
            if config_settings.debug_enabled:
                print(mstdout, mstderr, mreturncode)
    if xcoordnow < 0:
        xcoordnow = 0
    if xcoordnow > screen_width:
        xcoordnow = screen_width
    if ycoordnow < 0:
        ycoordnow = 0
    if ycoordnow > screen_height:
        ycoordnow = screen_height
    return xcoordnow, ycoordnow

cpdef myvector bresenham_line(int x1, int y1, int x2, int y2) noexcept nogil:
    cdef:
        myvector positions
        int dx = abs(x2 - x1)
        int dy = abs(y2 - y1)
        int sx = 1 if x1 < x2 else -1
        int sy = 1 if y1 < y2 else -1
        int err = dx - dy
        int e2
    positions.reserve((dx+dy)*5)
    while True:
        positions.push_back(mypair(x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return positions



cdef int add_swipe_closing_command(Py_ssize_t c, custom_dtype_struct[:] s, long tstamp, long random_number):
    (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 2, 0)
    c+=1
    (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 0, 0)
    c+=1
    (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 2, 0)
    c+=1
    (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 0, 0)
    c+=1
    (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 2, 0)
    c+=1
    (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 0, 0)
    c+=1
    (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 2, 0)
    c+=1
    (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 0, 0)
    return 0

cpdef create_swipe_command_through_points(
    long tstamp,
    object x_y_coordinates,
    int x_max,
    int screen_width,
    int y_max,
    int screen_height,
    long max_variationx=5,
    long max_variationy=5,
    unsigned short cmdcode_1_0=3,
    unsigned short cmdcode_1_1=53,
    unsigned short cmdcode_2_0=3,
    unsigned short cmdcode_2_1=54,
    long random_number_start=100,
    long random_number_switch=1,):
    cdef:
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray
        custom_dtype_struct[:] s
        myvector allcoords,tempcoords
        Py_ssize_t coordsize,j
        Py_ssize_t c=0
        long random_number=random_number_start
        long pressure_counter=0
        Py_ssize_t  allcoords_size
        unsigned int new_x
        unsigned int new_y
        unsigned int add_variations_x=0
        unsigned int add_variations_y=0
        list[tuple] allvariations
        Py_ssize_t tempcoords_ind, cmdsize_index, tmpa
        list tmpalist
        Py_ssize_t commandsize=4

    allvariations=list(
        zip(
            x_y_coordinates[: len(x_y_coordinates) - 1],
            [*x_y_coordinates[1:], x_y_coordinates[len(x_y_coordinates) - 1]],
        )
    )
    for tmpa in range(len(allvariations)):
        tmpalist=list(allvariations[tmpa])
        if not tmpalist:
            continue
        tempcoords = cubic_interp1d(
                    tmpalist,
                    0,
                    0,
                    0,
                    0,
                    False,
                    False,
                    False,
                    False,
                )
        if tempcoords.size()==0:
            continue
        if tmpalist[0][0] == tempcoords[0].first and tmpalist[0][1] == tempcoords[0].second:
            for tempcoords_ind in range(tempcoords.size()):
                allcoords.push_back(tempcoords[tempcoords_ind])
        else:
            for tempcoords_ind in range(tempcoords.size()-1,-1,-1):
                allcoords.push_back(tempcoords[tempcoords_ind])
    allcoords_size = allcoords.size()
    coordsize=(allcoords_size*commandsize)+(commandsize*2)
    struarray=np.zeros(coordsize,dtype=CUSTOM_DTYPE_PY)
    s=struarray
    if random_number_switch<1:
        random_number_switch=1
    c=0
    with nogil:
        for i in range(allcoords_size):
            if pressure_counter>9:
                pressure_counter=0
            if i%(random_number_switch)==0:
                random_number=(rand() % 99999) + (pressure_counter * 100000)
                pressure_counter+=1
            if i+1==allcoords_size or i==0:
                new_x=allcoords[i].first
                new_y=allcoords[i].second
            else:
                if max_variationx>0:
                    add_variations_x=(rand() % max_variationx)
                if max_variationy>0:
                    add_variations_y=(rand() % max_variationy)
                new_x=allcoords[i].first+add_variations_x
                new_y=allcoords[i].second+add_variations_y
                if new_x>screen_width:
                    new_x=allcoords[i].first
                if new_y>screen_height:
                    new_y=allcoords[i].second
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_1_0, cmdcode_1_1, <unsigned int>(new_x * x_max / screen_width))
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_2_0, cmdcode_2_1,<unsigned int>(new_y * y_max / screen_height))
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 2, 0)
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 0, 0)
            c+=1
    add_swipe_closing_command(c, struarray, tstamp, random_number)
    return struarray.astype(CUSTOM_DTYPE_PY_ALIGNED)

cpdef create_swipe_command_exact(
    long tstamp,
    int x1,
    int y1,
    int x2,
    int y2,
    int x_max,
    int screen_width,
    int y_max,
    int screen_height,
    long max_variationx=5,
    long max_variationy=5,
    unsigned short cmdcode_1_0=3,
    unsigned short cmdcode_1_1=53,
    unsigned short cmdcode_2_0=3,
    unsigned short cmdcode_2_1=54,
    long random_number_start=100,
    long random_number_switch=1,
):
    cdef:
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray

        custom_dtype_struct[:] s
        myvector allcoords = bresenham_line( x1* x_max / screen_width,  y1* y_max / screen_height,  x2* x_max / screen_width,  y2* y_max / screen_height)
        Py_ssize_t coordsize,j
        Py_ssize_t commandsize=4
        Py_ssize_t c=0
        long random_number=random_number_start
        long pressure_counter=0
        Py_ssize_t  allcoords_size = allcoords.size()
        unsigned int new_x
        unsigned int new_y
        unsigned int add_variations_x=0
        unsigned int add_variations_y=0
    coordsize=(allcoords_size*commandsize)+(commandsize*2)
    struarray=np.zeros(coordsize,dtype=CUSTOM_DTYPE_PY)
    s=struarray
    if random_number_switch<1:
        random_number_switch=1
    with nogil:
        for i in range(allcoords_size):
            if pressure_counter>9:
                pressure_counter=0
            if i%(random_number_switch)==0:
                random_number=(rand() % 99999) + (pressure_counter * 100000)
                pressure_counter+=1
            if i+1==allcoords_size or i==0:
                new_x=allcoords[i].first
                new_y=allcoords[i].second
            else:
                if max_variationx>0:
                    add_variations_x=(rand() % max_variationx)
                if max_variationy>0:
                    add_variations_y=(rand() % max_variationy)
                new_x=allcoords[i].first+add_variations_x
                new_y=allcoords[i].second+add_variations_y
                if new_x>x_max:
                    new_x=allcoords[i].first
                if new_y>y_max:
                    new_y=allcoords[i].second
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_1_0, cmdcode_1_1, new_x)
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_2_0, cmdcode_2_1, new_y)
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 2, 0)
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 0, 0)
            c+=1
    add_swipe_closing_command(c, struarray, tstamp, random_number)
    return struarray.astype(CUSTOM_DTYPE_PY_ALIGNED)


cpdef create_swipe_command(
    long tstamp,
    int x1,
    int y1,
    int x2,
    int y2,
    int x_max,
    int screen_width,
    int y_max,
    int screen_height,
    long max_variationx=5,
    long max_variationy=5,
    unsigned short cmdcode_1_0=3,
    unsigned short cmdcode_1_1=53,
    unsigned short cmdcode_2_0=3,
    unsigned short cmdcode_2_1=54,
    long random_number_start=100,
    long random_number_switch=4  ):
    cdef:
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray

        custom_dtype_struct[:] s
        myvector allcoords = bresenham_line(x1,y1,x2,y2)
        Py_ssize_t coordsize,j
        Py_ssize_t commandsize=4
        Py_ssize_t c=0
        long random_number=random_number_start
        long pressure_counter=0
        Py_ssize_t  allcoords_size = allcoords.size()
        unsigned int new_x
        unsigned int new_y
        unsigned int add_variations_x=0
        unsigned int add_variations_y=0
    if random_number_switch<1:
        random_number_switch=1
    coordsize=(allcoords_size*commandsize)+(commandsize*2)
    struarray=np.zeros(coordsize,dtype=CUSTOM_DTYPE_PY)
    s=struarray
    with nogil:
        for i in range(allcoords_size):
            if pressure_counter>9:
                pressure_counter=0
            if i%(random_number_switch)==0:
                random_number=(rand() % 99999) + (pressure_counter * 100000)
                pressure_counter+=1
            if i+1==allcoords_size or i==0:
                new_x=allcoords[i].first
                new_y=allcoords[i].second
            else:
                if max_variationx>0:
                    add_variations_x=(rand() % max_variationx)
                if max_variationy>0:
                    add_variations_y=(rand() % max_variationy)
                new_x=allcoords[i].first+add_variations_x
                new_y=allcoords[i].second+add_variations_y
                if new_x>screen_width:
                    new_x=allcoords[i].first
                if new_y>screen_height:
                    new_y=allcoords[i].second
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_1_0, cmdcode_1_1, <unsigned int>(new_x * x_max / screen_width))
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_2_0, cmdcode_2_1,<unsigned int>(new_y * y_max / screen_height))
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 2, 0)
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, 0, 0, 0)
            c+=1
    add_swipe_closing_command(c, struarray, tstamp, random_number)
    return struarray.astype(CUSTOM_DTYPE_PY_ALIGNED)


cpdef create_mouse_move_command(
    long tstamp,
    int x1,
    int y1,
    int x2,
    int y2,
    int x_max,
    int screen_width,
    int y_max,
    int screen_height,
    long max_variationx=5,
    long max_variationy=5,
    unsigned short cmdcode_1_0=3,
    unsigned short cmdcode_1_1=0,
    unsigned short cmdcode_2_0=3,
    unsigned short cmdcode_2_1=1  ):
    cdef:
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray

        custom_dtype_struct[:] s
        myvector allcoords = bresenham_line(x1,y1,x2,y2)
        Py_ssize_t coordsize,j
        Py_ssize_t commandsize=3
        Py_ssize_t c=0
        long random_number
        long pressure_counter=0
        Py_ssize_t  allcoords_size = allcoords.size()
        unsigned int new_x
        unsigned int new_y
        unsigned int add_variations_x=0
        unsigned int add_variations_y=0
    coordsize=allcoords_size*commandsize
    struarray=np.zeros(coordsize,dtype=CUSTOM_DTYPE_PY)
    s=struarray
    c=0
    with nogil:
        for i in range(allcoords_size):
            if pressure_counter>9:
                pressure_counter=0
            random_number=(rand() % 99999) + (pressure_counter * 100000)
            pressure_counter+=1
            if i+1==allcoords_size or i==0:
                new_x=allcoords[i].first
                new_y=allcoords[i].second
            else:
                if max_variationx>0:
                    add_variations_x=(rand() % max_variationx)
                if max_variationy>0:
                    add_variations_y=(rand() % max_variationy)
                new_x=allcoords[i].first+add_variations_x
                new_y=allcoords[i].second+add_variations_y
                if new_x>screen_width:
                    new_x=allcoords[i].first
                if new_y>screen_height:
                    new_y=allcoords[i].second
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_1_0, cmdcode_1_1, <unsigned int>(new_x * x_max / screen_width))
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number+1, cmdcode_2_0, cmdcode_2_1,<unsigned int>(new_y * y_max / screen_height))
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number+2, 0, 0, 0)
            c+=1
    return struarray.astype(CUSTOM_DTYPE_PY_ALIGNED)

cpdef create_mouse_move_command_exact(
    long tstamp,
    int x1,
    int y1,
    int x2,
    int y2,
    int x_max,
    int screen_width,
    int y_max,
    int screen_height,
    long max_variationx=5,
    long max_variationy=5,
    unsigned short cmdcode_1_0=3,
    unsigned short cmdcode_1_1=0,
    unsigned short cmdcode_2_0=3,
    unsigned short cmdcode_2_1=1   ):
    cdef:
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray
        custom_dtype_struct[:] s
        myvector allcoords = bresenham_line( x1* x_max / screen_width,  y1* y_max / screen_height,  x2* x_max / screen_width,  y2* y_max / screen_height)
        Py_ssize_t coordsize,j
        Py_ssize_t commandsize=3
        Py_ssize_t c=0
        long random_number
        long pressure_counter=0
        Py_ssize_t  allcoords_size = allcoords.size()
        unsigned int new_x
        unsigned int new_y
        unsigned int add_variations_x=0
        unsigned int add_variations_y=0
    coordsize=allcoords_size*commandsize
    struarray=np.zeros(coordsize,dtype=CUSTOM_DTYPE_PY)
    s=struarray
    c=0
    with nogil:
        for i in range(allcoords_size):
            if pressure_counter>9:
                pressure_counter=0
            random_number=(rand() % 99999) + (pressure_counter * 100000)
            pressure_counter+=1
            if i+1==allcoords_size or i==0:
                new_x=allcoords[i].first
                new_y=allcoords[i].second
            else:
                if max_variationx>0:
                    add_variations_x=(rand() % max_variationx)
                if max_variationy>0:
                    add_variations_y=(rand() % max_variationy)
                new_x=allcoords[i].first+add_variations_x
                new_y=allcoords[i].second+add_variations_y
                if new_x>x_max:
                    new_x=allcoords[i].first
                if new_y>y_max:
                    new_y=allcoords[i].second
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_1_0, cmdcode_1_1, new_x)
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number+1, cmdcode_2_0, cmdcode_2_1,new_y)
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number+2, 0, 0, 0)
            c+=1
    return struarray.astype(CUSTOM_DTYPE_PY_ALIGNED)


cpdef create_dd_command(
    str path_on_device_bin,
    object packed_dt,
    int command_chunk=3,
    str exec_or_eval = "exec",
    double sleepbetweencommand = 0,
    str inputdev = "/dev/input/event5",
    int blocksize = 72 * 24,
    bytes sep=b"",
    str add_su_cmd='',
):
    cdef:
        int voidformat = packed_dt.itemsize * command_chunk
        bytes binary_data
        int lendata
        int numberofloops
        str commandline, finalcmd
        str quotes = '"'
        str sleepbetweencommand_str
    binary_data = sep.join(packed_dt.view(f"V{voidformat}"))
    lendata = len(binary_data)
    numberofloops = (lendata // blocksize) + 1

    if sleepbetweencommand > 0:
        sleepbetweencommand_str = f"sleep {sleepbetweencommand}"
    else:
        sleepbetweencommand_str = ""
    if exec_or_eval == "eval":
        commandline = f"eval {quotes}dd status=none conv=sync count=1 skip=$skiphowmany bs=$blocksize if=$inputfile of=$outdevice{quotes}"
    else:
        commandline = 'dd status=none conv=sync count=1 skip="$skiphowmany" bs="$blocksize" if="$inputfile" of="$outdevice"'
    finalcmd = rf"""
{add_su_cmd}
#!/bin/sh
inputfile={path_on_device_bin}
outdevice={inputdev}
totalchars={lendata}
blocksize={blocksize}
howmanyloops={numberofloops}
skiphowmany=0
for line in $(seq 1 $howmanyloops); do
        skiphowmany=$((line-1))
        {commandline} >/dev/null 2>&1
        {sleepbetweencommand_str}
        skiphowmany=$((skiphowmany+1))
done
        """
    return binary_data, finalcmd


def logsplit(args):
    cdef:
        object iterator
        int n
    iterator = iter(args)
    for n, e in enumerate(iterator):
        yield list(chain([e], islice(iterator, n)))

def get_log_vector(Py_ssize_t a, double multiply_each_iterration):
    cdef:
        list[Py_ssize_t] logsplitlist=list(logsplit(list(range(a))))
        Py_ssize_t len_logsplitlist = len(logsplitlist)
        Py_ssize_t x,z,y
        list[Py_ssize_t] allresults
        Py_ssize_t multiply_each_iterration_int
    allresults=[]
    for x in range(len_logsplitlist):
        for z in range(len(logsplitlist[x])):
            multiply_each_iterration_int=<Py_ssize_t>(x*multiply_each_iterration)
            for y in range(multiply_each_iterration_int + 1):
                allresults.append(logsplitlist[x][z])
    return allresults


def create_mouse_move_command_natural(
    long tstamp,
    int x1,
    int y1,
    int x2,
    int y2,
    int x_max,
    int screen_width,
    int y_max,
    int screen_height,
    long max_variationx=5,
    long max_variationy=5,
    int command_chunk=3,
    unsigned short cmdcode_1_0=3,
    unsigned short cmdcode_1_1=0,
    unsigned short cmdcode_2_0=3,
    unsigned short cmdcode_2_1=1,
    double multiply_each_iterration=1.0
 ):
    cdef:
        np.ndarray packed_dt
    packed_dt=create_mouse_move_command(
    tstamp,
    x1,
    y1,
    x2,
    y2,
    x_max,
    screen_width,
    y_max,
    screen_height,
    max_variationx,
    max_variationy,
    cmdcode_1_0,
    cmdcode_1_1,
    cmdcode_2_0,
    cmdcode_2_1 )
    return np.frombuffer(packed_dt.view(f"V{packed_dt.itemsize*command_chunk}")[get_log_vector(len(packed_dt)//command_chunk,multiply_each_iterration)].tobytes(), dtype=CUSTOM_DTYPE_PY_ALIGNED)


def create_mouse_move_command_exact_natural(long tstamp,
int x1,
int y1,
int x2,
int y2,
int x_max,
int screen_width,
int y_max,
int screen_height,
long max_variationx=5,
long max_variationy=5,
int command_chunk=3,
unsigned short cmdcode_1_0=3,
unsigned short cmdcode_1_1=0,
unsigned short cmdcode_2_0=3,
unsigned short cmdcode_2_1=1 ):
    cdef:
        np.ndarray packed_dt

    packed_dt= create_mouse_move_command_exact(tstamp,
x1,
y1,
x2,
y2,
x_max,
screen_width,
y_max,
screen_height,
max_variationx,
max_variationy,
cmdcode_1_0,
cmdcode_1_1,
cmdcode_2_0,
cmdcode_2_1)
    return np.frombuffer(packed_dt.view(f"V{packed_dt.itemsize*command_chunk}")[get_log_vector(len(packed_dt)//command_chunk)].tobytes(), dtype=CUSTOM_DTYPE_PY_ALIGNED)



cdef list[list[Py_ssize_t],Py_ssize_t,Py_ssize_t,bint] _parse_coords(
    list[tuple] x_y_coordinates,
    Py_ssize_t minvalue_x=0,
    Py_ssize_t minvalue_y=0,
    Py_ssize_t maxvalue_x=0,
    Py_ssize_t maxvalue_y=0,
    bint check_minvalue_x=False,
    bint check_maxvalue_x=False,
    bint check_minvalue_y=False,
    bint check_maxvalue_y=False,
):

    cdef:
        list[tuple[Py_ssize_t]] onlyco
        Py_ssize_t x_y_coordinates_len=len(x_y_coordinates)
        tuple xycoordinate_index
        Py_ssize_t oneco_index
        list[Py_ssize_t] all_x_coords=[]
        list[Py_ssize_t] all_y_coords=[]
        dict[Py_ssize_t,Py_ssize_t] maxdict = {}
        Py_ssize_t minvalue_x_final,maxvalue_x_final,add_dummys
        bint isbad = False
        Py_ssize_t maxvalue_first_element_y,minvalue_first_element_y
        list lindspaced =[]
    onlyco = sorted([(int(ll[0]),int(ll[1])) for ll in x_y_coordinates], key=lambda x: x[0])
    maxvalue_first_element_y=onlyco[0][1]
    minvalue_first_element_y=onlyco[0][1]
    for oneco_index in range(x_y_coordinates_len):
        if onlyco[oneco_index][0] not in maxdict:
            maxdict[onlyco[oneco_index][0]] = onlyco[oneco_index][1]
        else:
            if onlyco[oneco_index][0] != onlyco[0][0]:
                if maxdict[onlyco[oneco_index][0]] < onlyco[oneco_index][1]:
                    maxdict[onlyco[oneco_index][0]] = onlyco[oneco_index][1]
            else:
                if maxdict[onlyco[oneco_index][0]] > onlyco[oneco_index][1]:
                    maxdict[onlyco[oneco_index][0]] = onlyco[oneco_index][1]
                    minvalue_first_element_y= onlyco[oneco_index][1]
                if maxvalue_first_element_y < onlyco[oneco_index][1]:
                    maxvalue_first_element_y=onlyco[oneco_index][1]

    for xycoordinate_index in maxdict.items():
        if check_minvalue_x:
            if xycoordinate_index[0] < minvalue_x:
                continue
        if check_maxvalue_x:
            if xycoordinate_index[0] > maxvalue_x:
                continue
        if check_minvalue_y:
            if xycoordinate_index[1] < minvalue_y:
                continue
        if check_maxvalue_y:
            if xycoordinate_index[1] > maxvalue_y:
                continue
        all_x_coords.append( xycoordinate_index[0])
        all_y_coords.append( xycoordinate_index[1])
    minvalue_x_final=all_x_coords[0]
    maxvalue_x_final=all_x_coords[len(all_x_coords)-1]
    if minvalue_x_final==maxvalue_x_final:
        isbad=True
        if maxvalue_first_element_y-minvalue_first_element_y>0:
            for add_dummys in range(1,maxvalue_first_element_y-minvalue_first_element_y):
                maxvalue_x_final=maxvalue_x_final+add_dummys
                all_x_coords.append(maxvalue_x_final)
            all_y_coords.extend([int(floatval) for floatval in linspace(minvalue_first_element_y,maxvalue_first_element_y,maxvalue_first_element_y-minvalue_first_element_y)])
        else:
            all_x_coords.append(minvalue_x_final+1)
            maxvalue_x_final=maxvalue_x_final+1
            all_y_coords.append(maxvalue_first_element_y)
    return  [all_x_coords,all_y_coords,minvalue_x_final,maxvalue_x_final,isbad]


cpdef cubic_interp1d(
    object x_y_coordinates,
    Py_ssize_t minvalue_x=0,
    Py_ssize_t minvalue_y=0,
    Py_ssize_t maxvalue_x=0,
    Py_ssize_t maxvalue_y=0,
    bint check_minvalue_x=False,
    bint check_maxvalue_x=False,
    bint check_minvalue_y=False,
    bint check_maxvalue_y=False,
):

    cdef:

        list xaslist_yaslist=_parse_coords(
        x_y_coordinates,
        minvalue_x=minvalue_x,
        minvalue_y=minvalue_y,
        maxvalue_x=maxvalue_x,
        maxvalue_y=maxvalue_y,
        check_minvalue_x=check_minvalue_x,
        check_maxvalue_x=check_maxvalue_x,
        check_minvalue_y=check_minvalue_y,
        check_maxvalue_y=check_maxvalue_y,)
        np.ndarray[Py_ssize_t, ndim=1, cast=False] full_x=np.array(xaslist_yaslist[0],dtype=np.int64)
        np.ndarray[Py_ssize_t, ndim=1, cast=False] full_y=np.array(xaslist_yaslist[1],dtype=np.int64)
        Py_ssize_t minxvalue = xaslist_yaslist[2]
        Py_ssize_t maxxvalue = xaslist_yaslist[3]
        bint isbad = xaslist_yaslist[4]
        Py_ssize_t size = len(full_x)
        Py_ssize_t isize = size - 1
        Py_ssize_t min_val = 1
        Py_ssize_t max_val = size - 1
        Py_ssize_t[:] x = full_x
        Py_ssize_t[:] y = full_y
        np.ndarray[Py_ssize_t, ndim=1, cast=False] full_output = np.arange(minxvalue,maxxvalue, dtype=np.int64)
        Py_ssize_t[:] output  = full_output
        Py_ssize_t x0len = len(output)
        np.ndarray[Py_ssize_t, ndim=1, cast=False] full_xdiff = np.array(diff(x),dtype=np.int64)
        Py_ssize_t[:] xdiff= full_xdiff
        np.ndarray[Py_ssize_t, ndim=1, cast=False] full_ydiff = np.array(diff(y),dtype=np.int64)
        Py_ssize_t[:] ydiff= full_ydiff
        np.ndarray[np.npy_double, ndim=1, cast=False] full_liv1= np.zeros(size, dtype=np.double)
        double[:] liv1= full_liv1
        np.ndarray[np.npy_double, ndim=1, cast=False] full_liv2= np.zeros((size - 1), dtype=np.double)
        double[:] liv2= full_liv2
        np.ndarray[np.npy_double, ndim=1, cast=False] full_z= np.zeros(size, dtype=np.double)
        double[:] z= full_z
        np.ndarray[Py_ssize_t, ndim=1, cast=False] full_x0 = np.asarray(output,dtype=np.int64).copy()
        Py_ssize_t[:] x0= full_x0
        np.ndarray[Py_ssize_t, ndim=1, cast=False] full_index= np.zeros(x0len, dtype=np.int64)
        Py_ssize_t[:] index= full_index
        Py_ssize_t indexlen=len(full_index)
        np.ndarray[np.npy_double, ndim=1, cast=False] full_xi1= np.zeros(x0len, dtype=np.double)
        double[:] xi1= full_xi1
        np.ndarray[np.npy_double, ndim=1, cast=False] full_xi0= np.zeros(x0len, dtype=np.double)
        double[:] xi0= full_xi0
        np.ndarray[np.npy_double, ndim=1, cast=False] full_yi1= np.zeros(x0len, dtype=np.double)
        double[:] yi1= full_yi1
        np.ndarray[np.npy_double, ndim=1, cast=False] full_yi0= np.zeros(x0len, dtype=np.double)
        double[:] yi0= full_yi0
        np.ndarray[np.npy_double, ndim=1, cast=False] full_zi1= np.zeros(x0len, dtype=np.double)
        double[:] zi1= full_zi1
        np.ndarray[np.npy_double, ndim=1, cast=False] full_zi0= np.zeros(x0len, dtype=np.double)
        double[:] zi0= full_zi0
        np.ndarray[np.npy_double, ndim=1, cast=False] full_hi1= np.zeros(x0len, dtype=np.double)
        double[:] hi1= full_hi1
        np.ndarray[Py_ssize_t, ndim=1, cast=False] full_resultsasint= np.zeros(x0len, dtype=np.int64)
        Py_ssize_t len_resultsasint=len(full_resultsasint)
        Py_ssize_t[:] resultsasint = full_resultsasint
        Py_ssize_t xdiff_last_index=len(xdiff)-1
        Py_ssize_t indexcounter = 0
        Py_ssize_t i,x0index,j,num_index
        double nboundry
        myvector positions
        list[unsigned int] tempbad
        Py_ssize_t len_tempbad, ind_tempbad

    with nogil:
        liv1[0] = sqrt(2 * xdiff[0])
        for i in range(1, size - 1, 1):
            liv2[i] = xdiff[i - 1] / liv1[i - 1]
            liv1[i] = sqrt(2 * (xdiff[i - 1] + xdiff[i]) - liv2[i - 1] * liv2[i - 1])
            nboundry = 6 * (ydiff[i] / xdiff[i] - ydiff[i - 1] / xdiff[i - 1])
            z[i] = (nboundry - liv2[i - 1] * z[i - 1]) / liv1[i]
        liv2[isize - 1] = xdiff[xdiff_last_index] / liv1[isize - 1]
        liv1[isize] = sqrt(2 * xdiff[xdiff_last_index] - liv2[isize - 1] * liv2[isize - 1])
        nboundry = 0.0
        z[isize] = (nboundry - liv2[isize - 1] * z[isize - 1]) / liv1[isize]
        z[isize] = z[isize] / liv1[isize]
        for i in range(size - 2, -1, -1):
            z[i] = (z[i] - liv2[i - 1] * z[i + 1]) / liv1[i]

        for x0index in range(x0len):
            for i in range(size):
                if x0[x0index] <= x[i]:
                    index[indexcounter] = i
                    indexcounter += 1
                    break
            else:
                index[indexcounter] = size
                indexcounter += 1

        for i in range(indexlen):
            if index[i] < min_val:
                index[i] = min_val
            elif index[i] > max_val:
                index[i] = max_val
        for num_index in range(x0len):
            xi1[num_index] = x[index[num_index]]
            yi1[num_index] = y[index[num_index]]
            zi1[num_index] = z[index[num_index]]
            xi0[num_index] = x[index[num_index] - 1]
            yi0[num_index] = y[index[num_index] - 1]
            zi0[num_index] = z[index[num_index] - 1]
            hi1[num_index] = xi1[num_index] - xi0[num_index]
        for j in range(len_resultsasint):
            resultsasint[j] = int(
                zi0[j] / (6 * hi1[j]) * (xi1[j] - x0[j]) ** 3
                + zi1[j] / (6 * hi1[j]) * (x0[j] - xi0[j]) ** 3
                + (yi1[j] / hi1[j] - zi1[j] * hi1[j] / 6) * (x0[j] - xi0[j])
                + (yi0[j] / hi1[j] - zi0[j] * hi1[j] / 6) * (xi1[j] - x0[j])
            )
        if isbad:
            for x0index in range(x0len):
                output[x0index]=minxvalue
            with gil:
                tempbad=sorted(set((zip(output, resultsasint))))
                for ind_tempbad in range(len(tempbad)):
                    positions.push_back(mypair(tempbad[ind_tempbad][0], tempbad[ind_tempbad][1]))
        else:
            for x0index in range(x0len):
                positions.push_back(mypair(output[x0index], resultsasint[x0index]))
    return positions

def create_mouse_move_command_through_points_natural(
    long tstamp,
    object x_y_coordinates,
    int x_max,
    int screen_width,
    int y_max,
    int screen_height,
    long max_variationx=5,
    long max_variationy=5,
    Py_ssize_t command_chunk=3,
    unsigned short cmdcode_1_0=3,
    unsigned short cmdcode_1_1=0,
    unsigned short cmdcode_2_0=3,
    unsigned short cmdcode_2_1=1,
    double multiply_each_iterration=1.0  ):
    cdef:
        np.ndarray packed_dt
    packed_dt=create_mouse_move_command_through_points(
    tstamp,
    x_y_coordinates,
    x_max,
    screen_width,
    y_max,
    screen_height,
    max_variationx,
    max_variationy,
    command_chunk,  cmdcode_1_0, cmdcode_1_1, cmdcode_2_0, cmdcode_2_1)
    return np.frombuffer(packed_dt.view(f"V{packed_dt.itemsize*command_chunk}")[get_log_vector(len(packed_dt)//command_chunk, multiply_each_iterration)].tobytes(), dtype=CUSTOM_DTYPE_PY_ALIGNED)



cpdef create_mouse_move_command_through_points(
    long tstamp,
    object x_y_coordinates,
    int x_max,
    int screen_width,
    int y_max,
    int screen_height,
    long max_variationx=5,
    long max_variationy=5,
    Py_ssize_t commandsize=3,
    unsigned short cmdcode_1_0=3,
    unsigned short cmdcode_1_1=0,
    unsigned short cmdcode_2_0=3,
    unsigned short cmdcode_2_1=1
    ):
    cdef:
        np.ndarray [custom_dtype_struct, ndim=1, cast=False] struarray
        custom_dtype_struct[:] s
        myvector allcoords,tempcoords
        Py_ssize_t coordsize,j
        Py_ssize_t c=0
        long random_number
        long pressure_counter=0
        Py_ssize_t  allcoords_size
        unsigned int new_x
        unsigned int new_y
        unsigned int add_variations_x=0
        unsigned int add_variations_y=0
        list[tuple] allvariations
        Py_ssize_t tempcoords_ind, cmdsize_index, tmpa
        list tmpalist

    allvariations=list(
        zip(
            x_y_coordinates[: len(x_y_coordinates) - 1],
            [*x_y_coordinates[1:], x_y_coordinates[len(x_y_coordinates) - 1]],
        )
    )
    for tmpa in range(len(allvariations)):
        tmpalist=list(allvariations[tmpa])
        if not tmpalist:
            continue
        tempcoords = cubic_interp1d(
                    tmpalist,
                    0,
                    0,
                    0,
                    0,
                    False,
                    False,
                    False,
                    False,
                )
        if tempcoords.size()==0:
            continue
        if tmpalist[0][0] == tempcoords[0].first and tmpalist[0][1] == tempcoords[0].second:
            for tempcoords_ind in range(tempcoords.size()):
                allcoords.push_back(tempcoords[tempcoords_ind])
        else:
            for tempcoords_ind in range(tempcoords.size()-1,-1,-1):
                allcoords.push_back(tempcoords[tempcoords_ind])
    allcoords_size = allcoords.size()
    coordsize=allcoords_size*commandsize
    struarray=np.zeros(coordsize,dtype=CUSTOM_DTYPE_PY)
    s=struarray
    c=0
    with nogil:
        for i in range(allcoords_size):
            if pressure_counter>9:
                pressure_counter=0
            random_number=(rand() % 99999) + (pressure_counter * 100000)
            pressure_counter+=1
            if i+1==allcoords_size or i==0:
                new_x=allcoords[i].first
                new_y=allcoords[i].second
            else:
                if max_variationx>0:
                    add_variations_x=(rand() % max_variationx)
                if max_variationy>0:
                    add_variations_y=(rand() % max_variationy)
                new_x=allcoords[i].first+add_variations_x
                new_y=allcoords[i].second+add_variations_y
                if new_x>screen_width:
                    new_x=allcoords[i].first
                if new_y>screen_height:
                    new_y=allcoords[i].second
            if new_x > screen_width:
                new_x=screen_width
            if new_y > screen_height:
                new_y=screen_height
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number, cmdcode_1_0, cmdcode_1_1, <unsigned int>(new_x * x_max / screen_width))
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number+1, cmdcode_2_0, cmdcode_2_1,<unsigned int>(new_y * y_max / screen_height))
            c+=1
            (s[c].a0, s[c].b0, s[c].c0, s[c].d0, s[c].e0)=(tstamp, random_number+2, 0, 0, 0)
            c+=1
    return struarray.astype(CUSTOM_DTYPE_PY_ALIGNED)

cpdef list[double] linspace(double start, double stop, Py_ssize_t number, bint endpoint=True):

    cdef:
        double num = float(number)
        double start1 = float(start)
        double stop1 = float(stop)
        double step
        list[double] results=[]
        Py_ssize_t i

    if number == 1:
        return [num]
    if endpoint:
        step = (stop1 - start1) / (num - 1)
    else:
        step = (stop1 - start1) / num
    for i in range(number):
        results.append(start1 + step * i)
    return results

cpdef list difflist(list lst):
    cdef:
        Py_ssize_t size = len(lst) - 1
        list r = [0] * size
        Py_ssize_t i

    for i in range(size):
        r[i] = lst[i + 1] - lst[i]
    return r

cdef list[Py_ssize_t] diff(Py_ssize_t[:] lst):
    cdef:
        Py_ssize_t size = len(lst) - 1
        list[Py_ssize_t] r = [0] * size
        Py_ssize_t i
    for i in range(size):
        r[i] = lst[i + 1] - lst[i]
    return r

def get_tmpfile(suffix=".bin"):
    tfp = NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    return filename


class SendeventClass:
    def __init__(
        self,

        str device_touchscreen,
        int x_max_device_touchscreen,
        int y_max_device_touchscreen,
        str device_mouse,
        int x_max_device_mouse,
        int y_max_device_mouse,
        str device_keyboard,
        int screen_width,
        int screen_height,
        str adb_path="",
        str device_serial="",
        str local_shell='',
        str local_shell_su='',
        str local_shell_su_cmd_exec='',
        tuple[unsigned short,unsigned short,unsigned short,unsigned short] mouse_move_codes=(3,0,3,1,),
        tuple[unsigned short,unsigned short,unsigned short,unsigned short] swipe_codes=(3,53,3,54,),
        str exe_su='su',
        str exe_su_cmd_exec='-c',
        str exe_sh='sh',
        str exe_getevent='getevent',
        tuple shell_for_mouse_position=(
        'adb',
        "-s",
        '127.0.0.1:5555',
        "shell",
    ),
        bytes regex_for_mouse_position=rb"_([XY])\b\s+[^\d]+(\d+)[^\d].*max\s+(\d+)",
        str add_su_to_dd_cmd='',
        str add_su_to_subprocess_cmd='',
        str add_su_to_input_subprocess='su',
        **kwargs
    ):
        self.mouse_move_codes=mouse_move_codes
        self.device_touchscreen=device_touchscreen
        self.device_mouse=device_mouse
        self.device_keyboard=device_keyboard
        self.x_max_device_touchscreen = x_max_device_touchscreen
        self.y_max_device_touchscreen = y_max_device_touchscreen
        self.x_max_device_mouse = x_max_device_mouse
        self.y_max_device_mouse = y_max_device_mouse
        self.screen_width = screen_width
        self.screen_height = screen_height
        tem_resultmap, tem_resultmap_press, tem_resultmap_release = (
            generate_keystrokes_dict()
        )
        self.key_map = CppUMap(tem_resultmap)
        self.key_map_press = CppUMap(tem_resultmap_press)
        self.key_map_release = CppUMap(tem_resultmap_release)
        add_mapping_keys(std_key_mapping_dict, self.key_map, self.key_map_press, self.key_map_release)
        self.kwargs=kwargs
        self.exe_su=exe_su
        self.exe_sh=exe_sh
        self.exe_getevent=exe_getevent
        self.shell_for_mouse_position=shell_for_mouse_position
        self.regex_for_mouse_position=regex_for_mouse_position
        self.swipe_codes=swipe_codes
        self.adb_path=adb_path
        self.device_serial=device_serial
        self.exe_su_cmd_exec=exe_su_cmd_exec
        self.local_shell=local_shell
        self.local_shell_su=local_shell_su
        self.local_shell_su_cmd_exec=local_shell_su_cmd_exec
        tem_resultmap_mouse, tem_resultmap_press_mouse, tem_resultmap_release_mouse = generate_mnouse_commands()
        self.mouse_map = CppUMap(tem_resultmap_mouse)
        self.mouse_map_press = CppUMap(tem_resultmap_press_mouse)
        self.mouse_map_release = CppUMap(tem_resultmap_release_mouse)
        self.add_su_to_dd_cmd=add_su_to_dd_cmd
        self.add_su_to_subprocess_cmd=add_su_to_subprocess_cmd
        self.add_su_to_input_subprocess=add_su_to_input_subprocess
    def map_keys(self, dict mapping_dict):
        add_mapping_keys(mapping_dict, self.key_map, self.key_map_press, self.key_map_release)
    def mouse_move_from_to(self, int x1, int y1, int x2, int y2,long max_variationx=5,long max_variationy=5):
        cdef:
            long tstamp=<long>time()
        return create_mouse_move_command(
        tstamp=tstamp,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        x_max=self.x_max_device_mouse,
        screen_width=self.screen_width,
        y_max=self.y_max_device_mouse,
        screen_height=self.screen_height,
        max_variationx=max_variationx,
        max_variationy=max_variationy,
        cmdcode_1_0=self.mouse_move_codes[0],
        cmdcode_1_1=self.mouse_move_codes[1],
        cmdcode_2_0=self.mouse_move_codes[2],
        cmdcode_2_1=self.mouse_move_codes[3],  )

    def mouse_move_from_to_natural(self, int x1, int y1, int x2, int y2,long max_variationx=5,long max_variationy=5,double multiply_each_iterration=1.0):
        cdef:
            long tstamp=<long>time()
        return create_mouse_move_command_natural(
        tstamp=tstamp,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        x_max=self.x_max_device_mouse,
        screen_width=self.screen_width,
        y_max=self.y_max_device_mouse,
        screen_height=self.screen_height,
        max_variationx=max_variationx,
        max_variationy=max_variationy,
        command_chunk=3,
        cmdcode_1_0=self.mouse_move_codes[0],
        cmdcode_1_1=self.mouse_move_codes[1],
        cmdcode_2_0=self.mouse_move_codes[2],
        cmdcode_2_1=self.mouse_move_codes[3],
        multiply_each_iterration=multiply_each_iterration)
    def mouse_move_through_coordinates(self, object x_y_coordinates,long max_variationx=5,long max_variationy=5):
        cdef:
            long tstamp=<long>time()
        return create_mouse_move_command_through_points(
    tstamp=tstamp,
    x_y_coordinates=x_y_coordinates,
    x_max=self.x_max_device_mouse,
    screen_width=self.screen_width,
    y_max=self.y_max_device_mouse,
    screen_height=self.screen_height,
    max_variationx=max_variationx,
    max_variationy=max_variationy,
    commandsize=3,
    cmdcode_1_0=self.mouse_move_codes[0],
    cmdcode_1_1=self.mouse_move_codes[1],
    cmdcode_2_0=self.mouse_move_codes[2],
    cmdcode_2_1=self.mouse_move_codes[3],
    )
    def mouse_move_through_coordinates_natural(self,object x_y_coordinates,long max_variationx=5,long max_variationy=5,double multiply_each_iterration=1.0):
        cdef:
            long tstamp=<long>time()
        return create_mouse_move_command_through_points_natural(
    tstamp=tstamp,
    x_y_coordinates=x_y_coordinates,
    x_max=self.x_max_device_mouse,
    screen_width=self.screen_width,
    y_max=self.y_max_device_mouse,
    screen_height=self.screen_height,
    max_variationx=max_variationx,
    max_variationy=max_variationy,
    command_chunk=3,
    cmdcode_1_0=self.mouse_move_codes[0],
    cmdcode_1_1=self.mouse_move_codes[1],
    cmdcode_2_0=self.mouse_move_codes[2],
    cmdcode_2_1=self.mouse_move_codes[3],
    multiply_each_iterration=multiply_each_iterration  )
    def mouse_get_position(self,**kwargs):
        return get_current_mouse_screen_position(
    shellcmd=self.shell_for_mouse_position,
    su_exe=self.exe_su,
    device=self.device_mouse,
    getevent=self.exe_getevent,
    screen_width=self.screen_width,
    screen_height=self.screen_height,
    regex_for_coords=self.regex_for_mouse_position,
    **kwargs,
)
    def mouse_move_from_current_to_natural(self, int x, int y,long max_variationx=5,long max_variationy=5,double multiply_each_iterration=1.0):
        cdef:
            tuple x1_y1=self.mouse_get_position()
        if len(x1_y1)==2:
            return self.mouse_move_from_to_natural(x1=x1_y1[0], y1=x1_y1[1], x2=x, y2=y,        max_variationx=max_variationx,
            max_variationy=max_variationy,multiply_each_iterration=multiply_each_iterration )
        else:
            raise IndexError(f'Could not get mouse coordinates: {x1_y1}')

    def mouse_move_from_current_to(self, int x, int y,long max_variationx=5,long max_variationy=5):
        cdef:
            tuple x1_y1=self.mouse_get_position()
        if len(x1_y1)==2:
            return self.mouse_move_from_to(x1=x1_y1[0], y1=x1_y1[1], x2=x, y2=y,        max_variationx=max_variationx,
            max_variationy=max_variationy, )
        else:
            raise IndexError(f'Could not get mouse coordinates: {x1_y1}')

    def mouse_move_through_coordinates_from_current(self,object x_y_coordinates,long max_variationx=5,long max_variationy=5, ):
        cdef:
            list _x_y_coordinates=list(x_y_coordinates)
            tuple x1_y1=self.mouse_get_position()
        if len(x1_y1)==2:
            _x_y_coordinates.insert(0,x1_y1)
            return self.mouse_move_through_coordinates(x_y_coordinates=_x_y_coordinates,max_variationx=max_variationx, max_variationy=max_variationy,)
        else:
            raise IndexError(f'Could not get mouse coordinates: {x1_y1}')

    def mouse_move_through_coordinates_from_current_natural(self,object x_y_coordinates,long max_variationx=5,long max_variationy=5,double multiply_each_iterration=1.0):
        cdef:
            list _x_y_coordinates=list(x_y_coordinates)
            tuple x1_y1=self.mouse_get_position()
        if len(x1_y1)==2:
            _x_y_coordinates.insert(0,x1_y1)
            return self.mouse_move_through_coordinates_natural(x_y_coordinates=_x_y_coordinates,max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        else:
            raise IndexError(f'Could not get mouse coordinates: {x1_y1}')

    def touchscreen_swipe_from_to(self, int x1, int y1, int x2, int y2,long max_variationx=5,long max_variationy=5,long random_number_start=100, long random_number_switch=4  ):
        cdef:
            long tstamp=<long>time()
        return create_swipe_command(
    tstamp=tstamp,
    x1=x1,
    y1=y1,
    x2=x2,
    y2=y2,
    x_max=self.x_max_device_touchscreen,
    screen_width=self.screen_width,
    y_max=self.y_max_device_touchscreen,
    screen_height=self.screen_height,
    max_variationx=max_variationx,
    max_variationy=max_variationy,
    cmdcode_1_0=self.swipe_codes[0],
    cmdcode_1_1=self.swipe_codes[1],
    cmdcode_2_0=self.swipe_codes[2],
    cmdcode_2_1=self.swipe_codes[3],
    random_number_start=random_number_start,
    random_number_switch=random_number_switch  )
    def touchscreen_swipe_from_to_exact(self, int x1, int y1, int x2, int y2,long max_variationx=5,long max_variationy=5,long random_number_start=100, long random_number_switch=4  ):
        cdef:
            long tstamp=<long>time()
        return create_swipe_command_exact(
    tstamp=tstamp,
    x1=x1,
    y1=y1,
    x2=x2,
    y2=y2,
    x_max=self.x_max_device_touchscreen,
    screen_width=self.screen_width,
    y_max=self.y_max_device_touchscreen,
    screen_height=self.screen_height,
    max_variationx=max_variationx,
    max_variationy=max_variationy,
    cmdcode_1_0=self.swipe_codes[0],
    cmdcode_1_1=self.swipe_codes[1],
    cmdcode_2_0=self.swipe_codes[2],
    cmdcode_2_1=self.swipe_codes[3],
    random_number_start=random_number_start,
    random_number_switch=random_number_switch  )

    def touchscreen_swipe_through_coordinates(self, object x_y_coordinates,long max_variationx=5,long max_variationy=5,long random_number_start=100, long random_number_switch=4):
        cdef:
            long tstamp=<long>time()
        return create_swipe_command_through_points(
    tstamp=tstamp,
    x_y_coordinates=x_y_coordinates,
    x_max=self.x_max_device_touchscreen,
    screen_width=self.screen_width,
    y_max=self.y_max_device_touchscreen,
    screen_height=self.screen_height,
    max_variationx=max_variationx,
    max_variationy=max_variationy,
    cmdcode_1_0=self.swipe_codes[0],
    cmdcode_1_1=self.swipe_codes[1],
    cmdcode_2_0=self.swipe_codes[2],
    cmdcode_2_1=self.swipe_codes[3],
    random_number_start=random_number_start,
    random_number_switch=random_number_switch )


    def keyboard_write_text(self,object text):
        cdef:
            object text2search
            list[bytes] allk
            Py_ssize_t textindex
        if isinstance(text, bytes):
            text2search=[x for x in text.decode()]

        elif isinstance(text,str):
            text2search=[x for x in text]
        else:
            text2search=text
        allk = []
        for textindex in range(len(text2search)):
            allk.append(self.key_map[<string>text2search[textindex].encode()])
        return np.frombuffer(b"".join(allk), dtype=CUSTOM_DTYPE_PY_ALIGNED)

    def keyboard_press_key(self,key,double duration):
        return [np.frombuffer((self.key_map_press[key]), dtype=CUSTOM_DTYPE_PY_ALIGNED),duration,np.frombuffer(self.key_map_release[key], dtype=CUSTOM_DTYPE_PY_ALIGNED)]

    def keyboard_press_key_combination(self,arraylikepy combination,double duration):
        cdef:
            list[bytes] bytedata_start = []
            list[bytes] bytedata_end = []
        for keyindex in range(len(combination)):

            bytedata_start.append(self.key_map_press[<string>combination[keyindex].encode()])
        for keyindex in range(len(combination)-1,-1,-1):
            bytedata_start.append(self.key_map_release[<string>combination[keyindex].encode()])
        return [np.frombuffer(b''.join(bytedata_start), dtype=CUSTOM_DTYPE_PY_ALIGNED),duration,np.frombuffer(b''.join(bytedata_end), dtype=CUSTOM_DTYPE_PY_ALIGNED)]

    def _press_mouse_button_long(self, key,double duration):
        return [np.frombuffer((self.mouse_map_press[<string>key]), dtype=CUSTOM_DTYPE_PY_ALIGNED),duration,np.frombuffer(self.mouse_map_release[key], dtype=CUSTOM_DTYPE_PY_ALIGNED)]
    def _press_mouse_button(self, key):
        return np.frombuffer(self.mouse_map_press[<string>key], dtype=CUSTOM_DTYPE_PY_ALIGNED)

    def mouse_btn_extra(self):
        return self._press_mouse_button(key=b"BTN_EXTRA")
    def mouse_btn_extra_long(self,double duration=1):
        return self._press_mouse_button_long(key=b"BTN_EXTRA",duration=duration)
    def mouse_btn_middle(self):
        return self._press_mouse_button(key=b"BTN_MIDDLE")
    def mouse_btn_middle_long(self,double duration=1):
        return self._press_mouse_button_long(key=b"BTN_MIDDLE",duration=duration)
    def mouse_btn_mouse(self):
        return self._press_mouse_button(key=b"BTN_MOUSE")
    def mouse_btn_mouse_long(self,double duration=1):
        return self._press_mouse_button_long(key=b"BTN_MOUSE",duration=duration)
    def mouse_btn_right(self):
        return self._press_mouse_button(key=b"BTN_RIGHT")
    def mouse_btn_right_long(self,double duration=1):
        return self._press_mouse_button_long(key=b"BTN_RIGHT",duration=duration)
    def mouse_btn_side(self):
        return self._press_mouse_button(key=b"BTN_SIDE")
    def mouse_btn_side_long(self,double duration=1):
        return self._press_mouse_button_long(key=b"BTN_SIDE",duration=duration)
    def mouse_scroll_down(self):
        return self._press_mouse_button(key=b"SCROLL_DOWN")
    def mouse_scroll_down_long(self,double duration=1):
        return self._press_mouse_button_long(key=b"SCROLL_DOWN",duration=duration)
    def mouse_scroll_up(self):
        return self._press_mouse_button(key=b"SCROLL_UP")
    def mouse_scroll_up_long(self,double duration=1):
        return self._press_mouse_button_long(key=b"SCROLL_UP",duration=duration)

    def pack_struct(self,list[tuple] data):
        cdef:
            Py_ssize_t datalen=len(data)
            list allpacked=[]
        for datalen in range(len(data)):
            allpacked.append(struckt_pack(*data[datalen]))

        return np.frombuffer(b''.join(allpacked), dtype=CUSTOM_DTYPE_PY_ALIGNED)

    def _execute_localshell_command(self,str path_on_device,int blocksize,object stuctarray,**kwargs):
        cdef:
            str tmpfilebin = ''
            str tmpfilesh = ''
            str finalcmd=''
            str tmpfilebindevice,tmpfileshdevice, executecmd,finalcmd_joined_str
            bytes binary_data
            object psru
            list command_files_device_bin
            list command_files_device_sh
            list command_files_pc_bin
            list command_files_pc_sh
            list finalcmd_joined
            list binary_data_list
            Py_ssize_t stucenumerate
        if isinstance(stuctarray,np.ndarray):
            tmpfilebindevice=f'{path_on_device}.bin'
            tmpfileshdevice =f'{path_on_device}.sh'
            binary_data, finalcmd=create_dd_command(
                path_on_device_bin=tmpfilebindevice,
                packed_dt=stuctarray,
                command_chunk=kwargs.get('command_chunk',3),
                exec_or_eval = "exec",
                sleepbetweencommand = 0,
                inputdev = kwargs.get('device'),
                blocksize = blocksize,
                sep=b"",add_su_cmd=self.add_su_to_dd_cmd if self.add_su_to_dd_cmd else ''
            )
            with open(tmpfilebindevice, mode="wb") as f:
                f.write(binary_data)
            with open(
                tmpfileshdevice, mode="w", encoding="utf-8", newline="\n"
            ) as f:
                f.write(finalcmd)
            if self.add_su_to_subprocess_cmd:
                executecmd=fr"{self.add_su_to_subprocess_cmd} {self.exe_su_cmd_exec} '{self.exe_sh} {tmpfileshdevice}'"
            elif self.add_su_to_input_subprocess:
                executecmd=f"""
{self.add_su_to_input_subprocess}
{finalcmd}
                """

            else:
                executecmd=fr"{self.exe_sh} {tmpfileshdevice}"
            psru=sru(
                self.local_shell,
                input=executecmd.encode(),
                env=os.environ, shell=True, cwd=os.getcwd()

            )
            if config_settings.debug_enabled:
                print(f'SUBPROC: {psru}')

            if kwargs.get('delete_temp_files_on_device',False):
                psru=sru(
                        self.local_shell,
                        input=f'rm -f {tmpfileshdevice}'.encode(),
                        env=os.environ,
                        shell=True,
                        cwd=os.getcwd()
                )
                if config_settings.debug_enabled:
                    print(f'SUBPROC: {psru}')
                psru=sru(     self.local_shell,
                        input=f'rm -f {tmpfilebindevice}'.encode(),
                        env=os.environ,
                        shell=True,
                        cwd=os.getcwd()

                )
                if config_settings.debug_enabled:
                    print(f'SUBPROC: {psru}')
            return binary_data, finalcmd, tmpfilebindevice, tmpfileshdevice,tmpfilebin,tmpfilesh,stuctarray

        else:
            command_files_device_bin=[]
            command_files_device_sh= []
            command_files_pc_bin=    []
            command_files_pc_sh=     []
            stucenumerate=0
            finalcmd_joined=[]
            binary_data_list=[]
            for strua in stuctarray:
                if isinstance(strua,np.ndarray):
                    tmpfilebin=get_tmpfile(suffix=".bin")
                    command_files_pc_bin.append(tmpfilebin)
                    tmpfilebindevice=f'{path_on_device}{stucenumerate}.bin'
                    command_files_device_bin.append(tmpfilebindevice)
                    binary_data, finalcmd=create_dd_command(
                        path_on_device_bin=tmpfilebindevice,
                        packed_dt=strua,
                        command_chunk=kwargs.get('command_chunk',3),
                        exec_or_eval = "exec",
                        sleepbetweencommand = 0,
                        inputdev = kwargs.get('device'),
                        blocksize = blocksize,
                        sep=b"",
                        add_su_cmd=self.add_su_to_dd_cmd if self.add_su_to_dd_cmd else '',
                    )
                    binary_data_list.append(binary_data)
                    finalcmd_joined.append(finalcmd)
                    with open(tmpfilebindevice, mode="wb") as f:
                        f.write(binary_data)

                    stucenumerate+=1
                else:
                    finalcmd_joined.append(f'sleep {strua}')
            finalcmd_joined_str='\n'.join(finalcmd_joined)
            tmpfileshdevice =f'{path_on_device}{stucenumerate}.sh'
            command_files_pc_sh.append(tmpfileshdevice)
            with open(
                        tmpfileshdevice, mode="w", encoding="utf-8", newline="\n"
                    ) as f:
                        f.write(finalcmd_joined_str)

            if self.add_su_to_subprocess_cmd:
                executecmd=fr"{self.add_su_to_subprocess_cmd} {self.exe_su_cmd_exec} '{self.exe_sh} {tmpfileshdevice}'"
            elif self.add_su_to_input_subprocess:
                executecmd=f"""
{self.add_su_to_input_subprocess}
{finalcmd}
                """

            else:
                executecmd=fr"{self.exe_sh} {tmpfileshdevice}"
            psru=sru(
                self.local_shell,
                input=executecmd.encode(),
                env=os.environ, shell=True, cwd=os.getcwd()

            )
            if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
            if kwargs.get('delete_temp_files_on_device',False):
                for t1 in command_files_device_bin:
                    psru=sru(
                        self.local_shell,
                        input=f'rm -f {t1}'.encode(),
                        env=os.environ,
                        shell=True,
                        cwd=os.getcwd()
                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
                for t1 in command_files_device_sh:
                    psru=sru(
                        self.local_shell,
                        input=f'rm -f {t1}'.encode(),
                        env=os.environ,
                        shell=True,
                        cwd=os.getcwd()
                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
            return binary_data_list, finalcmd_joined, command_files_device_bin, command_files_device_sh,command_files_pc_bin,command_files_pc_sh,stuctarray


    def _execute_adb_command(self,str path_on_device,int blocksize,object stuctarray,**kwargs):
        cdef:
            list adb_start_cmd=[self.adb_path,
                "-s",
                self.device_serial,]
            str tmpfilebin,tmpfilesh,tmpfilebindevice,tmpfileshdevice, executecmd
            bytes binary_data
            str finalcmd=''
            object psru
            list command_files_device_bin,finalcmd_joined,command_files_device_sh,command_files_pc_bin,command_files_pc_sh,binary_data_list
            Py_ssize_t stucenumerate=0
        if isinstance(stuctarray,np.ndarray):
            tmpfilebin=get_tmpfile(suffix=".bin")
            tmpfilesh=get_tmpfile(suffix=".sh")
            tmpfilebindevice=f'{path_on_device}.bin'
            tmpfileshdevice =f'{path_on_device}.sh'
            binary_data, finalcmd=create_dd_command(
                path_on_device_bin=tmpfilebindevice,
                packed_dt=stuctarray,
                command_chunk=kwargs.get('command_chunk',3),
                exec_or_eval = "exec",
                sleepbetweencommand = 0,
                inputdev = kwargs.get('device'),
                blocksize = blocksize,
                sep=b"",add_su_cmd=self.add_su_to_dd_cmd if self.add_su_to_dd_cmd else ''
            )
            with open(tmpfilebin, mode="wb") as f:
                f.write(binary_data)
            psru=sru(
            [
                *adb_start_cmd,
                "push",
                tmpfilebin,
                tmpfilebindevice,
            ]
                )
            if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
            if not self.add_su_to_input_subprocess:
                with open(
                    tmpfilesh, mode="w", encoding="utf-8", newline="\n"
                ) as f:
                    f.write(finalcmd)

                psru=sru(
                    [
                        *adb_start_cmd,
                        "push",
                        tmpfilesh,
                        tmpfileshdevice,
                    ]
                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
                if self.add_su_to_subprocess_cmd:
                    executecmd=fr"{self.add_su_to_subprocess_cmd} {self.exe_su_cmd_exec} '{self.exe_sh} {tmpfileshdevice}'"
                else:
                    executecmd=fr"{self.exe_sh} {tmpfileshdevice}"
                psru=sru(
                    [
                        *adb_start_cmd,
                        "shell",
                        executecmd,
                    ]
                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
            else:
                executecmd=f"""
{self.add_su_to_input_subprocess}
{finalcmd}
                """
                psru=sru(

                        [*adb_start_cmd,"shell",],
                        input=executecmd.encode(),
                        env=os.environ, shell=True, cwd=os.getcwd()

                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
            if kwargs.get('delete_temp_files_on_pc',False):
                try:
                    os.remove(tmpfilebin)
                except Exception:
                    if config_settings.debug_enabled:
                        errwrite()
                try:
                    os.remove(tmpfilesh)
                except Exception:
                    if config_settings.debug_enabled:
                        errwrite()
            if kwargs.get('delete_temp_files_on_device',False):
                psru=sru(
                    [
                        *adb_start_cmd,
                        "shell",
                        f'rm -f {tmpfileshdevice}',
                    ]
                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
                psru=sru(
                    [
                        *adb_start_cmd,
                        "shell",
                        f'rm -f {tmpfilebindevice}',
                    ]
                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
            return binary_data, finalcmd, tmpfilebindevice, tmpfileshdevice,tmpfilebin,tmpfilesh,stuctarray

        else:
            command_files_device_bin=[]
            command_files_device_sh=[]
            command_files_pc_bin=[]
            command_files_pc_sh=[]

            stucenumerate=0
            finalcmd_joined=[]
            binary_data_list=[]
            for strua in stuctarray:
                if isinstance(strua,np.ndarray):
                    tmpfilebin=get_tmpfile(suffix=".bin")
                    command_files_pc_bin.append(tmpfilebin)
                    tmpfilebindevice=f'{path_on_device}{stucenumerate}.bin'
                    command_files_device_bin.append(tmpfilebindevice)
                    binary_data, finalcmd=create_dd_command(
                        path_on_device_bin=tmpfilebindevice,
                        packed_dt=strua,
                        command_chunk=kwargs.get('command_chunk',3),
                        exec_or_eval = "exec",
                        sleepbetweencommand = 0,
                        inputdev = kwargs.get('device'),
                        blocksize = blocksize,
                        sep=b"",add_su_cmd=self.add_su_to_dd_cmd if self.add_su_to_dd_cmd else ''
                    )
                    binary_data_list.append(binary_data)
                    finalcmd_joined.append(finalcmd)
                    with open(tmpfilebin, mode="wb") as f:
                        f.write(binary_data)
                    psru=sru(
                    [
                        *adb_start_cmd,
                        "push",
                        tmpfilebin,
                        tmpfilebindevice,
                    ]
                        )
                    if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
                    stucenumerate+=1
                else:
                    finalcmd_joined.append(f'sleep {strua}')
            finalcmd_joined_str='\n'.join(finalcmd_joined)
            if not self.add_su_to_input_subprocess:
                tmpfilesh=get_tmpfile(suffix=".sh")
                command_files_pc_sh.append(tmpfilesh)
                with open(
                            tmpfilesh, mode="w", encoding="utf-8", newline="\n"
                        ) as f:
                            f.write(finalcmd_joined_str)
                tmpfileshdevice =f'{path_on_device}{stucenumerate}.sh'
                command_files_device_sh.append(tmpfileshdevice)
                psru=sru(
                            [
                                *adb_start_cmd,
                                "push",
                                tmpfilesh,
                                tmpfileshdevice,
                            ]
                        )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
                if self.add_su_to_subprocess_cmd:
                    executecmd=fr"{self.add_su_to_subprocess_cmd} {self.exe_su_cmd_exec} '{self.exe_sh} {tmpfileshdevice}'"
                else:
                    executecmd=fr"{self.exe_sh} {tmpfileshdevice}"
                psru=sru(
                    [
                        *adb_start_cmd,
                        "shell",
                        executecmd,
                    ]
                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
            else:
                executecmd=f"""
{self.add_su_to_input_subprocess}
{finalcmd}
                """
                psru=sru(

                        [*adb_start_cmd,"shell",],
                        input=finalcmd_joined_str.encode(),
                        env=os.environ, shell=True, cwd=os.getcwd()

                )
                if config_settings.debug_enabled: print(f'SUBPROC: {psru}')
            if kwargs.get('delete_temp_files_on_pc',False):
                for t1 in command_files_pc_sh:
                    try:
                        if os.path.exists(t1):
                            os.remove(t1)
                    except Exception:
                        if config_settings.debug_enabled:
                            errwrite()
                for t1 in command_files_pc_bin:
                    try:
                        if os.path.exists(t1):
                            os.remove(t1)
                    except Exception:
                        if config_settings.debug_enabled:
                            errwrite()
            if kwargs.get('delete_temp_files_on_device',False):
                for t1 in command_files_device_bin:
                    try:
                        psru=sru(
                            [
                                *adb_start_cmd,
                                "shell",
                                f'rm -f {t1}',
                            ]
                        )
                        if config_settings.debug_enabled:print(f'SUBPROC: {psru}')
                    except Exception:
                        if config_settings.debug_enabled:print(f'SUBPROC: {psru}')
                for t1 in command_files_device_sh:
                    try:
                        psru=sru(
                            [
                                *adb_start_cmd,
                                "shell",
                                f'rm -f {t1}',
                            ]
                        )
                        if config_settings.debug_enabled:print(f'SUBPROC: {psru}')
                    except Exception:
                        if config_settings.debug_enabled:print(f'SUBPROC: {psru}')
            return binary_data_list, finalcmd_joined, command_files_device_bin, command_files_device_sh,command_files_pc_bin,command_files_pc_sh,stuctarray

    def adb_mouse_move_from_to(self,
        int x1,
        int y1,
        int x2,
        int y2,
        long max_variationx=5,
        long max_variationy=5,
        str path_on_device="/sdcard/adb_mouse_move_from_to",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.mouse_move_from_to(x1=x1, y1=y1, x2=x2, y2=y2,max_variationx=max_variationx, max_variationy=max_variationy)
        return self._execute_adb_command(path_on_device=path_on_device,blocksize=blocksize,stuctarray=stuctarray,command_chunk=3,device=self.device_mouse,delete_temp_files_on_device=delete_temp_files_on_device,delete_temp_files_on_pc=delete_temp_files_on_pc,**kwargs)

    def adb_keyboard_press_key(self,
        key,
        double duration,
        str path_on_device="/sdcard/adb_keyboard_press_key",
        int blocksize=72,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.keyboard_press_key(key=key,duration=duration)
        return self._execute_adb_command(path_on_device=path_on_device,blocksize=blocksize,stuctarray=stuctarray,command_chunk=3,device=self.device_keyboard,delete_temp_files_on_device=delete_temp_files_on_device,delete_temp_files_on_pc=delete_temp_files_on_pc,**kwargs)

    def adb_mouse_move_from_to_natural(self,
        int x1,
        int y1,
        int x2,
        int y2,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/adb_mouse_move_from_to_natural",
        int blocksize=72 * 24 * 64,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_from_to_natural(x1=x1, y1=y1, x2=x2, y2=y2,max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_move_through_coordinates(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        str path_on_device="/sdcard/adb_mouse_move_through_coordinates",
        int blocksize=72*24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates(x_y_coordinates=x_y_coordinates,max_variationx=max_variationx,max_variationy=max_variationy)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_move_through_coordinates_natural(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/adb_mouse_move_through_coordinates_natural",
        int blocksize=72 * 24 * 4,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates_natural(x_y_coordinates=x_y_coordinates,max_variationx=max_variationx, max_variationy=max_variationy,multiply_each_iterration=multiply_each_iterration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_move_from_current_to_natural(self,
        int x,
        int y,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/adb_mouse_move_from_current_to_natural",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_from_current_to_natural(x=x, y=y,max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_move_from_current_to(self,
        int x,
        int y,
        long max_variationx=5,
        long max_variationy=5,
        str path_on_device="/sdcard/adb_mouse_move_from_current_to",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_from_current_to(x=x, y=y, max_variationx= max_variationx,max_variationy=max_variationy)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_move_through_coordinates_from_current(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        str path_on_device="/sdcard/adb_mouse_move_through_coordinates_from_current",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates_from_current(x_y_coordinates=x_y_coordinates, max_variationx=max_variationx, max_variationy=max_variationy, )
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_move_through_coordinates_from_current_natural(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/adb_mouse_move_through_coordinates_from_current_natural",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates_from_current_natural(x_y_coordinates=x_y_coordinates, max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_btn_extra(self,
        str path_on_device="/sdcard/adb_mouse_btn_extra",
        int blocksize=24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_btn_extra()
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_btn_extra_long(self,
        double duration=1,
        str path_on_device="/sdcard/adb_mouse_btn_extra_long",
        int blocksize=24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_btn_extra_long(duration=duration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_btn_middle(self,
        str path_on_device="/sdcard/adb_mouse_btn_middle",
        int blocksize=24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_btn_middle()
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_btn_middle_long(self,
        double duration=1,
        str path_on_device="/sdcard/adb_mouse_btn_middle_long",
        int blocksize=24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_btn_middle_long(duration=duration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_btn_mouse(self,str path_on_device="/sdcard/adb_mouse_btn_mouse",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_mouse()
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_btn_mouse_long(self,double duration=1,str path_on_device="/sdcard/adb_mouse_btn_mouse_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_mouse_long(duration=duration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_btn_right(self,str path_on_device="/sdcard/adb_mouse_btn_right",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_right()
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_btn_right_long(self,double duration=1,str path_on_device="/sdcard/adb_mouse_btn_right_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_right_long(duration=duration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_btn_side(self,str path_on_device="/sdcard/adb_mouse_btn_side",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_side()
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_btn_side_long(self,double duration=1,str path_on_device="/sdcard/adb_mouse_btn_side_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_side_long(duration=duration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_scroll_down(self,Py_ssize_t reps=10,str path_on_device="/sdcard/adb_mouse_scroll_down",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        cdef:
            list[bytes] stuctarray_list=[]
            Py_ssize_t i
            bytes stuctarray_byte
        stuctarray=self.mouse_scroll_down()
        stuctarray_byte=b''.join(stuctarray.view(f'V{stuctarray.itemsize}'))
        for i in range(reps):
            stuctarray_list.append(stuctarray_byte)
        stuctarray_list_full=np.frombuffer(b''.join(stuctarray_list),dtype=stuctarray.dtype)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray_list_full,
        command_chunk=1,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_scroll_down_long(self,double duration=1,str path_on_device="/sdcard/adb_mouse_scroll_down_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_scroll_down_long(duration=duration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=1,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_mouse_scroll_up(self,Py_ssize_t reps=10,str path_on_device="/sdcard/adb_mouse_scroll_up",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        cdef:
            list[bytes] stuctarray_list=[]
            Py_ssize_t i
            bytes stuctarray_byte
        stuctarray=self.mouse_scroll_up()
        stuctarray_byte=b''.join(stuctarray.view(f'V{stuctarray.itemsize}'))
        for i in range(reps):
            stuctarray_list.append(stuctarray_byte)
        stuctarray_list_full=np.frombuffer(b''.join(stuctarray_list),dtype=stuctarray.dtype)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray_list_full,
        command_chunk=1,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_scroll_up_long(self,double duration=1,str path_on_device="/sdcard/adb_mouse_scroll_up_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_scroll_up_long(duration=duration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=1,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_pack_struct_and_send(self,list[tuple] data,str path_on_device="/sdcard/adb_pack_struct_and_send",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,str device='/dev/input/event5',**kwargs):
        stuctarray=self.pack_struct(data)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=1,
        device=device,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_mouse_move_through_coordinates_from_current_natural(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/adb_mouse_move_through_coordinates_from_current_natural",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates_from_current_natural(x_y_coordinates=x_y_coordinates, max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_touchscreen_swipe_from_to(self,
        int x1,
        int y1,
        int x2,
        int y2,
        long max_variationx=5,
        long max_variationy=5,
        long random_number_start=100,
        long random_number_switch=4  ,
        str path_on_device="/sdcard/adb_touchscreen_swipe_from_to",
        int blocksize=4 * 24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.touchscreen_swipe_from_to(x1=x1, y1=y1, x2=x2, y2=y2, max_variationx=max_variationx, max_variationy=max_variationy, random_number_start=random_number_start,  random_number_switch=random_number_switch  )
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=4,
        device=self.device_touchscreen,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def adb_touchscreen_swipe_from_to_exact(self,
        int x1,
        int y1,
        int x2,
        int y2,
        long max_variationx=5,
        long max_variationy=5,
        long random_number_start=100,
        long random_number_switch=4  ,
        str path_on_device="/sdcard/adb_touchscreen_swipe_from_to_exact",
        int blocksize=4 * 24 * 4 * 4 * 4,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.touchscreen_swipe_from_to_exact(x1=x1,  y1=y1, x2=x2,  y2=y2, max_variationx=max_variationx, max_variationy=max_variationy, random_number_start=random_number_start,  random_number_switch=random_number_switch  )
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=4,
        device=self.device_touchscreen,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_touchscreen_swipe_through_coordinates(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        long random_number_start=100,
        long random_number_switch=4,
        str path_on_device="/sdcard/adb_touchscreen_swipe_through_coordinates",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.touchscreen_swipe_through_coordinates(x_y_coordinates=x_y_coordinates, max_variationx=max_variationx, max_variationy=max_variationy, random_number_start=random_number_start,  random_number_switch=random_number_switch)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=4,
        device=self.device_touchscreen,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_keyboard_write_text(self,
        object text,
        str path_on_device="/sdcard/adb_keyboard_write_text",
        int blocksize=144,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.keyboard_write_text(text=text)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=6,
        device=self.device_keyboard,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def adb_keyboard_press_key_combination(self,
        arraylikepy combination,
        double duration=1,
        str path_on_device="/sdcard/adb_keyboard_press_key_combination",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.keyboard_press_key_combination(combination=combination, duration=duration)
        return self._execute_adb_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_keyboard,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)





    def local_shell_mouse_move_from_to(self,
        int x1,
        int y1,
        int x2,
        int y2,
        long max_variationx=5,
        long max_variationy=5,
        str path_on_device="/sdcard/local_shell_mouse_move_from_to",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.mouse_move_from_to(x1=x1, y1=y1, x2=x2, y2=y2,max_variationx=max_variationx, max_variationy=max_variationy)
        return self._execute_local_shell_command(path_on_device=path_on_device,blocksize=blocksize,stuctarray=stuctarray,command_chunk=3,device=self.device_mouse,delete_temp_files_on_device=delete_temp_files_on_device,delete_temp_files_on_pc=delete_temp_files_on_pc,**kwargs)

    def local_shell_keyboard_press_key(self,
        key,
        double duration,
        str path_on_device="/sdcard/local_shell_keyboard_press_key",
        int blocksize=72,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.keyboard_press_key(key=key,duration=duration)
        return self._execute_local_shell_command(path_on_device=path_on_device,blocksize=blocksize,stuctarray=stuctarray,command_chunk=3,device=self.device_keyboard,delete_temp_files_on_device=delete_temp_files_on_device,delete_temp_files_on_pc=delete_temp_files_on_pc,**kwargs)

    def local_shell_mouse_move_from_to_natural(self,
        int x1,
        int y1,
        int x2,
        int y2,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/local_shell_mouse_move_from_to_natural",
        int blocksize=72 * 24 * 64,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_from_to_natural(x1=x1, y1=y1, x2=x2, y2=y2,max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_move_through_coordinates(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        str path_on_device="/sdcard/local_shell_mouse_move_through_coordinates",
        int blocksize=72*24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates(x_y_coordinates=x_y_coordinates,max_variationx=max_variationx,max_variationy=max_variationy)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_move_through_coordinates_natural(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/local_shell_mouse_move_through_coordinates_natural",
        int blocksize=72 * 24 * 4,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates_natural(x_y_coordinates=x_y_coordinates,max_variationx=max_variationx, max_variationy=max_variationy,multiply_each_iterration=multiply_each_iterration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_move_from_current_to_natural(self,
        int x,
        int y,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/local_shell_mouse_move_from_current_to_natural",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_from_current_to_natural(x=x, y=y,max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_move_from_current_to(self,
        int x,
        int y,
        long max_variationx=5,
        long max_variationy=5,
        str path_on_device="/sdcard/local_shell_mouse_move_from_current_to",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_from_current_to(x=x, y=y, max_variationx= max_variationx,max_variationy=max_variationy)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_move_through_coordinates_from_current(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        str path_on_device="/sdcard/local_shell_mouse_move_through_coordinates_from_current",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates_from_current(x_y_coordinates=x_y_coordinates, max_variationx=max_variationx, max_variationy=max_variationy, )
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_move_through_coordinates_from_current_natural(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/local_shell_mouse_move_through_coordinates_from_current_natural",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates_from_current_natural(x_y_coordinates=x_y_coordinates, max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_btn_extra(self,
        str path_on_device="/sdcard/local_shell_mouse_btn_extra",
        int blocksize=24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_btn_extra()
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_btn_extra_long(self,
        double duration=1,
        str path_on_device="/sdcard/local_shell_mouse_btn_extra_long",
        int blocksize=24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_btn_extra_long(duration=duration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_btn_middle(self,
        str path_on_device="/sdcard/local_shell_mouse_btn_middle",
        int blocksize=24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_btn_middle()
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_btn_middle_long(self,
        double duration=1,
        str path_on_device="/sdcard/local_shell_mouse_btn_middle_long",
        int blocksize=24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_btn_middle_long(duration=duration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_btn_mouse(self,str path_on_device="/sdcard/local_shell_mouse_btn_mouse",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_mouse()
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_btn_mouse_long(self,double duration=1,str path_on_device="/sdcard/local_shell_mouse_btn_mouse_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_mouse_long(duration=duration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_btn_right(self,str path_on_device="/sdcard/local_shell_mouse_btn_right",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_right()
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_btn_right_long(self,double duration=1,str path_on_device="/sdcard/local_shell_mouse_btn_right_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_right_long(duration=duration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_btn_side(self,str path_on_device="/sdcard/local_shell_mouse_btn_side",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_side()
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_btn_side_long(self,double duration=1,str path_on_device="/sdcard/local_shell_mouse_btn_side_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_btn_side_long(duration=duration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=2,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_scroll_down(self,Py_ssize_t reps=10,str path_on_device="/sdcard/local_shell_mouse_scroll_down",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        cdef:
            list[bytes] stuctarray_list=[]
            Py_ssize_t i
            bytes stuctarray_byte
        stuctarray=self.mouse_scroll_down()
        stuctarray_byte=b''.join(stuctarray.view(f'V{stuctarray.itemsize}'))
        for i in range(reps):
            stuctarray_list.append(stuctarray_byte)
        stuctarray_list_full=np.frombuffer(b''.join(stuctarray_list),dtype=stuctarray.dtype)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray_list_full,
        command_chunk=1,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_scroll_down_long(self,double duration=1,str path_on_device="/sdcard/local_shell_mouse_scroll_down_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_scroll_down_long(duration=duration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=1,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_mouse_scroll_up(self,Py_ssize_t reps=10,str path_on_device="/sdcard/local_shell_mouse_scroll_up",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        cdef:
            list[bytes] stuctarray_list=[]
            Py_ssize_t i
            bytes stuctarray_byte
        stuctarray=self.mouse_scroll_up()
        stuctarray_byte=b''.join(stuctarray.view(f'V{stuctarray.itemsize}'))
        for i in range(reps):
            stuctarray_list.append(stuctarray_byte)
        stuctarray_list_full=np.frombuffer(b''.join(stuctarray_list),dtype=stuctarray.dtype)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray_list_full,
        command_chunk=1,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_scroll_up_long(self,double duration=1,str path_on_device="/sdcard/local_shell_mouse_scroll_up_long",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,**kwargs):
        stuctarray=self.mouse_scroll_up_long(duration=duration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=1,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_pack_struct_and_send(self,list[tuple] data,str path_on_device="/sdcard/local_shell_pack_struct_and_send",int blocksize=24,bint delete_temp_files_on_device=False,bint delete_temp_files_on_pc=False,str device='/dev/input/event5',**kwargs):
        stuctarray=self.pack_struct(data)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=1,
        device=device,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_mouse_move_through_coordinates_from_current_natural(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        double multiply_each_iterration=1.0,
        str path_on_device="/sdcard/local_shell_mouse_move_through_coordinates_from_current_natural",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.mouse_move_through_coordinates_from_current_natural(x_y_coordinates=x_y_coordinates, max_variationx=max_variationx, max_variationy=max_variationy, multiply_each_iterration=multiply_each_iterration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_mouse,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_touchscreen_swipe_from_to(self,
        int x1,
        int y1,
        int x2,
        int y2,
        long max_variationx=5,
        long max_variationy=5,
        long random_number_start=100,
        long random_number_switch=4  ,
        str path_on_device="/sdcard/local_shell_touchscreen_swipe_from_to",
        int blocksize=4 * 24,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.touchscreen_swipe_from_to(x1=x1, y1=y1, x2=x2, y2=y2, max_variationx=max_variationx, max_variationy=max_variationy, random_number_start=random_number_start,  random_number_switch=random_number_switch  )
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=4,
        device=self.device_touchscreen,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)
    def local_shell_touchscreen_swipe_from_to_exact(self,
        int x1,
        int y1,
        int x2,
        int y2,
        long max_variationx=5,
        long max_variationy=5,
        long random_number_start=100,
        long random_number_switch=4  ,
        str path_on_device="/sdcard/local_shell_touchscreen_swipe_from_to_exact",
        int blocksize=4 * 24 * 4 * 4 * 4,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):

        stuctarray=self.touchscreen_swipe_from_to_exact(x1=x1,  y1=y1, x2=x2,  y2=y2, max_variationx=max_variationx, max_variationy=max_variationy, random_number_start=random_number_start,  random_number_switch=random_number_switch  )
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=4,
        device=self.device_touchscreen,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_touchscreen_swipe_through_coordinates(self,
        object x_y_coordinates,
        long max_variationx=5,
        long max_variationy=5,
        long random_number_start=100,
        long random_number_switch=4,
        str path_on_device="/sdcard/local_shell_touchscreen_swipe_through_coordinates",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.touchscreen_swipe_through_coordinates(x_y_coordinates=x_y_coordinates, max_variationx=max_variationx, max_variationy=max_variationy, random_number_start=random_number_start,  random_number_switch=random_number_switch)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=4,
        device=self.device_touchscreen,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_keyboard_write_text(self,
        object text,
        str path_on_device="/sdcard/local_shell_keyboard_write_text",
        int blocksize=144,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.keyboard_write_text(text=text)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=6,
        device=self.device_keyboard,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)

    def local_shell_keyboard_press_key_combination(self,
        arraylikepy combination,
        double duration=1,
        str path_on_device="/sdcard/local_shell_keyboard_press_key_combination",
        int blocksize=72*12,
        bint delete_temp_files_on_device=False,
        bint delete_temp_files_on_pc=False,
        **kwargs):
        stuctarray=self.keyboard_press_key_combination(combination=combination, duration=duration)
        return self._execute_local_shell_command(
        path_on_device=path_on_device,
        blocksize=blocksize,
        stuctarray=stuctarray,
        command_chunk=3,
        device=self.device_keyboard,
        delete_temp_files_on_device=delete_temp_files_on_device,
        delete_temp_files_on_pc=delete_temp_files_on_pc
        ,**kwargs)


cpdef add_mapping_keys(mapping_dict, key_map, key_map_press, key_map_release):
    cdef:
        list bytedata = []
        Py_ssize_t ini0
    for k, v in mapping_dict.items():
        bytedata.clear()
        for ini0 in range(len(v)):
            bytedata.append(key_map_press[<string>v[ini0].encode()])
        key_map_press[<string>k.encode()]= b"".join(bytedata)
        bytedata.clear()
        for ini0 in range(len(v)-1,-1,-1):
            bytedata.append(key_map_release[<string>v[ini0].encode()])
        key_map_release[<string>k.encode()]= b"".join(bytedata)
        bytedata.clear()
        for ini0 in range(len(v)):
            bytedata.append(key_map_press[<string>v[ini0].encode()])
        for ini0 in range(len(v)-1,-1,-1):
            bytedata.append(key_map_release[<string>v[ini0].encode()])
        key_map[<string>k.encode()] = b"".join(bytedata)
