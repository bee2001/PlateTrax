'''
MUHAMMAD ABIZAN PUTRA AMRAN | MUHAMMAD ABIZAN PUTRA AMRAN
50420776                    | 50420776
3IA06                       | 3IA06
SEMESTER 6                  | SEMESTER 6
ATA 2022/2023               | ACADEMIC YEAR 2022/2023
INFORMATIKA                 | INFORMATICS
FAKULTAS TEKNOLOGI INDUSTRI | INDUSTRIAL TECHNOLOGIES FACULTY
UNIVERSITAS GUNADARMA       | GUNADARMA UNIVERSITY

Note:
terpaksa menggunakan Pillow versi 9.5.0 karena Pillow versi 10.0.0 tidak ada Antialias yang dibutuhkan oleh pustaka
openCV
'''
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import easyocr
from datetime import datetime
from tkinter import messagebox, filedialog
import os
import csv

# Waktu dan tanggal.
now = datetime.now()
now2 = now.strftime("%Y/%m/%d %H:%M:%S")
date1 = now.strftime("%Y%m%d")

# Folder untuk menyimpan foto-foto nopol dan file CSV.
nopol_folder = f"Nopol_{date1}"
if not os.path.exists(nopol_folder):
    messagebox.showinfo("Info", f"Belum terbuat folder buat data nopol. Folder akan dibuat otomatis\nNama folder: {nopol_folder}")
    os.makedirs(nopol_folder)

# Membuka atau membuat file CSV.
csv_filename = f"PlateTrax_{date1}_mentahan.csv"
csv_file = os.path.join(nopol_folder, csv_filename)
if not os.path.isfile(csv_file):
    messagebox.showinfo("Info", f"Belum terbuat file buat data nopol. File akan dibuat otomatis\nNama file: {csv_filename}")
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nopol', 'Tanggal dan Waktu Masuk', 'Masuk/Keluar', 'Penghuni/Tamu'])

penghuniDB = 'Penghuni.csv'
# Memeriksa apakah ada database nopol penghuni dan adakah isinya
def read_csv_file(penghuniDB):
    if not os.path.isfile(penghuniDB):
        messagebox.showerror("Error", f"CSV file '{penghuniDB}' tidak ada. Aplikasi akan ditutup")
        exit()
        return

    with open(penghuniDB, 'r') as file:
        reader = csv.reader(file)
        header = next(reader, None)  # Get the header row
        if header is None:
            messagebox.showerror("Error", f"CSV file '{penghuniDB}' kosong atau tidak ada header. Aplikasi akan ditutup.")
            exit()
            return

        data = []
        for row in reader:
            if len(row) >= 1:
                data.append(row)

        if len(data) > 0:
            messagebox.showinfo("Info", f"CSV file '{penghuniDB}' ada data. Terdapat {len(data)} nopol terdaftar.")
            # Process the data as per your requirement
        else:
            messagebox.showinfo("Info", f"CSV file '{penghuniDB}' tidak ada data di bagian Nopol. Aplikasi akan ditutup.")
            exit()

# Cek jika penghuni apa tamu
def check_kalo_penghuni(input_value):
    with open(penghuniDB, 'r') as filePhn:
        reader = csv.reader(filePhn)
        next(reader)  # Skip the header row

        for row in reader:
            if input_value == row[0]:
                return True

    return False

# Boilerplate untuk widget Informasi.
Lorem_Ipsum = ("Foto Terekam\nMemroses......\nTerekam:\nB9999XXX\n" + now2 + "\nMasuk")

