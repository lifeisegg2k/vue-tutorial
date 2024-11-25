# Using S3

## Index

- [Requirement](#Requirement)
- [Pre-work](#Pre-work)
- [Boto3 specification for Python](#Boto3-specification-for-Python)
- [AWS CLI Command Reference for S3](#AWS-CLI-Command-Reference-for-S3)
- [Using awslocal](#Using-awslocal)

## Requirement

- [Dockerfile](./sample/Dockerfile)
- [docker-compose.yml](./sample/docker-compose-s3.yml)

## Pre-work

- [docker-compose.yml.base](./sample/docker-compose.yml.base) を `docker-compose.yml` にファイル名変更
- `docker-compose.yml` の内容を変更

  ```diff
  -   - SERVICES=serverless
  +   - SERVICES=s3
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
  CONTAINER ID        IMAGE                          COMMAND                   CREATED             STATUS             PORTS                     NAMES
  95d410b549ee        localstack_app                 "sh -c '\n  dockerize…"   21 minutes ago      Up 21 minutes                                localstack_app_1
  3070b57bc581        localstack/localstack:latest   "docker-entrypoint.sh"    21 minutes ago      Up 21 minutes      0.0.0.0:53->53/tcp,       localstack_localstack_1
                                                                                                                      0.0.0.0:443->443/tcp,
                                                                                                                      0.0.0.0:4566->4566/tcp,
                                                                                                                      4567-4570/tcp,
                                                                                                                      4572-4597/tcp,
                                                                                                                      0.0.0.0:4571->4571/tcp,
                                                                                                                      8080/tcp
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
s3 = boto3.client(
        service_name="s3",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )

# When using boto3.resource
s3_res = boto3.resource(
        service_name="s3",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )

# When using boto3.session.Session
session = boto3.session.Session(
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
        region_name="us-west-2"
    )
s3_ss = session.resource(
        service_name="s3",
        endpoint_url="http://localstack:4566"
    )

# When using localstack_client.session.Session
session_ls = localstack_client.session.Session()
s3_ls = session_ls.client("s3")
```

## AWS CLI Command Reference for S3

aws-cli command | description
---- | ----
aws s3 ls | バケットの一覧を表示する
aws s3 ls s3://{バケット名}/{パス} | バケットの内容を表示する
aws s3 mb s3://{バケット名} | バケットを作成する
aws s3 rb s3://{バケット名} | バケットを削除する(空でない場合は削除されない)
aws s3 rb s3://{バケット名} --force | バケットを削除する(空でなくても削除される)
aws s3 sync {フォルダパス} s3://{バケット名}/{パス} | バケットの内容をローカルのフォルダと同期する(追加・更新のみで削除されない)
aws s3 sync {フォルダパス} s3://{バケット名}/{パス} --delete | バケットの内容をローカルのフォルダと同期する(削除もされる)
aws s3 cp {ファイルパス} s3://{バケット名}/{パス} | ローカルのファイルをバケットにコピーする
aws s3 mv {ファイルパス} s3://{バケット名}/{パス} | ローカルのファイルをバケットに移動する
aws s3 rm s3://{バケット名}/{ファイルパス} | バケットのファイルを削除する
aws s3 rm s3://{バケット名}/{フォルダパス} --recursive | バケットのフォルダを削除する

## Using awslocal

- [Pre-work](#Pre-work)を実行後、

### Create a bucket

```sh
$ awslocal s3 mb s3://test-bucket
# result
make_bucket: test-bucket

$ awslocal s3 ls
# result
2006-02-03 08:45:09 test-bucket
```

### Copy a file over

```sh
$ touch test.txt
$ ls -alF test.txt
# result
-rw-r--r-- 1 circleci circleci 20 Dec 16 06:25 test.txt

$ awslocal s3 cp test.txt s3://test-bucket
# result
upload: ./test.txt to s3://test-bucket/test.txt

$ awslocal s3 ls s3://test-bucket
# result
2020-12-16 06:24:14          0 test.txt
```

### Delete this file

```sh
$ awslocal s3 rm s3://test-bucket/test.txt
# result
delete: s3://test-bucket/test.txt

$ awslocal s3 ls s3://test-bucket
# result none
```
