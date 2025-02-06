import argparse
from utils.commands import run_cmd
from utils.logger import Print
from utils.debug import Debug

def main():
    parser = argparse.ArgumentParser(description="Arch Customizer: customize Arch Linux")
    parser.add_argument("-d", "--debug", action="store_true", help="show debug information")
    parser.add_argument("-r", "--reboot", action="store_true", help="reboot the system after installation")
    args = parser.parse_args()

    if args.debug:
        Debug.DEBUG = True

        

    Print.success("Installation complete\n")

    if args.reboot:
        Print.info("Rebooting...")
        run_cmd("reboot")

if __name__ == "__main__":
    main()