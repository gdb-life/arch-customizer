import argparse
import json
import os
from utils.commands import run_cmd
from utils.logger import Print
from utils.debug import Debug

def install_yay():
    Print.info("Installing yay")
    run_cmd("git clone https://aur.archlinux.org/yay.git")
    os.chdir("yay/")
    run_cmd("makepkg -sirc --noconfirm")
    os.chdir("..")
    run_cmd("rm -rf yay")

def install_packages():
    Print.info("Installing packages")
    with open("packages.json", "r") as f:
        packages = json.load(f)
    for name, package in packages.items():
        Print.info(f"Installing {name}")
        run_cmd("yay -S --noconfirm " + " ".join(package))

def install_sddm():
    Print.info("Installing SDDM")
    run_cmd("sudo systemctl enable sddm")

def install_hyprland():
    Print.info("Installing hyprland")
    os.chdir(os.path.expanduser("~"))
    run_cmd("git clone https://github.com/gdb-life/arch-hyprland.git")
    os.chdir("arch-hyprland/")
    run_cmd("make")
    os.chdir("..")
    os.chdir("arch-customizer/")

def install_user_dirs():
    Print.info("Installing user dirs")
    config_file = os.path.expanduser("~/.config/user-dirs.dirs")
    user_dirs = {
        "XDG_DESKTOP_DIR": "$HOME/desktop",
        "XDG_DOWNLOAD_DIR": "$HOME/downloads",
        "XDG_DOCUMENTS_DIR": "$HOME/documents",
        "XDG_MUSIC_DIR": "$HOME/music",
        "XDG_PICTURES_DIR": "$HOME/pictures",
        "XDG_VIDEOS_DIR": "$HOME/videos",
        "XDG_TEMPLATES_DIR": "$HOME/templates",
        "XDG_PUBLICSHARE_DIR": "$HOME/public"
    }
    with open(config_file, "w") as f:
        for key, value in user_dirs.items():
            f.write(f'{key}="{value}"\n')

def install_zsh():
    Print.info("Installing zsh")
    os.chdir(os.path.expanduser("~"))
    run_cmd("sudo sed -i 's#^$(whoami):[^:]*:[^:]*:[^:]*:[^:]*:[^:]*:/.*#$(whoami):x:1000:1000::/home/$(whoami):/usr/bin/zsh#' /etc/passwd")
    
    run_cmd("sh -c \"$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\"")
    
    run_cmd("yay -S --noconfirm zsh-theme-powerlevel10k-git")
    run_cmd("echo 'source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme' >> ~/.zshrc")
    
    zsh_custom = os.path.expanduser("~/.oh-my-zsh/custom/plugins")
    run_cmd(f"git clone https://github.com/zsh-users/zsh-autosuggestions {zsh_custom}/zsh-autosuggestions")
    run_cmd(f"git clone https://github.com/zsh-users/zsh-syntax-highlighting.git {zsh_custom}/zsh-syntax-highlighting")
    
    zshrc_path = os.path.expanduser("~/.zshrc")
    with open(zshrc_path, "a") as f:
        f.write("\nplugins=(git sudo zsh-syntax-highlighting zsh-autosuggestions)\n")
    
    os.chdir(os.path.expanduser("~"))
    os.chdir("arch-customizer/")

def setup_sddm_autologin():
    Print.info("Setting up SDDM autologin")

    user = Print.input("Enter the username to autologin: ")
    session = Print.input("Enter the session to autologin: ")
    
    config_dir = "/etc/sddm.conf.d"
    config_file = os.path.join(config_dir, "autologin.conf")
    
    os.makedirs(config_dir, exist_ok=True)
    
    config_content = f"""
[Autologin]
User={user}
Session={session}
"""
    
    with open(config_file, "w") as f:
        f.write(config_content)

def setup_git():
    Print.info("Setting up git")
    name = Print.input("Enter your name: ")
    email = Print.input("Enter your email: ")
    run_cmd(f"git config --global user.name '{name}'")
    run_cmd(f"git config --global user.email '{email}'")
    
def main():
    parser = argparse.ArgumentParser(description="Arch Customizer: customize Arch Linux")
    parser.add_argument("-d", "--debug", action="store_true", help="show debug information")
    parser.add_argument("-r", "--reboot", action="store_true", help="reboot the system after installation")
    args = parser.parse_args()

    if args.debug:
        Debug.DEBUG = True

    install_yay()
    install_packages()
    install_sddm()
    install_hyprland()
    install_user_dirs()
    install_zsh()
    setup_sddm_autologin()
    setup_git()
    
    Print.success("Installation complete\n")

    if args.reboot:
        Print.info("Rebooting...")
        run_cmd("reboot")

if __name__ == "__main__":
    main()