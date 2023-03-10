#!/usr/bin/python3
import argparse, subprocess, sys
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
    linux_image = "linux-image-" + package_version
    linux_headers = "linux-headers-" + package_version
    output_image = subprocess.check_output(["/usr/bin/apt-cache", "search", linux_image], universal_newlines=True)
    output_headers = subprocess.check_output(["/usr/bin/apt-cache", "search", linux_headers], universal_newlines=True)
    check_package(output_image, linux_image)
    check_package(output_headers, linux_headers)
    
def get_user_password(): #get user password but don't show up on screen
    password = getpass.getpass(prompt="Enter your user password: ")
    return password

def build(vol_version, package_version):
    password = get_user_password()
    
    if (vol_version == '2'): #volatility 2 profile
        linux_image = "linux-image-" + package_version
        linux_headers = "linux-headers-" + package_version
        system_map = "/boot/System.map-" + package_version
        apt_install = ["/usr/bin/echo", password, "|" ,"/usr/bin/sudo", "-S", "/usr/bin/apt", "install", "-y"]
        zip_file = "./output/Ubuntu_" + package_version + "_profile.zip"
        zip_args = ["/usr/bin/sudo", "zip", zip_file, "./linux-build/module.dwarf", system_map]
        copy_args = ["cp", "-r", "./linux", "./linux-build", "&&", "cd", "./linux-build", "&&", "make"]
        subprocess.check_call([" ".join(apt_install), linux_image, linux_headers], shell=True)
        subprocess.check_call(" ".join(copy_args), shell=True)
        subprocess.check_call(" ".join(zip_args), shell=True)
        shutil.rmtree("./linux-build") #clear temp file
    
    elif (vol_version == '3'): #volatility 3 symbolic
        linux_dgbsym = "linux-image-" + package_version + "-dbgsym"
        system_map = "/boot/System.map-" + package_version
        vmlinux = "/usr/lib/debug/boot/vmlinux-" + package_version
        json_file = "./output/vmlinux-" + package_version + ".json"
        apt_install = ["/usr/bin/echo", password, "|" ,"/usr/bin/sudo", "-S", "/usr/bin/apt", "install", "-y"]
        dwarf_args = ["/usr/bin/sudo","./dwarf2json", "linux", "--system-map", system_map, "--elf", vmlinux, ">", json_file]
        subprocess.check_call([" ".join(apt_install), linux_dgbsym], shell=True)
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