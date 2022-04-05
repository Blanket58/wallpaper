from threading import Thread

import PySimpleGUI as sg

from src import Today, Specify, Random, logger_factory

logger = logger_factory('MAIN')


def today(window):
    logger.info('-' * 70)
    Today().process()
    window.write_event_value('-JOB-', '')


def specify(window, day):
    logger.info('-' * 70)
    Specify().process(day)
    window.write_event_value('-JOB-', '')


def random(window):
    logger.info('-' * 70)
    Random().process()
    window.write_event_value('-JOB-', '')


def main():
    sg.theme('SandyBeach')

    layout = [
        [sg.Text('Automatically download pictures from bing and set it to be desktop wallpaper.')],
        [
            sg.Radio('TODAY', group_id='TYPE', key='-TODAY-', default=True, enable_events=True),
            sg.Radio('DAYS AGO', group_id='TYPE', key='-SPECIFY-', enable_events=True),
            sg.Input(size=(5, 1), key='-SPECIFY_NUMBER-', disabled=True),
            sg.Radio('RANDOM', group_id='TYPE', key='-RANDOM-', enable_events=True)
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

        if event == 'Run' and not thread and values['-TODAY-']:
            thread = Thread(target=today, args=(window,), daemon=True)
            thread.start()
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', transparent_color='white', time_between_frames=100)
        if event == 'Run' and not thread and values['-SPECIFY-']:
            thread = Thread(target=specify, args=(window, values['-SPECIFY_NUMBER-']), daemon=True)
            thread.start()
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, background_color='white', transparent_color='white', time_between_frames=100)
        if event == 'Run' and not thread and values['-RANDOM-']:
            thread = Thread(target=random, args=(window,), daemon=True)
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
