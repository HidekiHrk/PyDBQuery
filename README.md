# PyDBQuery
A simple database query for python!<br><br>
![](https://img.shields.io/github/release/HidekiHrk/PyDBQuery.svg) ![](https://img.shields.io/github/issues/HidekiHrk/PyDBQuery.svg) ![](https://img.shields.io/github/forks/HidekiHrk/PyDBQuery.svg) ![](https://img.shields.io/github/stars/HidekiHrk/PyDBQuery.svg)	![](https://img.shields.io/github/license/HidekiHrk/PyDBQuery.svg) ![](https://img.shields.io/pypi/pyversions/PyDBQuery.svg) ![](https://img.shields.io/github/last-commit/HidekiHrk/PyDBQuery.svg) ![](https://img.shields.io/github/downloads/HidekiHrk/PyDBQuery/latest/total.svg) ![](https://img.shields.io/github/languages/code-size/HidekiHrk/PyDBQuery.svg)<br>
<br>
[![ko-fi](https://www.ko-fi.com/img/donate_sm.png)](https://ko-fi.com/F2F7P50M)

**Install:**<br>
_For the stable ver (recommended):_
```
pip install PyDBQuery
```
_For the dev ver:_
```
pip install PyDBQuery==0.2dev
```

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
**Supported DataTypes (including data inside list-like datatypes):** _int, float, str, dict, set, list, tuple_<br>
**obs:** (float, dict, set, list, tuple) types are **only** available in release v0.2dev.

**An portuguese example: click [heeeeereeeee](https://gist.github.com/HidekiHrk/c438a95d757d99b75c72b140da1e3450)!**<br>
For more informations please visit the [docs](https://pydbquery.readthedocs.io/en/latest/)!
