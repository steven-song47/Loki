from ..model.case_model import *
import re, random, datetime, time, json, copy
from operator import or_, and_
from functools import reduce
from sqlalchemy import MetaData
from datetime import datetime, timedelta
from .. import db


class DBAutoExec:

    def __init__(self, user_db=None):
        self.db = db if not user_db else user_db
        self.tables = {
            "table_execution": Execution,
            "table_project": ProjectInfo,
            "table_script": ScriptInfo,
            "table_case": CaseInfo,
            "table_error": Error
        }  # 表名称和表对象的映射关系

    def add_table(self, table_name, table):
        """
        添加表对象到映射关系
        """
        self.tables[table_name] = table

    def _merge_params(self, table_name, args):
        """
        合并参数，过滤掉不在表字段中的参数
        """
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found.")
        fields = [column.name for column in table.__table__.columns]
        return {k: v for k, v in args.items() if k in fields}

    def _update_params(self, table_name, fields_args, update_args):
        """
        更新参数，合并更新参数
        """
        fields_args.update(update_args)
        return fields_args

    def add_data(self, table_name, **args):
        """
        添加数据到指定表
        """
        item_id = ""
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found.")
        now_time = datetime.now()
        fields_args = self._merge_params(table_name, args)
        fields_args = self._update_params(table_name, fields_args,
                                          {"create_time": now_time, "update_time": now_time})
        try:
            with self.db.session.begin_nested():
                data = table(**fields_args)
                self.db.session.add(data)
                self.db.session.flush()
                item_id = data.id
                self.db.session.commit()
        except Exception as e:
            print(str(e))
            self.db.session.rollback()
        return item_id

    def get_data(self, table_name, **args):
        """
        从指定表获取数据
        """
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found.")
        data = list()
        fields_args = self._merge_params(table_name, args)
        result = table.query.filter_by(**fields_args).order_by(table.create_time.desc()).all()
        data = [row.as_dict() for row in result]
        return data

    def update_data(self, table_name, data_id, **args):
        """
        更新指定表的数据
        """
        table = self.tables.get(table_name)
        if not table:
            raise ValueError(f"Table '{table_name}' not found.")
        now_time = datetime.now()
        fields_args = self._merge_params(table_name, args)
        fields_args = self._update_params(table_name, fields_args, {"update_time": now_time})
        try:
            with self.db.session.begin_nested():
                data = table.query.get(data_id)
                if data:
                    for key, value in fields_args.items():
                        setattr(data, key, value)
                    self.db.session.commit()
        except Exception as e:
            print(str(e))
            self.db.session.rollback()

    def delete_data(self, table_name, data_id):
        """
        删除指定表的数据
        """
        pass

