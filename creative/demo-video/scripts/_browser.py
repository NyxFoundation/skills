"""Launch Chromium for record.py / snap.py, tolerating machines where
Playwright's own download is missing or unrunnable (NixOS, locked-down CI).

Order: $DEMO_CHROMIUM → Playwright's bundled build → a system chromium/chrome
on PATH → any chromium in the nix store. Recording and screenshots only need
a Chromium that starts; the exact build does not matter.
"""
import glob, os, shutil


def _candidates():
    env = os.environ.get("DEMO_CHROMIUM")
    if env:
        yield env
    for name in ("chromium", "chromium-browser", "google-chrome-stable", "google-chrome"):
        found = shutil.which(name)
        if found:
            yield found
    for path in sorted(glob.glob("/nix/store/*-chromium-*/bin/chromium"), reverse=True):
        yield path


def launch_chromium(p, **kw):
    """p is a sync_playwright() context. Returns a launched Browser."""
    if not os.environ.get("DEMO_CHROMIUM"):
        try:
            return p.chromium.launch(**kw)
        except Exception as first:
            err = first
    else:
        err = None
    for exe in _candidates():
        try:
            b = p.chromium.launch(executable_path=exe, **kw)
            print(f"[demo] using chromium at {exe}")
            return b
        except Exception as e:
            err = e
    raise SystemExit(
        f"could not launch chromium ({err}).\n"
        "Fix with `playwright install chromium`, or point DEMO_CHROMIUM at a chromium binary."
    )
