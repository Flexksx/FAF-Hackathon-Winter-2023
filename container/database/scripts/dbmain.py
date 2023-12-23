from dbclasses.Database import Database

db = Database()
db.create.reload_tables()
print(db.extract.subjects())

