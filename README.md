# Cursor Focus 🟡

A lightweight Windows utility that highlights your mouse cursor with a yellow ring.

## Setup

1. Run `App.exe` once.
2. Move `App.exe` into your Windows Startup folder if you want Cursor Focus to launch automatically when you sign in.
3. After that, no additional setup is required.

### Open the Startup Folder

Press:

`Win + R`

Then enter:

`shell:startup`

and press Enter.

Place `App.exe` in the folder that opens.

## Hotkey

`Ctrl + Shift + Alt + Z`

Press the hotkey to show the cursor highlight for 5 seconds.

## Features

* Yellow cursor highlight
* Auto-hides after 5 seconds
* Lightweight overlay
* Global hotkey
* Optional automatic startup with Windows

## Run from Source

```bash
python App.py
```

## Build

```bash
python -m PyInstaller --onefile --noconsole App.py
```
