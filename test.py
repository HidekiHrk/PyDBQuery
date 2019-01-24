from pydbquery.sqlite3 import Database
db = Database()
tbl1 = db.create_table("Person", name=str, age=int, gender=str, items=list, money=float)
hdk = tbl1.all().filter(name="Hideki")
if len(hdk) > 0:
    hideki = hdk[0]
else:
    hideki = tbl1.add(name="Hideki", age=17, gender="male", items=['opa', 'eae'], money=4)
print(f"Name: {hideki.name}\nAge: {hideki.age}\nGender: {hideki.gender}\nItems: {hideki.items}")
print(tbl1.all().objects)
hideki.items = [1,2,3,4,5,6,7]
hideki.save()
print(tbl1.all().objects[0].money)
hideki.delete()
tbl1.delete()