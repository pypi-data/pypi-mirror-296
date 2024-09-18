# @Coding: UTF-8
# @Time: 2024/9/11 21:54
# @Author: xieyang_ls
# @Filename: interpreter.py

from pymysql import Connect

from logging import info, basicConfig, INFO

from pyutils_xy.util import Assemble, HashAssemble

from pyutils_xy.exception import ConflictSignatureError, NoneSignatureError

basicConfig(level=INFO)


class Annotation:
    __connection = None

    __cursor = None

    __assemble: Assemble[str, object] = None

    @classmethod
    def connection(cls, host: str, port: int, username: str, password: str, database: str) -> callable:
        def decorator_func(func):
            def wrapper(*args, **kwargs):
                if cls.__connection is None or cls.__cursor is None:
                    cls.__connection = Connect(host=host, port=port, user=username, password=password)
                    cls.__connection.select_db(database)
                    cls.__cursor = cls.__connection.cursor()
                    info(f"Connected to database {database} is successfully")
                    func(*args, **kwargs)

            return wrapper

        return decorator_func

    @classmethod
    def singleton(cls, signature: str) -> callable:
        if type(signature) is not str:
            raise NoneSignatureError
        if cls.__assemble is None:
            cls.__assemble: Assemble[str, object] = HashAssemble()

        def get_signature(other_cls):

            def get_instance(*args, **kwargs) -> object:
                instance = cls.__assemble.get(signature)
                if instance is None:
                    instance = other_cls(*args, **kwargs)
                    cls.__assemble.put(signature, instance)
                if type(instance) is not other_cls:
                    raise ConflictSignatureError
                return instance

            return get_instance

        return get_signature

    @classmethod
    def get_instance_signature(cls, signature: str) -> object:
        return cls.__assemble.get(signature)


connection = Annotation.connection
singleton = Annotation.singleton
get_instance_signature = Annotation.get_instance_signature
