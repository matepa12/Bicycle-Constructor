import engine
import db
import os

if __name__ == '__main__':

    db_path = "bicycle_database.sqlite"

    if os.path.exists(db_path) is False:
        init_db = db.DBCreation(db_path)
        init_db.create_tables()
        init_db.populate_tables()
    else:
        init_db = db.DBCreation(db_path)

    main_window = engine.Engine(init_db)
    main_window.mainloop()

    init_db.close()