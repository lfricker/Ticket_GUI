import json


class mySettings:

    def __init__(self):
        print("mySettings Class created, ready to use")
        self.settingsAvailable = False
        self._font_defaults = {
            "name": {"family": "Arial", "size": 14, "file": ""},
            "datum": {"family": "Arial", "size": 9, "file": ""},
            "platz": {"family": "Arial", "size": 20, "file": ""},
        }

    def openSettings(self, path):
        if self.settingsAvailable == False:
            self.settingsAvailable = True
            # open the file
            print("Reading settings from ", path)
            self.path = path
            with open(path) as settingsFile:
                self.settings = json.load(settingsFile)
            self.__ensure_defaults()

    def getItemValue(self, item):
        if self.settingsAvailable:
            # search for the item and return
            print("Searching for ", item)
            print(self.settings[item])
            return self.settings[item]
        else:
            return 0

    def setItemValue(self, item, val):
        if self.settingsAvailable:
            self.settings[item] = val
            print("setting new value for", item)

    def saveSettings(self):
        if self.settingsAvailable:
            with open(self.path, "w") as outfile:
                json.dump(self.settings, outfile, indent=4)

    def createSettings(self, path):
        self.path = path
        # create the settings structure
        newSettings = {
            "veranstalter": "",
            "veranstaltung": "",
            "positionen": {
                "name": {"x": 0, "y": 0, "r": 0, "c": False},
                "platz": {"x": 0, "y": 0, "r": 0, "c": False},
                "datum": {"x": 0, "y": 0, "r": 0, "c": False},
            },
            "fonts": {k: v.copy() for k, v in self._font_defaults.items()},
        }
        with open(path, "w") as outfile:
            json.dump(newSettings, outfile, indent=4)
        self.openSettings(path)

    def __ensure_defaults(self):
        """Ensure new default sections exist when loading older files."""
        changed = False
        if "fonts" not in self.settings:
            self.settings["fonts"] = self._font_defaults.copy()
            changed = True
        else:
            # backfill missing font entries or keys
            for key, default in self._font_defaults.items():
                if key not in self.settings["fonts"]:
                    self.settings["fonts"][key] = default.copy()
                    changed = True
                else:
                    font_entry = self.settings["fonts"][key]
                    if "family" not in font_entry:
                        font_entry["family"] = default["family"]
                        changed = True
                    if "size" not in font_entry:
                        font_entry["size"] = default["size"]
                        changed = True
                    if "file" not in font_entry:
                        font_entry["file"] = default["file"]
                        changed = True

        if changed:
            self.saveSettings()
