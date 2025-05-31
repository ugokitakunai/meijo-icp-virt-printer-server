インストール方法
1. ReleaseからInstaller.exeをダウンロード
2. 実行
3. インストール完了後プリンター一覧にMeijo ICP Virtual Printerが表示されていることを確認

トラブルシューティング
・ポートが不明のエラーが出てインストールできない
Windowsの言語設定が日本語以外の場合にエラーが出る場合があります。
コマンドプロンプトで
cscript "C:/Windows/System32/Printing_Admin_Scripts/en-US/prnport.vbs" -a -r "Meijo ICP Virtual Printer Port" -h "127.0.0.1" -n 9101 -o raw
rundll32 printui.dll,PrintUIEntry /if /b "Meijo ICP Virtual Printer" /r "Meijo ICP Virtual Printer Port" /m "Microsoft PS Class Driver"
を実行すると手動でインストールできます。

・別のフォルダにインストールしたい
Startupのリンク先だけ変えてもらえれば自由にフォルダは動かせます。
インストーラーは対応していません(そのうち対応する予定です)

アンインストール方法
1. Startupフォルダから削除
2. 再起動
3. C:/Users/<USERNAME>/AppData/Local/MeijoPrintServiceを削除
4. Windowsの設定からMeijo ICP Virtual Printerを削除

免責: 
このソフトウェアは無保証です。本ソフトウェアは現状のまま提供されます。
システムのアップデートなどにより動作しなくなる可能性があります。
名城大学はこのプロジェクトに関わっていません。本ソフトウェアの使用または使用不能により発生したいかなる損害についても、作者は一切の責任を負いません。

