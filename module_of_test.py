import os
import logging
from logging import StreamHandler, Formatter
import sys


from airflow.models.baseoperator import BaseOperator


logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s] : %(levelname)s, MESSAGE: %(message)s'))
logger.addHandler(handler)


class LocalCsvToPostgresOperator(BaseOperator):
    def __init__(
        self,
        local_path: str,
        postgres_conn_id: str,
        table_name: str,
        columns_name: str,
        contains_substring: str = "flightlist",
        null_explicitly: bool = False,
        **kwargs
    ):
        self.local_path = local_path
        self.postgres_conn_id = postgres_conn_id
        self.null_explicitly = null_explicitly
        self.table_name = table_name
        self.columns_name = columns_name
        self.contains_substring = contains_substring
        super().__init__(**kwargs)

    def execute(self, context):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        import pandas as pd
        from io import StringIO

        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        conn = hook.get_conn()
        cursor = conn.cursor()

        file_list = []
        table = self.table_name
        columns = self.columns_name
        null_format = ", NULL 'null'" if self.null_explicitly else ""
        for root, _, files in os.walk(self.local_path):
            for file in files:
                if self.contains_substring in file:
                    logging.info(file)
                    file_list.append(os.path.join(root, file))
        for file_path in file_list:
            df = pd.read_csv(file_path)
            # Удаление строк, у которых отсутствуют колонки "distant" или "fap"
            df = df.dropna(subset=['destination', 'origin'], how='all')
            # Удаление строк, у которых значения в колонках "distant" и "fap" совпадают
            df = df[df['destination'] != df['origin']]
            csv_data = df.to_csv(index=False, header=True)
            csv_file = StringIO(csv_data)
            cursor.copy_expert(f"COPY {table} ({columns}) FROM STDIN WITH (format CSV, header TRUE{null_format});", csv_file)
            logging.info("Rows copied to table:", cursor.rowcount)        
            conn.commit()
        cursor.close()
        conn.close()