def bikinWidget():
    # Buat widgetnya.

    root.labelKamera = Label(root, bg="gray17", fg="white", text="Masukan Kamera", font=('Helvetica', 20))
    root.labelKamera.grid(row=1, column=1, padx=20, pady=10, columnspan=2)

    root.cameraLabel = Label(root, bg="black", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    root.tombolMSK = Button(root, text="Masuk", command=masuk, bg="light grey", font=('Consolas', 15),width=20)
    root.tombolMSK.grid(row=4, column=1, padx=10, pady=10)

    root.tombolKLR = Button(root, text="Keluar", command=keluar, bg="light grey", font=('Consolas', 15),width=20)
    root.tombolKLR.grid(row=4, column=2, padx=10, pady=10)

    root.Informasi = Text(root,height=8, width=40, bg="light grey", font=('Consolas', 15))
    root.Informasi.insert(END, "Menunggu input")
    root.Informasi.configure(state=DISABLED)
    root.Informasi.grid(row=2, column=3, padx=10, pady=10)

    read_csv_file(penghuniDB)
    Tampilan()

def Tampilan():
    try:
        # Merekam frame per frame.
        ret, frame = root.cap.read()

        if ret:
            # Memutar balik frame secara vertikal.
            frame = cv2.flip(frame, 1)

            # Menampilkan waktu dan tanggal
            cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                        (0, 255, 255))

            # Mengganti warna frame dari BGR ke RGB.
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            # Membuat memori gambar dari frame di atas dengan menggunakan antarmuka array.
            videoImg = Image.fromarray(cv2image)

            # Membuat objek kelas PhotoImage() untuk menampilkan frame.
            imgtk = ImageTk.PhotoImage(image=videoImg)

            # Mengkonfigurasikan label agar menampilkan frame.
            root.cameraLabel.configure(image=imgtk)

            # Menyimpan referensi.
            root.cameraLabel.imgtk = imgtk

            # Memanggil fungsi setelah 10 milidetik
            root.cameraLabel.after(10, Tampilan)
        else:
            # Mengkonfigurasikan label agar menampilkan frame.
            root.cameraLabel.configure(image='')

    except Exception as e:
        import traceback
        print(traceback.format_exc())

def masuk():
    root.Informasi.configure(state=NORMAL)
    root.Informasi.delete(1.0, END)
    root.Informasi.insert(END, "Foto Terekam\n")
    root.Informasi.insert(END, "Memroses......\n")
    # ketika tombol masuk dipencet
    nowM = datetime.now()
    nowM2 = nowM.strftime("%Y%m%d_%H%M%S")
    nowM3 = nowM.strftime("%Y/%m/%d %H:%M:%S")
    camM = root.cap
    ret, imgM = camM.read()
    fotoMasuk = os.path.join(nopol_folder, f"nopol_{nowM2}.jpg")
    cv2.imwrite(fotoMasuk, imgM)
    print(fotoMasuk)
    print('FOTO TERTANGKAP')
    # Mulai baca nopol
    print('MEMROSES.......')
    readerM = easyocr.Reader(['en'])
    bacaM = readerM.readtext(fotoMasuk, detail=0)
    bacaM2 = bacaM[:3]
    bacaM3 = ''.join(bacaM2)
    print(bacaM)
    print(bacaM3)
    print(nowM3)
    # memeriksa jika adakah nopol atau tidak serta memasuki nopol ke file CSV
    if len(bacaM3) > 0 :
        if check_kalo_penghuni(bacaM3):
            with open(penghuniDB, 'r') as filePhn:
                reader = csv.DictReader(filePhn)
                for row in reader:
                    if row['NOPOL'] == bacaM3:
                        penghuni_data = row['PENGHUNI']
                        alamat_data = row['ALAMAT']
                        break
            with open(csv_file,'a',newline='') as fileM:
                writer = csv.writer(fileM)
                writer.writerow([bacaM3, nowM3, 'MASUK', penghuni_data])
            root.Informasi.insert(END, "Terekam: \n")
            root.Informasi.insert(END, f"{bacaM3}\n")
            root.Informasi.insert(END, f"{nowM3}\n")
            root.Informasi.insert(END, f"{penghuni_data}\n")
            root.Informasi.insert(END, f"{alamat_data}\n")
            root.Informasi.insert(END, "Masuk")
            root.Informasi.configure(state=DISABLED)
            print('TEREKAM!(PENGHUNI)')
        else:
            with open(csv_file,'a',newline='') as fileM:
                writer = csv.writer(fileM)
                writer.writerow([bacaM3, nowM3, 'MASUK', 'TAMU'])
            root.Informasi.insert(END, "Terekam: \n")
            root.Informasi.insert(END, f"{bacaM3}\n")
            root.Informasi.insert(END, f"{nowM3}\n")
            root.Informasi.insert(END, "Tamu\n")
            root.Informasi.insert(END, "Masuk")
            root.Informasi.configure(state=DISABLED)
            print('TEREKAM!(TAMU)')

    else:
        print("TIDAK ADA NOPOL")
        print(readerM)
        root.Informasi.insert(END, "Tidak terdeteksi plat nomor\n")
        root.Informasi.insert(END, "Silahkan coba lagi")
        root.Informasi.configure(state=DISABLED)

