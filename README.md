# Clap-to-Claude

Listen on your microphone and open the **Claude desktop app** with a **double clap**.

A tiny background script for Windows. It watches the mic for two quick claps in a
row and launches Claude. That's it.

## Requirements

- Windows 10/11
- [Python 3](https://www.python.org/downloads/) (3.10+ recommended)
- The [Claude desktop app](https://claude.ai/download) installed
- A working microphone

## Install

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python clap_to_claude.py
```

Double-clap and Claude opens. Stop with `Ctrl+C`.

## Tuning

If it triggers too easily or misses your claps, watch your live mic levels and
pick a threshold:

```powershell
python clap_to_claude.py --calibrate
```

Then set `--threshold` (peak loudness, 0..1) and/or pick a specific mic:

```powershell
python clap_to_claude.py --devices              # list input devices
python clap_to_claude.py --threshold 0.3 --device 2
```

A clap usually peaks around `0.3`-`0.6` depending on your mic; pick a threshold
a bit below your clap peaks but above background noise.

## Run it at startup (optional)

1. Press `Win + R`, type `shell:startup`, press Enter.
2. Create a shortcut in that folder pointing to:
   ```
   pythonw.exe "C:\full\path\to\clap_to_claude.py"
   ```
   (`pythonw.exe` instead of `python.exe` runs it silently with no console window.)

## Note on the Claude launch ID

The script launches Claude via its app ID:

```
shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude
```

This is the same for standard Claude desktop installs. If yours differs, find it with:

```powershell
Get-StartApps | Where-Object { $_.Name -match 'claude' }
```

and update `CLAUDE_AUMID` near the top of `clap_to_claude.py`.

## License

See [LICENSE](LICENSE). Free to download and use; please don't modify or
redistribute.
