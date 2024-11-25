# Using DynamoDB

## Index

- [Requirement](#Requirement)
- [Pre-work](#Pre-work)
- [Boto3 specification for Python](#Boto3-specification-for-Python)
- [Using awslocal](#Using-awslocal)
  - Table List
  - Describe-table
  - Put item
  - Scan Table
  - Get item
  - Query

## Requirement

- [Dockerfile](./sample/Dockerfile)
- [docker-compose.yml](./sample/docker-compose-dynamodb.yml)

## Pre-work

- [docker-compose.yml.base](./sample/docker-compose.yml.base) を `docker-compose.yml` にファイル名変更
- `docker-compose.yml` の内容を変更

  ```diff
  -   - SERVICES=serverless
  +   - SERVICES=dynamodb,rds,secretsmanager
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
dynamodb = boto3.client(
        service_name="dynamodb",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )

# When using boto3.resource
dynamodb_res = boto3.resource(
        service_name="dynamodb",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )

# When using boto3.session.Session
session = boto3.session.Session(
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
        region_name="us-west-2"
    )
dynamodb_ss = session.resource(
        service_name="dynamodb",
        endpoint_url="http://localstack:4566"
    )

# When using localstack_client.session.Session
session_ls = localstack_client.session.Session()
dynamodb_ls = session_ls.client("dynamodb")
```

## Using awslocal

- [Pre-work](#Pre-work)を実行後、

### Create a table

```sh
$ awslocal dynamodb create-table \
    --table-name test_table  \
    --attribute-definitions AttributeName=first,AttributeType=S AttributeName=second,AttributeType=N \
    --key-schema AttributeName=first,KeyType=HASH AttributeName=second,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
# result
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "first",
                "AttributeType": "S"
            },
            {
                "AttributeName": "second",
                "AttributeType": "N"
            }
        ],
        "TableName": "test_table",
        "KeySchema": [
            {
                "AttributeName": "first",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "second",
                "KeyType": "RANGE"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": 1608099033.819,
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": 0.0,
            "LastDecreaseDateTime": 0.0,
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:us-east-1:000000000000:table/us-east-1_test_table"
    }
}
```

### Table List

```sh
$ awslocal dynamodb list-tables
# result
{
    "TableNames": [
        "test_table"
    ]
}
```

### Describe-table

```sh
$ awslocal dynamodb describe-table \
    --table-name test_table
# result
{
    "Table": {
        "AttributeDefinitions": [
            {
                "AttributeName": "first",
                "AttributeType": "S"
            },
            {
                "AttributeName": "second",
                "AttributeType": "N"
            }
        ],
        "TableName": "test_table",
        "KeySchema": [
            {
                "AttributeName": "first",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "second",
                "KeyType": "RANGE"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": 1608099033.819,
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": 0.0,
            "LastDecreaseDateTime": 0.0,
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:us-east-1:000000000000:table/us-east-1_test_table"
    }
}
```

### Put item

```sh
# 1st put-item
$ awslocal dynamodb put-item \
    --table-name test_table  \
    --item '{"first":{"S":"Jack"},"second":{"N":"42"}}'
# result
{
    "ConsumedCapacity": {
        "TableName": "test_table",
        "CapacityUnits": 1.0
    }
}
# 2nd put-item
$ awslocal dynamodb put-item \
    --table-name test_table  \
    --item '{"first":{"S":"Manish"},"second":{"N":"40"}}'
# result{
    "ConsumedCapacity": {
        "TableName": "test_table",
        "CapacityUnits": 1.0
    }
}
```

### Scan Table

```sh
$ awslocal dynamodb scan \
    --table-name test_table
# result
{
    "Items": [
        {
            "first": {
                "S": "Jack"
            },
            "second": {
                "N": "42"
            }
        },
        {
            "first": {
                "S": "Manish"
            },
            "second": {
                "N": "40"
            }
        }
    ],
    "Count": 2,
    "ScannedCount": 2,
    "ConsumedCapacity": null
}
```

### Get item

```sh
$ awslocal dynamodb get-item \
    --table-name test_table  \
    --key '{"first":{"S":"Manish"},"second":{"N":"40"}}'
# result
{
    "Item": {
        "first": {
            "S": "Manish"
        },
        "second": {
            "N": "40"
        }
    }
}
```

### Query

```sh
$ awslocal dynamodb query \
    --table-name test_table \
    --projection-expression "#first, #second" \
    --key-condition-expression "#first = :value" \
    --expression-attribute-values '{":value" : {"S":"Manish"}}' \
    --expression-attribute-names '{"#first":"first", "#second":"second"}'
# result
{
    "Items": [
        {
            "first": {
                "S": "Manish"
            },
            "second": {
                "N": "40"
            }
        }
    ],
    "Count": 1,
    "ScannedCount": 1,
    "ConsumedCapacity": null
}
```

### Drop Table

```sh
$ awslocal dynamodb delete-table \
    --table-name test_table
# result
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "first",
                "AttributeType": "S"
            },
            {
                "AttributeName": "second",
                "AttributeType": "N"
            }
        ],
        "TableName": "test_table",
        "KeySchema": [
            {
                "AttributeName": "first",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "second",
                "KeyType": "RANGE"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": 1614835581.385,
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": 0.0,
            "LastDecreaseDateTime": 0.0,
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:us-west-2:000000000000:table/test_table"
    }
}
```
