import nmap
import pandas as pd



def scan_ips(ips):
    nm = nmap.PortScanner()
    scan_results = []
    nmap_arguments = ""
    
    
    params_keys = ( "ports_open", "services", "os_info", "firewall_info",
                    "topology_info", "routing_info","vulnerabilities",
                    "performance_metrics", "advanced_network_fingerprints")
       

    for ip in ips:
        nm.scan(ip, arguments='-sV -O -T4')  # Escaneo detallado
       
        for host in nm.all_hosts():
            ports_open = []
            services = []
            os_info = "Unknown"
            firewall_info = "Unknown"
            topology_info = "Unknown"
            routing_info = "Unknown"
            vulnerabilities = []
            performance_metrics = "Unknown"
            advanced_network_fingerprints = "Unknown"
            
            if 'osmatch' in nm[host]:
                os_info = nm[host]['osmatch'][0]['name']
            if 'osclass' in nm[host]:
                os_info = nm[host]['osclass'][0]['osfamily']
            if 'fingerprint' in nm[host]:
                advanced_network_fingerprints = nm[host]['fingerprint']
            if 'tcp' in nm[host]:
                for port, port_info in nm[host]['tcp'].items():
                    ports_open.append(port)
                    services.append(port_info['name'])
            if 'scaninfo' in nm[host]:
                if 'tcp' in nm[host]['scaninfo']:
                    firewall_info = nm[host]['scaninfo']['tcp']['reason']
            if 'traceroute' in nm[host]:
                topology_info = nm[host]['traceroute']
            if 'routes' in nm[host]:
                routing_info = nm[host]['routes']
            if 'vulners' in nm[host]:
                vulnerabilities = nm[host]['vulners']
            if 'uptime' in nm[host]:
                performance_metrics = nm[host]['uptime']
            
            scan_results.append({
                'IP': host,
                'PortsOpen': ports_open,
                'Services': services,
                'OS': os_info,
                'FirewallInfo': firewall_info,
                'TopologyInfo': topology_info,
                'RoutingInfo': routing_info,
                'Vulnerabilities': vulnerabilities,
                'PerformanceMetrics': performance_metrics,
                'AdvancedNetworkFingerprints': advanced_network_fingerprints
            })

    return scan_results

def main():
    ips_to_scan = ['192.168.1.1', '192.168.1.2', '192.168.1.3']
    scan_results = scan_ips(ips_to_scan)
    df = pd.DataFrame(scan_results)
    
    print(df)



