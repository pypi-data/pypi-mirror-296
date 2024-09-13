# eventparser parser for Android

### Tested against Windows 10 / Python 3.11 / Anaconda / BlueStacks

### pip install cythonevparser

### Cython and a C compiler must be installed!

```PY
import time
import re as regexpython
import regex as re
from cythonevparser import clean_cache, create_temp_memdisk, EvParse
from cythondfprint import add_printer
import pandas as pd
from exceptdrucker import errwrite
import shutil
import os

import subprocess

add_printer(1)



def sendcmd(openshell, inputcmd, shell=True, timeout=10):
    try:
        p = subprocess.run(
            openshell,
            input=inputcmd if isinstance(inputcmd, bytes) else inputcmd.encode(),
            shell=shell,
            env=os.environ,
            cwd=os.getcwd(),
            capture_output=True,
            timeout=10,
        )
        return p.stdout, p.stderr, p.returncode
    except Exception as e:
        print(e)
    return None, None, None


def iskeyboardshown():
    try:
        stdout, stderr, returncode = sendcmd(
            openshell, keyboard_shown, shell=False, timeout=10
        )
        print(stdout, stderr, returncode)
        if b"mVisibleBound=true" in stdout and b"mInputShown=true" in stdout:
            return True
        return False
    except Exception as fe:
        errwrite()
    return False



clean_cache()
adb_exe = shutil.which("adb")
device_serial = "127.0.0.1:5560"
elements2check_regex = regexpython.compile(
    r"(?:(?:StateListAnimatorButton)|(?:p\.ral)|(?:android\.widget\.NumberPicker\$CustomEditText)|(?:AppCompatCheckBox))"
)
elements2check_min_area = 0.0001
elements2check_max_area = 50
sleep_after_each_dataframe = 0.1
screen_width = 720
screen_height = 1280

keyboard_shown = b'dumpsys input_method | grep -E "mInputShown|mVisibleBound"'
openshell = [
    adb_exe,
    "-s",
    device_serial,
    "shell",
]
create_temp_memdisk(
    memdisk_path="/media/ramdisk",
    adb_path=adb_exe,
    device_serial=device_serial,
    memdisk_size="128M",
    shell=False,
    su_exe="su",
)
evp = EvParse(
    adb_exe=adb_exe,
    device_serial=device_serial,
    field_size=50,
    record_count=50,
    sleep_between_each_scan=0.001,
    regex_nogil=True,
    device_shell="shell",
    uiautomator_cmd=b"uiautomator events",
    sleep_after_starting_thread=5,
    thread_daemon=True,
    uiautomator_kill_cmd=b"pkill uiautomator",
    timeout_scan=0.1,
    screen_width=screen_width,
    screen_height=screen_height,
    subproc_shell=False,
    with_children=False,
    add_screenshot=False,
    screenshot_kwargs=None,
    input_tap_center_x="aa_center_x",
    input_tap_center_y="aa_center_y",
    input_tap_input_cmd="input touchscreen tap",
    input_tap_kwargs=None,
    sendevent_mouse_move_start_x="aa_start_x",
    sendevent_mouse_move_start_y="aa_start_y",
    sendevent_mouse_move_end_x="aa_end_x",
    sendevent_mouse_move_end_y="aa_end_y",
    sendevent_mouse_move_y_max=65535,
    sendevent_mouse_move_x_max=65535,
    sendevent_mouse_move_inputdev="/dev/input/event5",
    sendevent_mouse_move_add=True,
    sendevent_mouse_move_kwargs=None,
    sendevent_mouse_move_su_exe="su",
    sendevent_mouse_move_sh_device="sh",
    sendevent_mouse_move_cwd_on_device="/media/ramdisk",
    sendevent_mouse_move_qty_blocks=4 * 24,
    debug=True,
    limited_mouse_move=True,
    scroll_x_begin_center_offset=30,
    scroll_y_begin_center_offset=30,
    scroll_x_end_center_offset=30,
    scroll_y_end_center_offset=30,
    add_move_and_tap=True,
)
callback_function_kwargs = {}
callback_function_kwargs["regex_to_check"] = rb"\bcom\..*"
callback_function_kwargs["regex_flags"] = re.IGNORECASE
evp.kill_ui_automator(["sh"])
time.sleep(5)
allresultdata = []

# b'[Inscreva-se gr\xc3\xa1tis]'
foundall = False
goodresults = []
result = evp.start_event_parser(
    callback_function=evp.callback_function,
    max_timeout=0.1,
    callback_function_kwargs=callback_function_kwargs,
    sleep_between_each_scan=0.01,
    print_elements=False,
)
myemail = "mariadanada@maya.com"
mypassword = "bonadnxa!Dx71"
evp.data_array[:] = b""
screenshotfolder = r"C:\savedshots"
df = pd.DataFrame()
rotcount = 0
emailput = False
killfirst = False
F = set()
# collected_frames = []
# last_resultstmp = []
while not foundall:
    try:
        time.sleep(2)
        dfx = evp.parse_elements_dataframe(with_children=True, with_windows=True)
        # collected_frames.append(dfx)
        evp.last_results.clear()
        for name, group in (
            dfx.loc[
                (dfx.aa_area > 0)
                & (dfx.aa_area_percentage < 50)
                & (dfx.aa_all_my_children.str.len() < 2)
                & (~dfx.aa_pflag_invalidated.str.contains("I", regex=False, na=False))
                & dfx.aa_enabled.str.contains("E", regex=False, na=False)
                & (~dfx.aa_visibility.str.contains("I", regex=False, na=False))
                & (dfx.aa_pflag_dirty_mask.str.contains(".", regex=False, na=False))
                & (
                    dfx.aa_clickable.str.contains("C", regex=False, na=False)
                    | (dfx.bb_misc_clickable.fillna(False))
                )
                & (dfx.aa_start_y > 0)
                & (dfx.aa_end_y < screen_height)
                & (
                    ~dfx.aa_classname.str.contains(
                        "StateListAnimatorImageButton", regex=False, na=False
                    )
                )
            ]
            .sort_values(by=["aa_end_x"], ascending=True)
            .groupby(
                [
                    "aa_original_string",
                    "aa_start_x",
                    "aa_start_y",
                    "aa_center_x",
                    "aa_center_y",
                ]
            )
        ):
            item = group.iloc[0]
            goodresults.clear()
            evp.starttime.clear()
            item.aa_mouse_move()
            evp.starttime.append(time.time())
            result = evp.start_event_parser(
                callback_function=evp.callback_function,
                max_timeout=0.1,
                callback_function_kwargs=callback_function_kwargs,
                sleep_between_each_scan=0.05,
                print_elements=False,
            )
            if evp.last_results:
                # last_resultstmp.append(evp.last_results)
                fra = item.to_frame().T
                dfi = pd.DataFrame(evp.last_results, dtype="object")
                goodresults.append(
                    pd.concat(
                        [
                            fra.loc[fra.index.repeat(len(dfi))].reset_index(drop=True),
                            dfi.rename(
                                columns={k: f"cc_{k}" for k in dfi.columns}
                            ).reset_index(drop=True),
                        ],
                        axis=1,
                    ).assign(dd_routcounter=rotcount, dd_matchcounter=range(len(dfi)))
                )
                rotcount += 1
                evp.last_results.clear()
            else:
                continue
            df = pd.concat(goodresults, ignore_index=True)
            df.ds_color_print_all()
            goodresults.clear()
            if F == {0, 1, 2, 3, 4, 5, 6, 7, 8}:
                F.clear()
                foundall = True
                break
            if F == {0, 1, 2, 3, 4, 5, 6, 7}:
                try:
                    agreee = dfx.loc[
                        dfx.aa_element_id.str.contains("agree")
                    ].drop_duplicates(subset="aa_center_y")
                    if not agreee.empty:
                        for k, i in agreee.iterrows():
                            i.aa_move_and_tap(0.001)
                        F.add(8)
                        break
                except Exception:
                    errwrite()
            if F == {0, 1, 2, 3, 4, 5, 6}:
                try:
                    gender_button = df.loc[
                        ((df.cc_Text == b"[Masculino]") | (df.cc_Text == b"[Feminino]"))
                        & df.aa_element_id.str.contains("gender_button")
                    ]
                    if not gender_button.empty:
                        gender_button.iloc[0].aa_mouse_move()
                        gender_button.iloc[0].aa_input_tap()
                        F.add(7)
                        break
                except Exception:
                    errwrite()
            if F == {0, 1, 2, 3, 4, 5}:
                try:
                    avancarbutton1 = df.loc[
                        (df.aa_element_id.str.contains("next", regex=False, na=False))
                        & (df.cc_Text == b"[Avan\xc3\xa7ar]")
                        & (df.cc_ClassName == b"android.widget.Button")
                    ]
                    if not avancarbutton1.empty:
                        avancarbutton2 = avancarbutton1.sort_values(
                            by=["dd_matchcounter", "aa_start_y"],
                        )
                        avancarbutton2.iloc[0].aa_move_and_tap(0.001)
                        F.add(6)
                        break
                except Exception:
                    errwrite()
            if F == {0, 1, 2, 3, 4}:
                try:
                    numpick = (
                        dfx.loc[
                            (
                                dfx.aa_element_id.str.contains(
                                    r"id/(?:(?:year)|(?:month)|(?:day))\s*$",
                                    regex=True,
                                    na=False,
                                )
                            )
                        ]
                        .drop_duplicates(
                            subset=[
                                "aa_element_id",
                            ]
                        )
                        .sort_values(by=["aa_element_id"], ascending=False)
                    )
                    if not numpick.empty:
                        dada = ["01", "m", "1987"][::-1]
                        indi = 0

                        for k, i in numpick.iterrows():
                            try:
                                i.aa_move_and_tap(0.001)
                                texttosend = dada[indi]
                                time.sleep(0.2)
                                sendcmd(
                                    openshell,
                                    inputcmd=f"input text '{texttosend}'",
                                    shell=False,
                                    timeout=10,
                                )
                                time.sleep(0.2)
                                indi += 1
                            except Exception:
                                errwrite()
                        evp.last_results.clear()
                        time.sleep(0.5)
                        for k, i in numpick.iterrows():
                            i.aa_move_and_tap(0.001)
                            break
                        evp.starttime.append(time.time())
                        result = evp.start_event_parser(
                            callback_function=evp.callback_function,
                            max_timeout=0.1,
                            callback_function_kwargs=callback_function_kwargs,
                            sleep_between_each_scan=0.05,
                            print_elements=True,
                        )
                        yearbin = dada[0].encode()
                        for r in evp.last_results:
                            try:
                                if yearbin in r["Text"]:
                                    break
                            except Exception:
                                errwrite()
                        else:
                            break
                        F.add(5)
                        break
                except Exception:
                    errwrite()
            if F == {0, 1, 2, 3}:
                try:
                    avancarbutton1 = df.loc[
                        (df.cc_Text == b"[Avan\xc3\xa7ar]")
                        & (df.cc_ClassName == b"android.widget.Button")
                        & (df.aa_element_id.str.contains("next", regex=False, na=False))
                    ]
                    if not avancarbutton1.empty:
                        avancarbutton2 = avancarbutton1.sort_values(
                            by=["dd_matchcounter", "aa_start_y"],
                        )
                        avancarbutton2.iloc[0].aa_move_and_tap(0.001)
                        F.add(4)
                        break
                except Exception:
                    errwrite()
            if F == {0, 1, 2}:
                try:
                    textfield1 = df.loc[
                        (df.cc_Text == b"[]")
                        & (df.cc_ClassName == b"android.widget.EditText")
                        & (df.aa_element_id.str.contains("aid=", regex=False, na=False))
                    ]
                    if not textfield1.empty:
                        textfield2 = textfield1.sort_values(
                            by=["dd_matchcounter", "aa_start_y"],
                        )
                        textfield2.iloc[0].aa_move_and_tap(0.001)
                        sendcmd(
                            openshell,
                            inputcmd=f"input text '{mypassword}'",
                            shell=False,
                            timeout=10,
                        )
                        F.add(3)
                        break
                except Exception:
                    errwrite()
            if F == {0, 1}:
                try:
                    avancarbutton1 = df.loc[
                        (df.cc_Text == b"[Avan\xc3\xa7ar]")
                        & (df.cc_ClassName == b"android.widget.Button")
                        & (df.aa_element_id.str.contains("next", regex=False, na=False))
                    ]
                    if not avancarbutton1.empty:
                        avancarbutton2 = avancarbutton1.sort_values(
                            by=["dd_matchcounter", "aa_start_y"],
                        )
                        avancarbutton2.iloc[0].aa_move_and_tap(0.001)
                        F.add(2)
                        break
                except Exception:
                    errwrite()
            if F == {0}:
                try:
                    textfield1 = df.loc[
                        (df.cc_Text == b"[]")
                        & (df.cc_ClassName == b"android.widget.EditText")
                        & (df.aa_element_id.str.contains("aid=", regex=False, na=False))
                    ]
                    if not textfield1.empty:
                        textfield2 = textfield1.sort_values(
                            by=["dd_matchcounter", "aa_start_y"],
                        )
                        textfield2.iloc[0].aa_move_and_tap()
                        sendcmd(
                            openshell,
                            inputcmd=f"input text '{myemail}'",
                            shell=False,
                            timeout=10,
                        )
                        F.add(1)
                        break
                except Exception:
                    errwrite()
            if F == set():
                try:
                    withrighttext = df.loc[
                        (
                            df.cc_Text.apply(
                                lambda x: b"[Inscreva-se gr\xc3\xa1tis]" in x
                            )
                        )
                        & df.aa_classname.str.contains(
                            "StateListAnimatorButton", regex=False, na=False
                        )
                        & df.cc_ClassName.apply(lambda x: b"android.widget.Button" in x)
                        & (
                            df.aa_element_id.str.contains(
                                r"^\s*$", regex=True, na=False
                            )
                        )
                    ]
                    if not withrighttext.empty:
                        withrighttext2 = withrighttext.sort_values(
                            by=["aa_start_y", "dd_matchcounter"],
                        )
                        withrighttext2.iloc[0].aa_move_and_tap(0.001)
                        F.add(0)
                        break
                except Exception:
                    errwrite()
    except Exception as fe:
        errwrite()
    except KeyboardInterrupt:
        break

```