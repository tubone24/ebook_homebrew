# -*- coding: utf-8 -*-

"""　連番ファイルのゴミ文字列を取り除くスクリプト
「hogehoge000.jpg」または「hoge0001hoge.png」のようなファイルの
hogehoge部分を取り除き、単純な連番（例 000.jpg）にするだけの
スクリプト
動作にはPIL (Pillow) と PyPDF2が必要です
pipなどを利用して環境を整えてください
　
"""
__author__ = 'tubone'
__version__ = '0.3.2'
__copyright__ = 'Copyright (c) tubone'
__license__ = "MIT License"

import sys
import os
import re
import argparse
import PIL
import PIL.Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import zipfile


def main():
    u"""    
    コマンドライン引数を参照する　オプションについてはusage()で
    """
    
    p = argparse.ArgumentParser(description=u'連番ファイルのゴミ文字列を取り除くスクリプト')
    p.add_argument('pathRootSrc', action='store', type=str, help=u'書き換え対象フォルダのパス指定.', metavar=None)
    p.add_argument('-d', '--digits', action='store', nargs='?', required=True, type=str, \
                   help=u'連番の桁数を指定', metavar=None)
    p.add_argument('-e', '--extension', action='store', nargs='?', required=True, type=str, \
                   help=u'書き換えるファイル拡張子を指定　※ドットをつけろ(例 .jpg)', metavar=None)
    p.add_argument('-m', '--manual', action='store_true', help=u'連番が被った際に手動書き換えモードに移行するか')
    p.add_argument('-b', '--before', action='store', nargs='?', type=str, \
                   help=u'連番名の前に指定文字列をくっつける', metavar=None)
    p.add_argument('-a', '--after', action='store', nargs='?', type=str, \
                   help=u'連番名の後に指定文字列をくっつける', metavar=None) 
    p.add_argument('-p', '--pdf', action='store', nargs='?', type=str, \
                   help=u'連番にした画像ファイルをpdf化する', metavar=None)
    p.add_argument('-P', '--pdfRemoveImage', action='store', nargs='?', type=str, \
                   help=u'連番にした画像ファイルをpdf化し画像ファイルは削除する', metavar=None) 
    p.add_argument('-z', '--zip', action='store', nargs='?', type=str, \
                   help=u'連番にしたファイルをzipに固める', metavar=None)
    p.add_argument('-Z', '--zipRemoveFiles', action='store', nargs='?', type=str, \
                   help=u'連番にしたファイルをzipに固め、ファイルは削除する', metavar=None)    
    args = p.parse_args()
    
    if (re.match(r'^\d*,?\d*$', args.digits)):
        if (args.manual):
            changeNameHand(name2number(args.pathRootSrc, args.digits, args.extension))
        else:
            name2number(args.pathRootSrc, args.digits, args.extension)
    else:
        print("入力値: %s ※連番桁の値が不正です 複数の桁数について処理するときはカンマ区切りで入力してください（例 3,5 -> 3桁と5桁を処理）" % args.digits)
        sys.exit(1)
    
    if (args.before != None or args.after != None):
        addstr(args.before, args.after, args.digits, args.extension)
    if (args.pdf != None):
        image2pdf(args.pdf, args.digits, args.extension, False)
    if (args.pdfRemoveImage != None):
        image2pdf(args.pdf, args.digits, args.extension, True)
    if (args.zip != None):
        makeZip(args.zip, False)
    if (args.zipRemoveFiles != None):
        makeZip(args.zipRemoveFiles, True)

