import os
import shutil
import subprocess
import platform


def ensure_firefox(build_dir):
    import sys
    import requests

    firefox_bin = os.path.join(build_dir, "firefox", "firefox")
    if os.path.exists(firefox_bin):
        return firefox_bin
    # Download latest Firefox ESR for Linux x86_64
    url = (
        "https://download.mozilla.org/?product=firefox-esr-latest&os=linux64&lang=en-US"
    )
    tar_path = os.path.join(build_dir, "firefox.tar.bz2")
    print("Downloading Firefox ESR...")
    subprocess.run(["wget", url, "-O", tar_path], check=True)
    subprocess.run(["tar", "-xjf", tar_path, "-C", build_dir], check=True)
    os.remove(tar_path)
    # Firefox is extracted to build_dir/firefox
    return firefox_bin


def ensure_geckodriver():
    import sys

    build_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "build")
    os.makedirs(build_dir, exist_ok=True)
    gecko_path = os.path.join(build_dir, "geckodriver")
    firefox_bin = ensure_firefox(build_dir)
    if shutil.which("geckodriver") or os.path.exists(gecko_path):
        # Add to PATH if not already
        if gecko_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = build_dir + os.pathsep + os.environ.get("PATH", "")
        # Set environment variable for Firefox binary
        os.environ["FIREFOX_BINARY"] = firefox_bin
        return
    sysname = platform.system().lower()
    if sysname == "linux":
        import requests

        url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
        resp = requests.get(url)
        for asset in resp.json()["assets"]:
            if asset["name"].endswith("linux64.tar.gz"):
                download_url = asset["browser_download_url"]
                break
        else:
            raise RuntimeError("No linux64 geckodriver found in latest release.")
        subprocess.run(
            ["wget", download_url, "-O", os.path.join(build_dir, "geckodriver.tar.gz")],
            check=True,
        )
        subprocess.run(
            ["tar", "-xzf", os.path.join(build_dir, "geckodriver.tar.gz")],
            cwd=build_dir,
            check=True,
        )
        subprocess.run(
            ["chmod", "+x", os.path.join(build_dir, "geckodriver")], check=True
        )
        os.remove(os.path.join(build_dir, "geckodriver.tar.gz"))
        os.environ["PATH"] = build_dir + os.pathsep + os.environ.get("PATH", "")
        os.environ["FIREFOX_BINARY"] = firefox_bin
    else:
        raise NotImplementedError("Only Linux is supported in this script.")
