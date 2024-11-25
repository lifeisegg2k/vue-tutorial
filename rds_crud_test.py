"""RDS CRUD Test"""

import os
import boto3
import psycopg2

RDS_ENDPOINT = os.environ.get('RDS_ENDPOINT') or 'http://localstack:4566'


def run_queries(instance):
    """Run Queries
    Args:
        instance: DB Instance
    Returns:
        None
    """
    print('Run DB queries against RDS instance %s' % instance['DBInstanceIdentifier'])
    print(instance)
    addr = instance['Endpoint']['Address']
    port = instance['Endpoint']['Port']
    conn = psycopg2.connect("dbname=test user=test password='test' host=%s port=%s" % (addr, port))
    with conn.cursor() as cur:
        cur.execute('CREATE TABLE person ("id" INTEGER, "name" VARCHAR not null, PRIMARY KEY ("id"))')
        cur.execute("INSERT INTO person VALUES (1, 'Jane')")
        cur.execute("INSERT INTO person VALUES (2, 'Alex')")
        cur.execute("INSERT INTO person VALUES (3, 'Maria')")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM person")
        result = cur.fetchall()
        print(result)


def create_db():
    """RDS db create
    Args:
        None
    Returns:
        instance: DB Instance
    """
    print('Creating RDS DB instance')
    client = connect_rds()
    instance = client.create_db_instance(Engine='postgres', DBInstanceClass='c1', DBInstanceIdentifier='i1')
    return instance['DBInstance']


def delete_db(instance):
    """RDS db drop
    Args:
        instance: DB Instance
    Returns:
        None
    """
    inst_id = instance['DBInstanceIdentifier']
    print('Deleting RDS DB instance %s' % inst_id)
    client = connect_rds()
    client.delete_db_instance(DBInstanceIdentifier=inst_id)


def connect_rds():
    """RDS connection
    Args:
        None
    Returns:
        connection pool
    """
    return boto3.client('rds', endpoint_url=RDS_ENDPOINT)


def main():
    """main
    Args:
        None
    Returns:
        None
    """
    instance = create_db()
    run_queries(instance)
    delete_db(instance)


if __name__ == '__main__':
    main()
