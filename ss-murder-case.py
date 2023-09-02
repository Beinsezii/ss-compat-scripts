#! /usr/bin/env python3
"""
Put in mod root folder and run.
Makes every single png file name and reference lowercase.

Very comprehensive; should fix just about anything automatically
including things that weren't even broken.

Vanilla and core mods seem to all expect lowercase so this
nuclear approach is technically optimal to avoid future problems
"""
__author__ = "Beinsezii"
__license__ = "GNU GPL V3"

import os
import re

assert os.path.exists('./mod_info.json')

text=[]
png=[]

for root, dir, files in os.walk('.'):
    for file in files:
        if file.endswith('.png'):
            png.append((root, file))
        elif file.endswith('.csv'):
            text.append(os.path.join(root, file))
        elif file.endswith('.json'):
            text.append(os.path.join(root, file))
        elif file.endswith('.ship'):
            text.append(os.path.join(root, file))
        elif file.endswith('.skin'):
            text.append(os.path.join(root, file))
        elif file.endswith('.wpn'):
            text.append(os.path.join(root, file))
        elif file.endswith('.proj'):
            text.append(os.path.join(root, file))
        elif file.endswith('.faction'):
            text.append(os.path.join(root, file))

for root, file in png:
    os.rename(os.path.join(root, file), os.path.join(root, file.lower()))

for t in text:
    data = ""
    with open(t, mode='r') as file:
        data = file.read()

    if not '.png' in data:
        continue

    with open(t, mode='w') as file:
        file.write(re.sub(r"[a-zA-Z0-9_]+\.png", lambda m: m.group(0).lower(), data))

