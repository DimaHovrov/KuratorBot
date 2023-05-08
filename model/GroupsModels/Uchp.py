import db.query_db as db


class Uchp:
    id: int
    name: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']


def get_type_by_id(id):
    try:
        db.query = f"""select * from Uchp where Id={id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        uchp = Uchp(id=id, name=row.Name)
        return uchp
    except Exception as exp:
        return False

def get_all_uchp():
    try:
        db.query = f"""select * from Uchp"""
        result = db.pool.retry_operation_sync(db.execute_query)
        uchps=[]

        for row in result[0].rows:
            uchp = Uchp(id = row.Id, name = row.Name)
            uchps.append(uchp)
        return uchps
    except Exception as exp:
        print(exp)
        return False
