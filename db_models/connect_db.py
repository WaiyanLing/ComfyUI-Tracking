import os

from sqlalchemy import create_engine
from ..config import config

connects = {}
connect_close_func_list = []

def get_engine(engine_key: str = "workflow_tracking"):
    multiprocess_engine_key = engine_key + "_" + str(os.getpid())
    if not connects.get(multiprocess_engine_key):
        if engine_key == "workflow_tracking":
            folder = config.DB_FOLDER
            database = config.DATABASE
            # data_base_url = f'sqlite:///{folder}\\{database}'
            data_base_url = f"sqlite:///{config.DB_FOLDER}\\{config.DATABASE}"
            engine = create_engine(
                data_base_url
            )
            connects[multiprocess_engine_key] = engine
            connect_close_func_list.append((1, engine.dispose))
        else:
            ...

    return connects[multiprocess_engine_key]


