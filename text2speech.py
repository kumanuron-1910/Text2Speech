# -*- coding: utf-8 -*-

import PySimpleGUI as sg
from gtts import gTTS
from pygame import mixer
import datetime
import threading
import os


# GUIテーマ設定
sg.theme('LightBlue2')

# GUIレイアウト設定
radio_layout = [[sg.Radio('英語', group_id='lang', key='-En-', default=True),
                 sg.Radio('日本語', group_id='lang', key='-Ja-', default=False)]]

layout = [[sg.Frame(title="言語",  layout=radio_layout, relief=sg.RELIEF_RAISED)],
          [sg.Multiline(size=(100, 10), key='-InputText-')],
          [sg.Button('読み上げ', key='-SpeechButton-'), sg.Button('クリア', key='-ClearButton-'), sg.Button('終了', key='-ExitButton-')]]

window = sg.Window(title='Text2Speech', layout=layout,
                   size=(650, 300), resizable=False)


# Text to speech 関数
def text_to_speech(input_text, language):

    # Text to speech処理
    tts = gTTS(text=input_text, lang=language)

    # 音声ファイル名設定
    get_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = 'Text2Speech_' + get_datetime + '.mp3'
    tts.save(filename)

    # プログラム内での音声再生の初期設定
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()

    # 音声再生中処理
    while True:
        if mixer.music.get_busy() == False:
            mixer.music.stop()
            mixer.music.unload()
            break
    os.remove(filename)


if __name__ == '__main__':

    # イベント処理
    while True:
        event, values = window.read()

        if event == '-ExitButton-' or event == sg.WIN_CLOSED:
            break
        elif event == '-ClearButton-':
            window['-InputText-'].update('')
        elif event == '-SpeechButton-' and values['-InputText-'] == '':
            sg.popup('テキストを入力してください!')
        elif event == '-SpeechButton-' and values['-En-'] == True:
            # スレッド処理
            speech_en_thread = threading.Thread(
                target=text_to_speech, args=(values['-InputText-'], 'en'))
            speech_en_thread.start()
        elif event == '-SpeechButton-' and values['-Ja-'] == True:
            # スレッド処理
            speech_ja_thread = threading.Thread(
                target=text_to_speech, args=(values['-InputText-'], 'ja'))
            speech_ja_thread.start()

    window.close()
