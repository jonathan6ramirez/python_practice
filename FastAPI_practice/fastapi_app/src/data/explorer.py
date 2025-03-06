from .init import conn, curs
from model.explorer import Explorer

curs.execute("""create table if not exists explorer(
                name text primary key,
                description text,
                country text)""")


def row_to_model(row: tuple) -> Explorer:
    print("________________________________")
    print("this is the row", row)
    print("________________________________")
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(explorer: Explorer) -> dict | None:
    return explorer.dict() if explorer else None


def get_one(name: str) -> Explorer:
    qry = "select * from explorer where name = ?"
    params = (name,)
    curs.execute(qry, params)
    print("________________________________")
    print("executing sql inside get_one", qry, params)
    print("________________________________")
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
    # print("Executing SQL inside create: ", qry, params)
    _ = curs.execute(qry, params)
    conn.commit()
    return get_one(explorer.name)
    # return {"name": explorer.name, "success": True}


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
