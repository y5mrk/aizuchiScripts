# aizuchiScripts

## Macでの環境構築手順
### 1. cloneなど
```Bash
$ git clone git@github.com:y5mrk/aizuchiScripts.git
$ cd ./aizuchiScrits
$ mkdir ./src/data
```

### 2. Anacondaの仮想環境構築
```Bash
$ conda create --name aizuchiScripts python=3.11.2
$ conda activate aizuchiScripts
$ conda env create -f packages.yaml
```

### 3. MeCabのインストールと設定
```Bash
$ brew install mecab
$ brew install mecab-ipadic
$ conda install -c anaconda swig        ### condaでMeCabを使うための設定
$ python -m pip install mecab-python3
```

### 4. envファイル作成
1. .env.exampleをコピー
    ```Bash
    $ cp .env.example .env
    ```
3. openAIのOrganization IDを調べ、と新たなSecret Keyを作成する
    - Organization ID： https://platform.openai.com/account/org-settings
    - API key：https://platform.openai.com/account/api-keys
      - 「create new secret key」から新たなSecret Keyを作成する
      - keyをコピーする
   
2. 3で調べたIDとkeyを、.envのAPI_ORGとAPI_KEYにそれぞれ貼り付ける

### 5. （openAIのモジュールがないと言われる場合）openAIのpackageの設定
1. openAIのモジュールのパスを調べる
    ```Bash
    $ pip show openai

    Name: openai
    Version: 0.27.8
    Summary: Python client library for the OpenAI API
    Home-page: https://github.com/openai/openai-python
    Author: OpenAI
    Author-email: support@openai.com
    License:
    Location: /Users/XXXXX/.pyenv/versions/3.11.2/lib/python3.11/site-packages     ### <- ここに記載されているパスをコピーしておく
    Requires: aiohttp, requests, tqdm
    Required-by:
    ```
2. pthファイルの置き場所を調べる    
    ```Bash
    $ python
    >>> import sys, pprint
    >>> pprint.pprint(sys.path)
    ['',
    '/Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python311.zip',
    '/Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python3.11',
    '/Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python3.11/lib-dynload',
    '/Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python3.11/site-packages']      ### <- /site-packagesとなってるパスを探してコピーしておく
    >>> # Ctrl + Dでぬける
    ```
3. pthファイルを作成
    ```Bash
    $ cd /Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python3.11/site-packages    ### <- 5-2でコピーした/site-packagesのパス
    $ vi importModule.pth

    ### エディタ起動後、5-1でコピーしたopenAIのLocationのパスを貼り付ける
    /Users/XXXXX/.pyenv/versions/3.11.2/lib/python3.11/site-packages
    ```
4. パスが追加されているかの確認
    ```Bash
    $ python
    >>> import sys, pprint
    >>> pprint.pprint(sys.path)
    ['',
    '/Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python311.zip',
    '/Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python3.11',
    '/Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python3.11/lib-dynload',
    '/Users/XXXXX/anaconda3/envs/aizuchiScripts/lib/python3.11/site-packages',
    '/Users/XXXXX/.pyenv/versions/3.11.2/lib/python3.11/site-packages']      ### <- openAIのLocationのパスが追加されているのを確認
    >>> # Ctrl + Dでぬける
    ```
5. `python ./src/combiningF0AndSilince.py`

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
