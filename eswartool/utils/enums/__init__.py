from dotenv import load_dotenv
load_dotenv(override=True)


import nmap


def scan_network(target):
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments='-sV -T4')

    for host in nm.all_hosts():
        print(f"Host: {host}")
        print(f"State: {nm[host].state()}")

        for proto in nm[host].all_protocols():
            print("Protocol: %s" % proto)
            ports = nm[host][proto].keys()
            for port in ports:
                print(f"Port: {port}\tState: {nm[host][proto][port]['state']}\tService: {nm[host][proto][port]['name']}\tVersion: {nm[host][proto][port]['version']}")

def main():
    target = '127.0.0.1'  # Cambia esto por tu objetivo de escaneo
    scan_network(target)

if __name__ == "__main__":
    main()

