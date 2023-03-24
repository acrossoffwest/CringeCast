
import re
import platform
import os
import langdetect
import subprocess

is_arm = "arm" in platform.processor()
print(f"is arm {is_arm}")

shell_utils_dir = os.path.dirname(os.path.dirname(__file__)) + "/CringeCast/shellscripts"


config = {
    'max_sentence_len':16,
    'max_api_str_len':200
}

def sanitize(s:str)-> str:
    return re.sub('[^0-9a-zA-Z,.?!\'żźćńółęąśŻŹĆĄŚĘŁÓŃ_ ]+', '', s) 

def smart_split(s:str) -> list:
    # since google voice API doesn't respond to strings longer than 200-chars
    # we're stripping longer strings into a couple of requests.
    s_return = []
    for ss in re.split('[.?!]',s):
        if len(ss) <= config['max_api_str_len']:
            s_return.append(ss)
        else:
            #think of something smarter! 
            s_return.append(ss[:config['max_api_str_len']])
    return s_return


def speak_single_sentence(sentence_sane:str, lang_sane:str="en") -> None:
    if is_arm:
        script_name = "speak_arm.sh"
    else:
        script_name = "speak.sh"

    command = f'sh {shell_utils_dir}/{script_name} "{sentence_sane}" {lang_sane}'
    # print("Calling command:" + command)
    os.system(command)

def speak(saying:str,lang:str) -> None:
    saying_sane = sanitize(saying)
    sentences_sane = smart_split(saying_sane)[:config['max_sentence_len']]
    if lang is None:
        try:
            lang_sane = langdetect.detect(sentences_sane[0])
        except langdetect.lang_detect_exception.LangDetectException:
            lang_sane = "en"
    else:
        lang_sane = sanitize(lang)
    [speak_single_sentence(s,lang_sane)
        for s in sentences_sane
    ]

def play_file(filename_no_ext:str) -> None:
    filename_sane = sanitize(filename_no_ext)+".mp3"

    if is_arm:
        script_name = "play_arm.sh"
    else:
        script_name = "play.sh"

    # print("Calling command:" + command)
    subprocess.run([f"{shell_utils_dir}/{script_name}", f"audio_files/{filename_sane}"])

def kill() -> None:
    os.system(f'{shell_utils_dir}/kill.sh')
    
def set_volume(volume:int) -> None:
    if is_arm:
        script_name = "set_vol_arm.sh"
    else:
        script_name = "set_vol.sh"

    os.system(f'{shell_utils_dir}/{script_name} {volume}')
        