def name2number(folderpass, digits, extension):
    u"""    
    ゴミ文字列を取り除き連番のみのファイル名にする関数
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
            maxdigit = max(map(int,(digits.split(","))))          
            newname = num.group().zfill(maxdigit) + extension # 連番名作成
            oldname = str(file)
            if (ext.search(file) and num):
                if os.path.isfile(newname): # 他の連番ファイルの有無を確認
                    print("ファイル名%sが存在するため%sは書き換えません" % (newname, oldname))
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
    file一覧のリストを引数とし、それらのファイル名を標準入力から読み込み書き換える関数
    """ 
    
    print("----------------------------------------------------")
    print("連番が被ったファイル名を手動で決定します\n")    
    for file in existfiles:
        print("ファイル名: %s を書き換えますか? (y/n/r)" % str(file))
        flug = input()
        if (flug == "y" or flug == "Y"):
            print("新しいファイル名を入力して下さい %s =>" % str(file))
            newname = input()
            while(os.path.isfile(newname)): # 被らないファイル名が指定されるまでループ ToDo:上書きモード作成
                print("既にファイル %s が存在しています　別の名前を指定して下さい %s => ?" % (newname, str(file)))
                newname = input()
            os.rename(file, newname)
            print("書き換え: %s => %s \n" % (str(file), newname))
        elif (flug == "r"):
            print("ファイル %s を削除します　よろしいですか? (y/n/c)" % str(file)) # y="Yes" n="No" c="check"
            flug = input()
            if (file[:-4] == ".jpg" or ".png" or ".gif"):
                if (flug == "c"):
                    d1 = PIL.Image.open(file) # 画像ファイルを開いて表示
                    d1.show()
            print("ファイル %s を削除します　本当によろしいですか? (y/n/r)" % str(file))
            flug = input()
            if (flug == "Y" or flug == "y"):
                os.remove(file)
                print("ファイル %sを削除しました" % file)
            elif (flug == "r"):
                print("リネームします。新しい名前を入力して下さい %s =>" % str(file))
                newname = input()
                while(os.path.isfile(newname)): # 被らないファイル名が指定されるまでループ ToDo:上書きモード作成
                    print("既にファイル %s が存在しています　別の名前を指定して下さい %s => ?" % (newname, str(file)))
                    newname = input()
                os.rename(file, newname)
                print("書き換え: %s => %s \n" % (str(file), newname))                
            else:
                print("ファイル %s はそのままにします\n" % str(file))
        else:
            print("%s はそのままにします \n" % str(file))
    print("全てのファイルの書き換えが終了しました\n")
    
def addstr(before, after, digits, extension):
    u"""    
    指定された文字列を連番の前または後ろにくっつける関数
    """ 
    print("----------------------------------------------------")
    files = os.listdir()
    ext = re.compile(extension) 
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
                center, e = str(file).split(".") # ファイル名を実と拡張子部分にわける
                newname = before + center + after + extension
                oldname = str(file)
                if (num):
                    if os.path.isfile(newname):
                        pass
                    else:
                        os.rename(file, newname)
                        print("書き換え: %s => %s" %(oldname, newname))   
    return None

def image2pdf(filename, digits, extension, removeflug):
    u"""
    画像ファイルをPDF化する関数
    """
    if (extension != ".jpg" and ".png" and ".gif"): # 画像じゃない場合弾く
        print("対応外の画像ファイル！ jpg, png, gifでオナシャス")
        sys.exit(1)
    
    fileWriter = PdfFileWriter()
    files = os.listdir()
    ext = re.compile(extension)
    files.sort()
    count = 1
    removefiles = []
    for file in files:
        num = re.search('\\d{' + str(digits) +'}', file)
        if (num == None):
            pass
        else:
            if (ext.search(file) and num):
                image = PIL.Image.open(file)
                pdfFile = str(file).replace(extension, ".pdf")
                image.save(pdfFile, "PDF", resolution = 100.0)
                with open(pdfFile, "rb") as f:
                    fileReader = PdfFileReader(f, "rb")
                    pageNum = fileReader.getNumPages()
                    for i in range(pageNum):
                        fileWriter.addPage(fileReader.getPage(i))
                        print("%s を%d ページ目に書き込みます" % (str(file), count))
                        count += 1
                    removefiles.append(pdfFile)
                    if (removeflug):
                        removefiles.append(file)
                    with open(filename, "wb") as outputs:
                        fileWriter.write(outputs)
    print("-------------------------------------------------------")
    print("書き込み終了！ ファイル名 %s \n" % filename)
    
    for file in removefiles:
        os.remove(file)
        print("ファイル名　%sを削除しました" % str(file))
    
    print("--------------------------------------------------------")
    print("終わり！成果物: %s" % filename)
    return None

def makeZip(filename, flug):
    """
    zipアーカイブを作る関数
    """
    files = os.listdir()
    count = 0
    zips = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    for file in files:
        zips.write(file)
        print("ファイル名 %s をzipアーカイブに追加しました" % str(file))
        count += 1
        if (flug):
            os.remove(file)
            print("ファイル名 %s を削除しました" % str(file))
    zips.close()
    print("---------------------------------------------------------")
    print("終わり！　成果物: %s" % str(filename))
    
if __name__ == "__main__":
    main()
