from setuptools import setup, find_packages

setup(
    name="iniloader",                        # パッケージ名
    version="0.1",                      # バージョン
    description="iniファイルの読み書き",# 説明
    author="Ruchi",                 # 作成者
    author_email="t@ruchi.main.jp", # 作成者のメールアドレス
    packages=find_packages(),           # パッケージを自動的に探す
    install_requires=[],                # 依存関係があれば指定
)
