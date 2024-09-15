import math
from tqdm import tqdm
from time import time
import json
from sqlalchemy import create_engine, text
import datetime
from ..helpers import *
from ..colored import *

from .mssql import *
from .delta import *
from .csv import *
from .parquet import *
from ..quality.checks import check

class source:
    def __init__(self, app, source_name: str, source_type: str, auto_save: bool = False):
        self.source_name = source_name
        self.source_type = source_type
        self.app = app
        self.data = None
        self.params = None
        self.auto_save = auto_save

    def load_data(self, params):
        source_type = self.source_type.strip().lower()
        if source_type == 'mssql':
            self.data = read_mssql(self.app, params)
            self.params = params
            return self
        elif source_type == 'delta':
            self.data = read_delta(self.app, params)
            self.params = params
            return self
        elif source_type == 'csv':
            self.data = read_csv(self.app, params)
            self.params = params
            return self
        elif source_type == 'parquet':
            self.data = read_parquet(self.app, params)
            self.params = params
            return self

    def create_delta_table(self, location: str, table_full_name: str):
        script = f'create table if not exists {table_full_name} ( '
        for row in self.data.dtypes:
            script += f'{row[0]} {row[1]},'
        script = script[0: len(script)-1]
        script += f''') using delta location '{location}' '''
        self.app.sql(script)

    
    def write_to_delta_table(self, target_table: str, chunk_size: int = 0):
        self.data.createOrReplaceTempView('tmp_tbl')
        if chunk_size == 0:
            self.app.sql(f'''
                insert into {target_table}
                select * from tmp_tbl
            ''')
        else:
            iter = 0
            cnt = self.data.count()
            total = math.ceil(cnt / chunk_size)
    
            with tqdm(total = total) as pbar:
                while iter < total:
                    self.app.sql(f'''
                                insert into {target_table}
                                select * from tmp_tbl limit {chunk_size} offset {iter*chunk_size}
                            ''')
                    iter += 1
                    pbar.update(1)

    def check(self, auto_save: bool = False):
        return check(source = self, auto_save = auto_save)

    def save(self):
        pass