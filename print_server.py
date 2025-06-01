import socket, atexit, subprocess, asyncio, os, uuid
from printer_manager import install_printer, uninstall_printer
from tkinter import messagebox
import check_update
import json

from get_settings import get_settings
app_settings = get_settings()

outdated = False

if app_settings.get("version_check", True):
    if check_update.check_update():
        outdated = True
    else:
        outdated = False

printer_name = "Meijo ICP Virtual Printer"
printer_port_name = "Meijo ICP Virtual Printer Port"

def _uninstall_printer() -> None:
    try:
        uninstall_printer(printer_name, printer_port_name)
    except Exception as e:
        print(f"Error uninstalling printer: {e}")

def _install_printer() -> None:
    try:
        install_printer(printer_name, printer_port_name)
    except Exception as e:
        print(f"Error installing printer: {e}")

async def run_print_server():
    print(f"Print server running with printer '{printer_name}' on port '{printer_port_name}'.")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 9101))

    ip, port = s.getsockname()
    print(f"Print server listening on {ip}:{port}")

    s.listen(1)
    loop = asyncio.get_event_loop()
    s.setblocking(False)
    try:
        while True:
            print("Waiting for a connection...")
            conn, addr = await loop.sock_accept(s)
            asyncio.create_task(handle_client(conn, addr))


    except KeyboardInterrupt:
        print("Shutting down print server.")
    finally:
        s.close()

async def _ps_to_pdf(filename):
    id = str(uuid.uuid4())
    subprocess.run(["./bin/gswin64c.exe", "-dNOPAUSE", "-dBATCH",
                    "-sDEVICE=pdfwrite", f"-sOutputFile={id}.pdf", filename],
                   check=True)
    os.remove(filename)
    return id + ".pdf"

async def webprint():
    import sslvpn
    sslvpn.do_print_icp("")
        

async def handle_client(conn, addr):
    global outdated # UnboundLocalErrorの対処

    print(f"Connection from {addr}")
    with open("icp_data.ps", "wb") as f:
        while True:
            try:
                data = await asyncio.get_event_loop().sock_recv(conn, 1024)
            except ConnectionResetError:
                break
            if not data:
                break
            f.write(data)
        print("Data saved to 'icp_data.ps'")
    conn.close()
    filename = await _ps_to_pdf(filename="icp_data.ps")
    if outdated:
        messagebox.showinfo("Info", "新しいバージョンがリリースされました。\nアップデートをおすすめします。")
        outdated = False # 何回も出ると鬱陶しいので1起動ごとに一回
        return
    import gui
    app = gui.App()
    app.mainloop()

    if not app.success:
        if os.path.exists(filename): # 例外発生防止のif
            os.remove(filename)
        return
    
    settings = app.settings

    import sslvpn

    try:
        await sslvpn.do_print_icp(
            job_id="VirtualPrinterJob",
            userid=app.id,
            password=app.password,
            file_name=filename,
            settings=settings
        )
    except Exception as e:
        messagebox.showerror("Error", f"プリントに失敗しました: {e}\nID, パスワードが正しいか確認してから再度印刷してください。")
    finally:
        if os.path.exists(filename):
            os.remove(filename)


async def main():
    try:
        await run_print_server()
    except Exception as e:
        print(f"Error in print server: {e}")

asyncio.run(main())
