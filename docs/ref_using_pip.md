# Install python library using pip

## Index

- [What is pip](#What-is-pip)
- [What is requirements.txt](#What-is-requirements.txt)
  - [Using](#Using)
  - [How to write pip](#How-to-write-pip)
- [requirements.txt to Pipfile](#requirements.txt-to-Pipfile)
- [pip Dependency](#pip-Dependency)
- [Discharge the file for Production Environment](#Discharge-the-file-for-Production-Environment)

## What is pip

- `pip` は、Python のパッケージを管理するためのツール
- パッケージには大きく分けて2つがあります。
  - 公式が配布しているもの
  - サードパーティが配布しているもの
- サードパーティのパッケージは `PyPI` というサイトで配布されています。
  - 公式サイトURL=> https://pypi.org/
- Using
  command | Desc.
  ---- | ----
  pip -V | Version 確認
  pip list | インストール済みのパッケージを一覧
  pip freeze | インストール済みパッケージを確認
  pip install {パッケージ名}<br>（例）pip install numpy<br>　　pip install 'numpy==1.14.2' | パッケージをインストールする
  pip install -r requirements.txt | 一括インストール
  pip install --upgrade {パッケージ名}<br>（例）pip install --upgrade pip | パッケージをアップグレード
  pip uninstall {パッケージ名}<br>（例）pip uninstall numpy<br>　　pip uninstall -y numpy | パッケージをアンインストール

## What is requirements.txt

- プロジェクトに `pip install` する必要がある`パッケージリスト`を記載しているファイルです。
- **requirements.txt** を使うことで環境構築の手間を削減することができるのです。

### Using

```sh
# 現環境でインストールされているパッケージを「requirements.txt」に出力
$ pip freeze > requirements.txt
```

### How to write pip

- 最新バージョンを取得する場合の書き方は、バージョン番号などは指定せず、パッケージ名だけ記述\
  `numpy`
- バージョン指定する場合の書き方\
  `numpy == 1.14.2`
- [公式サイト](https://pip.pypa.io/en/latest/reference/pip_install/#example-requirements-file) のサンプル

  ```py
  #
  ####### example-requirements.txt #######
  #
  ###### Requirements without Version Specifiers ######
  nose
  nose-cov
  beautifulsoup4
  #
  ###### Requirements with Version Specifiers ######
  #   See https://www.python.org/dev/peps/pep-0440/#version-specifiers
  docopt == 0.6.1         # Version Matching. Must be version 0.6.1
  keyring >= 4.1.1        # Minimum version 4.1.1
  coverage != 3.5         # Version Exclusion. Anything except version 3.5
  Mopidy-Dirble ~= 1.1    # Compatible release. Same as >= 1.1, == 1.*
  #
  ###### Refer to other requirements files ######
  -r other-requirements.txt
  #
  #
  ###### A particular file ######
  ./downloads/numpy-1.9.2-cp34-none-win32.whl
  http://wxpython.org/Phoenix/snapshot-builds/wxPython_Phoenix-3.0.3.dev1820+49a8884-cp34-none-win_amd64.whl
  #
  ###### Additional Requirements without Version Specifiers ######
  #   Same as 1st section, just here to show that you can put things in any order.
  rejected
  green
  #
  ```

## requirements.txt to Pipfile

- `pip freeze > requirements.txt` からの requirements.txt の中身は汚い
- `Pipfile` は、、Python のパッケージを管理するためのツール
- `Ruby` の `Gemfile` と `Gemfile.lock` 見たいに、`Pipfile` と `Pipfile.lock` が存在
- `[packages]` と `[dev-packages]` に分けて本番と開発環境用として利用可能
- requirements.txt から Pipfile に移行手順
  - `pipenv install -r requirements.txt` を実行すると `Pipfile` と `Pipfile.lock` が生成される
  - `pipenv graph` を実行して、パッケージの依存性確認
    - `pipenv graph` : 正向き依存性
    - `pipenv graph --reverse` : 逆向き依存性
  - `Pipfile` の中にパッケージのすべてが `[dev-packages]` にあるので、用途合わせて `[packages]` と `[dev-packages]` に振り分ける
  - `pipenv install -d`
    - 開発環境用インストール
    - `[packages]` と `[dev-packages]` 両方にあるパッケージ設置
  - `pipenv install -d`
    - 本番環境用インストール
    - `[packages]` にあるパッケージ設置

## pip Dependency

- [Changes to the pip dependency resolver in 20.3 (2020)](https://pip.pypa.io/en/stable/user_guide/#resolver-changes-2020)
- [pipの依存関係チェックが厳しくなる](https://qiita.com/ksato9700/items/ec30d726a1508c7985a0)

### Dependency check

- Dependency check

  <details><summary>pipdeptree</summary>

  ```sh
  $ pipdeptree
  bash: pipdeptree: command not found
  $ pip install pipdeptree
  Collecting pipdeptree
    Downloading pipdeptree-1.0.0-py3-none-any.whl (12 kB)
  Requirement already satisfied: pip>=6.0.0 in /home/circleci/.pyenv/versions/3.8.2/lib/python3.8/site-packages (from pipdeptree) (20.3.3)
  Installing collected packages: pipdeptree
  Successfully installed pipdeptree-1.0.0
  $ pipdeptree
  - aws-sam-cli-local==1.1.0.1
    - aws-sam-cli [required: >=1.1.0, installed: 1.13.2]
      - aws-lambda-builders [required: ==1.1.0, installed: 1.1.0]
        - setuptools [required: Any, installed: 41.2.0]
        - six [required: ~=1.11, installed: 1.15.0]
        - wheel [required: Any, installed: 0.34.2]
      - aws-sam-translator [required: ==1.32.0, installed: 1.32.0]
        - boto3 [required: ~=1.5, installed: 1.14.63]
          - botocore [required: >=1.17.63,<1.18.0, installed: 1.17.63]
            - docutils [required: >=0.10,<0.16, installed: 0.15.2]
            - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
            - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
              - six [required: >=1.5, installed: 1.15.0]
            - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
            - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
              - docutils [required: >=0.10,<0.16, installed: 0.15.2]
              - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
              - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
                - six [required: >=1.5, installed: 1.15.0]
              - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
        - jsonschema [required: ~=3.2, installed: 3.2.0]
          - attrs [required: >=17.4.0, installed: 20.3.0]
          - pyrsistent [required: >=0.14.0, installed: 0.17.3]
          - setuptools [required: Any, installed: 41.2.0]
          - six [required: >=1.11.0, installed: 1.15.0]
        - six [required: ~=1.15, installed: 1.15.0]
      - boto3 [required: ~=1.14.23, installed: 1.14.63]
        - botocore [required: >=1.17.63,<1.18.0, installed: 1.17.63]
          - docutils [required: >=0.10,<0.16, installed: 0.15.2]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
            - six [required: >=1.5, installed: 1.15.0]
          - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
        - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
        - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
          - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
            - docutils [required: >=0.10,<0.16, installed: 0.15.2]
            - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
            - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
              - six [required: >=1.5, installed: 1.15.0]
            - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
      - chevron [required: ~=0.12, installed: 0.13.1]
      - click [required: ~=7.1, installed: 7.1.2]
      - cookiecutter [required: ~=1.7.2, installed: 1.7.2]
        - binaryornot [required: >=0.4.4, installed: 0.4.4]
          - chardet [required: >=3.0.2, installed: 3.0.4]
        - click [required: >=7.0, installed: 7.1.2]
        - Jinja2 [required: <3.0.0, installed: 2.11.2]
          - MarkupSafe [required: >=0.23, installed: 1.1.1]
        - jinja2-time [required: >=0.2.0, installed: 0.2.0]
          - arrow [required: Any, installed: 0.17.0]
            - python-dateutil [required: >=2.7.0, installed: 2.8.0]
              - six [required: >=1.5, installed: 1.15.0]
          - jinja2 [required: Any, installed: 2.11.2]
            - MarkupSafe [required: >=0.23, installed: 1.1.1]
        - MarkupSafe [required: <2.0.0, installed: 1.1.1]
        - poyo [required: >=0.5.0, installed: 0.5.0]
        - python-slugify [required: >=4.0.0, installed: 4.0.1]
          - text-unidecode [required: >=1.3, installed: 1.3]
        - requests [required: >=2.23.0, installed: 2.23.0]
          - certifi [required: >=2017.4.17, installed: 2020.6.20]
          - chardet [required: >=3.0.2,<4, installed: 3.0.4]
          - idna [required: >=2.5,<3, installed: 2.10]
          - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
        - six [required: >=1.10, installed: 1.15.0]
      - dateparser [required: ~=0.7, installed: 0.7.6]
        - python-dateutil [required: Any, installed: 2.8.0]
          - six [required: >=1.5, installed: 1.15.0]
        - pytz [required: Any, installed: 2020.4]
        - regex [required: !=2019.02.19, installed: 2020.11.13]
        - tzlocal [required: Any, installed: 2.1]
          - pytz [required: Any, installed: 2020.4]
      - docker [required: ~=4.2.0, installed: 4.2.2]
        - requests [required: >=2.14.2,!=2.18.0, installed: 2.23.0]
          - certifi [required: >=2017.4.17, installed: 2020.6.20]
          - chardet [required: >=3.0.2,<4, installed: 3.0.4]
          - idna [required: >=2.5,<3, installed: 2.10]
          - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
        - six [required: >=1.4.0, installed: 1.15.0]
        - websocket-client [required: >=0.32.0, installed: 0.57.0]
          - six [required: Any, installed: 1.15.0]
      - Flask [required: ~=1.1.2, installed: 1.1.2]
        - click [required: >=5.1, installed: 7.1.2]
        - itsdangerous [required: >=0.24, installed: 1.1.0]
        - Jinja2 [required: >=2.10.1, installed: 2.11.2]
          - MarkupSafe [required: >=0.23, installed: 1.1.1]
        - Werkzeug [required: >=0.15, installed: 1.0.1]
      - jmespath [required: ~=0.10.0, installed: 0.10.0]
      - python-dateutil [required: ~=2.6,<2.8.1, installed: 2.8.0]
        - six [required: >=1.5, installed: 1.15.0]
      - PyYAML [required: ~=5.3, installed: 5.3.1]
      - requests [required: ==2.23.0, installed: 2.23.0]
        - certifi [required: >=2017.4.17, installed: 2020.6.20]
        - chardet [required: >=3.0.2,<4, installed: 3.0.4]
        - idna [required: >=2.5,<3, installed: 2.10]
        - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
      - serverlessrepo [required: ==0.1.10, installed: 0.1.10]
        - boto3 [required: ~=1.9,>=1.9.56, installed: 1.14.63]
          - botocore [required: >=1.17.63,<1.18.0, installed: 1.17.63]
            - docutils [required: >=0.10,<0.16, installed: 0.15.2]
            - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
            - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
              - six [required: >=1.5, installed: 1.15.0]
            - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
            - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
              - docutils [required: >=0.10,<0.16, installed: 0.15.2]
              - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
              - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
                - six [required: >=1.5, installed: 1.15.0]
              - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
        - pyyaml [required: ~=5.1, installed: 5.3.1]
        - six [required: ~=1.11, installed: 1.15.0]
      - tomlkit [required: ==0.7.0, installed: 0.7.0]
  - awscli-local==0.9
    - awscli [required: Any, installed: 1.18.140]
      - botocore [required: ==1.17.63, installed: 1.17.63]
        - docutils [required: >=0.10,<0.16, installed: 0.15.2]
        - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
        - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
          - six [required: >=1.5, installed: 1.15.0]
        - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
      - colorama [required: >=0.2.5,<0.4.4, installed: 0.4.3]
      - docutils [required: >=0.10,<0.16, installed: 0.15.2]
      - PyYAML [required: >=3.10,<5.4, installed: 5.3.1]
      - rsa [required: >=3.1.2,<=4.5.0, installed: 4.5]
        - pyasn1 [required: >=0.1.3, installed: 0.4.8]
      - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
        - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
          - docutils [required: >=0.10,<0.16, installed: 0.15.2]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
            - six [required: >=1.5, installed: 1.15.0]
          - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
    - localstack-client [required: Any, installed: 1.9]
      - boto3 [required: Any, installed: 1.14.63]
        - botocore [required: >=1.17.63,<1.18.0, installed: 1.17.63]
          - docutils [required: >=0.10,<0.16, installed: 0.15.2]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
            - six [required: >=1.5, installed: 1.15.0]
          - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
        - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
        - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
          - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
            - docutils [required: >=0.10,<0.16, installed: 0.15.2]
            - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
            - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
              - six [required: >=1.5, installed: 1.15.0]
            - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
  - localstack==0.12.2
    - boto3 [required: >=1.14.33, installed: 1.14.63]
      - botocore [required: >=1.17.63,<1.18.0, installed: 1.17.63]
        - docutils [required: >=0.10,<0.16, installed: 0.15.2]
        - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
        - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
          - six [required: >=1.5, installed: 1.15.0]
        - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
      - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
      - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
        - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
          - docutils [required: >=0.10,<0.16, installed: 0.15.2]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
            - six [required: >=1.5, installed: 1.15.0]
          - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
    - dnspython [required: ==1.16.0, installed: 1.16.0]
    - docopt [required: >=0.6.2, installed: 0.6.2]
    - localstack-client [required: >=0.14, installed: 1.9]
      - boto3 [required: Any, installed: 1.14.63]
        - botocore [required: >=1.17.63,<1.18.0, installed: 1.17.63]
          - docutils [required: >=0.10,<0.16, installed: 0.15.2]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
            - six [required: >=1.5, installed: 1.15.0]
          - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
        - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
        - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
          - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
            - docutils [required: >=0.10,<0.16, installed: 0.15.2]
            - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
            - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
              - six [required: >=1.5, installed: 1.15.0]
            - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
    - localstack-ext [required: >=0.11.0, installed: 0.12.1.1]
      - dnslib [required: >=0.9.10, installed: 0.9.14]
      - dnspython [required: >=1.16.0, installed: 1.16.0]
      - pyaes [required: >=1.6.0, installed: 1.6.1]
      - requests [required: >=2.20.0, installed: 2.23.0]
        - certifi [required: >=2017.4.17, installed: 2020.6.20]
        - chardet [required: >=3.0.2,<4, installed: 3.0.4]
        - idna [required: >=2.5,<3, installed: 2.10]
        - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
    - requests [required: >=2.20.0, installed: 2.23.0]
      - certifi [required: >=2017.4.17, installed: 2020.6.20]
      - chardet [required: >=3.0.2,<4, installed: 3.0.4]
      - idna [required: >=2.5,<3, installed: 2.10]
      - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
    - six [required: >=1.12.0, installed: 1.15.0]
  - moto==1.3.16
    - aws-xray-sdk [required: >=0.93,!=0.96, installed: 2.6.0]
      - botocore [required: >=1.11.3, installed: 1.17.63]
        - docutils [required: >=0.10,<0.16, installed: 0.15.2]
        - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
        - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
          - six [required: >=1.5, installed: 1.15.0]
        - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
      - future [required: Any, installed: 0.18.2]
      - jsonpickle [required: Any, installed: 1.4.2]
      - wrapt [required: Any, installed: 1.12.1]
    - boto [required: >=2.36.0, installed: 2.49.0]
    - boto3 [required: >=1.9.201, installed: 1.14.63]
      - botocore [required: >=1.17.63,<1.18.0, installed: 1.17.63]
        - docutils [required: >=0.10,<0.16, installed: 0.15.2]
        - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
        - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
          - six [required: >=1.5, installed: 1.15.0]
        - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
      - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
      - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
        - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
          - docutils [required: >=0.10,<0.16, installed: 0.15.2]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
            - six [required: >=1.5, installed: 1.15.0]
          - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
    - botocore [required: >=1.12.201, installed: 1.17.63]
      - docutils [required: >=0.10,<0.16, installed: 0.15.2]
      - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
      - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
        - six [required: >=1.5, installed: 1.15.0]
      - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
    - cfn-lint [required: >=0.4.0, installed: 0.43.0]
      - aws-sam-translator [required: >=1.25.0, installed: 1.32.0]
        - boto3 [required: ~=1.5, installed: 1.14.63]
          - botocore [required: >=1.17.63,<1.18.0, installed: 1.17.63]
            - docutils [required: >=0.10,<0.16, installed: 0.15.2]
            - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
            - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
              - six [required: >=1.5, installed: 1.15.0]
            - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
          - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
          - s3transfer [required: >=0.3.0,<0.4.0, installed: 0.3.3]
            - botocore [required: >=1.12.36,<2.0a.0, installed: 1.17.63]
              - docutils [required: >=0.10,<0.16, installed: 0.15.2]
              - jmespath [required: >=0.7.1,<1.0.0, installed: 0.10.0]
              - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
                - six [required: >=1.5, installed: 1.15.0]
              - urllib3 [required: >=1.20,<1.26, installed: 1.25.11]
        - jsonschema [required: ~=3.2, installed: 3.2.0]
          - attrs [required: >=17.4.0, installed: 20.3.0]
          - pyrsistent [required: >=0.14.0, installed: 0.17.3]
          - setuptools [required: Any, installed: 41.2.0]
          - six [required: >=1.11.0, installed: 1.15.0]
        - six [required: ~=1.15, installed: 1.15.0]
      - jsonpatch [required: Any, installed: 1.28]
        - jsonpointer [required: >=1.9, installed: 2.0]
      - jsonschema [required: ~=3.0, installed: 3.2.0]
        - attrs [required: >=17.4.0, installed: 20.3.0]
        - pyrsistent [required: >=0.14.0, installed: 0.17.3]
        - setuptools [required: Any, installed: 41.2.0]
        - six [required: >=1.11.0, installed: 1.15.0]
      - junit-xml [required: ~=1.9, installed: 1.9]
        - six [required: Any, installed: 1.15.0]
      - networkx [required: ~=2.4, installed: 2.5]
        - decorator [required: >=4.3.0, installed: 4.4.2]
      - pyyaml [required: Any, installed: 5.3.1]
      - six [required: ~=1.11, installed: 1.15.0]
    - cryptography [required: >=2.3.0, installed: 3.3]
      - cffi [required: >=1.12, installed: 1.14.4]
        - pycparser [required: Any, installed: 2.20]
      - six [required: >=1.4.1, installed: 1.15.0]
    - docker [required: >=2.5.1, installed: 4.2.2]
      - requests [required: >=2.14.2,!=2.18.0, installed: 2.23.0]
        - certifi [required: >=2017.4.17, installed: 2020.6.20]
        - chardet [required: >=3.0.2,<4, installed: 3.0.4]
        - idna [required: >=2.5,<3, installed: 2.10]
        - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
      - six [required: >=1.4.0, installed: 1.15.0]
      - websocket-client [required: >=0.32.0, installed: 0.57.0]
        - six [required: Any, installed: 1.15.0]
    - ecdsa [required: <0.15, installed: 0.14.1]
      - six [required: Any, installed: 1.15.0]
    - idna [required: >=2.5,<3, installed: 2.10]
    - Jinja2 [required: >=2.10.1, installed: 2.11.2]
      - MarkupSafe [required: >=0.23, installed: 1.1.1]
    - jsondiff [required: >=1.1.2, installed: 1.2.0]
    - MarkupSafe [required: <2.0, installed: 1.1.1]
    - mock [required: Any, installed: 4.0.2]
    - more-itertools [required: Any, installed: 8.6.0]
    - python-dateutil [required: >=2.1,<3.0.0, installed: 2.8.0]
      - six [required: >=1.5, installed: 1.15.0]
    - python-jose [required: >=3.1.0,<4.0.0, installed: 3.2.0]
      - ecdsa [required: <0.15, installed: 0.14.1]
        - six [required: Any, installed: 1.15.0]
      - pyasn1 [required: Any, installed: 0.4.8]
      - rsa [required: Any, installed: 4.5]
        - pyasn1 [required: >=0.1.3, installed: 0.4.8]
      - six [required: <2.0, installed: 1.15.0]
    - pytz [required: Any, installed: 2020.4]
    - PyYAML [required: >=5.1, installed: 5.3.1]
    - requests [required: >=2.5, installed: 2.23.0]
      - certifi [required: >=2017.4.17, installed: 2020.6.20]
      - chardet [required: >=3.0.2,<4, installed: 3.0.4]
      - idna [required: >=2.5,<3, installed: 2.10]
      - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
    - responses [required: >=0.9.0, installed: 0.12.1]
      - requests [required: >=2.0, installed: 2.23.0]
        - certifi [required: >=2017.4.17, installed: 2020.6.20]
        - chardet [required: >=3.0.2,<4, installed: 3.0.4]
        - idna [required: >=2.5,<3, installed: 2.10]
        - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
      - six [required: Any, installed: 1.15.0]
      - urllib3 [required: >=1.25.10, installed: 1.25.11]
    - setuptools [required: Any, installed: 41.2.0]
    - six [required: >1.9, installed: 1.15.0]
    - sshpubkeys [required: >=3.1.0, installed: 3.1.0]
      - cryptography [required: >=2.1.4, installed: 3.3]
        - cffi [required: >=1.12, installed: 1.14.4]
          - pycparser [required: Any, installed: 2.20]
        - six [required: >=1.4.1, installed: 1.15.0]
      - ecdsa [required: >=0.13, installed: 0.14.1]
        - six [required: Any, installed: 1.15.0]
    - werkzeug [required: Any, installed: 1.0.1]
    - xmltodict [required: Any, installed: 0.12.0]
    - zipp [required: Any, installed: 3.4.0]
  - pipdeptree==1.0.0
    - pip [required: >=6.0.0, installed: 20.3.3]
  - pipenv==2020.6.2
    - certifi [required: Any, installed: 2020.6.20]
    - pip [required: >=18.0, installed: 20.3.3]
    - setuptools [required: >=36.2.1, installed: 41.2.0]
    - virtualenv [required: Any, installed: 20.0.27]
      - appdirs [required: >=1.4.3,<2, installed: 1.4.4]
      - distlib [required: >=0.3.1,<1, installed: 0.3.1]
      - filelock [required: >=3.0.0,<4, installed: 3.0.12]
      - six [required: >=1.9.0,<2, installed: 1.15.0]
    - virtualenv-clone [required: >=0.2.5, installed: 0.5.4]
  - pipreqs==0.4.10
    - docopt [required: Any, installed: 0.6.2]
    - yarg [required: Any, installed: 0.1.9]
      - requests [required: Any, installed: 2.23.0]
        - certifi [required: >=2017.4.17, installed: 2020.6.20]
        - chardet [required: >=3.0.2,<4, installed: 3.0.4]
        - idna [required: >=2.5,<3, installed: 2.10]
        - urllib3 [required: >=1.21.1,<1.26,!=1.25.1,!=1.25.0, installed: 1.25.11]
  - psycopg2==2.8.6
  - pytest==6.1.2
    - attrs [required: >=17.4.0, installed: 20.3.0]
    - iniconfig [required: Any, installed: 1.1.1]
    - packaging [required: Any, installed: 20.7]
      - pyparsing [required: >=2.0.2, installed: 2.4.7]
    - pluggy [required: >=0.12,<1.0, installed: 0.13.1]
    - py [required: >=1.8.2, installed: 1.9.0]
    - toml [required: Any, installed: 0.10.2]
  ```

  <details>

## Discharge the file for Production Environment

- pipreqs

  <details><summary>pipreqs</summary>

  ```sh
  $ pip install pipreqs
  Collecting pipreqs
    Downloading pipreqs-0.4.10-py2.py3-none-any.whl (25 kB)
  Requirement already satisfied: docopt in /home/circleci/.pyenv/versions/3.8.2/lib/python3.8/site-packages (from pipreqs) (0.6.2)
  Collecting yarg
    Downloading yarg-0.1.9-py2.py3-none-any.whl (19 kB)
  Requirement already satisfied: requests in /home/circleci/.pyenv/versions/3.8.2/lib/python3.8/site-packages (from yarg->pipreqs) (2.23.0)
  Requirement already satisfied: certifi>=2017.4.17 in /home/circleci/.pyenv/versions/3.8.2/lib/python3.8/site-packages (from requests->yarg->pipreqs) (2020.6.20)
  Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in /home/circleci/.pyenv/versions/3.8.2/lib/python3.8/site-packages (from requests->yarg->pipreqs) (1.25.11)
  Requirement already satisfied: idna<3,>=2.5 in /home/circleci/.pyenv/versions/3.8.2/lib/python3.8/site-packages (from requests->yarg->pipreqs) (2.10)
  Requirement already satisfied: chardet<4,>=3.0.2 in /home/circleci/.pyenv/versions/3.8.2/lib/python3.8/site-packages (from requests->yarg->pipreqs) (3.0.4)
  Installing collected packages: yarg, pipreqs
  Successfully installed pipreqs-0.4.10 yarg-0.1.9
  $ ls
  bin  docker-compose.yml  Dockerfile  dynamo_crud_test.py  new.json  rds_crud_test.py  requirements.txt.bak
  $ pipreqs .
  INFO: Successfully saved requirements file in ./requirements.txt
  $ cat ./requirements.txt
  psycopg2==2.8.6
  boto3==1.14.63
  $
  ```

  <details>
