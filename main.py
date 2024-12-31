import subprocess
import sys
import re

def get_app_info(appid):
    result = subprocess.run(
        ["steamcmd", "+login", "anonymous", "+app_info_request", str(appid), "+login", "anonymous", "+app_info_print", str(appid), "+logoff", "+quit"],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    return result.stdout

def extract_paths_and_roots(app_info):
    paths_and_roots = re.findall(r'"root"\s+"([^"]+)"|"path"\s+"([^"]+)"', app_info)
    return paths_and_roots

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <appid>")
        sys.exit(1)

    appid = sys.argv[1]
    app_info = get_app_info(appid)
    paths_and_roots = extract_paths_and_roots(app_info)
    
    current_root = None
    for match in paths_and_roots:
        root, path = match
        if root:
            if root == "WinMyDocuments":
                current_root = r"%UserProfile%\Documents"
            elif root == "WinAppDataLocal":
                current_root = r"%Localappdata%"
            elif root == "gameinstall":
                current_root = r"Steam Library\steamapps\common\gamename"
            else:
                current_root = root
        if path:
            combined_path = f"{current_root}\\{path}".replace('/', '\\')
            print(combined_path)