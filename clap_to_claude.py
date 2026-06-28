"""
Clap-to-Claude: listen on the microphone and open the Claude desktop app
on a DOUBLE clap.

Usage:
    python clap_to_claude.py             # run the listener
    python clap_to_claude.py --calibrate # watch live levels to pick a threshold
    python clap_to_claude.py --devices   # list input devices
    python clap_to_claude.py --threshold 0.4 --device 2

Tweak THRESHOLD if it triggers too easily (raise it) or misses claps (lower it).
Stop with Ctrl+C.
"""

import argparse
import subprocess
import sys
import time

import numpy as np
import sounddevice as sd

# --- Tunables -----------------------------------------------------------
SAMPLE_RATE = 44100
BLOCK = 1024                 # ~23 ms per audio block
THRESHOLD = 0.35            # peak amplitude (0..1) that counts as a "loud" sound
CLAP_REFRACTORY = 0.15      # ignore this long after a clap (kills its own echo)
DOUBLE_MIN = 0.12           # min gap between the two claps (seconds)
DOUBLE_MAX = 0.80           # max gap between the two claps (seconds)
LAUNCH_COOLDOWN = 3.0       # don't relaunch within this many seconds

# Claude desktop app launch ID (from `Get-StartApps`)
CLAUDE_AUMID = r"shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude"
# ------------------------------------------------------------------------


def open_claude():
    # explorer.exe resolves the AppsFolder shell path and launches the MSIX app
    subprocess.Popen(["explorer.exe", CLAUDE_AUMID])


def list_devices():
    print(sd.query_devices())


def calibrate(device, threshold):
    print(f"Calibrating. Threshold is {threshold}. Clap and watch the peaks.")
    print("Pick a threshold a bit below your clap peaks but above background. Ctrl+C to stop.\n")
    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK,
                        device=device) as stream:
        while True:
            data, _ = stream.read(BLOCK)
            peak = float(np.abs(data).max())
            bar = "#" * int(peak * 60)
            flag = "  <== over threshold" if peak >= threshold else ""
            print(f"{peak:0.3f} |{bar}{flag}")


def run(device, threshold):
    print(f"Listening for double claps (threshold={threshold}). Ctrl+C to stop.")
    last_clap = 0.0          # time of the most recent single clap
    last_launch = 0.0
    in_clap = False          # are we currently inside a loud transient?

    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK,
                        device=device) as stream:
        while True:
            data, _ = stream.read(BLOCK)
            peak = float(np.abs(data).max())
            now = time.monotonic()

            if peak >= threshold:
                # rising edge = the start of a new clap (not the same one held)
                if not in_clap and (now - last_clap) > CLAP_REFRACTORY:
                    gap = now - last_clap
                    if DOUBLE_MIN <= gap <= DOUBLE_MAX and (now - last_launch) > LAUNCH_COOLDOWN:
                        print(">>> Double clap! Opening Claude.")
                        open_claude()
                        last_launch = now
                        last_clap = 0.0     # reset so a 3rd clap doesn't chain
                    else:
                        last_clap = now
                in_clap = True
            else:
                in_clap = False


def main():
    p = argparse.ArgumentParser(description="Open Claude on a double clap.")
    p.add_argument("--calibrate", action="store_true", help="show live mic levels")
    p.add_argument("--devices", action="store_true", help="list input devices")
    p.add_argument("--device", type=int, default=None, help="input device index")
    p.add_argument("--threshold", type=float, default=THRESHOLD, help="clap loudness 0..1")
    args = p.parse_args()

    if args.devices:
        list_devices()
        return
    try:
        if args.calibrate:
            calibrate(args.device, args.threshold)
        else:
            run(args.device, args.threshold)
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
