from easy_db import DataBase
db = DataBase(db_location_str="sqlite.db", create_if_none=True)

db.create_table("Player", { 
  "ID": int,
  "IP": str,
  "x": float,
  "y": float,
  "z": float,
  "w": float
})
