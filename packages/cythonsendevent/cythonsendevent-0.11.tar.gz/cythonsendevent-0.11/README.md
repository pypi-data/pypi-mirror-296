# Sendevent - Android with Cython

## pip install cythonsendevent

### Tested against Windows 10 / Python 3.11 / Anaconda / ADB / Bluestacks 5

### Important!

The module will be compiled when you import it for the first time. Cython and a C++ compiler must be installed!

```python
from cythonsendevent import SendeventClass, config_settings
from time import sleep
import shutil

config_settings.debug_enabled = False
adb_path = shutil.which("adb")
device_serial = "127.0.0.1:5560"

selfi = SendeventClass(
    device_touchscreen="/dev/input/event4",
    x_max_device_touchscreen=32767,  # getevent -lp
    y_max_device_touchscreen=32767,
    device_mouse="/dev/input/event5",
    x_max_device_mouse=65535,  # getevent -lp
    y_max_device_mouse=65535,
    device_keyboard="/dev/input/event3",
    screen_width=720,
    screen_height=1280,
    adb_path=adb_path,
    device_serial=device_serial,
    local_shell="",
    local_shell_su="",
    local_shell_su_cmd_exec="",
    mouse_move_codes=(
        3,
        0,
        3,
        1,
    ),
    swipe_codes=(
        3,
        53,
        3,
        54,
    ),
    exe_su="su",
    exe_su_cmd_exec="-c",
    exe_sh="sh",
    exe_getevent="getevent",
    shell_for_mouse_position=(
        adb_path,
        "-s",
        device_serial,
        "shell",
    ),
    regex_for_mouse_position=rb"_([XY])\b\s+[^\d]+(\d+)[^\d].*max\s+(\d+)",  # from getevent -lp
    add_su_to_dd_cmd="",
    add_su_to_subprocess_cmd="",
    add_su_to_input_subprocess="su",
)

# All mapped keycodes:
print(selfi.key_map)

# Write text (returns only numpy arrays)
text1 = b"Hello"
textarray1 = selfi.keyboard_write_text(text1)

text2 = list("Hello")
textarray2 = selfi.keyboard_write_text(text2)

text3 = tuple("Hello")
textarray3 = selfi.keyboard_write_text(text3)

text4 = getkeys = [
    "Q",
    "W",
    "E",
    "R",
    "T",
    "Y",
    "U",
    "I",
    "O",
    "P",
    "ç",
    "Ç",
    "ß",
    "ẞ",
    "+",
    ",",
    "-",
    ".",
    "/",
    "ã",
    "à",
    "Ã",
    "~",
    "a",
    "b",
    "ctrl+a",
]
textarray4 = selfi.keyboard_write_text(text4)
textarray4 = selfi.keyboard_write_text(text4)
press1 = selfi.keyboard_press_key(key="A", duration=0.1)
print(press1)
press2 = selfi.keyboard_press_key_combination(
    combination=["ctrl", "alt", "a"], duration=0.1
)
print(press2)
selfi.map_keys({"banana": ["KEY_B", "KEY_A", "KEY_N", "KEY_A", "KEY_N", "KEY_A"]})
press3 = selfi.keyboard_press_key(key="banana", duration=0.1)
print(press3)

# Writing text (using adb shell)
# If you are running the software on the device, substitute the prefix 'adb_' with 'local_shell_', e.g.
# adb_keyboard_press_key -> local_shell_keyboard_press_key
# adb_keyboard_write_text -> local_shell_keyboard_write_text
# Press key for a certain amount of time
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_keyboard_press_key(
    key="a",
    duration=1,
    path_on_device="/sdcard/adb_keyboard_press_key",
    blocksize=72,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
# write a text
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_keyboard_write_text(
    text="Hello my friend",
    path_on_device="/sdcard/adb_keyboard_write_text",
    blocksize=144,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)

# press key combination
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_keyboard_press_key_combination(
    combination=["ctrl", "a"],
    duration=1,
    path_on_device="/sdcard/adb_keyboard_press_key_combination",
    blocksize=72,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)


# Mouse moving

(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_move_from_to(
    x1=10,
    y1=10,
    x2=500,
    y2=400,
    max_variationx=5,  # variations from being a straight line
    max_variationy=5,
    path_on_device="/sdcard/tmpcmd",  # will be created
    blocksize=72 * 12,  # controls the speed
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)

(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_move_from_to_natural(
    x1=10,
    y1=10,
    x2=500,
    y2=800,
    max_variationx=3,
    max_variationy=3,
    multiply_each_iterration=2.0,
    path_on_device="/sdcard/adb_mouse_move_from_to_natural",
    blocksize=72 * 24 * 64,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)

x_y_coordinates = [(200, 300), (100, 700), (400, 300), (300, 700)]
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_move_through_coordinates(
    x_y_coordinates,
    max_variationx=5,
    max_variationy=5,
    path_on_device="/sdcard/adb_mouse_move_through_coordinates",
    blocksize=72 * 24,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)

x_y_coordinates = [(200, 300), (100, 700), (400, 300), (300, 700)]
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_move_through_coordinates_natural(
    x_y_coordinates,
    max_variationx=5,
    max_variationy=5,
    multiply_each_iterration=2.0,
    path_on_device="/sdcard/adb_mouse_move_through_coordinates_natural",
    blocksize=72 * 24 * 64,  # natural and exact have much more bytedata
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)


x_y_coordinates = [(200, 300), (100, 700), (400, 300), (300, 700)]
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_move_from_current_to_natural(
    x=500,
    y=800,
    max_variationx=5,
    max_variationy=5,
    multiply_each_iterration=2.0,
    path_on_device="/sdcard/adb_mouse_move_from_current_to_natural",
    blocksize=72 * 12 * 64,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_move_from_current_to(
    x=500,  # uses getevent -lp to get the current mouse position
    y=500,
    max_variationx=5,
    max_variationy=5,
    path_on_device="/sdcard/adb_mouse_move_from_current_to",
    blocksize=72 * 12,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
x_y_coordinates = [(200, 300), (100, 700), (400, 300), (300, 700)]
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_move_through_coordinates_from_current(
    x_y_coordinates,
    max_variationx=5,
    max_variationy=5,
    path_on_device="/sdcard/adb_mouse_move_through_coordinates_from_current",
    blocksize=72 * 12,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
x_y_coordinates = [(200, 300), (100, 700), (400, 300), (300, 700)]
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_move_through_coordinates_from_current_natural(
    x_y_coordinates,
    max_variationx=5,
    max_variationy=5,
    multiply_each_iterration=2.0,
    path_on_device="/sdcard/adb_mouse_move_through_coordinates_from_current_natural",
    blocksize=72 * 12 * 64,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)

(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_touchscreen_swipe_from_to(
    x1=10,
    y1=10,
    x2=500,
    y2=800,
    max_variationx=5,
    max_variationy=5,
    random_number_start=100,
    random_number_switch=4,
    path_on_device="/sdcard/adb_touchscreen_swipe_from_to",
    blocksize=12 * 24,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_touchscreen_swipe_from_to_exact(
    x1=10,
    y1=10,
    x2=500,
    y2=800,
    max_variationx=5,
    max_variationy=5,
    random_number_start=100,
    random_number_switch=4,
    path_on_device="/sdcard/adb_touchscreen_swipe_from_to_exact",
    blocksize=24 * 24 * 128,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)


(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_touchscreen_swipe_through_coordinates(
    x_y_coordinates=x_y_coordinates,
    max_variationx=5,
    max_variationy=5,
    random_number_start=100,
    random_number_switch=4,
    path_on_device="/sdcard/adb_touchscreen_swipe_through_coordinates",
    blocksize=12 * 24 * 16,
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)

# mouse commands binary data
print(selfi.mouse_map)
print(selfi.mouse_map_press)
print(selfi.mouse_map_release)

# as numpy struct arrays
btn_extra = selfi.mouse_btn_extra()
print(btn_extra)
btn_extra_long = selfi.mouse_btn_extra_long(duration=1)
print(btn_extra_long)
btn_middle = selfi.mouse_btn_middle()
print(btn_middle)
btn_middle_long = selfi.mouse_btn_middle_long(duration=1)
print(btn_middle_long)
btn_mouse = selfi.mouse_btn_mouse()
print(btn_mouse)
btn_mouse_long = selfi.mouse_btn_mouse_long(duration=1)
print(btn_mouse_long)
btn_right = selfi.mouse_btn_right()
print(btn_right)
btn_right_long = selfi.mouse_btn_right_long(duration=1)
print(btn_right_long)
btn_side = selfi.mouse_btn_side()
print(btn_side)
btn_side_long = selfi.mouse_btn_side_long(duration=1)
print(btn_side_long)
scroll_down = selfi.mouse_scroll_down()
print(scroll_down)
scroll_down_long = selfi.mouse_scroll_down_long(duration=1)
print(scroll_down_long)
scroll_up = selfi.mouse_scroll_up()
print(scroll_up)
scroll_up_long = selfi.mouse_scroll_up_long(duration=1)
print(scroll_up_long)


# Executing different mouse clicks:


(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_extra(
    path_on_device="/sdcard/adb_mouse_btn_extra",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
sleep(1)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_extra_long(
    duration=1,
    path_on_device="/sdcard/adb_mouse_btn_extra_long",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_middle(
    path_on_device="/sdcard/adb_mouse_btn_middle",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
sleep(1)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_middle_long(
    duration=1,
    path_on_device="/sdcard/adb_mouse_btn_middle_long",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_mouse(
    path_on_device="/sdcard/adb_mouse_btn_mouse",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
sleep(1)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_mouse_long(
    duration=1,
    path_on_device="/sdcard/adb_mouse_btn_mouse_long",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_right(
    path_on_device="/sdcard/adb_mouse_btn_right",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
sleep(1)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_right_long(
    duration=1,
    path_on_device="/sdcard/adb_mouse_btn_right_long",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_side(
    path_on_device="/sdcard/adb_mouse_btn_side",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
sleep(1)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_btn_side_long(
    duration=1,
    path_on_device="/sdcard/adb_mouse_btn_side_long",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_scroll_down(
    reps=10,
    path_on_device="/sdcard/adb_mouse_scroll_down",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)
sleep(1)

(
    binary_data,
    finalcmd,
    tmpfilebindevice,
    tmpfileshdevice,
    tmpfilebin,
    tmpfilesh,
    stuctarray,
) = selfi.adb_mouse_scroll_up(
    reps=10,
    path_on_device="/sdcard/adb_mouse_scroll_up",
    delete_temp_files_on_device=False,
    delete_temp_files_on_pc=False,
)

```