def keluar():
    root.Informasi.configure(state=NORMAL)
    root.Informasi.delete(1.0, END)
    root.Informasi.insert(END, "Foto Terekam\n")
    root.Informasi.insert(END, "Memroses......\n")
    # ketika tombol keluar dipencet
    nowK = datetime.now()
    nowK2 = nowK.strftime("%Y%m%d_%H%M%S")
    nowK3 = nowK.strftime("%Y/%m/%d %H:%M:%S")
    camK = root.cap
    ret, imgK = camK.read()
    fotoKeluar = os.path.join(nopol_folder, f"nopol_{nowK2}.jpg")
    cv2.imwrite(fotoKeluar, imgK)
    print(fotoKeluar)
    print('FOTO TERTANGKAP')
    # Mulai baca nopol
    print('MEMROSES.......')
    readerK = easyocr.Reader(['en'])
    bacaK = readerK.readtext(fotoKeluar, detail=0)
    bacaK2 = bacaK[:3]
    bacaK3 = ''.join(bacaK2)
    print(bacaK)
    print(bacaK3)
    print(nowK3)
    # memeriksa jika adakah nopol atau tidak serta memasuki nopol ke file CSV
    if len(bacaK3) > 0:
        if check_kalo_penghuni(bacaK3):
            with open(penghuniDB, 'r') as filePhn:
                reader = csv.DictReader(filePhn)
                for row in reader:
                    if row['NOPOL'] == bacaK3:
                        penghuni_data = row['PENGHUNI']
                        alamat_data = row['ALAMAT']
                        break
            with open(csv_file, 'a', newline='') as fileK:
                writer = csv.writer(fileK)
                writer.writerow([bacaK3, nowK3, 'KELUAR', penghuni_data])
            root.Informasi.insert(END, "Terekam: \n")
            root.Informasi.insert(END, f"{bacaK3}\n")
            root.Informasi.insert(END, f"{nowK3}\n")
            root.Informasi.insert(END, f"{penghuni_data}\n")
            root.Informasi.insert(END, f"{alamat_data}\n")
            root.Informasi.insert(END, "Keluar")
            root.Informasi.configure(state=DISABLED)
            print('TEREKAM!(PENGHUNI)')
        else:
            with open(csv_file, 'a', newline='') as fileM:
                writer = csv.writer(fileM)
                writer.writerow([bacaK3, nowK3, 'KELUAR', 'TAMU'])
            root.Informasi.insert(END, "Terekam: \n")
            root.Informasi.insert(END, f"{bacaK3}\n")
            root.Informasi.insert(END, f"{nowK3}\n")
            root.Informasi.insert(END, "Tamu\n")
            root.Informasi.insert(END, "Keluar")
            root.Informasi.configure(state=DISABLED)
            print('TEREKAM!(TAMU)')

    else:
        print("TIDAK ADA NOPOL")
        root.Informasi.insert(END, "Tidak terdeteksi plat nomor\n")
        root.Informasi.insert(END, "Silahkan coba lagi")
        root.Informasi.configure(state=DISABLED)

root = tk.Tk()

# Membuat objek kelas VideoCapture dengan indeks webcam
root.cap = cv2.VideoCapture(0)

# Mengatur lebar dan tinggi
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root.title("PlateTrax")
root.geometry("1100x650")
root.resizable(True, True)
root.configure(background = "gray17")

bikinWidget()
root.mainloop()