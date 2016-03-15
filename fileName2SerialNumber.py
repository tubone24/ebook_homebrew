# -*- coding: utf-8 -*-

"""　連番ファイルのゴミ文字列を取り除くスクリプト

「hogehoge000.jpg」または「hoge0001hoge.png」のようなファイルの
hogehoge部分を取り除き、単純な連番（例 000.jpg）にするだけの
スクリプトです
デジカメの写真ファイルとかにご利用下さい
実行環境はpython3.5.1です

[使い方] コマンドラインから　1.書き換え先のフォルダパス　2.連番の桁数　3.ファイル拡張子　を指定します
　　　　 フォルダパスは絶対参照で、ファイル拡張子は必ずドットを含めて下さい　　
"""
__author__ = 'tubone'
__version__ = '0.1'

import sys
import os
import re

def main(folderpass, digits, extension):
    u"""    
    第一引数にフォルダパス、第二引数に連番の桁数、第三引数に拡張子(例　.jpg)を指定します
    """    

    count = 0
    files = os.listdir(folderpass) # フォルダパスからファイル一覧を取得
    os.chdir(folderpass) # 作業ディレクトリ変更
    print("書き換え先フォルダ: " + folderpass)
    print("連番桁: %s桁" % digits)
    print("拡張子: %s" % extension)
    print("-------------------------------------------------------")
    for file in files:
        ext = re.compile(extension) # 拡張子の正規表現をコンパイル
        num = re.search('\\d{' + str(digits) +'}', file) # 取得ファイル名から連番部分を取り出す
        if (num == None): 
            pass
        else:
            newname = num.group() + extension # 連番名作成
            oldname = str(file)
            if (ext.search(file) and num):
                if os.path.isfile(newname): # 他の連番ファイルの有無を確認
                    print("ファイル名%sが存在するため%sは書き換えません" % (newname, oldname))
                else:
                    os.rename(file, newname) # 書き換え
                    print("書き換え: %s => %s" % (oldname, newname))
                    count += 1
            else:
                pass
    print("--------------------------------------------------------")
    print("処理終了！　書き換えファイル数: %s" % count)

if __name__ == "__main__":
    param = sys.argv
    main(param[1], param[2], param[3])
