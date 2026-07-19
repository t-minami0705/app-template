# 🛠️Class : Rectangle
#概要
矩形を表すデータクラス。矩形の座標、サイズ、色、四隅の頂点を保持し、座標⇔頂点の相互変換や幅、高さ変更時の頂点再計算を担当する。

## 🔧Base Method 
### ⚙️**init**()
#概要 
RectangleManagerの初期化を行う。

#処理内容 
- CommonResponseを初期化
- クラス名保持
- メソッド名保持
- Rectangleリスト生成
- 
## 🔧Factory Method 
### ⚙️from_xywh()
#概要
左上座標(X,Y)と幅・高さからRectangleオブジェクトを生成する。

#処理内容
- x,y,width,heightを保持
- 四隅の座標(points)を生成
- Rectangleを返却

#入出力
> [!note] 入力
> (x, y)
> width
> height

> [!note] 出力
>``` text
>┌────────────┐
>│            │
>│            │
>└────────────┘
>```
>P0  P1  P2  P3

### ⚙️from_points()
#概要
四隅の頂点情報からRectangleオブジェクトを生成する。

#処理内容 
pointsから左端、上橋、右下、下端を求め、x、y、width、heightを算出して保持する。

## 🔧Public Method 
### ⚙️update_from_points()
#概要 
現在保持しているpointからx、y、width、height を計算する。

#利用シーン
四隅の座標を直接編集したあと、points → x、y、width、height へ同期したい場合など。

### ⚙️update_points()
#概要 
現在保持しているx、y、width、height から points を再生成する。

#利用シーン
例えば rect.x += 20 などで位置変更した後、頂点情報を更新したい場合など。

### ⚙️update_points_from_width()
#概要 
矩形の左辺を固定し、右辺のみ移動することで幅を変更する。

#処理内容 
>[!note] 変更前
>```text
>変更前
>A────B
>│    │
>│    │
>D────C
>```

>[!note] 変更後
>```text
>変更後
>A──────B'
>│      │
>│      │
>D──────C'
>```
左側2点はそのまま。右側2点のみＸ座標を書き換える。

#利用シーン 
ドラッグ操作などで、「左固定・右だけ伸縮」を実現した場合など。

### ⚙️update_points_from_width()
#概要 
矩形の上辺を固定し、下辺のみ移動することで高さを変更する。

#処理内容 
>[!note] 変更前
>```text
>変更前
>A────B
>│    │
>│    │
>D────C
>```

>[!note] 変更後
>```text
>変更後
>A────B
>│    │
>│    │
>│    │
>│    │
>D'───C'
>```
上側2点は固定。下側2点だけY座標を変更する。

### ⚙️update_points_from_width()
#概要
Rectangleオブジェクトを管理するクラス。矩形そのものの処理ではなく、登録、削除、取得、件数取得 などコレクション操作を担当する。

## 🔧Collection操作
### ⚙️add_rectangle()
#概要 
Rectangleを管理対象へ追加する。

### ⚙️remove_rectangle()
#概要 
指定したRectangleを一覧を削除する。

### ⚙️clear_rectangles()
#概要 
現在登録されているRectangle数を返す。

# 📖 更新履歴
## 2026/07/09
### クラス構成
- 単独の四角図形を操作する機能
- 複数の図形を管理する機能

### 方法案

- 四角の図形を構成する構造体を定義する。
  x：起点（左上）X軸座標
  y：起点（左上）Y軸座標
  width：横幅
  height：高さ
  lineColor：枠線
  fillColor：塗りつぶし色
  points：4つ角のそれぞれの座標

## 2026/07/19
>[!Note] 全体イメージ
>``` text
>RectangleManager
>│
>├── Rectangle①
>│     ├ x
>│     ├ y
>│     ├ width
>│     ├ height
>│     └ points
>│
>├── Rectangle②
>│
>├── Rectangle③
>│
>└── Rectangle④
>```
>- Rectangleは「1つの矩形データ」と、そのデータを整合性を保ちながら更新する責務を持ちます。
>- **RectangleManager**は「複数のRectangleを管理する責務」を持ち、個々の矩形の形状変更には関与しません。

このように責務が分離することで、今後の機能を追加しやすい構成にしている。

#制作予定機能
 - 描画処理
 - 回転
 - 拡大縮小
 - 当たり（重なり）判定
 