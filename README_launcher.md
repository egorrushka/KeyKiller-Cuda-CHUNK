<!--
  KeyKiller-Cuda-CHUNK
  https://github.com/egorrushka/KeyKiller-Cuda-CHUNK
  Copyright (C) 2025  egorrushka
  Licensed under GNU AGPL v3 — see LICENSE.txt
  Original code: https://github.com/Qalander/KeyKiller-Cuda
-->

# KeyKiller Launcher 

GUI launcher for `kk.exe` with chunk-based search, progress tracking  
and visual range selection. Written in Python / tkinter (no extra dependencies).

**Requires:** Python 3.8+, Windows 10/11  
**Run:** `python launcher_kk_en.py`  
**Tested on:** NVIDIA RTX A4000 (48×128 cores, SM86), Windows 10 x64, ~1560 Mkey/s

Available in three languages:

| File | Language |
|------|----------|
| `launcher_kk.py`    | 🇷🇺 Russian |
| `launcher_kk_en.py` | 🇬🇧 English |
| `launcher_kk_ua.py` | 🇺🇦 Ukrainian |

---

## Features

### Puzzle selector
- Drop-down list with **48 unsolved puzzles** (#71 – #129)
- Selecting a puzzle **auto-fills**: Bitcoin address, hex range boundaries,  
  slider scale, Start/End fields and the bits label
- Switching puzzles asks whether to clear the visited-range history

### Range slider
- **Dual-handle slider** covering the full puzzle keyspace (0% – 100%)
- **Lock button 🔒** — links both handles so they move together as one,  
  preserving the chunk width (useful for sliding a fixed-size window across the range)
- **Start % / End %** input fields — type exact percentages and press Apply
- **Start HEX / End HEX** input fields — type exact hex values manually
- All four inputs (two % fields + two HEX fields) and the slider are **fully  
  synchronized** — changing any one instantly updates all others
- Visited ranges shown as **green stripes** on the slider track
- **Clear visited** button resets the green history on the track

### Search modes
- **Sequential** — scans Start → End in order; supports backup/resume (`-b` flag)
- **Random (-R)** — picks random positions within the chunk; no resume needed

### Main settings panel
- Path to `kk.exe` with file browser button
- GPU device ID field
- `-b` Resume checkbox (for sequential mode)
- **Save config** / **Load config** — persists all settings to `kk_config.json`

### Parameters / Info block
- Live display of: current puzzle, address, active chunk range, mode, full command

### Test block
- Independent section for testing the key-finding pipeline on a **known address**
- Manual input: Address, Start HEX, End HEX
- Mode selector: Sequential or Random
- **▶ RUN TEST** / **■ STOP** buttons with status indicator
- Separate config saved to `kk_test_config.json` (auto-loaded on startup)
- On key found: alert popup + result copied to `TEST_FOUND_<timestamp>.txt`

### Key found detection
- Background watcher monitors `found.txt` by **modification time**  
  (not file size — avoids false negatives when the file already exists from a previous run)
- On detection: popup alert, log entry, found key copied to `FOUND_<timestamp>.txt`
- Visited range automatically marked green on the slider after a completed run

### Launch behavior
- `kk.exe` runs in a **separate CMD window** — full GPU output visible there
- Launcher journal shows: timestamps, command used, start/stop events, found keys
- **Stop** button force-kills the kk.exe process tree via `taskkill /F /T`

---

## Saved files

| File | Contents |
|------|----------|
| `kk_config.json`      | Main settings: exe path, puzzle, GPU, mode, chunk, % values |
| `kk_test_config.json` | Test block settings: address, range, mode |
| `kk_history.json`     | Visited ranges shown on the slider (per puzzle) |
| `kk_progress.json`    | Current session: puzzle, address, chunk, mode, start time |
| `found.txt`           | Written by kk.exe when a key is found |
| `FOUND_<ts>.txt`      | Copy made by launcher at the moment of detection |
| `TEST_FOUND_<ts>.txt` | Copy made by launcher after a test run finds a key |

---

## Quick start

1. Place `launcher_kk_en.py` in the same folder as `kk.exe`
2. Run: `python launcher_kk_en.py`
3. Select a puzzle from the dropdown (e.g. **Puzzle 71**)
4. Set your chunk using the slider or the HEX / % fields
5. Choose a mode: Sequential or Random
6. Press **▶ START** — kk.exe opens in a separate CMD window
7. When the run completes, the chunk is automatically marked green on the slider

### Verify the setup before real searching

Use the **Test Block** to confirm everything works correctly:
- Address: `1PWCx5fovoEaoBowAvF5k91m2Xat9bMgwb`
- Start HEX: `400000000`
- End HEX: `7FFFFFFFF`
- Mode: Sequential

The key should be found in under 1 second on RTX A4000.

---

## Notes

- Only **Compressed P2PKH** addresses are supported (puzzles #51 and above)
- Puzzles #1–#50 use Uncompressed keys — kk.exe will not find them
- All JSON config files can be edited manually if needed
- All three language versions share the same config files — switching languages  
  does not lose any saved settings
