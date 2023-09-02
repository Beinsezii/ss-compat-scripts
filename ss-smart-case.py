#! /usr/bin/env python3
"""
Put in mod root folder and run.
Changes all refs to match actual names of PNGs
Also changes all backslashes to forward slashes

Less complete than the murder case approach.
Will not fix issues like "sHiP_glow1.png" since
the glow names are inferred and not referenced directly.
'Will also not fix incorrectly referencing vanilla assets.
"""
__author__ = "Beinsezii"
__license__ = "GNU GPL V3"

import os
import re
import difflib

assert os.path.exists('./mod_info.json')

EXT="png"

RE=re.compile(f'(?P<root>[a-zA-Z0-9_/\\\\]*?)(?P<file>[a-zA-Z0-9_]+\.{EXT})')

DRY=False

refs=[]
targets={}

def fix(match):
    try:
        return targets[os.path.join(match.group('root').replace('\\', '/'), match.group('file').lower()).lstrip('./')]
    except KeyError as e: # mods may ref vanilla assets which key errs
        return match.group(0)

for root, dir, files in os.walk('.'):
    for file in files:
        if file.endswith(f'.{EXT}'):
            targets[os.path.join(root, file.lower()).lstrip('./')] = os.path.join(root, file).lstrip('./')
        elif file.endswith('.csv'):
            refs.append(os.path.join(root, file))
        elif file.endswith('.json'):
            refs.append(os.path.join(root, file))
        elif file.endswith('.ship'):
            refs.append(os.path.join(root, file))
        elif file.endswith('.skin'):
            refs.append(os.path.join(root, file))
        elif file.endswith('.wpn'):
            refs.append(os.path.join(root, file))
        elif file.endswith('.proj'):
            refs.append(os.path.join(root, file))
        elif file.endswith('.faction'):
            refs.append(os.path.join(root, file))

for r in refs:
    data = ""
    with open(r, mode='r') as file:
        data = file.read()

    if not f'.{EXT}' in data:
        continue

    new = RE.sub(fix, data)

    if new != data:
        if DRY:
            print('\n'.join(difflib.ndiff(data.split('\n'), new.split('\n'))))
        else:
            with open(r, mode='w') as file:
                file.write(new)

