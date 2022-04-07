from pathlib import Path
from subprocess import Popen
from threading import Thread

import PySimpleGUI as sg

from src import *

logger = logger_factory('MAIN')


def today(cls, window):
    Today(cls).process()
    window.write_event_value('-JOB-', '')


def specify(cls, window, day):
    Specify(cls).process(day)
    window.write_event_value('-JOB-', '')


def random(cls, window):
    Random(cls).process()
    window.write_event_value('-JOB-', '')


def main():
    sg.theme('SandyBeach')

    layout = [
        [sg.Text('Automatically download pictures from bing and set it to be desktop wallpaper.')],
        [
            sg.Frame(
                'Mode',
                [
                    [sg.Radio('TODAY', group_id='TYPE', key='-TODAY-', default=True, enable_events=True)],
                    [
                        sg.Radio('DAYS AGO', group_id='TYPE', key='-SPECIFY-', enable_events=True),
                        sg.Input(size=(5, 1), key='-SPECIFY_NUMBER-', disabled=True)
                    ],
                    [sg.Radio('RANDOM', group_id='TYPE', key='-RANDOM-', enable_events=True)]
                ]
            ),
            sg.Frame(
                'Extractor',
                [
                    [sg.Combo(['Bing', 'IoLiuAPI'], default_value='IoLiuAPI', key='-EXTRACTOR-')]
                ]
            ),
            sg.Frame(
                'Options',
                [
                    [sg.Button('Open Pictures Folder', key='-Pictures-')],
                    [sg.Button('Reset Database', key='-RESET-', button_color='red')]
                ]
            )
        ],
        [
            sg.Button('Run'),
            sg.Button('Exit')
        ],
        [sg.MLine(size=(80, 20), key='-LOG-', reroute_stdout=True, write_only=True, autoscroll=True, auto_refresh=True)],
    ]

    window = sg.Window('Bing Wallpaper', layout, finalize=True)

    thread = None
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == '-SPECIFY-':
            window['-SPECIFY_NUMBER-'].update(disabled=False)
        if event in ('-TODAY-', '-RANDOM-'):
            window['-SPECIFY_NUMBER-'].update(disabled=True)

        if event == '-RESET-':
            with DataBase() as db:
                db.reset()
        if event == '-Pictures-':
            pictures_path = Path('pic').absolute()
            Popen(f'explorer {pictures_path}')

        if event == 'Run' and not thread:
            logger.info('-' * 70)
            if values['-EXTRACTOR-'] == 'Bing':
                cls = Bing
            else:
                cls = IoLiuAPI
            if values['-TODAY-']:
                thread = Thread(target=today, args=(cls, window,), daemon=True)
            if values['-SPECIFY-']:
                thread = Thread(target=specify, args=(cls, window, values['-SPECIFY_NUMBER-']), daemon=True)
            if values['-RANDOM-']:
                thread = Thread(target=random, args=(cls, window,), daemon=True)
            thread.start()
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', transparent_color='white', time_between_frames=100)

        if event == '-JOB-':
            thread.join()
            sg.popup_animated(None)
            thread = None
        if thread is not None:
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', transparent_color='white', time_between_frames=100)
    window.close()


if __name__ == '__main__':
    main()
