# PyDBQuery
![](https://img.shields.io/github/release/HidekiHrk/PyDBQuery.svg) ![](https://img.shields.io/github/issues/HidekiHrk/PyDBQuery.svg) ![](https://img.shields.io/github/forks/HidekiHrk/PyDBQuery.svg) ![](https://img.shields.io/github/stars/HidekiHrk/PyDBQuery.svg)	https://img.shields.io/github/license/HidekiHrk/PyDBQuery.svg
<br>A simple database query for python!

**Examples:**<br>
**Sqlite3:**<br>
```python
from pydbquery import sqlite3

db = sqlite3.Database(filename='data.db')
person_table = db.create_table("Person", name=str, age=int, job=str)
person_table.add(name="Jhonny", age=28, job="Programmer")
person_table.add(name="Anna", age=23, job="Designer")
person_list = person_table.all()
print(person_list.objects)
jhonny = person_list.filter(name="Jhonny")
if len(jhonny) > 0:
  jhonny = jhonny[0]
  print(jhonny.name, jhonny.age, jhonny.job, sep=' - ')
  jhonny.age = 30
  jhonny.save()
  print(jhonny.age)
```

For more informations please visit the [docs](https://pydbquery.readthedocs.io/en/latest/)!
