# Clap-to-Claude

Listen on your microphone and open the **Claude desktop app** with a **double clap**.

A tiny background script for Windows. It watches the mic for two quick claps in a
row and launches Claude. That's it.

---

## 🟢 Beginner's guide (start here if you're not techy)

Follow these steps in order. It takes about 5 minutes. **This only works on a
Windows PC or laptop — not on a phone.**

### Step 1 — Install Python
1. Go to <https://www.python.org/downloads/> and click the big **Download Python** button.
2. Open the downloaded file.
3. **IMPORTANT:** on the first screen, tick the box that says
   **"Add Python to PATH"** at the bottom. Then click **Install Now**.
4. When it finishes, click **Close**.

### Step 2 — Install the Claude desktop app
- Download and install it from <https://claude.ai/download>. Open it once to make
  sure it works, then you can close it.

### Step 3 — Download this project
1. On this GitHub page, click the green **`< > Code`** button (near the top right).
2. Click **Download ZIP**.
3. Find the downloaded `clap-to-claude-main.zip` (usually in your **Downloads**
   folder), right-click it, and choose **Extract All… → Extract**.

### Step 4 — Install what the script needs
1. Open the extracted folder.
2. Click in the address bar at the top of the folder window, type `powershell`,
   and press **Enter**. (A blue window opens, already in the right folder.)
3. Type this and press **Enter**:
   ```powershell
   pip install -r requirements.txt
   ```
   Wait for it to finish (a few lines of text).

### Step 5 — Run it
In that same blue window, type and press **Enter**:
```powershell
python clap_to_claude.py
```
Now **clap twice quickly** — Claude should open! 🎉

To stop it, click the blue window and press **Ctrl + C**, or just close the window.

### Step 6 (optional) — Make it start automatically when you turn on your PC
So you never have to launch it manually:
1. Press **Win + R**, type `shell:startup`, press **Enter**. A folder opens.
2. Right-click inside it → **New → Shortcut**.
3. For the location, paste this (replace the path with where *your* file actually is):
   ```
   pythonw.exe "C:\Users\YourName\Downloads\clap-to-claude-main\clap_to_claude.py"
   ```
   Tip: `pythonw.exe` (with a "w") runs it silently in the background with no window.
4. Click **Next → Finish**. Done — it'll run quietly every time you start Windows.

---

## ⚙️ Make it your own (things you can change)

Open `clap_to_claude.py` in **Notepad** (right-click → Open with → Notepad) and
look near the top for the `# --- Tunables ---` section. Change a number, save the
file, and run it again.

| Setting | What it does | Try this if… |
|---|---|---|
| `THRESHOLD` (0.35) | How loud a clap must be to count (0–1). | It misses your claps → **lower** it (e.g. 0.25). It triggers by accident → **raise** it (e.g. 0.45). |
| `DOUBLE_MIN` (0.12) | Shortest gap allowed between the two claps (seconds). | Fast double-claps aren't registering → lower it slightly. |
| `DOUBLE_MAX` (0.80) | Longest gap allowed between the two claps (seconds). | You clap slowly → raise it. Two unrelated claps trigger it → lower it. |
| `CLAP_REFRACTORY` (0.15) | Brief "deaf" period after a clap so its echo isn't counted twice. | Echoey room causing false double-claps → raise it a little. |
| `LAUNCH_COOLDOWN` (3.0) | Won't re-open Claude again within this many seconds. | — |
| `CLAUDE_AUMID` | The app that gets launched. | **You can make it open a different app!** See below. |

### Find the right sensitivity for your mic
Not sure what number to use? Run this to watch your live mic levels while you clap:
```powershell
python clap_to_claude.py --calibrate
```
Pick a `THRESHOLD` a bit **below** your clap peaks but **above** the background noise.

You can also set it from the command line without editing the file:
```powershell
python clap_to_claude.py --devices               # list your microphones
python clap_to_claude.py --threshold 0.3 --device 2   # use a specific mic + sensitivity
```

### Open a different app instead of Claude (advanced, optional)
The line `CLAUDE_AUMID = ...` is just the ID of the app to open. To launch a
different installed app, find its ID by running this in PowerShell:
```powershell
Get-StartApps
```
Copy the `AppID` of the app you want, and replace the value of `CLAUDE_AUMID`
with `shell:AppsFolder\<that AppID>`.

---

## For developers (quick version)

```powershell
pip install -r requirements.txt
python clap_to_claude.py
```

CLI flags: `--calibrate`, `--devices`, `--device <n>`, `--threshold <0..1>`.

The Claude launch ID used is `shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude`,
which is standard for Claude desktop installs.

---

## License

See [LICENSE](LICENSE). Free to download and use; please don't modify or
redistribute.
