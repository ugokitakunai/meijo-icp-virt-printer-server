## インストール方法
1. Releaseから`Installer.exe`をダウンロード  
2. 実行  
3. インストール完了後、プリンター一覧に **Meijo ICP Virtual Printer** が表示されていることを確認

## 印刷設定について
  Wordなどにある印刷設定はpdfを作成するために使用されるだけで、In Campus Printやこれには反映されません。
  例えば、Wordで部数: 5に指定した場合、5ページのpdfファイルが作成されIn Campus Printに送信されます。
  その場合、In Campus Print上では部数:1, ページ数:5と表示されます。
  
  4 in 1などの設定はどちらか片方だけ設定するようにしてください。実験していませんがおそらく16 in 1のページが出力されます。

## トラブルシューティング

- **Can't not load DLL等のエラーが発生 / 印刷の設定画面が出てこない**
  Visual C++ 再頒布可能パッケージをインストールしてください
  [配布サイト](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist?view=msvc-170)

- **ポートが不明のエラーが出てインストールできない**  
  Windowsの言語設定が日本語以外の場合にエラーが出ることがあります。  
  コマンドプロンプトで以下を実行すると手動でインストール可能です
    ```cmd
    cscript "C:/Windows/System32/Printing_Admin_Scripts/en-US/prnport.vbs" -a -r "Meijo ICP Virtual Printer Port" -h "127.0.0.1" -n 9101 -o raw
    rundll32 printui.dll,PrintUIEntry /if /b "Meijo ICP Virtual Printer" /r "Meijo ICP Virtual Printer Port" /m "Microsoft PS Class Driver"
    ```

- **別のフォルダにインストールしたい**  
  Startupフォルダのリンク先(`%UserProfile%/AppData/Local/MeijoPrintService/python/Scripts/python.exe`)だけ変更すれば自由にフォルダは移動できます。  
  インストーラーは現時点では対応していません（そのうち対応予定です）。
  Tempフォルダではなく`print_server.py`があるフォルダに一時ファイルを作成するため書き込みできないフォルダに移動すると使用できなくなります(修正予定)

## アンインストール方法

1. Startupフォルダから該当ショートカットを削除  
2. PCを再起動  
3. `C:/Users/<USERNAME>/AppData/Local/MeijoPrintService` を削除  
4. Windowsの設定から **Meijo ICP Virtual Printer** を削除

## 免責

このソフトウェアは無保証です。本ソフトウェアは現状のまま提供されます。  
システムのアップデートなどにより動作しなくなる可能性があります。  
名城大学はこのプロジェクトに関わっていません。  
本ソフトウェアの使用または使用不能により発生したいかなる損害についても、作者は一切の責任を負いません。

## Special Thanks

- [virtualPrinter](https://github.com/TheHeadlessSourceMan/virtualPrinter)  
- [GhostScript](https://ghostscript.com/)