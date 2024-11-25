# boto3 client rds

- Syntax
- `boto3.client('rds')`

## ModifiedDBCluster

Amazon Aurora DB クラスターの設定を変更します

リクエストでこれらのパラメーターと新しい値を指定することにより、1つ以上のデータベース構成パラメーターを変更できます

ここでは、**AWS-SCALE-SAM** APP での仕様について一部のパラメータを選別して使用する方法を記述する

### Request Syntax

```py
response = client.modify_db_cluster(
    DBClusterIdentifier='string',
    NewDBClusterIdentifier='string',
    ApplyImmediately=True|False,
    BackupRetentionPeriod=123,
    DBClusterParameterGroupName='string',
    VpcSecurityGroupIds=[
        'string',
    ],
    Port=123,
    MasterUserPassword='string',
    OptionGroupName='string',
    PreferredBackupWindow='string',
    PreferredMaintenanceWindow='string',
    EnableIAMDatabaseAuthentication=True|False,
    BacktrackWindow=123,
    CloudwatchLogsExportConfiguration={
        'EnableLogTypes': [
            'string',
        ],
        'DisableLogTypes': [
            'string',
        ]
    },
    EngineVersion='string',
    AllowMajorVersionUpgrade=True|False,
    DBInstanceParameterGroupName='string',
    Domain='string',
    DomainIAMRoleName='string',
    ScalingConfiguration={
        'MinCapacity': 123,
        'MaxCapacity': 123,
        'AutoPause': True|False,
        'SecondsUntilAutoPause': 123,
        'TimeoutAction': 'string'
    },
    DeletionProtection=True|False,
    EnableHttpEndpoint=True|False,
    CopyTagsToSnapshot=True|False,
    EnableGlobalWriteForwarding=True|False
)
```

### 使用パラメータ

- `DBClusterIdentifier='string'`
  - 必須
  - 変更されるクラスターの DB クラスター ID
  - 大文字と小文字は区別なし
- `ApplyImmediately=True|False`
  - PreferredMaintenanceWindowDB クラスターの設定に関係なく、この要求の変更と保留中の変更ができるだけ早く非同期的に適用されるかどうかを示す値
  - このパラメーターが無効になっている場合、DB クラスターへの変更は次のメンテナンスウィンドウで適用
- `ScalingConfiguration={ .. }`
  - 必須
  - DB クラスターのスケーリングプロパティ
  serverlessDB エンジンモードでは、DB クラスターのスケーリングプロパティのみを変更できます
  - Syntax

    ``` python
    ScalingConfiguration={
        'MinCapacity': 123,
        'MaxCapacity': 123,
        'AutoPause': True|False,
        'SecondsUntilAutoPause': 123,
        'TimeoutAction': 'string'
    }
    ```

  - `'MinCapacity': 123`
    - serverlessDB エンジンモードでの Aurora DB クラスターの最小容量
    - Aurora MySQL の場合、有効な容量値は 1, 2, 4, 8, 16, 32, 64, 128, 256
    - **Aurora PostgreSQL** の場合、有効な容量値は **2**, **4**, **8**, **16**, **32**, **64**, **192**, **384**
    - 最大容量は最小容量以上である必要があります
  - `'MaxCapacity': 123`
    - serverlessDB エンジンモードでの Aurora DB クラスターの最大容量
  - `'AutoPause': True|False`
    - serverlessDB エンジンモードで Aurora DB クラスターの自動一時停止を許可するかどうかを示す値
    - DB クラスターは、アイドル状態（接続がない）の場合にのみ一時停止できます
    > ※ 注意 : DB クラスターが 7日を超えて一時停止している場合、DB クラスターはスナップショットでバックアップされる可能性があります。この場合、DB クラスターへの接続要求があると、DB クラスターが復元されます
  - `'SecondsUntilAutoPause': 123`
    - serverless モードの Aurora DB クラスターが一時停止するまでの時間（秒単位）
  - `'TimeoutAction': 'string'`
    - `ForceApplyCapacityChange` または `RollbackCapacityChange` のいずれかで、タイムアウトに達したときに実行するアクション
    - `ForceApplyCapacityChange` は、容量を指定された値にできるだけ早く設定します
    - デフォルトの `RollbackCapacityChange` は、タイムアウト期間にスケーリングポイントが見つからない場合、容量の変更を無視します。
    > ※ 注意 : `ForceApplyCapacityChange` を指定すると、Aurora Serverless がスケーリングポイントを見つけられないようにする接続がドロップされる可能性があります

### 使用しないパラメータ

- `NewDBClusterIdentifier='string'`
  - DB クラスターの名前を変更するときの DB クラスターの新しい DB クラスター ID
- `BackupRetentionPeriod=123`
  - 自動バックアップが保持される日
- `DBClusterParameterGroupName='string'`
  - DB クラスターのすべてのインスタンスに適用する DB パラメーターグループの名前
- `VpcSecurityGroupIds=[ .. ]`
  - DB クラスターが属する VPC セキュリティグループのリスト
- `Port=123`
  - DB クラスターが接続を受け入れるポート番号
- `MasterUserPassword='string'`
  - マスターデータベースユーザーの新しいパスワード
- `OptionGroupName='string'`
  - DB クラスターを指定されたオプショングループに関連付ける必要があることを示す値
- `PreferredBackupWindow='string'`
  - BackupRetentionPeriod パラメータを使用して自動バックアップが有効になっている場合に自動バックアップが作成される毎日の時間範囲
- `PreferredMaintenanceWindow='string'`
  - UTC での、システムメンテナンスが発生する可能性のある週単位の時間範囲
- `EnableIAMDatabaseAuthentication=True|False`
  - AWS IAM アカウントのデータベースアカウントへのマッピングを有効にするかどうかを示す値
- `BacktrackWindow=123`
  - ターゲットのバックトラックウィンドウ（秒単位）
  - バックトラッキングを無効にするには、この値を0に設定
- `CloudwatchLogsExportConfiguration={ .. }`
  - 特定の DB クラスターの CloudWatchLogs へのエクスポートを有効にするログタイプの設定設定
- `EngineVersion='string'`
  - アップグレード先のデータベースエンジンのバージョン番号
  - このパラメーターを変更すると、停止します
  - ApplyImmediately 有効になっていない限り、変更は次のメンテナンスウィンドウで適用される
- `AllowMajorVersionUpgrade=True|False`
  - メジャーバージョンのアップグレードが許可されているかどうかを示す値
- `DBInstanceParameterGroupName='string'`
  - DB クラスターに使用する DB クラスターパラメーターグループの名前
- `Domain='string'`
  - DB クラスターの移動先の ActiveDirectory ディレクトリ ID
- `DomainIAMRoleName='string'`
  - ディレクトリサービスへの API 呼び出しを行うときに使用される IAM ロールの名前を指定します
- `DeletionProtection=True|False,`
  - DB クラスターで削除保護が有効になっているかどうかを示す値
- `EnableHttpEndpoint=True|False,`
  - Aurora サーバーレス DB クラスターの HTTP エンドポイントを有効にするかどうかを示す値
- `CopyTagsToSnapshot=True|False`
  - DB クラスターから DB クラスターのスナップショットにすべてのタグをコピーするかどうかを示す値
- `EnableGlobalWriteForwarding=True|False`
  - このクラスターから Aurora グローバルデータベースのプライマリクラスターに書き込み操作を転送できるようにするかどうかを示す値

## Reference

- [boto3 dynamodb](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)
- [boto3 RDS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html)
- [boto3 Redshift](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html)
- [Redshift](https://dev.classmethod.jp/articles/implemente-redshift-cluster-pause-from-lambda/)
