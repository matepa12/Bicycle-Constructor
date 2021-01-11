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
                      "name TEXT NOT NULL UNIQUE",
                      "company TEXT",
                      "value FLOAT NOT NULL",
                      "part_group TEXT NOT NULL"),
            "custom_subsystems": ("_id INTEGER PRIMARY KEY AUTOINCREMENT",
                                  "name TEXT NOT NULL UNIQUE",
                                  "subsystem_group TEXT NOT NULL",
                                  "chosen_parts TEXT DEFAULT empty")
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

    def company_input(self, values: tuple):
        self.db.execute("INSERT INTO companies (name) VALUES (?)", values)
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
                                       f"WHERE {column_filter} = ?", (column_filter_value,)).fetchall():
                table_name_list.append(row[0])
        return table_name_list

    def read_custom_subsystem_parts(self, subsystem_name: str) -> set:
        if subsystem_name == 'Please add subsystem' or subsystem_name == '':
            return set()
        parts_cursor = self.db.execute(f"SELECT chosen_parts FROM custom_subsystems WHERE name = ?",
                                       (subsystem_name,)).fetchone()
        if not parts_cursor:
            return set()

        if parts_cursor[0] == "empty" or not parts_cursor[0]:
            return set()
        else:
            chosen_parts = set(map(int, parts_cursor[0].split(".")))
            return chosen_parts

    def read_custom_subsystem_column(self):
        parts_cursor = self.db.execute(f"SELECT name, chosen_parts FROM custom_subsystems").fetchall()
        row_list = []
        for row in parts_cursor:
            if row[1]:
                name = row[0]
                chosen_parts = set(map(int, row[1].split(".")))
                row_list.append((name, chosen_parts))
        return row_list

    def write_custom_subsystem_parts(self, updated_parts: set, subsystem_name: str):
        to_be_updated = ".".join(set(map(str, updated_parts)))
        self.db.execute("UPDATE custom_subsystems SET chosen_parts = ? WHERE name = ?",
                        (to_be_updated, subsystem_name))
        self.db.commit()

    def get_part_id(self, part_name: str):
        cursor = self.db.execute("SELECT _id FROM parts WHERE name = ?", (part_name,))
        return cursor.fetchone()[0]

    def get_part_attribute_from_id(self, attribute: str, part_id: int):
        cursor = self.db.execute(f"SELECT {attribute} FROM parts WHERE _id = ?", (part_id,))
        return cursor.fetchone()[0]

    def remove_record(self, table: str, name: str):
        self.db.execute(f"DELETE FROM {table} WHERE name = ?", (name,))
        self.db.commit()

    def close(self):
        self.db.close()
