import enigne
import db
import os

if __name__ == '__main__':

    init_db = db.DBCreation("bicycle_database.sqlite")
    if os.path.exists("bicycle_database.sqlite") is False:
        init_db.create_tables()
        init_db.populate_tables()

    main_window = enigne.BCGUIEngine()

    init_db.close()