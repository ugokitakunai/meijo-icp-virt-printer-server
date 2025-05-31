from printer_manager import install_printer

def _install_printer() -> None:
    try:
        install_printer(printer_name, printer_port_name)
    except Exception as e:
        print(f"Error installing printer: {e}")

printer_name = "Meijo ICP Virtual Printer"
printer_port_name = "Meijo ICP Virtual Printer Port"

if __name__ == "__main__":
    _install_printer()