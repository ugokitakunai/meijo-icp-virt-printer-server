import cryptography.fernet
import customtkinter as ctk
from tkinter import messagebox
import asyncio
from cryptography.fernet import Fernet
import win32crypt
import cryptography

# 暗号化キー
with open("fernet_key.dat", "rb") as f:
    encrypted_key = f.read()
key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
cipher = Fernet(key)

# ログイン
class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to_main):
        super().__init__(master)
        master.title("ログイン")
        self.label = ctk.CTkLabel(self, text="メイネットIDでログイン")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="ユーザー名")
        self.entry.pack(pady=10)
        self.entry_password = ctk.CTkEntry(self, placeholder_text="パスワード", show="*")
        self.entry_password.pack(pady=10)

        self.button = ctk.CTkButton(self, text="ログイン", command=lambda: switch_to_main(id=self.entry.get(), password=self.entry_password.get()))
        self.button.pack(pady=10)


# ログイン後の印刷設定
class PrintFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # ログイン中のアカウントを表示
        account_frame = ctk.CTkFrame(self, fg_color="transparent")
        account_frame.pack(fill="both", anchor="nw")

        self.label = ctk.CTkLabel(account_frame, text=f"ログイン中: {master.id}")
        self.label.pack(anchor="w")

        self.button = ctk.CTkButton(account_frame, text="アカウントを切り替え", command=self.logout)
        self.button.pack(anchor="w", pady=(2, 0))


        # 印刷設定
        # 用紙
        paper_frame = ctk.CTkFrame(self, fg_color="transparent")
        paper_frame.pack(pady=(20, 10), anchor="nw")

        paper_label = ctk.CTkLabel(paper_frame, text="用紙")
        paper_label.pack(side="left", padx=(0, 10))

        self.paper_select = ctk.CTkOptionMenu(paper_frame, values=["A4", "A3"])
        self.paper_select.pack(side="left")

        sides_frame = ctk.CTkFrame(self, fg_color="transparent")
        sides_frame.pack(pady=(0, 0), anchor="nw")

        # 印刷面(両面/片面)
        sides_label = ctk.CTkLabel(sides_frame, text="印刷面")
        sides_label.pack(side="left", padx=(0, 10))
        self.sides_select = ctk.CTkOptionMenu(sides_frame, values=["片面", "両面"])
        self.sides_select.pack(side="left")

        # レイアウト
        n_in_one_frame = ctk.CTkFrame(self, fg_color="transparent")
        n_in_one_frame.pack(pady=(10, 0), anchor="nw")
        n_in_one_label = ctk.CTkLabel(n_in_one_frame, text="レイアウト")
        n_in_one_label.pack(side="left", padx=(0, 10))
        self.n_in_one_select = ctk.CTkOptionMenu(n_in_one_frame, values=["1 in 1", "2 in 1", "4 in 1"])
        self.n_in_one_select.pack(side="left")

        # 綴じ方向
        binding_frame = ctk.CTkFrame(self, fg_color="transparent")
        binding_frame.pack(pady=(10, 0), anchor="nw")
        binding_label = ctk.CTkLabel(binding_frame, text="綴じ方向")
        binding_label.pack(side="left", padx=(0, 10))
        self.binding_select = ctk.CTkOptionMenu(binding_frame, values=["長辺", "短辺"])
        self.binding_select.pack(side="left")

        # 向き
        direction_frame = ctk.CTkFrame(self, fg_color="transparent")
        direction_frame.pack(pady=(10, 0), anchor="nw")
        direction_label = ctk.CTkLabel(direction_frame, text="印刷方向")
        direction_label.pack(side="left", padx=(0, 10))
        self.direction_select = ctk.CTkOptionMenu(direction_frame, values=["縦", "横"])
        self.direction_select.pack(side="left")

        # ボタンの追加
        self.print_button = ctk.CTkButton(self, text="印刷", command=self.get_settings)
        self.print_button.pack(pady=(20, 10), anchor="se")

    def get_settings(self):
        self.master.paper = self.paper_select.get()
        self.master.sides = self.sides_select.get()
        self.master.n_in_one = self.n_in_one_select.get()
        self.master.binding = self.binding_select.get()
        self.master.direction = self.direction_select.get()

        # GUIを終了して印刷処理を開始
        self.master.on_closing()

    def logout(self):   
        self.master.login_frame.pack(expand=True, fill="both")
        self.pack_forget()
        # credentials.keyを削除
        # ファイル自体削除してもいいけど空のバイトで上書きしてる
        with open("credentials.key", "wb") as f:
            f.write(b"")
        self.master.id = ""
        self.master.password = ""


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x350")
        self.title("ログイン")

        self.lift()
        self.attributes("-topmost", True) # 最前面に表示
        # なぜか裏に行くことが多かったので追加
        # TODO: 後で設定で変更できるようにする

        # credentials.keyが存在しない場合は作成する
        try: 
            with open("credentials.key", "rb") as f:
                encrypted_data = f.read().split(b'\n\n')
                if len(encrypted_data) == 2:
                    self.id = cipher.decrypt(encrypted_data[0]).decode()
                    self.password = cipher.decrypt(encrypted_data[1]).decode()
                else:
                    self.id = ""
                    self.password = ""
        except cryptography.fernet.InvalidToken:
            messagebox.showerror("エラー", "暗号化キーが無効です。再度ログインしてください。")
            self.id = ""
            self.password = ""
        except FileNotFoundError:
            with open("credentials.key", "wb") as f:
                f.write(b"")
            self.id = ""
            self.password = ""
        except Exception as e:
            messagebox.showerror("エラー", f"予期しないエラーが発生しました: {e}")
            self.destroy()

            
        self.attempt_frame = PrintFrame(self)
        self.login_frame = LoginFrame(self, self.login_attempt)
        if not self.id or not self.password:
            self.login_frame.pack(expand=True, fill="both")
        else:
            self.attempt_frame.pack(expand=True, fill="both")

    def on_closing(self):
        settings = {
            "paper": self.paper,
            "sides": self.sides,
            "n_in_one": self.n_in_one,
            "binding": self.binding,
            "direction": self.direction,
        }
        self.settings = settings
        self.destroy()

    def login_attempt(self, id, password):
        if not id or not password:
            messagebox.showerror("エラー", "ユーザー名とパスワードを入力してください。")
            return
        
        self.id = id
        self.password = password

        with open("credentials.key", "wb") as f:
            encrypted_id = cipher.encrypt(id.encode())
            encrypted_password = cipher.encrypt(password.encode())
            f.write(encrypted_id + b'\n\n' + encrypted_password)

        self.id = id
        self.password = password
        self.title = "印刷"  # TODO: なんか動かないので後で確認, 動作には問題ないのであとで
        # IDとかを正しく描画するために再定義
        self.attempt_frame = PrintFrame(self)
        self.login_frame.pack_forget()
        self.attempt_frame.pack(expand=True, fill="both")
        return


if __name__ == "__main__":
    ctk.set_appearance_mode("dark") 
    ctk.set_default_color_theme("dark-blue") 
    app = App()
    app.mainloop()
    print("アプリケーションを終了しました。")
