from setuptools import setup, find_packages
import PyPokeClasses
setup(
    name="PyPokeClasses",  # パッケージ名
    version=PyPokeClasses.__version__,  # バージョン
    author="Atama12",  # 作者名
    author_email="atama5860@gmail.com",  # メールアドレス
    description="A class-based Package for accessing and interacting with PokeAPI's JSON data.",  # パッケージの説明
    long_description=open("README.md", "r",encoding="utf-8").read(),  # 長い説明（READMEから）
    long_description_content_type="text/markdown",  # READMEのフォーマット（markdownの場合）
    url="https://github.com/atama12/PyPokeClasses.git",  # リポジトリのURL
    packages=['PyPokeClasses','PyPokeClasses.Berries','PyPokeClasses.Contests','PyPokeClasses.Encounters','PyPokeClasses.Evolution','PyPokeClasses.Games','PyPokeClasses.Items','PyPokeClasses.Locations','PyPokeClasses.Machines','PyPokeClasses.Moves','PyPokeClasses.Pokemon'],  # パッケージを自動で探してくれる
    keywords="PyPokeClasses pypokeclasses pokeAPI",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # 対応するPythonのバージョン
    install_requires=[
        "requests",  # 必要なパッケージ
        "typing",
        
    ],
)
