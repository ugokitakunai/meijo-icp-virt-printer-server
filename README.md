# インストール方法

1. Releaseから`Installer.exe`をダウンロード  
2. 実行  
3. インストール完了後、プリンター一覧に **Meijo ICP Virtual Printer** が表示されていることを確認

# トラブルシューティング

- **ポートが不明のエラーが出てインストールできない**  
  Windowsの言語設定が日本語以外の場合にエラーが出ることがあります。  
  コマンドプロンプトで以下を実行すると手動でインストール可能です（コマンドは省略）。

- **別のフォルダにインストールしたい**  
  Startupフォルダのリンク先だけ変更すれば自由にフォルダは移動できます。  
  インストーラーは現時点では対応していません（そのうち対応予定です）。

# アンインストール方法

1. Startupフォルダから該当ショートカットを削除  
2. PCを再起動  
3. `C:/Users/<USERNAME>/AppData/Local/MeijoPrintService` を削除  
4. Windowsの設定から **Meijo ICP Virtual Printer** を削除

# 免責

このソフトウェアは無保証です。本ソフトウェアは現状のまま提供されます。  
システムのアップデートなどにより動作しなくなる可能性があります。  
名城大学はこのプロジェクトに関わっていません。  
本ソフトウェアの使用または使用不能により発生したいかなる損害についても、作者は一切の責任を負いません。

# Special Thanks

The implementation logic of this software was inspired by the open-source project:

- [virtualPrinter](https://github.com/TheHeadlessSourceMan/virtualPrinter)  
  A Python-based virtual printer using PostScript over a TCP socket.

No code was directly reused; the project was built from scratch based on original implementations.