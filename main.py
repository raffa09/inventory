# PROGRAM MANAJEMEN STOK BARANG
# Final Project - Uji Kompetensi

# Materi yang dicakup

#   a. Tipe data & Variable
#   b. String, Bilangan & Operator
#   c. Seleksi Kondisi
#   d. Perulangan
#   e. List dan Tuple
#   f. Fungsi
#   g. Modul & Eksepsi


from datetime import datetime


# [MATERI g - EKSEPSI] membuat eksepsi (error) buatan sendiri
class StokTidakCukup(Exception):
    """Dipakai saat jumlah yang dijual melebihi stok."""
    pass


# [MATERI a - TIPE DATA & VARIABLE]
# dict : data barang -> {nama: {"stok": int, "harga": int}}
# list : riwayat transaksi (bisa bertambah terus)
# tuple: daftar menu (isinya tetap, tidak bisa diubah)


stok_barang = {
    "Beras":  {"stok": 10, "harga": 14000},
    "Minyak": {"stok": 5,  "harga": 18000},
    "Gula":   {"stok": 0,  "harga": 16000},   # contoh barang habis
}

riwayat = []  # [MATERI e - LIST] tiap isinya berupa tuple

MENU = (  # [MATERI e - TUPLE]
    "Lihat Stok Barang",
    "Restok Barang (Tambah Stok)",
    "Tambah Barang Baru",
    "Jual Barang",
    "Lihat Riwayat Transaksi",
    "Lihat Total Nilai Stok",
    "Keluar",
)

BATAS_MENIPIS = 3  # variabel tipe int, stok <= angka ini dianggap menipis

# [MATERI f - FUNGSI] fungsi dengan parameter dan return value

def tampilkan_menu(daftar_menu):
    """Menampilkan menu dari tuple MENU."""
    print("\n=== PROGRAM MANAJEMEN STOK BARANG ===")
    # [MATERI d - PERULANGAN] for + enumerate
    for nomor, nama_menu in enumerate(daftar_menu, start=1):
        print(f"{nomor}. {nama_menu}")


def format_rupiah(angka):
    """Mengubah angka 14000 menjadi 'Rp14.000' (return string)."""
    return "Rp" + f"{angka:,}".replace(",", ".")


def catat_riwayat(jenis, barang, jumlah):
    """Menyimpan transaksi ke list riwayat dalam bentuk tuple."""
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # pakai modul datetime
    riwayat.append((waktu, jenis, barang, jumlah))


def input_angka(pesan):
    """
    Meminta input angka bulat.
    Mengembalikan int, atau None jika input bukan angka.
    """
    # [MATERI g - EKSEPSI] try / except
    try:
        return int(input(pesan))
    except ValueError:
        print("Input tidak valid! Harap masukkan angka.")
        return None


def input_nama(pesan):
    """Membersihkan input nama: hapus spasi & huruf pertama kapital."""
    # [MATERI b - STRING] strip() dan capitalize()
    return input(pesan).strip().capitalize()


def hitung_total_nilai(data):
    """Menghitung total nilai seluruh stok (stok x harga)."""
    total = 0
    for info in data.values():
        total += info["stok"] * info["harga"]   # [MATERI b - OPERATOR] * dan +=
    return total


def jual(data, nama, jumlah):
    """
    Mengurangi stok saat penjualan. Mengembalikan total harga.
    Melempar StokTidakCukup jika stok kurang.
    """
    if jumlah > data[nama]["stok"]:
        raise StokTidakCukup(f"Stok {nama} hanya {data[nama]['stok']} pcs.")
    data[nama]["stok"] -= jumlah                 # operator -=
    return jumlah * data[nama]["harga"]          # operator *


# Fungsi untuk tiap menu

def menu_lihat_stok():
    print("\n--- DAFTAR STOK BARANG ---")
    # [MATERI c - SELEKSI KONDISI]
    if not stok_barang:
        print("Belum ada barang di dalam sistem.")
        return

    # [MATERI d - PERULANGAN] for dengan dictionary .items()
    for barang, info in stok_barang.items():
        stok = info["stok"]
        if stok == 0:
            status = " (HABIS!)"
        elif stok <= BATAS_MENIPIS:
            status = " (menipis)"
        else:
            status = ""
        print(f"- {barang}: {stok} pcs @ {format_rupiah(info['harga'])}{status}")


