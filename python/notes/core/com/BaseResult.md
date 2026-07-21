# 🧩Class : BaseResult
#概要
`BaseResult` は、アプリケーション全体で共通利用される **結果オブジェクトの標準形** を提供する。 例外を直接スローせず、

> 「呼び出し元が結果を見て処理を判断する」 という設計方針を実現するためのクラス。

これは、層をまたいで例外を伝播させると責務が曖昧になりやすいという問題を避け、 **例外をドメインイベントのように扱う**ための仕組みとも言える。

#主な特徴
- Application層・Domain層・Repository層で共通利用可能
- 例外を投げずに「成功／失敗」を返すための標準フォーマット 
- クラス名・メソッド名・結果コード・メッセージ・エラー内容・スタックトレースを統一管理
- 呼び出し元が結果を見て処理を分岐できる
- ログ出力・監視・例外ハンドリングを一貫した形で実装できる
- `_initialize()` により再利用が容易

#使用イメージ
#### Repository 層
``` Python
def fetch_user(user_id: int) -> BaseResult:
    result = BaseResult()
    result.class_name = "UserRepository"
    result.method_name = "fetch_user"

    try:
        user = db.get(user_id)
        result.result_code = 0
        result.result_msg = "Success"
    except Exception as e:
        result.result_code = 1
        result.result_errmsg = str(e)
        result.stack_trace = traceback.format_exc()

    return result
```

#### Domain 層
``` Python
repo_result = user_repository.fetch_user(10)

if repo_result.result_code != 0:
    return repo_result  # そのまま上位層へ返す
```

#### Application 層
``` Python
result = user_service.create_user(data)

if result.result_code == 0:
    print("ユーザー作成成功")
else:
    logger.error(result.stack_trace)
    print("失敗:", result.result_errmsg)

```

#実装のポイント
### 🧱 プロパティによる安全なアクセス

各フィールドは `_class_name` のように **プライベート変数**として保持され、 `@property` によって **読み書きのインターフェースを統一**している。

## 🔧Base Method 
### ⚙️  \_\_init\_\_
　BaseResultクラスのコンストラクタ。
``` python
def _initalize(self) -> None:
    self._method_name = ""
    self._result_code = 0
    self._result_mag = ""
    self._result_errmsg = ""
    self._stack_trace = ""
```

#プロパティ一覧
- **class_name** — 実行元クラス名
- **method_name** — 実行メソッド名
- **result_code** — 成功/失敗を示すコード
- **result_msg** — 結果メッセージ
- **result_errmsg** — エラー内容
- **stack_trace** — 例外発生時のスタックトレース

## コールアウト例（Obsidian / GitHub対応）

> [!Note] `BaseResult` は「例外を層で伝播させない」設計を実現するための標準フォーマット。 呼び出し元が結果を見て処理を判断することで、層の責務が明確になる。

## 📖まとめ
`BaseResult` は、アプリケーション層・ドメイン層・インフラ層を横断して利用できる **例外を値として扱うための共通基底クラス**。

これにより、

- 層の責務が明確になる
- 例外伝播の複雑さを排除できる
- ログ・監視・エラー処理が統一される
- 呼び出し元が明確に成功／失敗を判定できる

というメリットが得られる。