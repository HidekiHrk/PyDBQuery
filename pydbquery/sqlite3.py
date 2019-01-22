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
            column_class = namedtuple("Column", "name type")
            if type(name) != str:
                raise ValueError(f"database name must be str, not {type(name).__name__}")
            self.name = name
            self.conn = db.conn
            self.c = db.cursor
            self.db = db
            if not all(kwargs.get(x) in [str, int] for x in kwargs):
                raise ValueError(f"column names must be str and be one of these: TEXT, INT")
            str_int = { str: "TEXT", int: "INT" }
            cols_str = ', '.join(map(lambda x: f"{x} {str_int.get(kwargs.get(x))}", kwargs))
            self.cols = list(map(lambda x: column_class(x, kwargs.get(x)), kwargs))
            self.c.execute(f"CREATE TABLE IF NOT EXISTS {self.name} ({cols_str})")

        class QueryObject:
            def __init__(self, table, **kwargs):
                self._table = table
                for x in kwargs:
                    type_transform = lambda x: x if type(x) != str else f'"{x}"'
                    exec(f"self.{x} = {type_transform(kwargs.get(x))}")

            def save(self):
                sdict = self.__dict__
                self_id = sdict['id']
                sdict = dict(map(lambda x: [x, sdict.get(x)],
                    filter(lambda z: z.lower() not in ['id', '_table'], sdict)))
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
            for x in all_items:
                dct = {}
                for z in range(len(x)):
                    dct[cols_str[z]] = x[z]
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
            self.c.execute(f"INSERT INTO {self.name} ({', '.join(kwargs)}) values({','.join(['?'] * len(kwargs))})",
                (*kwargs.values(),)
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
