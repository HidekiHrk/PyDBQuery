from pydbquery.sqlite3 import Database
db = Database()
tbl1 = db.create_table("Person", name=str, age=int, gender=str)
hdk = tbl1.all().filter(name="Hideki")
if len(hdk) > 0:
    hideki = hdk[0]
else:
    hideki = tbl1.add(name="Hideki", age=17, gender="male")
print(f"Name: {hideki.name}\nAge: {hideki.age}\nGender: {hideki.gender}")
print(tbl1.all().objects)
hideki.name = "ata"
hideki.save()
print(tbl1.all().objects[0].name)
hideki.delete()
tbl1.delete()