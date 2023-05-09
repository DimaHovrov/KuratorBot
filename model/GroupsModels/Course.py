import db.query_db as db


class Course:
    id: int
    number: int
    type_id: int

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.number = kwargs['number']
        self.type_id = kwargs['type_id']


class CourseWithName:
    id: int
    number: int
    type_name: str
    type_id: int

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.number = kwargs['number']
        self.type_name = kwargs['type_name']
        self.type_id = kwargs['type_id']


def get_type_by_id(id):
    try:
        db.query = f"""select * from Course where Id={id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        course = Course(id=id, number=row.Number, type_id=row.TypeId)
        return course
    except Exception as exp:
        return False


def get_type_with_name_by_id(id):
    try:
        db.query = f"""select Course.Id as Id, Course.Number as CourseNumber, 
                       Type.Name as TypeName, Type.Id as TypeId
                       from Course 
                       inner join Type 
                       on Course.TypeId=Type.Id
                       where Course.Id = {id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        course = CourseWithName(
            id=id, number=row.CourseNumber, type_name=row.TypeName, type_id = row.TypeId)
        return course
    except Exception as exp:
        print(exp)
        return False


def get_all_courses():
    try:
        db.query = f"""select Course.Id as CourseId, Course.Number as CourseNumber, 
                       Type.Name as TypeName, Type.Id as TypeId
                       from Course
                       inner join Type
                       on Type.Id = Course.TypeId
                       order by TypeId, CourseNumber DESC"""
        courses = []
        result = db.pool.retry_operation_sync(db.execute_query)
        for row in result[0].rows:
            course = CourseWithName(
            id=row.CourseId, number=row.CourseNumber, type_name=row.TypeName, type_id = row.TypeId)
            courses.append(course)

        return courses
    except Exception as exp:
        print(exp)
        return False
