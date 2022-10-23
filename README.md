# aizuchiScripts

## AIYVoiceKitのラズパイ上での動かし方
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
