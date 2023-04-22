# coding=utf-8
from .. import db


class ProjectInfo(db.Model):
    __tablename__ = "project_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    tool = db.Column(db.String(50))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ScriptInfo(db.Model):
    __tablename__ = "script_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project_info.id"))
    title = db.Column(db.String(50))
    file = db.Column(db.String(500))
    duration = db.Column(db.Integer)
    state = db.Column(db.String(50))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CaseInfo(db.Model):
    __tablename__ = "case_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    script_id = db.Column(db.Integer, db.ForeignKey("script_info.id"))
    name = db.Column(db.String(200))
    full_name = db.Column(db.String(500))
    scenario = db.Column(db.String(200))
    result = db.Column(db.String(50))
    code = db.Column(db.String(5000))
    duration = db.Column(db.Integer)
    state = db.Column(db.String(50))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Error(db.Model):
    __tablename__ = "error_list"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    err = db.Column(db.String(500))
    level = db.Column(db.Integer)
    type = db.Column(db.String(50))
    solution = db.Column(db.String(500))
    case = db.Column(db.Integer, db.ForeignKey("case_info.id"))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Execution(db.Model):
    __tablename__ = "execution_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project_info.id"))
    script = db.Column(db.Integer)
    tests = db.Column(db.Integer)
    passes = db.Column(db.Integer)
    failures = db.Column(db.Integer)
    pending = db.Column(db.Integer)
    pass_percent = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
