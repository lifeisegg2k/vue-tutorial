# Using SAM

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

```sh
$ dc exec app bash
~/project$ ls
bin                 events    Pipfile.lock      requirements.txt          samconfig.migrate.toml  src
doc                 layer     __pycache__       requirements.txt.bak      samconfig.prod.toml     template.yaml
docker-compose.yml  new.json  rds_crud_test.py  run_pytest.sh             samconfig.toml          tests
Dockerfile          Pipfile   README.md         samconfig.integrate.toml  samconfig.vnv.toml
~/project$ samlocal build
Building codeuri: src/functions/aws_scale_trigger/ runtime: python3.8 metadata: {} functions: ['AwsScaleTriggerFunction']
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource
Building codeuri: src/functions/aws_scale_selecter/ runtime: python3.8 metadata: {} functions: ['AwsScaleSelecterFunction']
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource
Building codeuri: src/functions/aws_scale_as/ runtime: python3.8 metadata: {} functions: ['AwsScaleASFunction']
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource
Building layer 'AwsScaleLayer'
Running PythonPipBuilder:ResolveDependencies
Running PythonPipBuilder:CopySource

Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Invoke Function: sam local invoke
[*] Deploy: sam deploy --guided

~/project$ awslocal s3 mb s3://test
make_bucket: test
~/project$ samlocal package --s3-bucket test --output-template-file packaged.yml
Uploading to 60d939f49ed2401eccf11e472f7b40b7  2283 / 2283.0  (100.00%)
Uploading to 35b02211d10b9c1d55cfd1ac5b4845e0  2479 / 2479.0  (100.00%)
Uploading to 8725a7740d91e6698e4b46bdad3d0e5a  2203 / 2203.0  (100.00%)
Uploading to c7cb66f1d1aeff542976478aa578be2b  8202642 / 8202642.0  (100.00%)

Successfully packaged artifacts and wrote output template to file packaged.yml.
Execute the following command to deploy the packaged template
sam deploy --template-file /home/circleci/project/packaged.yml --stack-name <YOUR STACK NAME>

~/project$ less packaged.yml
~/project$ samlocal deploy --stack-name s3 --s3-bucket test --template-file packaged.yml --capabilities CAPABILITY_IAM --parameter-overrides 'Repository=test OauthToken=test'

        Deploying with following values
        ===============================
        Stack name                   : s3
        Region                       : us-west-2
        Confirm changeset            : False
        Deployment s3 bucket         : test
        Capabilities                 : ["CAPABILITY_IAM"]
        Parameter overrides          : {'Repository': 'test', 'OauthToken': 'test'}
        Signing Profiles           : {}

Initiating deployment
=====================
Uploading to aws-scale-integrate/218854763d43c03e85f5cc071e55e404.template  5888 / 5888.0  (100.00%)

Waiting for changeset to be created..

CloudFormation stack changeset
-------------------------------------------------------------------------------------------------
Operation                LogicalResourceId        ResourceType             Replacement
-------------------------------------------------------------------------------------------------
+ Add                    AwsScaleASFunctionRole   AWS::IAM::Role           N/A
+ Add                    AwsScaleASFunctionScal   AWS::Lambda::Permissio   N/A
                         eDownSchedulePermissio   n
                         n
+ Add                    AwsScaleTriggerFunctio   AWS::Lambda::Permissio   N/A
                         nASPermissionProd        n
+ Add                    AwsScaleTriggerFunctio   AWS::IAM::Role           N/A
                         nRole
+ Add                    AwsScaleASFunctionScal   AWS::Events::Rule        N/A
                         eUpSchedule
+ Add                    AwsScaleTriggerFunctio   AWS::Lambda::Function    N/A
                         n
+ Add                    AwsScaleSelecterFuncti   AWS::IAM::Role           N/A
                         onRole
+ Add                    AwsScaleSelecterFuncti   AWS::Lambda::Permissio   N/A
                         onAwsScaleSelecterEven   n
                         tPermission
+ Add                    AwsScaleASFunctionScal   AWS::Events::Rule        N/A
                         eDownSchedule
+ Add                    AwsScaleASFunction       AWS::Lambda::Function    N/A
+ Add                    ScaleApiDeployment25ea   AWS::ApiGateway::Deplo   N/A
                         27e7c8                   yment
+ Add                    ScaleApiProdStage        AWS::ApiGateway::Stage   N/A
+ Add                    AwsScaleLayerf0c9e25dc   AWS::Lambda::LayerVers   N/A
                         7                        ion
+ Add                    AwsScaleTriggerBucket    AWS::S3::Bucket          N/A
+ Add                    AwsScaleASFunctionScal   AWS::Lambda::Permissio   N/A
                         eUpSchedulePermission    n
+ Add                    ScaleApi                 AWS::ApiGateway::RestA   N/A
                                                  pi
+ Add                    AwsScaleSelecterFuncti   AWS::Lambda::Function    N/A
                         on
-------------------------------------------------------------------------------------------------

Changeset created successfully. arn:aws:cloudformation:us-west-2:000000000000:changeSet/samcli-deploy1608266797/6a7a4cdc-b56c-4cdc-a8a3-70b50a61c0a1


2020-12-18 04:46:37 - Waiting for stack create/update to complete

CloudFormation events from changeset
-------------------------------------------------------------------------------------------------
ResourceStatus           ResourceType             LogicalResourceId        ResourceStatusReason
-------------------------------------------------------------------------------------------------
CREATE_COMPLETE          AWS::CloudFormation::S   s3                       -
                         tack
-------------------------------------------------------------------------------------------------

CloudFormation outputs from deployed stack
-------------------------------------------------------------------------------------------------
Outputs
-------------------------------------------------------------------------------------------------
Key                 AwsScaleApi
Description         -
Value               https://.execute-api.us-west-2.amazonaws.com/Prod/
-------------------------------------------------------------------------------------------------

Successfully created/updated stack - s3 in us-west-2

~/project$ samlocal deploy --guided

Configuring SAM deploy
======================

        Looking for config file [samconfig.toml] :  Found
        Reading default arguments  :  Success

        Setting default arguments for 'sam deploy'
        =========================================
        Stack Name [aws-scale-integrate]:
        AWS Region [us-west-2]:
        Parameter S3BucketName [aws-scale-integrate]:
        Parameter DbClusterID [integrate-serverless]:
        Parameter EnvRegion [us-west-2]:
        Parameter ENV [dev]:
        Parameter VpcId [vpc-003ff6f53ca2b22b4]:
        Parameter VpcEndpointId [vpce-00b051a9cd4dc5189]:
        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
        Confirm changes before deploy [y/N]: y
        #SAM needs permission to be able to create roles to connect to the resources in your template
        Allow SAM CLI IAM role creation [Y/n]:
        Save arguments to configuration file [Y/n]:
        SAM configuration file [samconfig.toml]:
        SAM configuration environment [default]:

        Looking for resources needed for deployment: Not found.
        Creating the required resources...
Error: Failed to create managed resources: Waiter StackCreateComplete failed: Waiter encountered a terminal failure state
~/project$ awslocal s3 mb s3://aws-scale-integrate
make_bucket: aws-scale-integrate
~/project$ samlocal deploy --guided

Configuring SAM deploy
======================

        Looking for config file [samconfig.toml] :  Found
        Reading default arguments  :  Success

        Setting default arguments for 'sam deploy'
        =========================================
        Stack Name [aws-scale-integrate]:
        AWS Region [us-west-2]:
        Parameter S3BucketName [aws-scale-integrate]:
        Parameter DbClusterID [integrate-serverless]:
        Parameter EnvRegion [us-west-2]:
        Parameter ENV [dev]:
        Parameter VpcId [vpc-003ff6f53ca2b22b4]:
        Parameter VpcEndpointId [vpce-00b051a9cd4dc5189]:
        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
        Confirm changes before deploy [y/N]: y
        #SAM needs permission to be able to create roles to connect to the resources in your template
        Allow SAM CLI IAM role creation [Y/n]:
        Save arguments to configuration file [Y/n]:
        SAM configuration file [samconfig.toml]: test.toml
        SAM configuration environment [default]:

        Looking for resources needed for deployment: Found!

                Managed S3 bucket: aws-sam-cli-managed-default-samclisourcebucket-749b9457
                A different default S3 bucket can be set in samconfig.toml

        Saved arguments to config file
        Running 'sam deploy' for future deployments will use the parameters saved above.
        The above parameters can be changed by modifying samconfig.toml
        Learn more about samconfig.toml syntax at
        https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html
Uploading to aws-scale-integrate/60d939f49ed2401eccf11e472f7b40b7  2283 / 2283.0  (100.00%)
Uploading to aws-scale-integrate/35b02211d10b9c1d55cfd1ac5b4845e0  2479 / 2479.0  (100.00%)
Uploading to aws-scale-integrate/8725a7740d91e6698e4b46bdad3d0e5a  2203 / 2203.0  (100.00%)
Uploading to aws-scale-integrate/c7cb66f1d1aeff542976478aa578be2b  8202642 / 8202642.0  (100.00%)

        Deploying with following values
        ===============================
        Stack name                   : aws-scale-integrate
        Region                       : us-west-2
        Confirm changeset            : True
        Deployment s3 bucket         : aws-sam-cli-managed-default-samclisourcebucket-749b9457
        Capabilities                 : ["CAPABILITY_IAM"]
        Parameter overrides          : {'S3BucketName': 'aws-scale-integrate', 'DbClusterID': 'integrate-serverless', 'EnvRegion': 'us-west-2', 'ENV': 'dev', 'VpcId': 'vpc-003ff6f53ca2b22b4', 'VpcEndpointId': 'vpce-00b051a9cd4dc5189'}
        Signing Profiles           : {}

Initiating deployment
=====================
Uploading to aws-scale-integrate/67e7b90dfb8cf2d4f7e61bc506145e22.template  6164 / 6164.0  (100.00%)

Waiting for changeset to be created..

CloudFormation stack changeset
-------------------------------------------------------------------------------------------------
Operation                LogicalResourceId        ResourceType             Replacement
-------------------------------------------------------------------------------------------------
+ Add                    AwsScaleASFunctionRole   AWS::IAM::Role           N/A
+ Add                    AwsScaleASFunctionScal   AWS::Lambda::Permissio   N/A
                         eDownSchedulePermissio   n
                         n
+ Add                    AwsScaleTriggerFunctio   AWS::Lambda::Permissio   N/A
                         nASPermissionProd        n
+ Add                    AwsScaleTriggerFunctio   AWS::IAM::Role           N/A
                         nRole
+ Add                    AwsScaleASFunctionScal   AWS::Events::Rule        N/A
                         eUpSchedule
+ Add                    AwsScaleTriggerFunctio   AWS::Lambda::Function    N/A
                         n
+ Add                    AwsScaleSelecterFuncti   AWS::IAM::Role           N/A
                         onRole
+ Add                    AwsScaleSelecterFuncti   AWS::Lambda::Permissio   N/A
                         onAwsScaleSelecterEven   n
                         tPermission
+ Add                    AwsScaleASFunctionScal   AWS::Events::Rule        N/A
                         eDownSchedule
+ Add                    AwsScaleASFunction       AWS::Lambda::Function    N/A
+ Add                    ScaleApiDeployment25ea   AWS::ApiGateway::Deplo   N/A
                         27e7c8                   yment
+ Add                    ScaleApiProdStage        AWS::ApiGateway::Stage   N/A
+ Add                    AwsScaleLayerf908e948b   AWS::Lambda::LayerVers   N/A
                         3                        ion
+ Add                    AwsScaleTriggerBucket    AWS::S3::Bucket          N/A
+ Add                    AwsScaleASFunctionScal   AWS::Lambda::Permissio   N/A
                         eUpSchedulePermission    n
+ Add                    ScaleApi                 AWS::ApiGateway::RestA   N/A
                                                  pi
+ Add                    AwsScaleSelecterFuncti   AWS::Lambda::Function    N/A
                         on
-------------------------------------------------------------------------------------------------

Changeset created successfully. arn:aws:cloudformation:us-west-2:000000000000:changeSet/samcli-deploy1608267071/fa585fc5-4698-4a85-96b0-77e936bdcf77


Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y

2020-12-18 04:51:14 - Waiting for stack create/update to complete

CloudFormation events from changeset
-------------------------------------------------------------------------------------------------
ResourceStatus           ResourceType             LogicalResourceId        ResourceStatusReason
-------------------------------------------------------------------------------------------------
CREATE_COMPLETE          AWS::CloudFormation::S   aws-scale-integrate        -
                         tack
-------------------------------------------------------------------------------------------------

CloudFormation outputs from deployed stack
-------------------------------------------------------------------------------------------------
Outputs
-------------------------------------------------------------------------------------------------
Key                 AwsScaleApi
Description         -
Value               https://.execute-api.us-west-2.amazonaws.com/Prod/
-------------------------------------------------------------------------------------------------

Successfully created/updated stack - aws-scale-integrate in us-west-2
```
