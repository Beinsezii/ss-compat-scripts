# ss-compat-scripts
Python scripts to automatically fix compatibiltiy issues with Star Sector mods on unix OSes with case-sensitive filesystems (Linux/Steam Deck/Mac OSX)

## Usage
Put the python file in your mod root directory and run it. Python is natively available on most systems.

For mod authors, I recommend trying `ss-smart-case.py` as the minimal footprint will make a clean looking git commit

For users who just want a mod to work, I recommend using `ss-murder-case.py` which will force a mod to work whether it wants to or not

## ss-smart-case.py
Attmpets to smartly find which references don't match their appropriate png filenames and correct them
 + Minimal footprint
 - Not comprehensive; will not fix misnamed vanilla references or inferred references like glow maps

## ss-murder-case.py
Replaces every png and its reference with a lower-case version
 + Comprehensive; should fix almost anything
 - Nuclear approach which renames everything even if it's not necessary
