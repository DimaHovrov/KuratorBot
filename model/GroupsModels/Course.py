import db.query_db as db


class Course:
    id: int
    name: str
    type_id: int

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.type_id = kwargs['type_id']


class CourseWithName:
    id: int
    name: str
    type_name: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.type_name = kwargs['type_name']


def get_type_by_id(id):
    try:
        db.query = f"""select * from Course where Id={id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        course = Course(id=id, name=row.Name, type_id=row.TypeId)
        return course
    except Exception as exp:
        return False


def get_type_with_name_by_id(id):
    try:
        db.query = f"""select Course.Id as Id, Course.Name as CourseName, Type.Name as TypeName
                       from Course 
                       inner join Type 
                       on Course.TypeId=Type.Id
                       where Course.Id = {id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        course = CourseWithName(
            id=id, name=row.CourseName, type_id=row.TypeName)
        return course
    except Exception as exp:
        return False
