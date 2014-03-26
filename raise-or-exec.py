#!/usr/bin/env python

import argparse
import daemon
import itertools
import pipes
import subprocess


# required packages:
# wmctrl, ratmenu, python-daemon

(
    WMCTRL_WID,
    WMCTRL_DESKTOP,
    WMCTRL_WCLASS,
    WMCTRL_MACHINE,
    WMCTRL_TITLE,
) = range(5)


def run(command):
    with daemon.DaemonContext():
        subprocess.check_call(command)


def activate_cmd(window_info):
    return ['wmctrl', '-ia', window_info[WMCTRL_WID]]


def activate(window_info):
    run(activate_cmd(window_info))


def activate_shell(window_info):
    return ' '.join(
        pipes.quote(part)
        for part in activate_cmd(window_info)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('window_class')
    parser.add_argument('command', nargs='+')
    args = parser.parse_args()

    window_info = [
        line.split()
        for line in subprocess.check_output('wmctrl -lx'.split()).splitlines()
    ]
    matching_windows = [
        info
        for info in window_info
        if info[WMCTRL_WCLASS] == args.window_class
    ]

    matching_windows_count = len(matching_windows)
    if matching_windows_count == 0:
        print('no windows found - starting new')
        run(args.command)
    elif matching_windows_count == 1:
        print('window found - raising')
        activate(matching_windows[0])
    else:
        print('more than one window found - showing selection menu')
        assert matching_windows_count > 1
        menu_items = itertools.chain.from_iterable(
            (' '.join(info[WMCTRL_TITLE:]), activate_shell(info))
            for info in matching_windows
        )
        run(
            ['ratmenu', '-fg', 'green', '-bg', 'black', '-style', 'dreary']
            + list(menu_items)
        )


if __name__ == '__main__':
    main()
