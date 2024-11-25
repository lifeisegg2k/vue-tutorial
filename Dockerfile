FROM cimg/python:3.8.2

ENV PATH $PATH:/root/.local/bin:/usr/bin
# docker image にて既に存在するディレクトリー
ENV BASE_DIR=/home/circleci/project
# docker image にて既に存在するユーザー
USER circleci
WORKDIR $BASE_DIR

COPY . $BASE_DIR

RUN bin/make_aws_credentials.sh
# pip 20.3.1 固定
# 理由は、
# 一貫性を保つ為
#   PIP のバージョンが日々アップデートされるので、
#   関連ライブラリの整合性をアップデートに合わせるのが大変
RUN pip install pip==20.3.1
# 関連 Pip ライブラリー設置
RUN pip install -r requirements.txt
