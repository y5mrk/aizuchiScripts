# aizuchiScripts

## AIYVoiceKitのラズパイ上での動かし方
### 1. OpenJTalkの準備
1. [この手順](http://raspi.seesaa.net/article/415482141.html)でラズパイをセットアップ
2. このリポジトリの`./aizuchiScripts/cmd/jsay`ファイルをラズパイ上に`/usr/local/bin/jsay`のパスで置く
3. 以下のコマンドで実行権限を付与
    ```Bash
    $ sudo chmod +x /usr/local/bin/jsay
    ```

### 2. AIYVoiceKitのソースコードの準備
1. [公式ドキュメント](https://aiyprojects.withgoogle.com/voice/)で開発環境構築
2. [google/aiyprojects-raspbian](https://github.com/google/aiyprojects-raspbian/releases)の最新版のコードをラズパイ上に置く
3. ↑のソースコードの`./AIY-projects-python/checkpoints/`配下に、`./aizuchiScripts/src/`以下の動かしたいファイルを置く
4. ラズパイにsshした状態で、以下のコマンドで実行
    ```Bash
    $ python3 ~/AIY-projects-python/checkpoints/<ファイル名>.py
    ```

## 開発する時
[google/aiyprojects-raspbian](https://github.com/google/aiyprojects-raspbian/releases)がパッケージ管理になっていない(?要確認)ので、  
cloneしてきて`./AIY-projects-python/checkpoints/`配下に、ソースコードを置く必要がある。
