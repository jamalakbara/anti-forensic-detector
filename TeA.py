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
    if not os.path.exists(os.path.join(BASE_DIR, "list_package")):
        os.mkdir(os.path.join(BASE_DIR, "list_package"))

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
        listApp_list = list()
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
            print("""
            TABEL LIST APP ANTI FORENSIK
            """)
            print(tabel_list_app)
    else:
        print("===================Gagal Bikin List===================")

    backupStat = False
    while not backupStat:
        if not os.path.exists(os.path.join(BASE_DIR, "hasil_backup")):
            os.mkdir(os.path.join(BASE_DIR, "hasil_backup"))
            print("""
                ===================Belum Pernah Backup Data. Silakan Backup Dulu!!===================
                """)
            namaBckup = input("Masukin nama file backup : ")

            print("""
                ===================Tunggu Sebentar Lagi Nge-Backup Nanti Juga Beres===================
                     ===================Oiya Jangan Dicabut Hp-nya Nanti Error===================""")
            print()

            os.chdir("platform-tools")

            adbCmd = subprocess.run(f"adb backup -apk -shared -all -f ../hasil_backup/{namaBckup}.ab", shell=True)

            if adbCmd.returncode == 0:
                backupStat = True
                print("===================BACKUP BERHASIL===================")
        else:
            listDir = os.listdir(os.path.join(BASE_DIR, "hasil_backup"))
            for dir in listDir:
                cekFile = re.search(r"(\w+)\.ab", dir)
                if cekFile:
                    namaBckup = cekFile.group(1)
                    backupStat = True
                    print("""
                        ===================Sudah Pernah Backup Data===================
                        """)
                    os.chdir("platform-tools")

    if os.path.exists("C:\Program Files (x86)\Java"):
        for dir in os.listdir("C:\Program Files (x86)\Java"):
            if "jre" in dir:
                jre = re.search(r"(jre.*)", dir)
                jreFolder = jre.group(1)

                javaExec = os.path.join("C:\Program Files (x86)\Java", jreFolder, "bin", "java.exe")
        else:
            os.chdir("../")
            if os.path.exists("android-backup-extractor"):
                listDir = os.listdir(os.path.join(BASE_DIR, "hasil_backup"))
                tarStat = False
                for dir in listDir:
                    cekFile = re.search(r"(\w+)\.tar", dir)
                    if cekFile:
                        namaBckup = cekFile.group(1)
                        tarStat = True
                        print("""
                        ===================Sudah Pernah Backup Data===================
                        """)

                if tarStat == False:
                    print("===================Tunggu Sebentar Lagi Bikin .tar===================")
                    extract = subprocess.run(
                        f'"{javaExec}" -jar "android-backup-extractor\\abe.jar" unpack "hasil_backup/{namaBckup}.ab" "hasil_backup/{namaBckup}.tar"',
                        shell=True)
                    if extract.returncode == 0:
                        print()
                        print("===================Bikin .tar Beres===================")

                os.chdir("hasil_backup")
                print()
                print("===================Tunggu Sebentar Lagi Ngekstrak===================")
                if os.path.exists("C:\Program Files\WinRAR"):
                    for pck in dict_app["Nama Package"]:
                        ngekstrak = subprocess.run(
                            f'"C:\Program Files\WinRAR\WinRAR.exe" x -ibck {namaBckup}.tar *"apps\{pck}\"*', shell=True)
                    else:
                        subprocess.run(
                            f'"C:\Program Files\WinRAR\WinRAR.exe" x -ibck {namaBckup}.tar *"shared\"*', shell=True)
                    # if ngekstrak.returncode == 0:
                    #     print()
                    #     print("===================Ngekstrak Beres===================")
                else:
                    print()
                    print("===================INSTALL WINRAR DULU SANA!!!===================")
            else:
                print("===================GAADA FOLDER 'android-backup-extractor'===================")
    else:
        print("===================Belom Install Java===================")