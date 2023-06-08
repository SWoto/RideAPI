from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


def assert_compare(in1, in2):
    if in1 != in2:
        raise Exception(
            "Test table results don't match with expected values. in1: {}, in2:{}".format(in1, in2))

# Verify is container was raised as it should with basic test rows.
# This helps to verify the conenction string and that the container is running


def verify_init_sql():
    with db.engine.connect() as conn:
        expected = [(1, 'test row 1', True), (2, 'test row 2', False)]
        result = conn.execute(text("SELECT * FROM public.test"))
        for cnt, item in enumerate(result):
            assert_compare(expected[cnt], item)


# class SingletonMeta(type):
#     _instances = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             instance = super().__call__(*args, **kwargs)
#             cls._instances[cls] = instance
#         return cls._instances[cls]


# class SingletonSQLAlchemy(SQLAlchemy, metaclass=SingletonMeta):
#     def __init__(self, *argv, **kargv) -> None:
#         super(SingletonSQLAlchemy, self).__init__(*argv, **kargv)
        


db = SQLAlchemy()
