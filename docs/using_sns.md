# Using SNS & SQS

## Index

- [Requirement](#Requirement)
- [Pre-work](#Pre-work)
- [Boto3 specification for Python](#Boto3-specification-for-Python)
- [Using python](#Using-python)
- [Using awslocal](#Using-awslocal)
  - [SNS](#SNS)
  - [SQS](#SQS)

## Requirement

- [Dockerfile](./sample/Dockerfile)
- [docker-compose.yml](./sample/docker-compose-sns.yml)

## Pre-work

- [docker-compose.yml.base](./sample/docker-compose.yml.base) を `docker-compose.yml` にファイル名変更
- `docker-compose.yml` の内容を変更

  ```diff
  -   - SERVICES=serverless
  +   - SERVICES=sns,sqs
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
sns = boto3.client(
        service_name="sns",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )
sqs = boto3.client(
        service_name="sqs",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )

# When using boto3.resource
sns_res = boto3.resource(
        service_name="sns",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )
sqs_res = boto3.resource(
        service_name="sqs",
        region_name="us-west-2",
        endpoint_url="http://localstack:4566"
    )

# When using boto3.session.Session
session = boto3.session.Session(
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
        region_name="us-west-2"
    )
sns_ss = session.resource(
        service_name="sns",
        endpoint_url="http://localstack:4566"
    )
sqs_ss = session.resource(
        service_name="sqs",
        endpoint_url="http://localstack:4566"
    )

# When using localstack_client.session.Session
session_ls = localstack_client.session.Session()
sns_ls = session_ls.client("sns")
sqs_ls = session_ls.client("sqs")
```

## Using awslocal

- 以下の `SNS`、`SQS`を試す場合は、[Pre-work](#Pre-work)事前に実行する必要あります。

### SNS

#### Create a topic

```sh
$ awslocal sns list-topics \
    --region us-west-2
# result
{
    "Topics": []
}

$ awslocal sns create-topic \
    --name test-topic \
    --region us-west-2
# result
{
    "TopicArn": "arn:aws:sns:us-west-2:000000000000:test-topic"
}

$ awslocal sns list-topics \
    --region us-west-2
# result
{
    "Topics": [
        {
            "TopicArn": "arn:aws:sns:us-west-2:000000000000:test-topic"
        }
    ]
}
```

#### Subscribe to the topic

```sh
$ awslocal sns subscribe \
    --region us-west-2 \
    --topic-arn arn:aws:sns:us-west-2:000000000000:test-topic \
    --protocol email \
    --notification-endpoint test@sample.com
# result
{
    "SubscriptionArn": "arn:aws:sns:us-west-2:000000000000:test-topic:40afe4b5-e1bb-4bd8-a165-ca26fc5d3245"
}

$ awslocal sns list-subscriptions \
    --region us-west-2
# result
{
    "Subscriptions": [
        {
            "SubscriptionArn": "arn:aws:sns:us-west-2:000000000000:test-topic:40afe4b5-e1bb-4bd8-a165-ca26fc5d3245",
            "Owner": "",
            "Protocol": "email",
            "Endpoint": "test@sample.com",
            "TopicArn": "arn:aws:sns:us-west-2:000000000000:test-topic"
        }
    ]
}
```

#### Publish to this topic

```sh
$ awslocal sns publish \
    --region us-west-2 \
    --topic-arn arn:aws:sns:us-west-2:000000000000:test-topic \
    --message 'Test Message!'
# result
{
    "MessageId": "6b50c94d-3221-4aba-9c23-9d9a693969cf"
}
```

### SQS

#### Create a Queue

```sh
$ awslocal sqs create-queue \
    --queue-name test_queue
# result
{
    "QueueUrl": "http://localstack:4566/000000000000/test_queue"
}

$ awslocal sqs list-queues
# result
{
    "QueueUrls": [
        "http://localstack:4566/000000000000/test_queue"
    ]
}
```

#### Send a message to this queue

```sh
$ awslocal sqs send-message \
    --queue-url http://localstack:4566/000000000000/test_queue \
    --message-body 'Test Message!'
# result
{
    "MD5OfMessageBody": "df69267381a60e476252c989db9ac8ad",
    "MessageId": "43cba3c8-a6e5-0919-3caa-25c0b39cc95f"
}
```

#### Receive the message from this queue

```sh
$ awslocal sqs receive-message \
    --queue-url http://localstack:4566/000000000000/test_queue
# result
{
    "Messages": [
        {
            "MessageId": "43cba3c8-a6e5-0919-3caa-25c0b39cc95f",
            "ReceiptHandle": "pqevoafwawxdmuwchoncktpkwuqnjedglcwvfmjtzdxlorswrcezthhdtxolppeykwxyrohzhyixluguyesntgacwpsibcuionrssokatdbhsmzecwdhcgwwrsnoxsynqqjukscdnswjhyjqflvqrbeonenyyvemkcrbndwjfjlmunyshiiuoeksx",
            "MD5OfBody": "df69267381a60e476252c989db9ac8ad",
            "Body": "Test Message!",
            "Attributes": {
                "SenderId": "AIDAIT2UOQQY3AUEKVGXU",
                "SentTimestamp": "1608101274124",
                "ApproximateReceiveCount": "1",
                "ApproximateFirstReceiveTimestamp": "1608101318952"
            }
        }
    ]
}
```

#### Delete this message

```sh
$ awslocal sqs delete-message \
    --queue-url http://localstack:4566/000000000000/test_queue \
    --receipt-handle 'pqevoafwawxdmuwchoncktpkwuqnjedglcwvfmjtzdxlorswrcezthhdtxolppeykwxyrohzhyixluguyesntgacwpsibcuionrssokatdbhsmzecwdhcgwwrsnoxsynqqjukscdnswjhyjqflvqrbeonenyyvemkcrbndwjfjlmunyshiiuoeksx'
# result none
```
