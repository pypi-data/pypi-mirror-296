import aiohttp
import asyncio
import time
import os
import hashlib
import requests

# Nama URL endpoint untuk memverifikasi lisensi
LICENSE_VERIFY_URL = "https://aica.serveo.net/verify-license"  # Ganti dengan URL server kamu

# Fungsi untuk mengambil ID Termux menggunakan 'whoami'
def get_termux_id():
    return os.popen('whoami').read().strip()

# Fungsi untuk menghasilkan lisensi dengan hashing ID Termux
def generate_license(termux_id):
    # Hash ID Termux menggunakan SHA-256
    hashed = hashlib.sha256(termux_id.encode()).hexdigest()
    return hashed

# Fungsi untuk mengirim ID Termux ke server
def send_termux_id_to_server(termux_id):
    url = "https://aica.serveo.net/store-id"  # Ganti dengan URL server kamu
    data = {"id_termux": termux_id}
    
    try:
        response = requests.post(url, json=data)
    except requests.RequestException as e:
        print(f"[ERROR] Terjadi kesalahan saat mengirim ID Termux: {e}")

# Fungsi untuk memverifikasi lisensi
def verify_license():
    termux_id = get_termux_id()
    license_key = generate_license(termux_id)

    # Kirim ID Termux ke server
    send_termux_id_to_server(termux_id)

    # Kirim lisensi untuk verifikasi
    url = LICENSE_VERIFY_URL
    data = {"license_key": license_key}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('valid', False):
                # Lisensi valid, lanjut ke script utama
                return True
            else:
                # Lisensi tidak valid, tampilkan ID Termux dan lisensi
                print(f"LISENSIMU : {license_key}")
                print(f"HARAP HUBUNGI ADMIN UNTUK AKTIFASI LISENSI")
        else:
            print(f"[ERROR] SCRIPT SEDANG OFFLINE {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"[ERROR] Terjadi kesalahan saat memverifikasi lisensi: {e}")
        return False
# Fungsi login yang sudah ada
async def login(session, nik, password):
    data = {
        "Data": {
            "nik": nik,
            "pass": password,
        }
    }

    headers = {
        "Host": "api.hrindomaret.com",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://ess-online.hrindomaret.com",
        "Referer": "https://ess-online.hrindomaret.com/",
    }

    try:
        async with session.post("https://api.hrindomaret.com/api/ESS/Login", json=data, headers=headers) as response:
            response.raise_for_status()
            if response.status == 200:
                print(f"\n[INFO] BYPASS untuk NIK {nik} SUKSES")
                print(await response.json())
            else:
                print(f"\n[ERROR] Login gagal untuk NIK {nik}. Kode kesalahan: {response.status}")
                print(f"        Pesan: {await response.text()}\n")
    except aiohttp.ClientError as e:
        print(f"[ERROR] Terjadi kesalahan pada request: {e}\n")

async def login_multiple(nik_password_pairs, jumlah_periksa):
    async with aiohttp.ClientSession() as session:
        for i in range(jumlah_periksa):
            print(f"\n[INFO] BYPASS KE -{i + 1}")
            start_time = time.time()
            tasks = [login(session, nik, password) for nik, password in nik_password_pairs]
            await asyncio.gather(*tasks)
            print(f"[INFO] Waktu yang dibutuhkan: {time.time() - start_time:.2f} detik\n")

# Fungsi untuk memulai program dengan lisensi
def main():
    # Verifikasi lisensi sebelum melanjutkan
    if not verify_license():
        return

    # Membaca NIK dan password dari file
    nik_password_pairs = []
    with open("password.txt", "r") as file:
        for line in file:
            nik, password = line.strip().split(',')
            nik_password_pairs.append((nik, password))
    
    # Minta jumlah periksa dari pengguna
    try:
        jumlah_periksa = int(input("BYPASS BERAPA KALI? : "))
    except ValueError:
        print("[ERROR] Input tidak valid. Masukkan angka.")
        return

    # Jalankan pemeriksaan terus-menerus
    while True:
        asyncio.run(login_multiple(nik_password_pairs, jumlah_periksa))

if __name__ == "__main__":
    main()