# SAM Template に S3 Bucket を Resource 宣言する際の注意点

## SAM の Resource として宣言した Bucket は、別の SAM から Resource として宣言できない問題

- 明確な説明文などを見つけることができませんでした。

## 推論

- 宣言された SAM（CloudFormationのスタック）の所有権を持つ
  - 既存 Bucket は利用できません。
    > 初期生成権限に従うっと見える（正確な根拠はないが経験を元でみると）
  - SAM Deploy する時、SAM（CloudFormationのスタック）から Bucket を生成する
  - 2回目の Deploy からは、生成しない
- 別の SAM から同じ Bucket を宣言すると
  - Bucket を生成しようとする
  - 所有権がないのっとエラーを吐き出す
- ただし、Lambda などの他のサビースでアクセスなど作業は可能
