import sqlite3


class DBCreation:

    def __init__(self, database_path: str):
        self.db = sqlite3.connect(f"{database_path}")

    def create_tables(self):
        base_tables = {
            "companies": ("_id INTEGER PRIMARY KEY",
                          "name TEXT"),
            "subsystem_groups": ("_id INTEGER PRIMARY KEY",
                                 "name TEXT NOT NULL"),
            "part_groups": ("_id INTEGER PRIMARY KEY",
                            "name TEXT NOT NULL",
                            "subsystem_group TEXT NOT NULL"),
            "parts": ("_id TEXT PRIMARY KEY",
                      "name TEXT NOT NULL",
                      "part_group TEXT NOT NULL",
                      "company TEXT",
                      "value INTEGER NOT NULL")
        }
        for key in base_tables:
            self.db.execute(f"CREATE TABLE IF NOT EXISTS {key} "
                            f"({','.join(value for value in base_tables[key])})")

    def populate_tables(self):
        subsystems = {"bicycle_base": ("frame",
                                       "saddle",
                                       "seatpost",
                                       "seatpost clamp",
                                       "handlebar",
                                       "stem",
                                       "headset",
                                       "fork",
                                       "grips",
                                       "other",
                                       ),
                      "drive_system": ("front derailleur",
                                       "rear derailleur",
                                       "front gear shifter",
                                       "rear gear shifter",
                                       "crankset",
                                       "pedals",
                                       "chainring",
                                       "casette",
                                       "chain",
                                       "bottom bracket",
                                       "chain guide",
                                       "other",
                                       ),
                      "brake_system": ("front brake",
                                       "rear brake",
                                       "brake pads",
                                       "front brake disc",
                                       "rear brake disc",
                                       "other",
                                       ),
                      "wheels": ("front hub",
                                 "rear hub",
                                 "rim",
                                 "tube",
                                 "tyre",
                                 "other",
                                 )
                      }
        for index, key in enumerate(subsystems):

            self.db.execute("INSERT INTO subsystem_groups (name) VALUES (?)", (key,))

            for value in subsystems[key]:
                self.db.execute("INSERT INTO part_groups (name, subsystem_group) VALUES (?, ?)",
                                (value, index + 1))
        self.db.commit()

    def close(self):
        self.db.close()


class Parts:

    def __init__(self, part_name: str, part_group: str, company: str = None, value: float = 0):
        self.part_name = part_name
        self.part_group = part_group
        self.company = company
        self.value = value
