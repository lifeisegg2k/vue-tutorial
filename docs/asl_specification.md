# Amazon States Language

## ASL ?

ASL(Amazon States Language) は JSON ベースの構造化言語で、`State Machine`および作業を実行できる状態のコレクション (`Task` 状態) の定義、次に移行する状態の決定 (`Choice` 状態)、エラーによる実行の停止 (`Fail` 状態) などに使用されます。

- [Statelint](https://github.com/awslabs/statelint)

## 仕様

- [仕様 | English](https://states-language.net/spec.html)
- **注意**:\
  以下のは、あくまで[Google翻訳](https://translate.google.co.jp/?hl=ja&tab=TT)を利用して、訳したので、意味合いが違う場合があります。

## State Machine の構造

`State Machine`は JSON オブジェクトで表されます。

### Example: Hello World

`State Machine`の操作は、JSONオブジェクト、つまり最上位の `States` オブジェクトのフィールドで表される状態によって指定されます。この例では、 `HelloWorld` という名前の状態が1つあります。

```json
{
    "Comment": "A simple minimal example of the States language",
    "StartAt": "Hello World",
    "States": {
        "Hello World": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
            "End": true
        }
    }
}
```

この`State Machine`が起動すると、インタープリターは開始状態を識別することによって実行を開始します。その状態を実行してから、その状態が`End`状態としてマークされているかどうかを確認します。そうである場合、マシンは終了し、結果を返します。状態が`End`状態でない場合、インタプリタは `Next` フィールドを探して、次に実行する状態を決定します。Terminal State（`Succeed`、`Fail`、または`End`状態）に達するか、ランタイムエラーが発生するまで、このプロセスを繰り返します。

この例では、マシンに `HelloWorld` という名前の単一の状態が含まれています。 `HelloWorld` はTask Stateであるため、インタープリターはそれを実行しようとします。 `Resource` フィールドの値を調べると、Lambda関数を指していることがわかります。そのため、インタープリターはその関数を呼び出そうとします。Lambda関数が正常に実行されると、マシンは正常に終了します。

`State Machine`は JSON オブジェクトで表されます。

### Top-level fields

`State Machine`には、`States` という名前のオブジェクトフィールドが必要です。このフィールドのフィールドは状態を表します。

`State Machine`には、`StartAt` という名前の文字列フィールドが必要です。その値は、`States` フィールドの名前の1つと完全に一致する必要があります。インタプリタは、指定された状態でマシンの実行を開始します。

`State Machine`には、人間が読める形式のマシンの説明のために提供される `Comment` という名前の文字列フィールドがある場合があります。

`State Machine`には、マシンで使用されるステート言語のバージョンを示す `バージョン` という名前の文字列フィールドがある場合があります。このドキュメントではバージョン1.0について説明します。省略した場合、 `バージョン` のデフォルト値は文字列 `1.0` です。

`State Machine`には、 `TimeoutSeconds` という名前の整数フィールドがある場合があります。提供されている場合は、マシンの実行が許可されている最大秒数を提供します。マシンが指定された時間より長く実行される場合、インタプリタは`States.Timeout` エラー名でマシンに失敗します。

## コンセプト

### States

状態は、最上位の `States` オブジェクトのフィールドとして表されます。長さが 128 Unicode 文字以下でなければならない状態名がフィールド名です。ステート名は、`State Machine`全体のスコープ内で一意である必要があります。状態は、タスク（作業単位）を説明するか、フロー制御（例：Choice）を指定します。

Lambda関数を実行する状態の例を次に示します。

```json
"HelloWorld": {
    "Type": "Task",
    "Resource": "arn:aws:lambda:us-east-1:123456789012:function:HelloWorld",
    "Next": "NextState",
    "Comment": "Executes the HelloWorld Lambda function"
}
```

Note:

1. すべての States には `Type` フィールドが必要です。このドキュメントでは、このフィールドの値を状態の Type と呼び、上記の例のような状態を ‘ と呼びます。
1. どの States にも、人間が読める形式のコメントや説明を保持するための `Comment` フィールドがあります。
1. ほとんどの状態Typeには、このドキュメントで指定されている追加のフィールドが必要です。
1. Choice、Succeed、Failを除くすべての状態には、値がブール値でなければならない `End` という名前のフィールドがある場合があります。 `Terminal State` という用語は、`{ "End"：true }` の状態、`{ "Type"： "Succeed" }`の状態、または `{ "Type"： "Fail" }` の状態を意味します。

### Transitions

遷移は状態をリンクし、`State Machine`の制御フローを定義します。非終端状態を実行した後、インタープリターは次の状態への遷移に従います。ほとんどの状態 Type では、遷移は無条件であり、状態の `Next` フィールドで指定されます。

選択状態を除いて、すべての非端末状態には `Next` フィールドが必要です。 `Next` フィールドの値は、別の状態の名前と正確かつ大文字と小文字を区別して一致する必要があります。

状態は、他の状態からの複数の着信遷移を持つことができます。

### Timestamps

選択状態と待機状態は、タイムスタンプを表す JSON フィールド値を処理します。これらは、ISO 8601 のRFC3339 プロファイルに準拠する必要がある文字列です。 さらに、日付と時刻を区切るために大文字の `T` 文字を使用する必要があり、数字がない場合は大文字の `Z` 文字を使用する必要があります。タイムゾーンオフセット、たとえば `2016-03-14T01：59：00Z` 。

### Data

インタープリターは、状態間でデータを渡して、計算を実行したり、`State Machine`のフローを動的に制御したりします。このようなデータはすべて JSON で表現する必要があります。

`State Machine`が起動すると、呼び出し元は入力として初期 JSON テキストを提供できます。これは、入力としてマシンの開始状態に渡されます。 入力が提供されていない場合、デフォルトは空の JSON オブジェクト`{}`です。入力としての JSON テキストであり、任意の出力を生成できます。これは JSON テキストである必要があります。 2つの状態が遷移によってリンクされると、最初の状態からの出力が入力として2番目の状態に渡されます。 マシンの端末状態からの出力は、その出力として扱われます。

たとえば、2つの数値を加算する単純な`State Machine`について考えてみます。

```json
{
    "StartAt": "Add",
    "States": {
        "Add": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-1:123456789012:function:Add",
            "End": true
        }
    }
}
```

`Add` Lambda 関数が次のように定義されているとします。

```js
exports.handler = function(event, context) {
  context.succeed(event.val1 + event.val2);
};
```

次に、この`State Machine`が入力`{ "val1": 3, "val2": 4 }`で起動された 場合、出力は数値`7`で構成されるJSONテキストになります。

JSON エンコードされたデータに適用される通常の制約が適用されます。特に、次の点に注意してください。

1. JSON の数値は通常、JavaScriptのセマンティクスに準拠しており、通常は倍精度の IEEE-854 値に対応します。これと他の相互運用性の懸念については、RFC8259 を参照してください 。
1. スタンドアロンの "-区切り文字列、ブール値、および数値は、有効な JSON テキストです。

### The Context Object

インタプリタは、実行およびその他の実装の詳細に関する情報を実行中の`State Machine`に提供できます。これは、 `Context Object` と呼ばれる JSON オブジェクトの形式で提供されます。このバージョンのStates Language 仕様では、Context Object の内容は指定されていません。

### Paths

パスは `$` で始まる文字列であり、JSON テキストでコンポーネントを識別するために使用されます。構文は JsonPath の構文です。

パスが2つのドル記号である `$$` で始まる場合、これは、Context Object 内のコンテンツを識別することを目的としていることを示します。最初のドル記号は削除され、ドル記号で始まる残りのテキストは、Context Object に適用される JSONPath として解釈されます。

### Reference Paths

参照パスは、JSON 構造内の単一のノード（演算子 `@` 、 `,` 、 `：` 、および `?` ）のみを識別できるように構文が制限されたパスです。サポートされていません-すべての参照パスは、単一の値、配列、またはオブジェクト（subtree）への明確な参照である必要があります。

たとえば、状態入力データに値が含まれている場合：

```json
{
    "foo": 123,
    "bar": ["a", "b", "c"],
    "car": {
        "cdr": true
    }
}
```

次に、次の参照パスが返されます。

```sh
$.foo => 123
$.bar => ["a", "b", "c"]
$.car.cdr => true
```

パスと参照パスは、このドキュメントの後半で指定するように、`State Machine`のフローを制御したり、ステートの設定やオプションを構成したりするために、特定のステートで使用されます。

受け入れ可能な参照パス構文の例を次に示します。

```sh
$.store.book
$.store\.book
$.\stor\e.boo\k
$.store.book.title
$.foo.\.bar
$.foo\@bar.baz\[\[.\?pretty
$.&Ж中.\uD800\uDF46
$.ledgers.branch[0].pending.count
$.ledgers.branch[0]
$.ledgers[0][22][315].foo
$['store']['book']
$['store'][0]['book']
```

### Payload Template

`State Machine`インタープリターは、有用な作業を行うためにタスクへの入力としてデータをディスパッチし、タスクから出力を受け取ります。タスクのフォーマットの期待に応えるために入力データを再形成し、同様に戻ってくる出力を再形成することがしばしば望まれます。この目的のために、Payload Template と呼ばれる JSON オブジェクト構造が提供されています。

`Task`、`Map`、`Parallel`、および`Pass`の各状態では、Payload Template は `Parameters` という名前のフィールドの値です。`Task`、`Map`、および`Parallel`状態には、 `ResultSelector` という名前のフィールドの値である別の Payload Template があります。

Payload Template は JSON オブジェクトである必要があります。必須フィールドはありません。インタプリタは、このセクションで説明されているように Payload Template を処理します。その処理の結果はペイロードと呼ばれます。

例を示すために、Task Stateには `Parameters` という名前のフィールドがあり、その値はペイロードテンプレートです。 次のTask Stateを検討してください:

```json
"X": {
    "Type": "Task",
    "Resource": "arn:aws:states:us-east-1:123456789012:task:X",
    "Next": "Y",
    "Parameters": {
        "first": 88,
        "second": 99
    }
}
```

この場合、ペイロードは、値がそれぞれ 88 と 99 である `first` フィールドと `second` フィールドを持つオブジェクトです。処理を実行する必要はなく、ペイロードはペイロードテンプレートと同じです。

ペイロードテンプレートの入力とコンテキストオブジェクトからの値は、フィールドの命名規則、パス、および組み込み関数を組み合わせてペイロードに挿入できます。

ペイロードテンプレート内のフィールド（ただし、深くネストされている）の名前が `.$` で終わる場合、その値は以下のルールに従って変換され、フィールドの名前が `.$` サフィックスを削除するように変更されます。

フィールド値が1つの `$` のみで始まる場合、値はパスでなければなりません。この場合、パスはペイロードテンプレートの入力に適用され、新しいフィールド値になります。

フィールド値が `$$` で始まる場合、最初のドル記号は削除され、残りはパスでなければなりません。この場合、パスはコンテキストオブジェクトに適用され、新しいフィールド値になります。

フィールド値が `$` で始まらない場合、それは組み込み関数でなければなりません（以下を参照）。インタプリタが組み込み関数を呼び出し、結果が新しいフィールド値になります。

パスが有効であるが正常に適用できない場合、インタープリターは `States.ParameterPathFailure` のエラー名でマシンの実行に失敗します。評価中に組み込み関数が失敗した場合、インタープリターは `States.IntrinsicFailure` というエラー名でマシンの実行に失敗します。

文字 `.$` で終わるフィールドの名前が `.$` サフィックスを削除するように変更された後、JSONオブジェクトのフィールド名が重複してはなりません。

```json
"X": {
    "Type": "Task",
    "Resource": "arn:aws:states:us-east-1:123456789012:task:X",
    "Next": "Y",
    "Parameters": {
        "flagged": true,
        "parts": {
            "first.$": "$.vals[0]",
            "last3.$": "$.vals[3:]"
        },
        "weekday.$": "$$.DayOfWeek",
        "formattedOutput.$": "States.Format('Today is {}', $$.DayOfWeek)"
    }
}
```

Pへの入力が次のとおりであると仮定します:

```json
{
    "flagged": 7,
    "vals": [0, 10, 20, 30, 40, 50]
}
```

さらに、Context Object が次のようになっているとします:

```json
{
    "DayOfWeek": "TUESDAY"
}
```

この場合、 `リソース` フィールドで識別されるコードへの有効な入力は次のようになります:

```json
{
    "flagged": true,
    "parts": {
        "first": 0,
        "last3": [30, 40, 50]
    },
    "weekday": "TUESDAY",
    "formattedOutput": "Today is TUESDAY"
}
```

### Intrinsic Functions

States Languageは、プログラミング言語の関数のように見え、ペイロードテンプレートがタスクリソースとの間でやり取りされるデータを処理するのに役立つ構造である、少数の `Intrinsic Functions`を提供します。 組み込み関数の完全なリストについては、Appendix Bを参照してください。。

データの準備に使用されている `States.Format` という名前の組み込み関数の例を次に示します:

```json
"X": {
    "Type": "Task",
    "Resource": "arn:aws:states:us-east-1:123456789012:task:X",
    "Next": "Y",
    "Parameters": {
        "greeting.$": "States.Format('Welcome to {} {}\\'s playlist.', $.firstName, $.lastName)"
    }
}
```

1. 組み込み関数は文字列でなければなりません。
1. 組み込み関数は、組み込み関数名で始まらなければなりません。組み込み関数名には、文字`A`から`Z`、`a`から`z`、`0`から`9`、 `.` 、および `_` のみを含める必要があります。\
この仕様で定義されているすべての組み込み関数には、 `States` で始まる名前が付いています。他の実装では、名前が `States` で始まってはならない独自の組み込み関数を定義できます。
1. 組み込み関数名の直後には、 `（` と `）` で囲まれ、コンマで区切られた0個以上の引数のリストが続く必要があります。
1. 組み込み関数の引数は、アポストロフィ(')文字、数字、null、Paths、またはnested Intrinsic Functionsで囲まれた文字列にすることができます。
1. string, number or null引数の値は、引数自体です。 パスである引数の値は、ペイロードテンプレートの入力に適用した結果です。 組み込み関数である引数の値は、関数呼び出しの結果です。\
上記の例では、States.Formatの最初の引数は、フォーマットテンプレート文字列を生成するパスである可能性があることに注意してください。
1. 次の文字はすべての組み込み関数用に予約されており、エスケープする必要があります： `' { } \`\
予約文字のいずれかを予約文字として機能せずに値の一部として表示する必要がある場合は、バックスラッシュでエスケープする必要があります。\
文字 `\` をエスケープ文字として使用せずに値の一部として表示する必要がある場合は、バックスラッシュを使用してエスケープする必要があります。

    ```text
    リテラル文字列 \' は ' を表します
    リテラル文字列 \{ は { を表します
    リテラル文字列 \} は } を表します
    リテラル文字列 \\ は \ を表します
    ```

    JSON では、文字列リテラル値に含まれるすべての円記号を別の円記号でエスケープする必要があるため、上記は次のようになります。

    ```text
    エスケープ文字列 \\' は ' を表します
    エスケープ文字列 \\{ は { を表します
    エスケープ文字列 \\} は } を表します
    エスケープ文字列 \\\\ は \ を表します
    ```

    組み込み関数でオープンエスケープバックスラッシュ`\`が見つかった場合、インタープリターはランタイムエラーをスローします。

### Input and Output Processing

上記のように、データはJSONテキストとして状態間で渡されます。 ただし、States は、入力データのサブセットのみを処理したい場合があり、そのデータを入力に表示される方法とは異なる構造にする必要がある場合があります。 同様に、出力として渡すデータの形式と内容を制御したい場合があります。

これをサポートするために、 `InputPath` 、 `Parameters` 、 `ResultSelector` 、 `ResultPath` 、および `OutputPath` という名前のフィールドが存在します。

失敗状態と成功状態を除くすべての状態には、 `InputPath` と `OutputPath` が含まれる場合があります。

結果を生成する可能性のある状態には、 `パラメーター` 、 `ResultSelector` 、および `ResultPath` （Task State, Parallel State, and Map State）がある場合があります。

Pass Stateには、出力値を制御するための `Parameters` と `ResultPath` がある場合があります。

#### Using InputPath, Parameters, ResultSelector, ResultPath and OutputPath

この説明では、 `raw input` とは、状態への入力であるJSONテキストを意味します。  `Result` とは、状態が生成するJSONテキストを意味します。たとえば、Task Stateによって呼び出された外部コード、Parallel StatesまたはMap Statesの分岐の組み合わせ結果、またはパス状態の `Result` フィールドの値から生成されます。  `Effective input` とは、InputPathとパラメータを適用した後の入力を意味し、 `effective result` とは、ResultSelectorで処理した後の結果を意味し、 `effective output` とは、ResultSelector、ResultPath、およびOutputPathで結果を処理した後の最終状態出力を意味します。

1. `InputPath` の値はパスである必要があります。これは、States のraw inputに適用されて、その一部またはすべてを選択します。その選択は、たとえば、Task Stateのリソースや選択状態の選択セレクターに渡す際に、状態によって使用されます。
1. `Parameters` の値は、JSONオブジェクトであるペイロードテンプレートである必要があります。その入力は、raw inputにInputPathを適用した結果です。  `Parameters` フィールドが指定されている場合、そのペイロードは、抽出および埋め込み後、有効な入力になります。
1. `ResultSelector` の値は、入力が結果であり、ペイロードが置き換えられて有効な結果になるペイロードテンプレートである必要があります。
1. `ResultPath` の値は、状態の結果とのraw inputの組み合わせまたは置換を指定する参照パスである必要があります。
1. `ResultPath` の値は `$$` で始まってはなりません。つまり、コンテキストオブジェクトにコンテンツを挿入するために使用することはできません。
1. `OutputPath` の値はパスである必要があります。これは、ResultPathの適用後に状態の出力に適用され、次の状態のraw inputとして機能する有効な出力を生成します。

JsonPathを入力JSONテキストに適用すると、複数の値が生成される可能性があることに注意してください。たとえば、次のテキストがあります。

```json
{ "a": [1, 2, 3, 4] }
```

次に、JsonPath `$.a[0,1]` を適用すると、結果は2つのJSONテキスト1と2になります。これが発生すると、インタープリターはテキストを配列に収集するため、この例では 状態には入力が表示されます。

```json
[ 1, 2 ]
```

同じルールがOutputPath処理にも適用されます。 OutputPathの結果に複数の値が含まれている場合、有効な出力はそれらすべてを含むJSON配列です。

`ResultPath` フィールドの値は、raw inputを基準にして、結果を配置する場所を指定する参照パスです。 raw inputにResultPath値でアドレス指定された場所にフィールドがある場合、出力ではそのフィールドは破棄され、状態の結果によって上書きされます。 それ以外の場合は、状態出力に新しいフィールドが作成され、必要に応じて間にフィールドが作成されます。 たとえば、raw inputが与えられた場合：

```json
{
    "master": {
        "detail": [1, 2, 3]
    }
}
```

状態の結果が数値`6`であり、 `ResultPath` が`$.master.detail`である場合、出力では `detail`フィールドが上書きされます。

```json
{
    "master": {
        "detail": 6
    }
}
```

代わりに`$.master.result.sum`の `ResultPath` が使用された場合、結果はraw inputと結合され、`result`と`sum`を含む新しいフィールドのチェーンが生成されます。

```json
{
    "master": {
        "detail": [1, 2, 3],
        "result": {
            "sum": 6
        }
    }
}
```

InputPathの値が`null`の場合、raw inputは破棄され、状態の有効な入力は空のJSONオブジェクト`{}`であることを意味します。 `null`の値を持つことは、 `InputPath` フィールドがないこととは異なることに注意してください。

ResultPathの値が`null`の場合、それは状態の結果が破棄され、そのraw inputがその結果になることを意味します。

OutputPathの値が`null`の場合、入力と結果が破棄され、状態からの有効な出力は空のJSONオブジェクト`{}`であることを意味します。

#### Defaults

InputPath、Parameters、ResultSelector、ResultPath、およびOutputPathはそれぞれオプションです。InputPathのデフォルト値は `$` であるため、デフォルトでは、有効な入力はraw inputのみです。ResultPathのデフォルト値は `$` であるため、デフォルトでは、状態の結果が入力を上書きして置き換えます。OutputPathのデフォルト値は `$` であるため、デフォルトでは、状態の有効な出力はResultPathの処理の結果です。

パラメータとResultSelectorにはデフォルト値がありません。存在しない場合、入力に影響はありません。

したがって、InputPath、Parameters、ResultSelector、ResultPath、またはOutputPathのいずれも指定されていない場合、状態は提供されたとおりにraw inputを消費し、その結果を次の状態に渡します。

#### Input/Output Processing Examples

数値のペアを合計するLambdaタスクの上記の例を考えてみましょう。示されているように、その入力は `{ "val1": 3, "val2": 4 }`あり、その出力は `7`です。

入力がもう少し複雑だとします。

```json
{
    "title": "Numbers to add",
    "numbers": { "val1": 3, "val2": 4 }
}
```

次に、次を追加して状態定義を変更するとします。

```json
"InputPath": "$.numbers",
"ResultPath": "$.sum"
```

最後に、Lambda関数の4行目を次のように簡略化するとします。`return JSON.stringify(total)` これはおそらく関数のより良い形式であり、実際には数学を行うことだけを気にし、その結果がどのようにラベル付けされるかは気にしないはずです。

この場合、出力は次のようになります。

```json
{
    "title": "Numbers to add",
    "numbers": { "val1": 3, "val2": 4 },
    "sum": 7
}
```

インタプリタは、目的の効果を実現するために、複数レベルのJSONオブジェクトを構築する必要がある場合があります。Task Stateへの入力が次のとおりであるとします。

```json
{ "a": 1 }
```

タスクからの出力が `Hi!` であり、 `ResultPath` フィールドの値が `$.b.greeting` であるとします。 その場合、状態からの出力は次のようになります。

```json
{
    "a": 1,
    "b": {
        "greeting": "Hi!"
    }
}
```

#### Runtime Errors

States の入力が文字列 `foo` であり、その `ResultPath` フィールドの値が `$.x` であるとします。 その場合、ResultPathは適用できず、インタープリターは `States.ResultPathMatchFailure` のエラー名でマシンに失敗します。

### Errors

どの状態でもランタイムエラーが発生する可能性があります。 エラーは、`State Machine`定義の問題（直前で説明した `ResultPath` の問題など）、タスクの失敗（Lambda関数によってスローされる例外など）、またはネットワークパーティションイベントなどの一時的な問題が原因で発生する可能性があります。

状態がエラーを報告した場合、インタープリターのデフォルトのアクションは、`State Machine`全体に障害が発生することです。

#### Error representation

エラーは、エラー名と呼ばれる大文字と小文字を区別する文字列によって識別されます。 States言語は、既知のエラーに名前を付ける一連の組み込み文字列を定義します。これらはすべて、接頭辞 `States` で始まります。 Appendix Aを参照してください。

States は、接頭辞 `States.` で始まらない他の名前のエラーを報告する場合があります。

#### Retrying after error

Task States, Parallel States, and Map Statesには、 `Retry` という名前のフィールドがある場合があります。このフィールドの値は、リトライアーと呼ばれるオブジェクトの配列である必要があります。

各Retrierには、 `ErrorEquals` という名前のフィールドが含まれている必要があります。このフィールドの値は、エラー名と一致する文字列の空でない配列である必要があります。

状態がエラーを報告すると、インタープリターはリトライアーをスキャンし、エラー名がリトライアーの `ErrorEquals` フィールドの値に表示されると、そのリトライアーに記述されている再試行ポリシーを実装します。

個々のリトライアーは、通常は時間間隔を増やしながら、特定の回数の再試行を表します。

Retrierには、 `IntervalSeconds` という名前のフィールドが含まれる場合があります。このフィールドの値は、最初の再試行の前の秒数を表す正の整数でなければなりません（デフォルト値：1）。  `MaxAttempts` という名前のフィールド。その値は負でない整数でなければならず、再試行の最大回数を表します（デフォルト：3）。  `BackoffRate` という名前のフィールド。これは、試行ごとに再試行間隔を増やす乗数である数値です（デフォルト：2.0）。 BackoffRateの値は 1.0 以上でなければなりません。

値が0の `MaxAttempts` フィールドは有効であり、一部のエラーを再試行しないように指定していることに注意してください。

これは、3秒と4.5秒の待機後に 2 回の再試行を行うリトライアーの例です。

```json
"Retry" : [
    {
        "ErrorEquals": [ "States.Timeout" ],
        "IntervalSeconds": 3,
        "MaxAttempts": 2,
        "BackoffRate": 1.5
    }
]
```

Retrierの `ErrorEquals` フィールドの予約名 `States.ALL` はワイルドカードであり、任意のエラー名と一致します。 このような値は、 `ErrorEquals` 配列に単独で表示される必要があり、 `Retry` 配列の最後のRetrierに表示される必要があります。

これは、デフォルトの再試行パラメーターを使用して、 `States.Timeout` 以外のエラーを再試行するリトライアーの例です。

```json
"Retry": [
    {
        "ErrorEquals": [ "States.Timeout" ],
        "MaxAttempts": 0
    },
    {
        "ErrorEquals": [ "States.ALL" ]
    }
]
```

`MaxAttempts` フィールドで許可されている回数よりも多くエラーが繰り返される場合、再試行は停止し、通常のエラー処理が再開されます。

#### Complex retry scenarios

Retrierのパラメータは、単一のStates実行のコンテキストで、そのRetrierへのすべての訪問に適用されます。 これは例によって最もよく示されています。 次のTask Stateを考慮してください。

```json
"X": {
    "Type": "Task",
    "Resource": "arn:aws:states:us-east-1:123456789012:task:X",
    "Next": "Y",
    "Retry": [
        {
            "ErrorEquals": [ "ErrorA", "ErrorB" ],
            "IntervalSeconds": 1,
            "BackoffRate": 2,
            "MaxAttempts": 2
        },
        {
            "ErrorEquals": [ "ErrorC" ],
            "IntervalSeconds": 5
        }
    ],
    "Catch": [
        {
            "ErrorEquals": [ "States.ALL" ],
            "Next": "Z"
        }
    ]
}
```

このタスクが4回連続して失敗し、エラー名 `ErrorA` 、 `ErrorB` 、 `ErrorC` 、および `ErrorB` がスローされたとします。 最初の2つのエラーは最初のリトライアーと一致し、1秒と2秒の待機を引き起こします。 3番目のエラーは2番目のリトライアーと一致し、5秒間待機します。 4番目のエラーは最初のリトライアーと一致しますが、2回のリトライの `MaxAttempts` 上限にすでに達しているため、リトライアーは失敗し、実行は `Catch` フィールドを介して `Z` 状態にリダイレクトされます。

インタプリタが何らかの方法で別の状態に移行すると、すべてのRetrierパラメータがリセットされることに注意してください。

#### Fallback states

Task State、Parallel States、およびMap Statesには、 `Catch` という名前のフィールドがある場合があります。このフィールドの値は、Catchersと呼ばれるオブジェクトの配列である必要があります。

各キャッチャーには、リトライアーの `ErrorEquals` フィールドとまったく同じように指定された `ErrorEquals` という名前のフィールドと、値がState名と完全に一致する文字列でなければならない `Next` という名前のフィールドが含まれている必要があります。

状態がエラーを報告し、リトライアーがないか、再試行がエラーの解決に失敗した場合、インタープリターは配列順にキャッチャーをスキャンし、エラー名がキャッチャーの `ErrorEquals` フィールドの値に表示されると、遷移します。  `Next` フィールドの値で指定された状態へのマシン。

Retrierの `ErrorEquals` フィールドに表示される予約名 `States.ALL` はワイルドカードであり、任意のエラー名と一致します。 このような値は、 `ErrorEquals` 配列に単独で表示される必要があり、 `Catch` 配列の最後のキャッチャーに表示される必要があります。

#### Error output

状態がエラーを報告し、それがCatcherと一致して別の状態に転送されると、状態の結果（したがって、Catcherの`Next`フィールドで識別される状態への入力）は、エラー出力と呼ばれるJSONオブジェクトになります。エラー出力には、エラー名を含む `Error` という名前の文字列値フィールドが必要です。エラーに関する人間が読めるテキストを含む、 `Cause` という名前の文字列値フィールドを含める必要があります。

Catcherには `ResultPath` フィールドがあります。これはStateのトップレベルの `ResultPath` とまったく同じように機能し、Stateの元の入力にエラー出力を挿入して、Catcherの `Next` 状態の入力を作成するために使用できます。  `ResultPath` フィールドが指定されていない場合のデフォルト値は `$` です。これは、出力が完全にエラー出力で構成されていることを意味します。

これは、Lambda関数が未処理のJava例外をスローしたときに `RecoveryState` という名前の状態に遷移し、それ以外の場合はおそらくターミナルである `EndMachine` 状態に遷移するキャッチャーの例です。

また、この例では、最初のキャッチャーがエラー名と一致する場合、 `RecoveryState` への入力は元の状態入力になり、エラー出力は最上位の `error-info` フィールドの値になります。その他のエラーの場合、 `EndMachine` への入力はエラー出力になります。

```json
"Catch": [
    {
        "ErrorEquals": [ "java.lang.Exception" ],
        "ResultPath": "$.error-info",
        "Next": "RecoveryState"
    },
    {
        "ErrorEquals": [ "States.ALL" ],
        "Next": "EndMachine"
    }
]
```

各キャッチャーは、処理する複数のエラーを指定できます。

状態に `Retry` フィールドと `Catch` フィールドの両方がある場合、インタープリターは最初に適切なRetrierを使用し、再試行ポリシーがエラーの解決に失敗した場合にのみ、一致するCatcher遷移を適用します。

## State Types

注意として、状態タイプは `Type` フィールドの値によって指定されます。このフィールドは、すべての状態オブジェクトに表示される必要があります。

### Table of State Types and Fields

多くのフィールドは、複数の状態Typeで表示できます。 次の表は、どのフィールドがどの状態で表示されるかをまとめたものです。 1つの状態Typeに固有のフィールドは除外されます。

States | Task | Parallel | Map | Pass | Wait | Choice | Succeed | Fail
--- | --- | --- | --- | --- | --- | --- | --- | ---
Type | Required | Required | Required | Required | Required | Required | Required | Required
Comment | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed
InputPath, OutputPath | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed | Allowed | -
One of: Next or "End":true | Required | Required | Required | Required | Required | - | - | -
ResultPath | Allowed | Allowed | Allowed | Allowed | - | - | - | -
Parameters | Allowed | Allowed | Allowed | Allowed | - | - | - | -
ResultSelector | Allowed | Allowed | Allowed | - | - | - | - | -
Retry, Catch | Allowed | Allowed | Allowed | - | - | - | - | -

### Pass State

パス状態（ `"Type"： "Pass"` で識別）は、デフォルトで入力を出力に渡し、作業を実行しません。

合格状態には、 `Result` という名前のフィールドがある場合があります。 存在する場合、その値は仮想タスクの出力として扱われ、 `ResultPath` フィールド（存在する場合）で指定されたとおりに配置されて、次の状態に渡されます。  `Result` が提供されていない場合、出力は入力です。 したがって、 `Result` も `ResultPath` も指定されていない場合、PassStateは入力を出力にコピーします。

これは、おそらくテスト目的で、いくつかの固定データを`State Machine`に挿入するパス状態の例です。

```json
"No-op": {
    "Type": "Pass",
    "Result": {
        "x-datum": 0.381018,
        "y-datum": 622.2269926397355
    },
    "ResultPath": "$.coords",
    "Next": "End"
}
```

この状態への入力が次のとおりであると仮定します:

```json
{
    "georefOf": "Home"
}
```

その場合、出力は次のようになります:

```json
{
    "georefOf": "Home",
    "coords": {
        "x-datum": 0.381018,
        "y-datum": 622.2269926397355
    }
}
```

### Task State

Task State（ `"Type": "Task"` で識別）により、インタープリターは状態の `Resource` フィールドで識別される作業を実行します。

これが例です:

```json
"TaskState": {
    "Comment": "Task State example",
    "Type": "Task",
    "Resource": "arn:aws:states:us-east-1:123456789012:task:HelloWorld",
    "Next": "NextState",
    "TimeoutSeconds": 300,
    "HeartbeatSeconds": 60
}
```

Task Stateには `Resource` フィールドを含める必要があります。その値は、実行する特定のタスクを一意に識別するURIである必要があります。 States言語は、URIスキームやURIの他の部分を制約しません。

Task Stateには `Parameters` フィールドを含めることができ、その値はペイロードテンプレートでなければなりません。Task Stateには `ResultSelector` フィールドを含めることができ、その値はペイロードテンプレートでなければなりません。

タスクはオプションでタイムアウトを指定できます。タイムアウト（ `TimeoutSeconds` および `HeartbeatSeconds` フィールド）は秒単位で指定され、正の整数でなければなりません。

合計タイムアウトとハートビートタイムアウトの両方を間接的に提供できます。Task Stateには `TimeoutSecondsPath` フィールドと `HeartbeatSecondsPath` フィールドがあり、これらは参照パスである必要があり、解決されると、値が正の整数であるフィールドを選択する必要があります。Task Stateには、 `TimeoutSeconds` と `TimeoutSecondsPath` の両方、または `HeartbeatSeconds` と `HeartbeatSecondsPath` の両方を含めてはなりません。

指定する場合、 `HeartbeatSeconds` 間隔は `TimeoutSeconds` 値よりも小さくする必要があります。

指定しない場合、 `TimeoutSeconds` のデフォルト値は60です。

状態が指定されたタイムアウトより長く実行される場合、または指定されたハートビートよりも長い時間がタスクからのハートビートの間に経過する場合、インタープリターは`States.Timeout`エラー名で状態に失敗します。

### Choice State

Choice State（ `"Type": "Choice"` で識別）は、`State Machine`に分岐ロジックを追加します。

選択状態には、値が空でない配列である `Choices` フィールドが必要です。 配列の各要素はJSONオブジェクトである必要があり、選択ルールと呼ばれます。 選択ルールを評価して、ブール値を返すことができます。 トップレベルの選択ルール、つまり `Choices` 配列のメンバーである選択ルールには、 `Next` フィールドが必要です。このフィールドの値は、State名と一致する必要があります。

インタプリタは、配列順に最上位の選択ルールに対してパターン一致を試み、入力値と比較のメンバーが完全に一致する最初の選択ルールの`Next`フィールドで指定された状態に遷移します- 演算子配列。

これは選択状態の例です。

```json
"DispatchEvent": {
    "Type": "Choice",
    "Choices": [
        {
            "Not": {
                "Variable": "$.type",
                "StringEquals": "Private"
            },
            "Next": "Public"
        },
        {
            "And": [
                {
                    "Variable": "$.value",
                    "IsPresent": true
                },
                {
                    "Variable": "$.value",
                    "IsNumeric": true
                },
                {
                    "Variable": "$.value",
                    "NumericGreaterThanEquals": 20
                },
                {
                    "Variable": "$.value",
                    "NumericLessThan": 30
                }
            ],
            "Next": "ValueInTwenties"
        },
        {
            "Variable": "$.rating",
            "NumericGreaterThanPath": "$.auditThreshold",
            "Next": "StartAudit"
        }
    ],
    "Default": "RecordEvent"
}
```

この例では、マシンが次の入力値で起動されていると仮定します:

```json
{
    "type": "Private",
    "value": 22
}
```

次に、インタプリタは `value` フィールドに基づいて `ValueInTwenties` 状態に移行します。

選択ルールは、Boolean式またはData-test式のいずれかである必要があります。

### Boolean expression

ブール式は、 `And` 、 `Or` 、または `Not` という名前のフィールドを含むJSONオブジェクトです。 フィールド名が `And` または `Or` の場合、値は選択ルールの空でないオブジェクト配列である必要があり、 `Next` フィールドを含めることはできません。 インタプリタは配列要素を順番に処理し、期待どおりにブール評価を実行し、ブール値が明確に決定されたときに配列処理を停止します。

`Not` フィールドを含むブール式の値は、 `Next` フィールドを含まない単一の選択ルールである必要があります。 選択ルールが評価するブール値の逆数を返します。

### Data-test expression

データテスト式選択ルールは、フィールドとその値に関するアサーションであり、データに応じてブール値を生成します。 データテスト式には、値がパスでなければならない `Variable` という名前のフィールドが含まれている必要があります。

各選択ルールには、比較演算子を含むフィールドが1つだけ含まれている必要があります。 次の比較演算子がサポートされています。

1. StringEquals, StringEqualsPath
1. StringLessThan, StringLessThanPath
1. StringGreaterThan, StringGreaterThanPath
1. StringLessThanEquals, StringLessThanEqualsPath
1. StringGreaterThanEquals, StringGreaterThanEqualsPath
1. StringMatches \
    Note: 値は、1つ以上の`*`文字を含む可能性のある文字列である必要があります。変数パスによって選択されたデータ値が値と一致する場合、式はtrueになります。ここで、値の`*`は0文字以上に一致します。したがって、 `foo*.log`は`foo23.log`に一致し、`*.log`は`zebra.log`に一致し、`foo*.*`は`foobar.zebra`に一致します。`*`以外の文字は、マッチング中に特別な意味を持ちません。

    文字`*`をワイルドカードとして使用せずに値の一部として表示する必要がある場合は、バックスラッシュでエスケープする必要があります。

    文字`\`をエスケープ文字として使用せずに値の一部として表示する必要がある場合は、バックスラッシュを使用してエスケープする必要があります。

    リテラル文字列`\*`は`*`を表します。\
    リテラル文字列`\\`は`\`を表します。

    JSONでは、文字列リテラル値に含まれるすべての円記号を別の円記号でエスケープする必要があるため、上記は次のようになります。

    エスケープ文字列`\\*`は`*`を表します。\
    エスケープ文字列`\\\\`は`\`を表します。

    StringMatches文字列にオープンエスケープバックスラッシュ`\`が見つかった場合、インタプリタはランタイムエラーをスローします。
1. NumericEquals, NumericEqualsPath
1. NumericLessThan, NumericLessThanPath
1. NumericGreaterThan, NumericGreaterThanPath
1. NumericLessThanEquals, NumericLessThanEqualsPath
1. NumericGreaterThanEquals, NumericGreaterThanEqualsPath
1. BooleanEquals, BooleanEqualsPath
1. TimestampEquals, TimestampEqualsPath
1. TimestampLessThan, TimestampLessThanPath
1. TimestampGreaterThan, TimestampGreaterThanPath
1. TimestampLessThanEquals, TimestampLessThanEqualsPath
1. TimestampGreaterThanEquals, TimestampGreaterThanEqualsPath
1. IsNull \
    Note: これは、値が組み込みのJSONリテラルnullであることを意味します。
1. IsPresent \
    Note: この場合、変数フィールドパスが入力のいずれにも一致しない場合、例外はスローされず、選択ルールはfalseを返します。
1. IsNumeric
1. IsString
1. IsBoolean
1. IsTimestamp

`Path` で終わる演算子の場合、値はパスである必要があります。これは、状態の有効な入力に適用され、変数パスによって生成される値と比較される値を生成します。

値を比較する各演算子について、値が適切なタイプ（String、number、boolean、またはTimestamp）の両方でない場合、比較はfalseを返します。タイムスタンプと見なされるフィールドは、文字列型のコンパレータで照合できることに注意してください。

さまざまな文字列コンパレータは、大文字と小文字の区別、空白の折りたたみ、Unicode形式の正規化などの特別な処理を行わずに、文字列を文字ごとに比較します。

相互運用性のために、数値比較は、IEEE754-2008 `binary64` データ型を使用して表現できる大きさまたは精度以外の値で機能すると想定すべきではないことに注意してください。特に、`[-(2**53)+1、(2**53)-1]`の範囲外の整数は、期待どおりに比較できない場合があります。

選択状態には `Default` フィールドがあり、その値は状態名と一致しなければならない文字列でなければなりません。どの選択ルールも一致しない場合、その状態が実行されます。選択状態が選択ルールと一致せず、 `Default` 遷移が指定されていない場合、インタープリターは実行時のStates.NoChoiceMatchedエラーを発生させます。

### Wait State

待機状態（ `"Type": "Wait"` で識別）により、インタープリターはマシンが指定された時間継続するのを遅らせます。 時間は、秒単位で指定された待機時間、またはISO-8601拡張オフセット日時形式文字列として指定された絶対有効期限として指定できます。

たとえば、次の待機状態は、`State Machine`に10秒の遅延を導入します:

```json
"wait_ten_seconds": {
    "Type": "Wait",
    "Seconds": 10,
    "Next": "NextState"
}
```

これは絶対時間まで待機します:

```json
"wait_until": {
  "Type": "Wait",
  "Timestamp": "2016-03-14T01:59:00Z",
  "Next": "NextState"
}
```

待機時間をハードコーディングする必要はありません。 これは同じ例で、データへの参照パスを使用してタイムスタンプ時刻を検索するように作り直されました。これは`{ "expirydate"： "2016-03-14T01：59：00Z" }`のようになります。

```json
"wait_until": {
    "Type": "Wait",
    "TimestampPath": "$.expirydate",
    "Next": "NextState"
}
```

待機状態には、 `Seconds` 、 `SecondsPath` 、 `Timestamp` 、または `TimestampPath` のいずれかが含まれている必要があります。

### Succeed State

Succeed State（ `"Type": "Succeed"`で識別）は、`State Machine`を正常に終了するか、Parallel Stateのブランチを終了するか、MapStateのiterationを終了します。 Succeed Stateの出力はその入力と同じですが、 `InputPath` や `OutputPath` によって変更される可能性があります。

Succeed Stateは、マシンを終了する以外に何もしないChoice-Stateブランチの便利なターゲットです。:

```json
"SuccessState": {
    "Type": "Succeed"
}
```

成功状態は最終状態であるため、 `Next` フィールドはありません。

### Fail State

失敗状態（ `"Type": "Fail"` で識別）は、マシンを終了し、失敗としてマークします。

これが例です:

```json
"FailState": {
    "Type": "Fail",
    "Error": "ErrorA",
    "Cause": "Kaiju attack"
}
```

失敗状態には、 `Error` という名前の文字列フィールドが必要です。これは、エラー処理（再試行/キャッチ）、操作、または診断の目的で使用できるエラー名を提供するために使用されます。 失敗状態には、人間が読めるメッセージを提供するために使用される `Cause` という名前の文字列フィールドが必要です。

失敗状態は最終状態であるため、 `Next` フィールドはありません。

### Parallel State

Parallel States（ `"Type": "Parallel"` で識別）により、 `branches` が並列実行されます。

次に例を示します。:

```json
"LookupCustomerInfo": {
    "Type": "Parallel",
    "Branches": [
        {
            "StartAt": "LookupAddress",
            "States": {
                "LookupAddress": {
                    "Type": "Task",
                    "Resource": "arn:aws:lambda:us-east-1:123456789012:function:AddressFinder",
                    "End": true
                }
            }
        },
        {
            "StartAt": "LookupPhone",
            "States": {
                "LookupPhone": {
                    "Type": "Task",
                    "Resource": "arn:aws:lambda:us-east-1:123456789012:function:PhoneFinder",
                    "End": true
                }
            }
        }
    ],
    "Next": "NextState"
}
```

Parallel Stateにより、インタプリタは `StartAt` フィールドで指定された状態から始まる各ブランチを可能な限り同時に実行し、各ブランチが終了する（`terminal state`に達する）まで待ってから、ParallelStateの `Next` フィールドを処理します。上記の例では、これは、インタプリタが `LookupAddress` と `LookupPhoneNumber` の両方が終了するのを待ってから `NextState` に移行することを意味します。

上記の例では、LookupAddressブランチとLookupPhoneNumberブランチが並行して実行されます。

Parallel Statesには、要素がオブジェクトでなければならない配列である `Branches` という名前のフィールドが含まれている必要があります。各オブジェクトには、 `States` および `StartAt` という名前のフィールドが含まれている必要があります。これらの意味は、`State Machine`のトップレベルのフィールドとまったく同じです。

Parallel Stateブランチの `States` フィールドの状態には、その `States` フィールドの外側のフィールドをターゲットとする `Next` フィールドがあってはなりません。状態には、同じ `States` フィールド内にない限り、ParallelStateブランチの `States` フィールド内の状態名と一致する `Next` フィールドがあってはなりません。

言い換えると、ブランチの `States` フィールド内の状態は相互にのみ遷移でき、その `States` フィールド外の状態は遷移できません。

未処理のエラーまたは失敗状態への移行によっていずれかのブランチが失敗した場合、Parallel States全体が失敗したと見なされ、すべてのブランチが終了します。エラーがParallel Stateによって処理されない場合、インタープリターはエラーでマシンの実行を終了する必要があります。

失敗状態とは異なり、パラレル内の成功状態は、それ自体のブランチを終了するだけです。 Succeed Stateは、入力を出力として渡します。 `InputPath` と `OutputPath` によって変更される可能性があります。

Parallel Stateは、各ブランチの `StartAt` 状態への入力として、その入力（ `InputPath` フィールドでフィルタリングされる可能性があります）を渡します。これは、ブランチからの出力を含むブランチごとに1つの要素を持つ配列である結果を生成します。出力配列の要素は、 `ブランチ` 配列に表示されるのと同じ順序でブランチに対応します。すべての要素が同じタイプである必要はありません。

通常の方法で状態の `ResultPath` フィールドを使用して、出力配列を入力データに挿入できます。

たとえば、次のParallel Statesについて考えてみます:

```json
"FunWithMath": {
    "Type": "Parallel",
    "Branches": [
        {
            "StartAt": "Add",
            "States": {
                "Add": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::task:Add",
                    "End": true
                }
            }
        },
        {
            "StartAt": "Subtract",
            "States": {
                "Subtract": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::task:Subtract",
                    "End": true
                }
            }
        }
    ],
    "Next": "NextState"
}
```

`FunWithMath` 状態に入力としてJSON配列`[3、2]`が指定された場合、 `Add` 状態と `Subtract` 状態の両方がその配列を入力として受け取ります。  `Add` の出力は`5`、 `Subtract` の出力は`1`、ParallelStateの出力はJSON配列になります:

```json
[ 5, 1 ]
```

### Map State

Map States（ `"Type": "Map"` で識別）により、インタープリターは配列のすべての要素を、場合によっては並列に処理し、各要素を他の要素から独立して処理します。 このドキュメントでは、 `iteration` という用語を使用して、そのようなネストされた実行をそれぞれ説明します。

Parallel Stateは、複数の異なる`State Machine`ブランチを同じ入力に適用しますが、Map Stateは、単一の`State Machine`を複数の入力要素に適用します。:

1. `Iterator` フィールドの値は、配列の各要素を処理する`State Machine`を定義するオブジェクトです。
1. `ItemsPath` フィールドの値は、有効な入力のどこに配列フィールドがあるかを識別する参照パスです。
1. `MaxConcurrency` フィールドの値は、イテレータの呼び出しを並行して実行できる上限を提供する整数です。

次の入力データの例を考えてみましょう:

```json
{
    "ship-date": "2016-03-14T01:59:00Z",
    "detail": {
        "delivery-partner": "UQS",
        "shipped": [
            { "prod": "R31", "dest-code": 9511, "quantity": 1344 },
            { "prod": "S39", "dest-code": 9511, "quantity": 40 },
            { "prod": "R31", "dest-code": 9833, "quantity": 12 },
            { "prod": "R40", "dest-code": 9860, "quantity": 887 },
            { "prod": "R40", "dest-code": 9511, "quantity": 1220 }
        ]
    }
}
```

`shipped` 配列の各要素に単一のLambda関数 `ship-val` を適用する必要があるとします。 適切なMap Statesの例を次に示します。

```json
"Validate-All": {
    "Type": "Map",
    "InputPath": "$.detail",
    "ItemsPath": "$.shipped",
    "MaxConcurrency": 0,
    "Iterator": {
        "StartAt": "Validate",
        "States": {
            "Validate": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ship-val",
                "End": true
            }
        }
    },
    "ResultPath": "$.detail.shipped",
    "End": true
}
```

上記の例では、 `ship-val` ラムダ関数は `shipped` フィールドの各要素に対して 1回実行されます。 1回のiterationへの入力は :

```json
{
    "prod": "R31",
    "dest-code": 9511,
    "quantity": 1344
}
```

`ship-val` 関数も出荷の宅配便にアクセスする必要があるとします。これは各iterationで同じです。  `Parameters` フィールドは、各iterationのraw inputを構築するために使用できます:

```json
"Validate-All": {
    "Type": "Map",
    "InputPath": "$.detail",
    "ItemsPath": "$.shipped",
    "MaxConcurrency": 0,
    "Parameters": {
        "parcel.$": "$$.Map.Item.Value",
        "courier.$": "$.delivery-partner"
    },
    "Iterator": {
        "StartAt": "Validate",
        "States": {
          "Validate": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:123456789012:function:ship-val",
              "End": true
          }
        }
    },
    "ResultPath": "$.detail.shipped",
    "End": true
}
```

`ship-val` Lambda関数は、 `ItemsPath` で選択された配列の要素ごとに1回実行されます。 上記の例では、 `Parameters` で指定された1回のiterationへのraw inputは次のようになります。:

```json
{
    "parcel": {
        "prod": "R31",
        "dest-code": 9511,
        "quantity": 1344
    },
    "courier": "UQS"
}
```

上記の例では、ResultPathの結果は入力と同じになり、 `detail.shipped` フィールドは配列によって上書きされます。この配列では、各要素が `ship-val` Lambda関数の出力に適用されます。 対応する入力要素。

#### Map State input/output processing

`InputPath` フィールドは通常どおり動作し、raw inputの一部（この例では `detail` フィールドの値）を選択して、有効な入力として機能させます。

Map Statesには `ItemsPath` フィールドが含まれる場合があり、その値は参照パスである必要があります。参照パスは有効な入力に適用され、値がJSON配列であるフィールドを識別しなければなりません（MUST）。

`ItemsPath` のデフォルト値は `$` です。これは、有効な入力全体を意味します。したがって、Map Statesに `InputPath` フィールドも `ItemsPath` フィールドもない場合、状態へのraw inputはJSON配列であると想定されます。

各呼び出しへの入力は、デフォルトでは、 `ItemsPath` 値で識別される配列フィールドの単一の要素ですが、 `Parameters` フィールドを使用してオーバーライドできます。

各iterationで、Map States内（イテレータフィールド内の子状態は除く）で、コンテキストオブジェクトには、 `Item` という名前のオブジェクトフィールドを含む `Map` という名前のオブジェクトフィールドがあり、 `Index` という名前の整数フィールドが含まれます。  その値は、iterationで処理されている（ゼロベースの）配列インデックスであり、 `Index` という名前のフィールドであり、その値は、処理されている配列要素です。

各iterationで、Map States内（イテレータフィールド内の子状態は除く）で、コンテキストオブジェクトには`Map`という名前のオブジェクトフィールドがあり、`Item`という名前のオブジェクトフィールドが含まれ、次に`Index`という名前の整数フィールドが含まれます。 その値はiterationで処理されている（ゼロベースの）配列インデックスであり、その値は処理されている配列要素である`Value`という名前のフィールドです。

#### Map State concurrency

Map Statesには、負でない整数の `MaxConcurrency` フィールドが含まれる場合があります。 デフォルト値はゼロです。これは、呼び出しの並列処理に制限を設けず、インタープリターに可能な限り同時にiterationを実行するように要求します。

`MaxConcurrency` の値がゼロ以外の場合、インタープリターは同時iteration回数がその値を超えることを許可しません。

MaxConcurrency値1は特別であり、インタープリターが入力に出現する順序で配列要素ごとに1回イテレーターを呼び出し、前のiterationが実行を完了するまでiterationを開始しないという効果があります。

### Map State Iterator definition

Map Statesには、 `Iterator` という名前のオブジェクトフィールドが含まれている必要があります。このフィールドには、 `States` および `StartAt` という名前のフィールドが含まれている必要があります。これらの意味は、`State Machine`のトップレベルのフィールドとまったく同じです。

`Iterator` フィールドの `States` フィールドの状態には、その `States` フィールドの外側のフィールドをターゲットとする `Next` フィールドがあってはなりません。状態には、同じ `States` フィールド内にない限り、 `Iterator` フィールドの `States` フィールド内の状態名と一致する `Next` フィールドがあってはなりません。

言い換えると、イテレータの `States` フィールド内の状態は相互にのみ遷移でき、その `States` フィールド外の状態は相互に遷移できません。

未処理のエラーまたは失敗状態への移行が原因でiterationが失敗した場合、Map States全体が失敗したと見なされ、すべてのiterationが終了します。エラーがMap Statesによって処理されない場合、インタープリターはエラーでマシンの実行を終了する必要があります。

失敗状態とは異なり、マップ内の成功状態は、それ自体のiterationを終了するだけです。 Succeed Stateは、入力を出力として渡します。 `InputPath` と `OutputPath` によって変更される可能性があります。

## Appendices

### Appendix A: Predefined Error Codes

Code | Description
--- | ---
States.ALL | エラー名に一致するワイルドカード。
States.Timeout | Task Stateが `TimeoutSeconds` 値より長く実行されたか、 `HeartbeatSeconds` 値より長い時間ハートビートに失敗しました。
States.TaskFailed | 実行中にTask Stateが失敗しました。
States.Permissions | 指定されたコードを実行するための特権が不十分なため、Task Stateが失敗しました。
States.ResultPathMatchFailure | Stateの `ResultPath` フィールドは、Stateが受け取った入力には適用できません。
States.ParameterPathFailure | Stateの `Parameters` フィールド内で、パスを使用して名前が `.$` で終わるフィールドを置き換える試みは失敗しました。
States.BranchFailed | Parallel Statesの分岐に失敗しました。
States.NoChoiceMatched | 選択状態は、入力から抽出された条件フィールドに一致するものを見つけることができませんでした。
States.IntrinsicFailure | ペイロードテンプレート内で、組み込み関数を呼び出そうとして失敗しました。

### Appendix B: List of Intrinsic Functions

#### States.Format

この組み込み関数は、1つ以上の引数を取ります。 最初の値は文字列である必要があり、文字シーケンス`{}`のインスタンスを0個以上含めることができます。 組み込み関数には、`{}`の出現と同じ数の引数が残っている必要があります。 インタプリタは、最初の引数の文字列を返します。各`{}`は、組み込み関数の位置に対応する引数の値に置き換えられます。

必要に応じて、`{`および`}`文字をそれぞれ`\\{`および`\\}`としてエスケープできます。

引数がパスの場合、それを入力に適用すると、文字列、ブール値、数値、またはnullの値が生成される必要があります。 いずれの場合も、値は自然な文字列表現です。 文字列値には `` 文字を含めることはできません。値はJSON配列またはオブジェクトであってはなりません。

たとえば、次のペイロードテンプレートがあるとします:

```json
{
    "Parameters": {
        "foo.$": "States.Format('Your name is {}, we are in the year {}', $.name, 2020)"
    }
}
```

ペイロードテンプレートへの入力が次のようになっているとします。:

```json
{
    "name": "Foo",
    "zebra": "stripe"
}
```

ペイロードテンプレートを処理した後、新しいペイロードは次のようになります。:

```json
{
    "foo": "Your name is Foo, we are in the year 2020"
}
```

#### States.StringToJson

この組み込み関数は、値が文字列でなければならない単一の引数を取ります。 インタープリターはJSONパーサーをValueに適用し、解析されたJSONフォームを返します。

たとえば、次のペイロードテンプレートがあるとします :

```json
{
    "Parameters": {
        "foo.$": "States.StringToJson($.someString)"
    }
}
```

ペイロードテンプレートへの入力が次のようになっているとします。:

```json
{
    "someString": "{\"number\": 20}",
    "zebra": "stripe"
}
```

ペイロードテンプレートを処理した後、新しいペイロードは次のようになります。:

```json
{
    "foo": {
        "number": 20
    }
}
```

#### States.JsonToString

この組み込み関数は、パスでなければならない単一の引数を取ります。 インタプリタは、パスで識別されるデータを表すJSONテキストである文字列を返します。

たとえば、次のペイロードテンプレートがあるとします:

```json
{
    "Parameters": {
        "foo.$": "States.JsonToString($.someJson)"
    }
}
```

ペイロードテンプレートへの入力が次のようになっているとします。:

```json
{
    "someJson": {
        "name": "Foo",
        "year": 2020
    },
    "zebra": "stripe"
}
```

ペイロードテンプレートを処理した後、新しいペイロードは次のようになります。:

```json
{
    "foo": "{\"name\":\"Foo\",\"year\":2020}"
}
```

#### States.Array

この組み込み関数は、0個以上の引数を取ります。 インタープリターは、引数の値を含むJSON配列を指定された順序で返します。

たとえば、次のペイロードテンプレートがあるとします:

```json
{
    "Parameters": {
        "foo.$": "States.Array('Foo', 2020, $.someJson, null)"
    }
}
```

ペイロードテンプレートへの入力が次のようになっているとします。:

```json
{
    "someJson": {
        "random": "abcdefg"
    },
    "zebra": "stripe"
}
```

ペイロードテンプレートを処理した後、新しいペイロードは次のようになります。:

```json
{
    "foo": [
        "Foo",
        2020,
        {
            "random": "abcdefg"
        },
        null
    ]
}
```
