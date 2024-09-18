import configparser
import os
import psycopg2
import psycopg2.sql


class PyLogsClient:

    def __init__(self, config_file_path: str, overwrite_schema: bool = False):
        self.db_config = self._get_db_config(config_file_path=config_file_path)
        self.overwrite_schema = overwrite_schema

    def connect(self) -> None:
        try:
            self.db_conn = psycopg2.connect(**self.db_config["db_params"])
        except Exception as e:
            print(e)
            raise ConnectionError(
                f"Database connnection failed! Check credentails")

        if self._table_exists() and not all(self._check_table_schema()) and not self.overwrite_schema:
            raise NameError(f"""Table with name {self.db_config["table_name"]} already exists and schema of the table
                            does not matches the required schema. Either correct the schema manually or set
                            `overwrite_schema` property to True in which case the data will be lost""")
        elif self._table_exists() and not all(self._check_table_schema()) and self.overwrite_schema:
            self._drop_table()
            self._create_logs_table()
        elif not self._table_exists():
            self._create_logs_table()

    def close(self) -> None:
        if self.db_conn:
            self.db_conn.close()

    def _check_table_schema(self):
        # Define the queries to check the table schema
        primary_key_query = psycopg2.sql.SQL("""
            SELECT column_name
            FROM information_schema.key_column_usage
            WHERE table_schema = %s AND table_name = %s AND constraint_name LIKE %s
        """)

        column_type_query = psycopg2.sql.SQL("""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
        """)

        with self.db_conn.cursor() as cursor:
            # Check for primary key column 'id'
            cursor.execute(primary_key_query, ('public',
                           self.db_config["table_name"], self.db_config["table_name"] + "_pkey"))
            primary_keys = cursor.fetchall()
            primary_keys = [pk[0] for pk in primary_keys]
            has_id_primary_key = 'id' in primary_keys

            # Check column types
            cursor.execute(column_type_query,
                           ('public', self.db_config["table_name"]))
            columns = cursor.fetchall()
            column_types = {col[0]: (col[1], col[2]) for col in columns}

            has_content_column = column_types.get(
                'content', (None,))[0] == 'text'
            has_type_column = column_types.get('type', (None,))[
                0] == 'character varying'
            type_length_correct = column_types.get(
                'type', (None, None))[1] == 255

            return has_id_primary_key, has_content_column, has_type_column, type_length_correct

    def _table_exists(self) -> bool:
        with self.db_conn.cursor() as cursor:
            query = psycopg2.sql.SQL(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = %s AND table_name = %s)")
            cursor.execute(query, ('public', self.db_config["table_name"]))
            exists = cursor.fetchone()[0]
            return exists

    def _drop_table(self):
        with self.db_conn.cursor() as cursor:
            query = psycopg2.sql.SQL("DROP table {}").format(
                psycopg2.sql.Identifier(self.db_config["table_name"]))
            cursor.execute(query)
            self.db_conn.commit()

    def _create_logs_table(self):
        with self.db_conn.cursor() as cursor:
            query = psycopg2.sql.SQL(
                "CREATE table if not exists {} (id SERIAL,content TEXT NOT NULL,type VARCHAR(255), PRIMARY KEY (id))").format(psycopg2.sql.Identifier(self.db_config["table_name"]))
            cursor.execute(query)
            self.db_conn.commit()

    def create_log(self, content: str, type: str):
        with self.db_conn.cursor() as cursor:
            query = psycopg2.sql.SQL(
                "INSERT into {} (content, type) values (%s, %s)").format(psycopg2.sql.Identifier(self.db_config["table_name"]))
            cursor.execute(
                query, (content, type))
            self.db_conn.commit()

    def _get_db_config(self, config_file_path: str) -> dict[str, str]:
        db_config = {
            "db_params": {
                'dbname': None,
                'user': None,
                'password': None,
                'host': None,
                'port': None
            },
            "table_name": None
        }

        self.config = configparser.ConfigParser()

        if os.path.exists(config_file_path):
            self.config.read(config_file_path)
        else:
            raise FileNotFoundError(f"No such file: {config_file_path}")

        section_name = "Database"

        if self._section_exists_in_config_file(section_name):
            db_config["db_params"]["dbname"] = self._get_property_from_config_file(
                section_name, "dbName")
            db_config["db_params"]["host"] = self._get_property_from_config_file(
                section_name, "host")
            db_config["db_params"]["port"] = int(self._get_property_from_config_file(
                section_name, "port"))
            db_config["db_params"]["password"] = self._get_property_from_config_file(
                section_name, "password")
            db_config["db_params"]["user"] = self._get_property_from_config_file(
                section_name, "user")
            db_config["table_name"] = self._get_property_from_config_file(
                section_name, "tableName", "pylogs")
        else:
            raise KeyError("Database section not present in config file")

        return db_config

    def _section_exists_in_config_file(self, section_name: str) -> bool:
        return self.config.has_section(section_name)

    def _get_property_from_config_file(self, section_name: str, property_name: str, fallback: str | None = None) -> str:
        if self.config.has_option(section_name, property_name):
            return self.config.get(section_name, property_name)
        elif not self.config.has_option(section_name, property_name) and fallback is not None:
            return fallback
        else:
            raise KeyError(f"No such key in Database section: {property_name}")
