import sqlite3


class DBCreation:

    def __init__(self, database_path: str):
        self.db = sqlite3.connect(f"{database_path}")

    def create_tables(self):
        base_tables = {
            "companies": ("_id INTEGER PRIMARY KEY AUTOINCREMENT",
                          "name TEXT"),
            "subsystem_groups": ("_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                 "name TEXT NOT NULL"),
            "part_groups": ("_id INTEGER PRIMARY KEY AUTOINCREMENT",
                            "name TEXT NOT NULL",
                            "subsystem_group TEXT NOT NULL"),
            "parts": ("_id INTEGER PRIMARY KEY AUTOINCREMENT",
                      "name TEXT NOT NULL",
                      "company TEXT",
                      "value FLOAT NOT NULL",
                      "part_group TEXT NOT NULL"),
            "custom_subsystems": ("_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                  "name TEXT NOT NULL",
                                  "subsystem_group TEXT NOT NULL",
                                  "chosen_parts TEXT")
        }
        for key in base_tables:
            self.db.execute(f"CREATE TABLE IF NOT EXISTS {key} "
                            f"({','.join(value for value in base_tables[key])})")
        self.db.commit()

    def populate_tables(self):
        subsystems = {"Bicycle base": ("Frame",
                                       "Saddle",
                                       "Seatpost",
                                       "Seatpost clamp",
                                       "Handlebar",
                                       "Stem",
                                       "Headset",
                                       "Fork",
                                       "Grips",
                                       "Other",
                                       ),
                      "Drive system": ("Front derailleur",
                                       "Rear derailleur",
                                       "Front gear shifter",
                                       "Rear gear shifter",
                                       "Crankset",
                                       "Pedals",
                                       "Chainring",
                                       "Casette",
                                       "Chain",
                                       "Bottom bracket",
                                       "Chain guide",
                                       "Other",
                                       ),
                      "Brake system": ("Front brake",
                                       "Rear brake",
                                       "Brake pads",
                                       "Front brake disc",
                                       "Rear brake disc",
                                       "Other",
                                       ),
                      "Wheels": ("Front hub",
                                 "Rear hub",
                                 "Rim",
                                 "tube",
                                 "Tyre",
                                 "Other",
                                 )
                      }
        for key in subsystems:

            self.db.execute("INSERT INTO subsystem_groups (name) VALUES (?)", (key,))

            for value in subsystems[key]:
                self.db.execute("INSERT INTO part_groups (name, subsystem_group) VALUES (?, ?)",
                                (value, key))
        self.db.commit()

    def get_subsystem_list(self, subsystem_group):
        subsystem_list = []

        for row in self.db.execute("SELECT "
                                   "_id, name, subsystem_group, chosen_parts  "
                                   "FROM custom_subsystems"):
            if row[2] == subsystem_group:
                subsystem_list.append(row[1])

        if not subsystem_list:
            subsystem_list = ["Please add subsystem"]

        return subsystem_list

    def subsystem_input(self, values: tuple):
        self.db.execute("INSERT INTO custom_subsystems (name, subsystem_group) VALUES (?, ?)", values)
        self.db.commit()

    def part_input(self, values: tuple):
        self.db.execute("INSERT INTO parts (name, company, value, part_group) VALUES (?, ?, ?, ?)", values)
        self.db.commit()

    def get_table_names_list(self,
                             table_name: str,
                             column_filter: str = None,
                             column_filter_value: str = None):
        table_name_list = []
        if column_filter is None or column_filter_value is None:
            for row in self.db.execute(f"SELECT name FROM {table_name}").fetchall():
                table_name_list.append(row[0])
        else:
            for row in self.db.execute(f"SELECT name FROM {table_name} "
                                       f"WHERE {column_filter} = {column_filter_value}").fetchall():
                table_name_list.append(row[0])
        return table_name_list

    def close(self):
        self.db.close()
