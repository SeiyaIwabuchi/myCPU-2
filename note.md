フェッチ→デコード→オペランド読み出し→実行
#### フェッチ
メモリから読み出す。
プログラムカウンタに示されている番地から命令レジスタへ転送する。
#### デコード
プログラムカウンタからデコーダへ送り出す。
各制御装置へ信号を送り出す。
#### オペランド読み出し
処理に必要なデータをメモリから取り出して
#### 実行
レジスタやメモリ、PCなどの記憶装置に対して書き込む
#### CPUでは実装しない部分
コンパイラによるインライン展開
### 目標
四則演算ができる電卓を作る！
繰り返し計算ができる！（平均を求められる）

#### 実装する命令
3語長
##### 転送系
- レジスタ <--> メモリ
    - LD
    - ST
- レジスタ <--> レジスタ
    - LD
##### 制御系
- ゼロ分岐
    - JZE
- 負分岐
    - JMI
- 待ち
    - NOP
##### 演算系
- 算術加算
    - ADD
- 減算は負数の加算で実現する。
#### メモリ管理
- 定数定義
    - DC
- 領域確保
    - DS

#### 三語で一命令
1語目は命令
2は宛先レジスタ
3はレジスタかメモリ番地
数値の範囲は-8~7

#### 命令一覧
|文字列|意味|
|:-:|:-:|
|n|任意の数字|
|addr|メモリのアドレスかラベル|
|size|領域サイズを表す。単位はワード|

|命令|動作|構文|
|:-:|:-:|:-:|
|LD|(メモリ)->レジスタ|LD GRn addr|
|LD|レジスタ->レジスタ|LD GRn GRn|
|ST|レジスタ->(メモリ)|ST GRn addr|
|JZE|ゼロフラグが1の時ジャンプ先にジャンプする|JZE addr|
|JMI|ゼロフラグとサインフラグが1の時ジャンプ先にジャンプする|JMI addr|
|NOP|何もしない命令|NOP|
|ADD|算術加算を行う|ADD GRn GRn|
|DC|定数を定義する|DC n|
|DS|領域を確保する|DS size|

#### データフロー
```plantuml
@startuml
object PC
object MEM
object IR
object GRn
object compar
object FR
object crystal
object SC
object RS
object INple
object OUTple
object COMple
object decoder
object ALU
object 定数0
object AR
object addrSelector
PC --> addrSelector:フェッチ
MEM --> IR:フェッチ
MEM --> INple:LD
INple --> GRn:LD,ADD
GRn --> MEM:ST
GRn --> OUTple:LD1
定数0 --> OUTple:LD0
compar --> FR:実行
MEM --> COMple:実行
GRn --> COMple:実行
COMple --> compar
MEM --> PC:JZE,JMI
MEM --> RS:格納先レジスタ
GRn --> OUTple:ADD1
GRn --> OUTple:ADD2
ALU --> INple:ADD
OUTple --> ALU:LD,ADD
MEM --> AR:アドレス格納
AR --> addrSelector:オペランド読み出し
addrSelector --> MEM:アドレス
@enduml
```

#### 制御フロー
```plantuml
@startuml
object PC
object MEM
object IR
object GRn
object compar
object FR
object crystal
object SC
object RS
object INple
object OUTple
object COMple
object decoder
object ALU
object 定数0
object AWplex
object AR
object addrSelector
crystal --> SC:順序管理器
crystal --> PC:クロック立ち下\nがり毎に加算
SC --> IR:1クロック目
crystal --> IR:1クロック目立上が\nりでIR確定(フェッチ)
RS --> decoder:GRのenable切り替え
crystal --> RS:2クロック目立\n上がりで確定
SC --> RS:2クロック目
IR --> AWplex:（LDかADD）以外か
decoder --> AWplex:enable信号
AWplex --> GRn:enable信号か0
crystal --> GRn:クロック
crystal --> MEM:クロック
IR --> ALU:加算か転送か
IR --> INple:LDか
IR --> MEM:STか
crystal --> AR:3クロック目立ち\n上がりで確定
SC --> AR:3クロック目
SC --> addrSelector:3クロック目
@enduml
```