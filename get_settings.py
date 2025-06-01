import json

def get_settings() -> dict:
    default_settings = {
        "version_check": True,
        "always_top_window": True,
    }
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            app_settings = json.load(f)
    except Exception as e:
        print(f"Error reading settings: {e}")
        app_settings = default_settings
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(app_settings, f, indent=4)


    return app_settings

