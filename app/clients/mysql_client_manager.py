from app.conf.app_config import DBConfig, app_config


class MySQLClientManager:
    def __init__(self,config:DBConfig):
        self.engine=None
        self.config=config

    def init(self):
        pass
    def close(self):
        pass

meta_mysql_client_manager=MySQLClientManager(app_config.db_meta)
dw_mysql_client_manager=MySQLClientManager(app_config.db_dw)
