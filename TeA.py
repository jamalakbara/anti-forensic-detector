import subprocess
import os
import pandas as pd
import re

try:
    BASE_DIR = os.getcwd()
    os.chdir("platform-tools")
except FileNotFoundError:
    print("""
    ===================GAADA FOLDER PLATFORM-TOOLS===================
   ===================EXTRACT DULU KE DIRECTORY INI===================""")
else:
    if not os.path.exists(os.path.join(BASE_DIR, "hasil_backup")):
        os.mkdir(os.path.join(BASE_DIR, "hasil_backup"))

    if not os.path.exists(os.path.join(BASE_DIR, "list_package")):
        os.mkdir(os.path.join(BASE_DIR, "list_package"))

    namaBckup = input("Masukin nama file backup : ")

    print("""
    ===================Tunggu Sebentar Lagi Nge-Backup Nanti Juga Beres===================
         ===================Oiya Jangan Dicabut Hp-nya Nanti Error===================""")
    print()

    adbCmd = subprocess.run(f"adb backup -apk -shared -all -f ../hasil_backup/{namaBckup}.ab", shell=True)

    if adbCmd.returncode == 0:
        if os.path.exists(f"../hasil_backup/{namaBckup}.ab"):
            print("""
               ===================Tunggu Sebentar Lagi Buat List Package===================
            ===================Oiya Jangan Dicabut Lagi Hp-nya Nanti Error===================""")
            adbCmd = subprocess.run(f"adb shell pm list package > ../list_package/list.txt", shell=True)
            print()
            os.chdir("../")
            if os.path.exists("list_package/list.txt"):
                listPackage = pd.read_excel("data_set/list package.xlsx")

                packages = pd.read_csv("list_package/list.txt", delimiter=" ", header=None)
                packages.rename(columns={
                    0: "Nama Package"
                }, inplace=True)

                dict_app = {
                    "Nama App": list(),
                    "Nama Package": list()
                }
                for index in packages.index:
                    cek = re.search(r"package:(\w+\..+)", packages.loc[index, "Nama Package"])
                    for i in listPackage.index:
                        try:
                            if cek.group(1).strip() == listPackage.loc[i, "package"].strip():
                                dict_app["Nama App"].append(listPackage.loc[i, "name apk"].strip())
                                dict_app["Nama Package"].append(listPackage.loc[i, "package"].strip())
                        except AttributeError:
                            pass
                else:
                    tabel_list_app = pd.DataFrame(dict_app)
                    print()
                    print("===================Tabel List Aplikasi Anti Forensik===================")
                    print(tabel_list_app)

                    if os.path.exists("C:\Program Files (x86)\Oxygen Forensics"):
                        os.chdir("C:\Program Files (x86)\Oxygen Forensics\Oxygen Forensic Detective\OFD12")
                        startOxy = subprocess.run(["start", "OxyDetective.exe"], shell=True)
                        if startOxy.returncode == 0:
                            print()
                            print("===================Membuka Oxygen Detective Forensic===================")
                            print()
                    else:
                        print("===================Oxygen Detective Forensic Tidak Ditemukan===================")
            else:
                print("===================Gagal Bikin List===================")

        else:
            print("===================Gagal Backup===================")

