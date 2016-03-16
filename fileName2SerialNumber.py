# -*- coding: utf-8 -*-

"""　連番ファイルのゴミ文字列を取り除くスクリプト

「hogehoge000.jpg」または「hoge0001hoge.png」のようなファイルの
hogehoge部分を取り除き、単純な連番（例 000.jpg）にするだけの
スクリプトです
デジカメの写真ファイルとかにご利用下さい
実行環境はpython3.5.1です
[使い方]
コマンドライン引数に
書き換えファイルが存在する対象フォルダ　を指定（必須）
-d または --digits オプションで連番桁数を指定　（オプションだけど必須）
-e または --extension オプションで変更したいファイルの拡張子を指定　（オプションだけど必須）
-m または --manual で処理後、連番が被ってしまうファイル(例 000a.jpg と 000b.jpgとか)のファイル名を手動で入力するモードに移行します。
-b または --before で連番の前に指定した文字列をくっつけます
-a または --after で連番の後に指定した文字列をくっつけます

※フォルダパスは絶対参照で、ファイル拡張子は必ずドットを含めて下さい　　
　
"""
__author__ = 'tubone'
__version__ = '0.3'

import sys
import os
import re
import argparse

def main():
    u"""    
    コマンドライン引数で書き換え対象フォルダ、連番桁数、拡張子、手動書き換えを行うかを指定します
    """
    
    p = argparse.ArgumentParser(description=u'連番ファイルのゴミ文字列を取り除くスクリプト')
    p.add_argument('path_root_src', \
                   action='store', \
                   nargs=None, \
                   const=None, \
                   default=None, \
                   type=str, \
                   choices=None, \
                   help=u'書き換え対象フォルダのパス指定.', \
                   metavar=None)
    p.add_argument('-d', '--digits', \
                   action='store', \
                   nargs='?', \
                   const=None, \
                   default=None, \
                   required=True, \
                   type=int, \
                   choices=None, \
                   help=u'連番の桁数を指定', \
                   metavar=None)
    p.add_argument('-e', '--extension', \
                   action='store', \
                   nargs='?', \
                   const=None, \
                   default=None, \
                   required=True, \
                   type=str, \
                   choices=None, \
                   help=u'書き換えるファイル拡張子を指定　※ドットをつけろ(例 .jpg)', \
                   metavar=None)
    p.add_argument('-m', '--manual', \
                   action='store_true', \
                   help=u'連番が被った際に手動書き換えモードに移行するか')
    p.add_argument('-b', '--before', \
                   action='store', \
                   nargs='?', \
                   const=None, \
                   default=None, \
                   type=str, \
                   choices=None, \
                   help=u'連番名の前に指定文字列をくっつける', \
                   metavar=None)
    p.add_argument('-a', '--after', \
                   action='store', \
                   nargs='?', \
                   const=None, \
                   default=None, \
                   type=str, \
                   choices=None, \
                   help=u'連番名の後に指定文字列をくっつける', \
                   metavar=None)    
    
    args = p.parse_args()
    
    if (args.manual):
        changeNameHand(name2number(args.path_root_src, args.digits, args.extension))
    else:
        name2number(args.path_root_src, args.digits, args.extension)
        
    if (args.before != None or args.after != None):
        addstr(args.before, args.after, args.digits, args.extension)    

def name2number(folderpass, digits, extension):
    u"""    
    第一引数にフォルダパス、第二引数に連番の桁数、第三引数に拡張子(例　.jpg)を指定します
    """    

    count = 0
    existfiles = []
    files = os.listdir(folderpass) # フォルダパスからファイル一覧を取得
    os.chdir(folderpass) # 作業ディレクトリ変更
    print("書き換え先フォルダ: " + folderpass)
    print("連番桁: %s桁" % digits)
    print("拡張子: %s" % extension)
    print("-------------------------------------------------------")
    ext = re.compile(extension) # 拡張子の正規表現をコンパイル
    for file in files:
        num = re.search('\\d{' + str(digits) +'}', file) # 取得ファイル名から連番部分を取り出す
        if (num == None): 
            pass
        else:
            newname = num.group() + extension # 連番名作成
            oldname = str(file)
            if (ext.search(file) and num):
                if os.path.isfile(newname): # 他の連番ファイルの有無を確認
                    print("ファイル名%sが存在するため%sは書き換えません" % (str(file), oldname))
                    if (oldname != newname):
                        existfiles.append(file) # 同一連番で他の文字列(例 000a と 000b)によって区別しているものをリスト
                        
                else:
                    os.rename(file, newname) # 書き換え
                    print("書き換え: %s => %s" % (oldname, newname))
                    count += 1
            else:
                pass
    print("--------------------------------------------------------")
    print("処理終了！　書き換えファイル数: %s" % count)
    return existfiles

def changeNameHand(existfiles):
    u"""    
    file一覧のリストを引数とし、それらのファイル名を標準入力から読み込み書き換えます
    """ 
    
    print("----------------------------------------------------")
    print("連番が被ったファイル名を手動で決定します\n")    
    for file in existfiles:
        print("ファイル名: %s を書き換えますか? (y/n)" % str(file))
        flug = input()
        if (flug == "y" or flug == "Y"):
            print("新しいファイル名を入力して下さい %s =>" % str(file))
            newname = input()
            while(os.path.isfile(newname)): # 被らないファイル名が指定されるまでループ ToDo:上書きモード作成
                print("既にファイル %s が存在しています　別の名前を指定して下さい %s => ?" % (str(file), str(file)))
                newname = input()
            os.rename(file, newname)
            print("書き換え: %s => %s \n" % (str(file), newname))
        else:
            print("%s はそのままにします \n" % str(file))
    print("全てのファイルの書き換えが終了しました\n")
    
def addstr(before, after, digits, extension):
    u"""    
    第一引数に前につける文字列、第二引数に後につける文字列、第三引数に連番桁数、第四引数に拡張子を指定します
    """ 
    print("----------------------------------------------------")
    files = os.listdir()
    ext = re.compile(extension) # 拡張子の正規表現をコンパイル 
    if (before != None):
        print("連番ファイル名の前に %s をくっつけます" % before)
    if (after != None):
        print("連番ファイル名の後に %s をくっつけます" % after)
    
    for file in files:
        num = re.search('\\d{' + str(digits) +'}', file) # 取得ファイル名から連番部分を取り出す
        if (before == None):
            before = ""
        if (after == None):
            after = ""
        
        if (num == None):
            pass
        else:
            if (ext.search(file)):
                center, e = str(file).split(".")
                newname = before + center + after + extension
                oldname = str(file)
                if (num):
                    if os.path.isfile(newname):
                        pass
                    else:
                        os.rename(file, newname)
                        print("書き換え: %s => %s" %(oldname, newname))   
    return None
    
if __name__ == "__main__":
    main()
