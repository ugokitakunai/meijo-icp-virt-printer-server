import subprocess

def _port_remove(printer_port_name: str) -> None:
    cmd = [
        "cscript", r"C:/Windows/System32/Printing_Admin_Scripts/ja-JP/prnport.vbs",
        "-d", "-r", printer_port_name
           ]
    with subprocess.Popen(cmd, stdin=None, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True) as p:
        stdout, _ = p.communicate()

    return stdout

def _printer_remove(printer_name: str) -> None:
    cmd = [
        "rundll32", "printui.dll,PrintUIEntry",
        "/dl", "/n", printer_name
    ]
    with subprocess.Popen(cmd, stdin=None, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True) as p:
        stdout, _ = p.communicate()

    return stdout

def _add_printer_port(printer_port_name) -> None:
    cmd = [
        "cscript",
        r"C:/Windows/System32/Printing_Admin_Scripts/ja-JP/prnport.vbs",
        "-a", "-r", printer_port_name, "-h", "127.0.0.1", "-n", "9101", "-o", "raw"
    ]
    with subprocess.Popen(cmd, stdin=None, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True) as p:
        stdout, _ = p.communicate()

def _add_printer(printer_name, printer_port_name) -> None:
    cmd = [
        "rundll32", "printui.dll,PrintUIEntry",
        "/if", "/b", printer_name,
        "/r", printer_port_name, "/m", "Microsoft Print To PDF"
    ]
    with subprocess.Popen(cmd, stdin=None, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True) as p:
        stdout, _ = p.communicate()

def install_printer(printer_name: str = "Meijo ICP Virtual Printer", printer_port_name: str = "Meijo ICP Virtual Printer Port") -> None:
    if printer_exists(printer_name):
        print(f"Printer '{printer_name}' already exists. Uninstalling.")
        uninstall_printer(printer_name, printer_port_name)

        if printer_exists(printer_name):
            print(f"Failed to uninstall printer '{printer_name}'.")
            return
    print("installing port")
    _add_printer_port(printer_port_name)
    print("installing printer")
    _add_printer(printer_name, printer_port_name)
    print(f"Printer '{printer_name}' installed with port '{printer_port_name}'.")

def uninstall_printer(printer_name: str = "Meijo ICP Virtual Printer", printer_port_name: str = "Meijo ICP Virtual Printer Port") -> None:
    _printer_remove(printer_name)
    _port_remove(printer_port_name)
    print(f"Printer '{printer_name}' and port '{printer_port_name}' removed.")

def printer_exists(printer_name: str) -> bool:
    try:
        result = subprocess.run(
            ["powershell", "-Command", f"Get-Printer -Name '{printer_name}'"],
            capture_output=True, text=True, check=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"プリンタ確認中にエラー: {e}")
        return False