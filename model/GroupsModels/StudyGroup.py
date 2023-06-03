import db.query_db as db


class StudyGroup:
    id: int
    group_id: int
    course_id: int
    uchp_id: int

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.group_id = kwargs['group_id']
        self.course_id = kwargs['course_id']
        self.uchp_id = kwargs['uchp_id']


class StudyGroupWithName:
    id: int
    group_name: str
    course_number: str
    uchp_name: str
    type_name: str

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.group_name = kwargs['group_name']
        self.course_number = kwargs['course_number']
        self.uchp_name = kwargs['uchp_name']
        self.type_name = kwargs['type_name']


def get_study_group_by_id(id):
    try:
        db.query = f"""select * from StudyGroup where Id={id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        study_group = StudyGroup(id=id, name=row.Name, type_id=row.TypeId)
        return study_group
    except Exception as exp:
        return False


def get_study_group_with_name_by_id(id):
    try:
        db.query = f"""select Course.Number as CourseNumber,
                       Group.Name as GroupName, Uchp.Name as UchpName, Type.Name as TypeName
                       from StudyGroup
                       inner join Course
                       on Course.Id=StudyGroup.CourseId
                       inner join Group
                       on StudyGroup.GroupId = Group.Id
                       inner join Uchp
                       on StudyGroup.UchpId = Uchp.Id
                       inner join Type
                       on Course.TypeId = Type.Id
                       where Course.Id = {id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        study_group_with_name = StudyGroupWithName(
            id=id, group_name=row.GroupName,
            course_number=row.CourseNumber, uchp_name=row.UchpName,
            type_name=row.TypeName)
        return study_group_with_name
    except Exception as exp:
        return False
    
def get_study_group_with_name_by_group_id(id):
    try:
        db.query = f"""select Course.Number as CourseNumber,
                       Group.Name as GroupName, Uchp.Name as UchpName, Type.Name as TypeName
                       from StudyGroup
                       inner join Course
                       on Course.Id=StudyGroup.CourseId
                       inner join Group
                       on StudyGroup.GroupId = Group.Id
                       inner join Uchp
                       on StudyGroup.UchpId = Uchp.Id
                       inner join Type
                       on Course.TypeId = Type.Id
                       where StudyGroup.Id = {id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        row = result[0].rows[0]
        study_group_with_name = StudyGroupWithName(
            id=id, group_name=row.GroupName,
            course_number=row.CourseNumber, uchp_name=row.UchpName,
            type_name=row.TypeName)
        return study_group_with_name
    except Exception as exp:
        return False


def get_all_study_group_with_name():
    try:
        db.query = f"""select StudyGroup.Id as id,Course.Number as CourseNumber,
                       Group.Name as GroupName, Uchp.Name as UchpName, Type.Name as TypeName
                       from StudyGroup
                       inner join Course
                       on Course.Id=StudyGroup.CourseId
                       inner join Group
                       on StudyGroup.GroupId = Group.Id
                       inner join Uchp
                       on StudyGroup.UchpId = Uchp.Id
                       inner join Type
                       on Course.TypeId = Type.Id"""
        result = db.pool.retry_operation_sync(db.execute_query)
        
        study_group_with_name = []
        for row in result[0].rows:
            study_group_with_name.append(StudyGroupWithName(
                id=row.id, group_name=row.GroupName,
                course_number=row.CourseNumber, uchp_name=row.UchpName,
                type_name=row.TypeName))
        return study_group_with_name
    except Exception as exp:
        return False


def get_study_groups_by_ids(uchp_id, course_id):
    try:
        db.query = f"""select StudyGroup.Id as StudyGroupId,
                       Course.Number as CourseNumber,
                       Group.Name as GroupName, Uchp.Id as UchpId, Type.Name as TypeName,Course.Id as CourseId
                       from StudyGroup
                       inner join Course
                       on Course.Id=StudyGroup.CourseId
                       inner join Group
                       on StudyGroup.GroupId = Group.Id
                       inner join Uchp
                       on StudyGroup.UchpId = Uchp.Id
                       inner join Type
                       on Course.TypeId = Type.Id
                       where CourseId = {course_id} and UchpId = {uchp_id}"""
        result = db.pool.retry_operation_sync(db.execute_query)
        return result[0].rows
    except Exception as exp:
        print(exp)
        return False
