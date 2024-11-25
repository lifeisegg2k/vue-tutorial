# Using RDS

## Index

- [Requirement](#Requirement)
- [Pre-work](#Pre-work)
- [Boto3 specification for Python](#Boto3-specification-for-Python)
- [Using python](#Using-python)
- [Using awslocal](#Using-awslocal)
- [Creation of a SecretsManager secret with the DB password](#Creation-of-a-SecretsManager-secret-with-the-DB-password)

## Requirement

- [Dockerfile](./sample/Dockerfile)
- [docker-compose.yml](./sample/docker-compose-rds.yml)

## Pre-work

- [docker-compose.yml.base](./sample/docker-compose.yml.base) を `docker-compose.yml` にファイル名変更
- `docker-compose.yml` の内容を変更

  ```diff
  -   - SERVICES=serverless
  +   - SERVICES=rds,secretsmanager
  ```

- docker-compose 実行

  ```sh
  $ ls
  docker-compose.yml  Dockerfile  rds_crud_test.py  requirements.txt
  # run docker-compose
  $ docker-compose up -d
  Recreating localstack_localstack_1 ... done
  Recreating localstack_app_1        ... done
  # verify process for docker-compose
  $ docker-compose ps
              Name                     Command           State                                                 Ports
  -------------------------------------------------------------------------------------------------------------------------------------------------------------
  localstack_app_1          sh -c                     Up
                              dockerize -wait t ...
  localstack_localstack_1   docker-entrypoint.sh      Up      0.0.0.0:443->443/tcp, 0.0.0.0:4566->4566/tcp, 4567/tcp, 4568/tcp, 4569/tcp, 4570/tcp,
                                                              0.0.0.0:4571->4571/tcp, 4572/tcp, 4573/tcp, 4574/tcp, 4575/tcp, 4576/tcp, 4577/tcp, 4578/tcp,
                                                              4579/tcp, 4580/tcp, 4581/tcp, 4582/tcp, 4583/tcp, 4584/tcp, 4585/tcp, 4586/tcp, 4587/tcp,
                                                              4588/tcp, 4589/tcp, 4590/tcp, 4591/tcp, 4592/tcp, 4593/tcp, 4594/tcp, 4595/tcp, 4596/tcp,
                                                              4597/tcp, 0.0.0.0:53->53/tcp, 8080/tcp
  # verify docker image version
  $ docker ps
  CONTAINER ID        IMAGE                          COMMAND                   CREATED             STATUS              PORTS                                                                                                                              NAMES
  95d410b549ee        localstack_app                 "sh -c '\n  dockerize…"   21 minutes ago      Up 21 minutes                                                                                                                                          localstack_app_1
  3070b57bc581        localstack/localstack:latest   "docker-entrypoint.sh"    21 minutes ago      Up 21 minutes       0.0.0.0:53->53/tcp, 0.0.0.0:443->443/tcp, 0.0.0.0:4566->4566/tcp, 4567-4570/tcp, 4572-4597/tcp, 0.0.0.0:4571->4571/tcp, 8080/tcp   localstack_localstack_1
  [ec2-user@ip-10-0-1-254 localstack]$
  # run app container
  $ docker-compose exec app bash
  circleci@baf07633d693:~/project$ ls
  docker-compose.yml  Dockerfile  rds_crud_test.py  requirements.txt
  circleci@baf07633d693:~/project$
  ```

## Boto3 specification for Python

```py
import boto3
import localstack_client.session

# When using boto3.client
rds = boto3.client(
        service_name="rds",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )

# When using boto3.resource
rds_res = boto3.resource(
        service_name="rds",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )

# When using boto3.session.Session
session = boto3.session.Session(
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
        region_name="us-west-2"
    )
rds_ss = session.resource(
        service_name="rds",
        endpoint_url="http://localstack:4566"
    )

# When using localstack_client.session.Session
session_ls = localstack_client.session.Session()
rds_ls = session_ls.client("rds")
```

## Using python

- [Pre-work](#Pre-work)を実行後、
- [rds crud test by python | rds_crud_test.py](./sample/rds_crud_test.py)

```sh
# run sample python
$ python rds_crud_test.py
# result
Creating RDS DB instance
Run DB queries against RDS instance i1
{'DBInstanceIdentifier': 'i1', 'DBInstanceClass': 'c1', 'Engine': 'postgres', 'DBInstanceStatus': 'available', 'MasterUsername': 'test', 'DBName': 'test', 'Endpoint': {'Address': 'localstack', 'Port': 4512}, 'AllocatedStorage': 20, 'InstanceCreateTime': datetime.datetime(2020, 12, 16, 5, 30, 50, 924000, tzinfo=tzlocal()), 'PreferredBackupWindow': '03:50-04:20', 'BackupRetentionPeriod': 1, 'DBSecurityGroups': [], 'VpcSecurityGroups': [], 'DBParameterGroups': [{'DBParameterGroupName': 'default.postgres9.3', 'ParameterApplyStatus': 'in-sync'}], 'PreferredMaintenanceWindow': 'wed:06:38-wed:07:08', 'MultiAZ': False, 'EngineVersion': '9.3.3', 'AutoMinorVersionUpgrade': False, 'ReadReplicaDBInstanceIdentifiers': [], 'LicenseModel': 'license-included', 'OptionGroupMemberships': [{'OptionGroupName': 'default.postgres9.3', 'Status': 'in-sync'}], 'PubliclyAccessible': False, 'StatusInfos': [], 'StorageType': 'gp2', 'StorageEncrypted': False, 'DbiResourceId': 'db-M5ENSHXFPU6XHZ4G4ZEI5QIO2U', 'CopyTagsToSnapshot': False, 'DBInstanceArn': 'arn:aws:rds:us-west-2:000000000000:db:i1', 'IAMDatabaseAuthenticationEnabled': False}
[(1, 'Jane'), (2, 'Alex'), (3, 'Maria')]
Deleting RDS DB instance i1
$
```

## Using awslocal

- [Pre-work](#Pre-work)を実行後、

### RDS

#### Creation of an RDS database by awslocal

```sh
$ awslocal rds create-db-instance \
    --db-instance-identifier db1 \
    --db-instance-class c1 \
    --engine postgres \
    --region us-west-2
# result
{
    "DBInstance": {
        "DBInstanceIdentifier": "db1",
        "DBInstanceClass": "c1",
        "Engine": "postgres",
        "DBInstanceStatus": "available",
        "MasterUsername": "test",
        "DBName": "test",
        "Endpoint": {
            "Address": "localstack",
            "Port": 4511
        },
        "AllocatedStorage": 20,
        "InstanceCreateTime": "2020-12-16T04:37:40.255Z",
        "PreferredBackupWindow": "03:50-04:20",
        "BackupRetentionPeriod": 1,
        "DBSecurityGroups": [],
        "VpcSecurityGroups": [],
        "DBParameterGroups": [
            {
                "DBParameterGroupName": "default.postgres9.3",
                "ParameterApplyStatus": "in-sync"
            }
        ],
        "PreferredMaintenanceWindow": "wed:06:38-wed:07:08",
        "MultiAZ": false,
        "EngineVersion": "9.3.3",
        "AutoMinorVersionUpgrade": false,
        "ReadReplicaDBInstanceIdentifiers": [],
        "LicenseModel": "license-included",
        "OptionGroupMemberships": [
            {
                "OptionGroupName": "default.postgres9.3",
                "Status": "in-sync"
            }
        ],
        "PubliclyAccessible": false,
        "StatusInfos": [],
        "StorageType": "gp2",
        "StorageEncrypted": false,
        "DbiResourceId": "db-M5ENSHXFPU6XHZ4G4ZEI5QIO2U",
        "CopyTagsToSnapshot": false,
        "DBInstanceArn": "arn:aws:rds:us-west-2:000000000000:db:db1",
        "IAMDatabaseAuthenticationEnabled": false
    }
}
```

#### running a simple SELECT 123 query via the RDS Data API

```sh
# secret-arn create
awslocal secretsmanager create-secret \
    --name db_pass \
    --secret-string test
# result
{
    "ARN": "arn:aws:secretsmanager:us-east-1:000000000000:secret:db_pass-YnVVa",
    "Name": "db_pass",
    "VersionId": "6c41005a-354e-4280-8e4d-1ac1a700bc34"
}
# running a simple SELECT 123 query via the RDS Data API
$ awslocal rds-data execute-statement \
    --database test \
    --resource-arn arn:aws:rds:us-west-2:000000000000:db:db1 \
    --secret-arn arn:aws:secretsmanager:us-east-1:000000000000:secret:db_pass-YnVVa \
    --sql 'SELECT 123'
# result
{
    "columnMetadata": [
        {
            "name": "?column?",
            "type": 23
        }
    ],
    "records": [
        [
            {
                "doubleValue": 123
            }
        ]
    ]
}
```

### Aurora PostgreSQL

#### Create DB instance  for Aurora PostgreSQL

```sh
$ awslocal rds create-db-instance \
    --db-instance-identifier sample-instance \
    --db-cluster-identifier sample-cluster \
    --engine aurora-postgresql \
    --db-instance-class c1
# result
{
    "DBInstance": {
        "DBInstanceIdentifier": "sample-instance",
        "DBInstanceClass": "c1",
        "Engine": "aurora-postgresql",
        "DBInstanceStatus": "available",
        "MasterUsername": "test",
        "DBName": "test",
        "Endpoint": {
            "Address": "localstack",
            "Port": 4511
        },
        "AllocatedStorage": 0,
        "InstanceCreateTime": "2020-12-18T00:52:07.918Z",
        "PreferredBackupWindow": "03:50-04:20",
        "BackupRetentionPeriod": 1,
        "DBSecurityGroups": [],
        "VpcSecurityGroups": [],
        "DBParameterGroups": [
            {
                "DBParameterGroupName": "None",
                "ParameterApplyStatus": "in-sync"
            }
        ],
        "PreferredMaintenanceWindow": "wed:06:38-wed:07:08",
        "MultiAZ": false,
        "EngineVersion": "None",
        "AutoMinorVersionUpgrade": false,
        "ReadReplicaDBInstanceIdentifiers": [],
        "LicenseModel": "license-included",
        "OptionGroupMemberships": [
            {
                "OptionGroupName": "None",
                "Status": "in-sync"
            }
        ],
        "PubliclyAccessible": false,
        "StatusInfos": [],
        "StorageType": "gp2",
        "DBClusterIdentifier": "sample-cluster",
        "StorageEncrypted": false,
        "DbiResourceId": "db-M5ENSHXFPU6XHZ4G4ZEI5QIO2U",
        "CopyTagsToSnapshot": false,
        "DBInstanceArn": "arn:aws:rds:us-east-1:000000000000:db:sample-instance",
        "IAMDatabaseAuthenticationEnabled": false
    }
}
```

#### Create DB cluster for Aurora PostgreSQL

```sh
$ awslocal rds create-db-cluster \
    --db-cluster-identifier sample-cluster \
    --engine aurora-postgresql
{
    "DBCluster": {
        "DBClusterIdentifier": "sample-cluster",
        "Status": "available",
        "Engine": "aurora-postgresql",
        "DBClusterArn": "arn:aws:rds:us-east-1:000000000000:cluster:sample-cluster",
        "ScalingConfigurationInfo": {}
    }
}
```

#### Modify DB cluster for Aurora PostgreSQL

```sh
$ awslocal rds modify-current-db-cluster-capacity \
    --db-cluster-identifier sample-cluster \
    --capacity 64
{
    "DBClusterIdentifier": "sample-cluster",
    "PendingCapacity": 64,
    "CurrentCapacity": 64
}
```

## Creation of a SecretsManager secret with the DB password

- `--region us-west-2` のオプションを入れればのは指定したリジョンで生成できます。
- `Data API` を使用する場合は、
  - `--region us-west-2` のオプションを外すか`--region us-east-1`を使用
  - まだ、LocalStack でサポートされてない
- 以下の `create`、`list`、`delete`を試す場合は、[Pre-work](#Pre-work)事前に実行する必要あります。

### create

```sh
$ awslocal secretsmanager create-secret \
    --region us-west-2 \
    --name test_pass \
    --secret-string test_rds
# result
{
    "ARN": "arn:aws:secretsmanager:us-west-2:000000000000:secret:test_pass-huaug",
    "Name": "test_pass",
    "VersionId": "a5c5ada4-7710-4c5c-8cba-8a1a17d520c3"
}
```

### list

```sh
$ awslocal secretsmanager list-secrets \
    --region us-west-2
# result
{
    "SecretList": [
        {
            "ARN": "arn:aws:secretsmanager:us-west-2:000000000000:secret:test_pass-huaug",
            "Name": "test_pass",
            "Description": "",
            "KmsKeyId": "",
            "RotationEnabled": false,
            "RotationLambdaARN": "",
            "RotationRules": {
                "AutomaticallyAfterDays": 0
            },
            "Tags": [],
            "SecretVersionsToStages": {
                "a5c5ada4-7710-4c5c-8cba-8a1a17d520c3": [
                    "AWSCURRENT"
                ]
            }
        }
    ]
}
```

### delete

```sh
$ awslocal secretsmanager delete-secret \
    --secret-id test_pass \
    --region us-west-2
# result
{
    "ARN": "arn:aws:secretsmanager:us-west-2:000000000000:secret:test_pass-huaug",
    "Name": "test_pass",
    "DeletionDate": 1610683969.990506
}
```