def menu_restok():
    print("\n--- RESTOK BARANG ---")
    nama = input_nama("Masukkan nama barang yang ingin direstok: ")

    if nama not in stok_barang:
        print(f"Barang '{nama}' tidak ditemukan. Tambahkan dulu sebagai barang baru.")
        return

    tambah = input_angka(f"Masukkan jumlah stok tambahan untuk {nama}: ")
    if tambah is None:
        return

    if tambah > 0:
        stok_barang[nama]["stok"] += tambah
        catat_riwayat("Restok", nama, tambah)
        print(f"Berhasil! Stok {nama} sekarang {stok_barang[nama]['stok']} pcs.")
    else:
        print("Jumlah stok harus lebih dari 0!")


def menu_tambah_barang():
    print("\n--- TAMBAH BARANG BARU ---")
    nama = input_nama("Masukkan nama barang baru: ")

    # [MATERI b - OPERATOR LOGIKA] "or" pada kondisi
    if nama == "" or nama in stok_barang:
        print("Nama kosong atau barang sudah ada. Gunakan menu Restok jika sudah ada.")
        return

    stok_awal = input_angka(f"Masukkan stok awal untuk {nama}: ")
    if stok_awal is None:
        return
    harga = input_angka(f"Masukkan harga satuan {nama} (Rp): ")
    if harga is None:
        return

    # operator logika "and" + perbandingan
    if stok_awal >= 0 and harga > 0:
        stok_barang[nama] = {"stok": stok_awal, "harga": harga}
        catat_riwayat("Barang baru", nama, stok_awal)
        print(f"Barang '{nama}' berhasil ditambahkan.")
    else:
        print("Stok tidak boleh negatif dan harga harus lebih dari 0!")


def menu_jual():
    print("\n--- JUAL BARANG ---")
    nama = input_nama("Masukkan nama barang yang dijual: ")

    if nama not in stok_barang:
        print(f"Barang '{nama}' tidak ditemukan.")
        return

    jumlah = input_angka(f"Jumlah {nama} yang dijual: ")
    if jumlah is None:
        return
    if jumlah <= 0:
        print("Jumlah harus lebih dari 0!")
        return

    # [MATERI g - EKSEPSI] menangkap eksepsi buatan sendiri
    try:
        total = jual(stok_barang, nama, jumlah)
    except StokTidakCukup as pesan_error:
        print(f"Gagal menjual! {pesan_error}")
    else:
        catat_riwayat("Jual", nama, jumlah)
        print(f"Terjual {jumlah} pcs {nama}. Total: {format_rupiah(total)}")
        # operator modulus (%) dan floor division (//)
        lusin = jumlah // 12
        sisa = jumlah % 12
        if lusin > 0:
            print(f"(Setara {lusin} lusin + {sisa} pcs)")
    finally:
        print("Transaksi penjualan selesai diproses.")


def menu_riwayat():
    print("\n--- RIWAYAT TRANSAKSI ---")
    if len(riwayat) == 0:
        print("Belum ada transaksi.")
        return

    # [MATERI e] unpacking tuple di dalam perulangan list
    for no, (waktu, jenis, barang, jumlah) in enumerate(riwayat, start=1):
        print(f"{no}. [{waktu}] {jenis} - {barang}: {jumlah} pcs")


def menu_total_nilai():
    print("\n--- TOTAL NILAI STOK ---")
    total = hitung_total_nilai(stok_barang)
    jumlah_jenis = len(stok_barang)
    print(f"Jumlah jenis barang : {jumlah_jenis}")
    print(f"Total nilai stok    : {format_rupiah(total)}")


# PROGRAM UTAMA

def main():
    # [MATERI d - PERULANGAN] while agar program berjalan terus sampai keluar
    while True:
        tampilkan_menu(MENU)
        pilihan = input(f"Pilih menu (1-{len(MENU)}): ").strip()

        # [MATERI c - SELEKSI KONDISI] if / elif / else
        if pilihan == "1":
            menu_lihat_stok()
        elif pilihan == "2":
            menu_restok()
        elif pilihan == "3":
            menu_tambah_barang()
        elif pilihan == "4":
            menu_jual()
        elif pilihan == "5":
            menu_riwayat()
        elif pilihan == "6":
            menu_total_nilai()
        elif pilihan == "7":
            print("\nTerima kasih telah menggunakan program ini!")
            break
        else:
            print(f"\nPilihan tidak valid! Silakan pilih angka 1-{len(MENU)}.")


# Agar main() hanya jalan saat file dieksekusi langsung
if __name__ == "__main__":
    main()