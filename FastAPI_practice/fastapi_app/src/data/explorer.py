from .init import conn, curs
from model.explorer import Explorer

curs.execute("""create table if not exists explorer(
                name text primary key,
                description text,
                country text)""")


def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(explorer: Explorer) -> dict | None:
    return explorer.dict() if explorer else None


def get_one(name: str) -> Explorer:
    qry = "select * from explorer where name = ?"
    params = tuple(name)
    print("Fetching get_one inside the data layer", qry, params)
    curs.execute(qry, params)
    return row_to_model(curs.fetchone())


def get_all(name: str | None) -> list[Explorer]:
    qry = "select * from explorer"
    curs.execute(qry)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer):
    qry = """INSERT INTO explorer(name, country, description)
             VALUES(?, ?, ?)"""
    # print("this is the explorer object", explorer)
    params = tuple(model_to_dict(explorer).values())
    print("Executing SQL: ", qry, params)
    _ = curs.execute(qry, params)
    conn.commit()
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    qry = """update explorer set
             name = :name,
             country = :country,
             description = :description,
             where name = :name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    _ = curs.execute(qry, params)
    return get_one(explorer.name)


def replace(name: str, explorer: Explorer):
    return explorer


def delete(explorer: Explorer) -> bool:
    qry = "delete from explorer where name = :name"
    params = {"name": explorer.name}
    res = curs.execute(qry, params)
    return bool(res)
