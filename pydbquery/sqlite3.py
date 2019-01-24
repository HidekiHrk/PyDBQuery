import sqlite3
from collections import namedtuple

# default configs #
db_filename = "data.db"

# classes #
class Database:
    def __init__(self, filename=db_filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()
        self.tables = []

    class Table:
        def __init__(self, table_name, db, **kwargs):
            name = table_name
            kwargs['id'] = int
            supported_types = { 
                str: "TEXT", int: "INT",
                float: "REAL",
                list: "TEXT", set: "TEXT",
                tuple: "TEXT", dict: "TEXT"
                }
            self.__supported_types = supported_types
            column_class = namedtuple("Column", "name type")
            if type(name) != str:
                raise ValueError(f"database name must be str, not {type(name).__name__}")
            self.name = name
            self.conn = db.conn
            self.c = db.cursor
            self.db = db
            if not all(kwargs.get(x) in list(supported_types) for x in kwargs):
                raise ValueError(f"column type must be one of these: {', '.join(map(lambda x: x.__name__, list(supported_types)))}")
            cols_str = ', '.join(map(lambda x: f"{x} {supported_types.get(kwargs.get(x))}", kwargs))
            self.cols = list(map(lambda x: column_class(x, kwargs.get(x)), kwargs))
            self.c.execute(f"CREATE TABLE IF NOT EXISTS {self.name} ({cols_str})")

        class QueryObject:
            def __init__(self, table, **kwargs):
                self._table = table
                for x in kwargs:
                    type_transform = lambda x: x if type(x) != str else f'"{x}"'
                    exec(f"self.{x} = {type_transform(kwargs.get(x))}")

            def save(self):
                eval_types = [list, set, tuple, dict]
                cols_dict = dict(map(lambda x: [x.name, x.type], self._table.cols))
                sdict = self.__dict__
                self_id = sdict['id']
                sdict = dict(map(lambda x: [x, sdict.get(x)],
                    filter(lambda z: z.lower() not in ['id', '_table'], sdict)))
                for x in sdict:
                    itm = sdict.get(x)
                    coltype = cols_dict.get(x)
                    if type(itm) == int and coltype == float:
                        sdict[x] = float(itm)
                    elif type(itm) == float and coltype == int:
                        sdict[x] = int(itm)
                    elif type(itm) != coltype:
                        raise TypeError(f"Item: {x}'s type must be {coltype.__name__}")
                    elif type(itm) in eval_types:
                        sdict[x] = str(itm)
                querystr = ', '.join(map(lambda x: f"{x} = ?", sdict))
                self._table.c.execute(f"UPDATE {self._table.name} SET {querystr} WHERE id = ?", (*sdict.values(), self_id))
                self._table.conn.commit()
                return self
            
            def delete(self):
                self._table.c.execute(f"DELETE FROM {self._table.name} WHERE id = ?", (self.__dict__['id'],))
                self._table.conn.commit()

        def Query(self, **kwargs):
            qry_obj = self.QueryObject(self, **kwargs)
            return qry_obj
            #return namedtuple("QueryObj", f"save delete {' '.join(kwargs)}")(qry_obj.save, qry_obj.delete, **kwargs)

        def all(self):
            cols_str = list(map(lambda x: x.name, self.cols))
            self.c.execute(f"SELECT {', '.join(cols_str)} FROM {self.name}")
            all_items = self.c.fetchall()
            query_dicts = []
            cols_dict = dict(map(lambda x: [x.name, x.type], self.cols))
            eval_types = [list, set, tuple, dict]
            for x in all_items:
                dct = {}
                for z in range(len(x)):
                    item = x[z]
                    if cols_dict.get(cols_str[z]) in eval_types:
                        item = eval(x[z])
                    dct[cols_str[z]] = item
                query_dicts.append(dct)
            query_list = list(map(lambda x: self.Query(**x), query_dicts))
            def fil(**kwargs):
                cols = list(cols_str)
                if not all(x in cols for x in kwargs):
                    raise ValueError(f"incorrect columns")
                final_list = query_list
                for x in kwargs:
                    final_list = list(filter(lambda y: eval(f"y.{x}") == kwargs.get(x), final_list))
                return final_list
            return namedtuple("Query", "filter objects")(fil, query_list)

        def first(self):
            qry = self.all().objects
            return qry[0] if len(qry) > 0 else None

        def last(self):
            qry = self.all().objects
            return qry[-1] if len(qry) > 0 else None
        
        def add(self, **kwargs):
            all_objs = list(map(lambda x: x.id, self.all().objects))
            max_id = 0
            if len(all_objs) > 0:
                max_id = max(all_objs)
            kwargs['id'] = max_id + 1
            cols_str = list(map(lambda x: x.name, self.cols))
            if not all(x in cols_str for x in kwargs):
                raise ValueError(f"incorrect columns")
            cols_dict = dict(map(lambda x: [x.name, x.type], self.cols))
            eval_types = [list, set, tuple, dict]
            kvalues = []
            for x in kwargs:
                itm = kwargs.get(x)
                coltype = cols_dict.get(x)
                str(kwargs.get(x)) if cols_dict.get(x) in eval_types else kwargs.get(x)
                if coltype in eval_types:
                    if type(itm) == coltype:
                        kvalues.append(str(itm))
                    else:
                        raise TypeError(f"Item: {x}'s type must be {coltype.__name__}")
                elif type(itm) in [int, str, float]:
                    kvalues.append(str(itm) if coltype == str else itm)
                else:
                    raise TypeError(f"Item type must be one of these {', '.join(map(lambda x: x.__name__, list(self.__supported_types)))}")
            self.c.execute(f"INSERT INTO {self.name} ({', '.join(kwargs)}) values({','.join(['?'] * len(kwargs))})",
                (*kvalues,)
            )
            self.conn.commit()
            return self.Query(**kwargs)

        def __eq__(self, other):
            if type(other) == type(self):
                return self.name == other.name
            return False
        
        def delete(self):
            self.c.execute(f"DROP TABLE IF EXISTS {self.name}")
            self.conn.commit()
            self.db.tables = list(filter(lambda x: x != self, self.db.tables))

    def create_table(self, table_name, **kwargs):
        tbl = self.Table(table_name, self, **kwargs)
        self.tables.append(tbl)
        return tbl

if __name__ == "__main__":
    pass
