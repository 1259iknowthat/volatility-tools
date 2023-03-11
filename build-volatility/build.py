#!/usr/bin/python3
import argparse, subprocess, sys, os
import getpass, shutil

def check_volatility(vol_version): #check if volatility version are valid
    if (vol_version != "2" and vol_version != "3"):
        print("Invalid volatility version")
        print("Valid volatility versions are: 2 and 3")
        sys.exit()
        
def check_package(output, package):
    packages_list = [pkg.split(" - ")[0] for pkg in output.splitlines()]
    if package not in packages_list:
        print("Invalid package version. Package does not exist!")
        print("Package: {}".format(package))
        print("Example of a valid package version: 5.15.0-1032-realtime")
        sys.exit()
        
def check(package_version): #check if packages are valid
    linux_image = "linux-image-{}".format(package_version)
    linux_headers = "linux-headers-{}".format(package_version)
    output_image = subprocess.check_output(["/usr/bin/apt-cache", "search", linux_image], universal_newlines=True)
    output_headers = subprocess.check_output(["/usr/bin/apt-cache", "search", linux_headers], universal_newlines=True)
    check_package(output_image, linux_image)
    check_package(output_headers, linux_headers)
    
def get_user_password(): #get user password but don't show up on screen
    password = getpass.getpass(prompt="Enter your user password: ")
    return password

def before_reboot(vol_version, package_version, apt_install, install_folder):
    linux_version = "Linux {}".format(package_version)
    linux_image = "linux-image-{}".format(package_version)
    linux_headers = "linux-headers-{}".format(package_version)
    subprocess.check_call("{} {} {}".format(apt_install, linux_image, linux_headers), shell=True)
    rc_command = "echo 'cd {} && python3 build.py -vol {} -ver {}' >> ~/.bashrc".format(install_folder, vol_version, package_version)
    reboot_value = "echo 1 > ./reboot_value.temp"
    auto_open_term = "cp ./terminal.desktop ~/.config/autostart/"
    grub = "GRUB_CMDLINE_LINUX_DEFAULT='quiet splash'"
    auto_boot_version = 'echo "{} {}" | /usr/bin/sudo tee -a /etc/default/grub'.format(grub, linux_version)
    make_dir = "mkdir -p ~/.config/autostart"
    subprocess.check_call(rc_command, shell=True)
    subprocess.check_call(reboot_value, shell=True)
    subprocess.check_call(make_dir, shell=True)
    subprocess.check_call(auto_open_term, shell=True)
    subprocess.check_call(auto_boot_version, shell=True)
    os.system('sudo reboot -f')
    
def after_reboot(package_version, system_map, password):
    zip_file = "./output/Ubuntu_{}_profile.zip".format(package_version)
    build_args = ["cp", "-r", "./linux", "./linux-build", "&&", "cd", "./linux-build", "&&", "make"]
    zip_args = "echo {} | /usr/bin/sudo -S zip {} ./linux-build/module.dwarf {}".format(password, zip_file, system_map)
    remove_command = "sed -i '$d' {}"
    remove_file = "rm -f ~/.config/autostart/terminal.desktop"
    subprocess.check_call(" ".join(build_args), shell=True)
    subprocess.check_call(zip_args, shell=True)

    #clear temp files and commands
    subprocess.check_call(remove_command.format("~/.bashrc"), shell=True)
    shutil.rmtree("./linux-build") 
    os.remove("./reboot_value.temp")
    subprocess.check_call(remove_file, shell=True)
    
def build(vol_version, package_version):
    password = get_user_password()
    apt_install = "/bin/echo {} | /usr/bin/sudo -S /usr/bin/apt install -y".format(password)
    system_map = "/boot/System.map-{}".format(package_version)
    current_file_path = os.path.abspath(__file__)
    install_folder = (current_file_path.split("/"))
    del install_folder[len(install_folder)-1]
    install_folder = "/".join(install_folder)
    if (vol_version == '2'): #volatility 2 profile
        temp_file = "{}/reboot_value.temp".format(install_folder)        
        value = open(temp_file , 'r').readlines()[0].strip() if os.path.isfile(temp_file) else '0'
        if value == '0':
            before_reboot(vol_version, package_version, apt_install, install_folder)
        else:
            after_reboot(package_version, system_map, password)
    elif (vol_version == '3'): #volatility 3 symbolic
        linux_dgbsym = "linux-image-{}-dbgsym".format(package_version)
        vmlinux = "/usr/lib/debug/boot/vmlinux-{}".format(package_version)
        json_file = "./output/vmlinux-{}.json".format(package_version)
        dwarf_args = ["/usr/bin/sudo","./dwarf2json", "linux", "--system-map", system_map, "--elf", vmlinux, ">", json_file]
        add_apt_source = """
            echo "deb http://ddebs.ubuntu.com $(lsb_release -cs) main restricted universe multiverse
deb http://ddebs.ubuntu.com $(lsb_release -cs)-updates main restricted universe multiverse
deb http://ddebs.ubuntu.com $(lsb_release -cs)-proposed main restricted universe multiverse" | \
sudo tee /etc/apt/sources.list.d/ddebs.list
        """
        update_apt_source = """
            sudo apt install ubuntu-dbgsym-keyring &&
            sudo apt-get update
        """
        subprocess.check_call(add_apt_source, shell=True)
        subprocess.check_call(update_apt_source, shell=True)
        subprocess.check_call("{} {}".format(apt_install, linux_dgbsym), shell=True)
        subprocess.check_call(" ".join(dwarf_args), shell=True)
        
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-vol", "--volatility", metavar="<version>", help="Version of Volatility", required=True)
    parser.add_argument("-ver", "--version", metavar="<version>", help="Version of linux headers/image package", required=True)
    args = parser.parse_args()
    vol_version = args.volatility
    package_version = args.version
    check_volatility(vol_version)
    check(package_version)
    build(vol_version, package_version)
    
if __name__=="__main__":
    main()