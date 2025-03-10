from .init import conn, curs, IntegrityError
from model.explorer import Explorer
from error import Missing, Duplicate

curs.execute("""create table if not exists explorer(
                name text primary key,
                description text,
                country text)""")


def row_to_model(row: tuple) -> Explorer:
    # print("________________________________")
    # print("this is the row", row)
    # print("________________________________")
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(explorer: Explorer) -> dict | None:
    return explorer.dict() if explorer else None


def get_one(name: str) -> Explorer:
    qry = "select * from explorer where name = ?"
    params = (name,)
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found.")


def get_all() -> list[Explorer]:
    qry = "select * from explorer"
    curs.execute(qry)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer):
    if not explorer:
        return None

    qry = """INSERT INTO explorer(name, description, country)
             VALUES(:name, :country, :description)"""
    params = model_to_dict(explorer)

    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists.")

    return get_one(explorer.name)


# NOTE: Should the name string be the one to be passed to the name_orig parameter since that
# is what is being read to select the row and update it with the body parameters
def modify(name: str, explorer: Explorer) -> Explorer | None:
    if not (name and explorer):
        return None

    qry = """update explorer set
             name = :name,
             country = :country,
             description = :description,
             where name = :name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = name
    curs.execute(qry, params)

    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {name} not found.")


def replace(name: str, explorer: Explorer):
    return explorer


def delete(name: str):
    if not name:
        return False

    qry = "delete from explorer where name = :name"
    params = {"name": name}
    res = curs.execute(qry, params)

    if curs.rowcount == 1:
        conn.commit()
        return bool(res)
    else:
        raise Missing(msg=f"Explorer {name} not found.")
