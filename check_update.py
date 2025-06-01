import json
import requests

def check_update() -> bool:
    with open("version.json", "r", encoding="utf-8") as f:
        version_info = json.load(f)
    current_version = version_info["version"]

    url = "https://raw.githubusercontent.com/ugokitakunai/meijo-icp-virt-printer-server/refs/heads/main/version.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        latest_version_info = response.json()
        latest_version = latest_version_info["version"]

        major_current, minor_current, patch_current = map(int, current_version.split('.'))
        major_latest, minor_latest, patch_latest = map(int, latest_version.split('.'))

        if (major_latest > major_current or
            (major_latest == major_current and minor_latest > minor_current) or
            (major_latest == major_current and minor_latest == minor_current and patch_latest > patch_current)):
            return True
        else:
            return False
    except requests.RequestException as e:
        return False
    
if __name__ == "__main__":
    if check_update():
        print("アップデートがあります。")
    else:
        print("アップデートはありません。")