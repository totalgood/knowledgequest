import os

import numpy as np
from sqlalchemy import create_engine


DEFAULT_ENVIRON = dict(
    POSTGRES_KNOWLEDGEQUEST_DB_NAME='knowledgequest',
    POSTGRES_KNOWLEDGEQUEST_DB_USERNAME='kq',
    POSTGRES_KNOWLEDGEQUEST_DB_PW=str(str(3.1) + '{:5g}'.format(np.round((np.abs(100*np.pi*np.random.rand()) + 1), 4))),  
    )

CREATEDB_SQL_TEMPLATE = """
    CREATE DATABASE {POSTGRES_KNOWLEDGEQUEST_DB_NAME};
    CREATE USER {POSTGRES_KNOWLEDGEQUEST_DB_USERNAME} WITH PASSWORD '{POSTGRES_KNOWLEDGEQUEST_DB_PW}';
    ALTER ROLE {POSTGRES_KNOWLEDGEQUEST_DB_USERNAME} SET client_encoding TO 'utf8';
    ALTER ROLE {POSTGRES_KNOWLEDGEQUEST_DB_USERNAME} SET default_transaction_isolation TO 'read committed';
    ALTER ROLE {POSTGRES_KNOWLEDGEQUEST_DB_USERNAME} SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE knowledgequest TO {POSTGRES_KNOWLEDGEQUEST_DB_USERNAME};
    """

def execute_sql(engine='postgres://postgres@/postgres', sql=CREATEDB_SQL_TEMPLATE, **kwargs):
    """ Based on stackoverflow.com/a/8977109/623735 -- create a postgres database using sqlalchemy """
    env = DEFAULT_ENVIRON.copy()
    env.update(dict(os.environ))
    env.update(kwargs)
    sql.format(**env).splitlines()
    engine = create_engine(engine or 'sqlite:///enron_emails.db', echo=False) if not engine or isinstance(engine, str) else engine
    connection = engine.connect()
    connection.execute("commit")  # can't create a database from withing a transaction, so close the current transaction with a commit
    for statement in sql:
        print('SQL: {}'.format(statement))
        result = connection.execute(statement)
        connection.execute("commit")  # commit each transaction individually
        print('RESULT TABLE')
        print('------------')
        for row in result:
            print(row)
        print('------------')
    connection.close()
