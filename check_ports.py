#!/usr/bin/env python3
import socket
import json
from datetime import datetime

# Configuration
MAIL_SERVERS = [
    "mailhub1-external.be.ch",
    "mailhub2-external.be.ch"
]
PORT_TO_CHECK = 25  # SMTP
TIMEOUT = 5  # seconds

def check_port(host, port, timeout=5):
    """Check if a port is open on the given host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.gaierror:
        return False
    except socket.timeout:
        return False
    except Exception:
        return False

def main():
    results = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "port": PORT_TO_CHECK,
    }
    
    all_ok = True
    
    for i, server in enumerate(MAIL_SERVERS, 1):
        is_open = check_port(server, PORT_TO_CHECK, TIMEOUT)
        
        results[f"server{i}_host"] = server
        results[f"server{i}_status"] = "open" if is_open else "closed"
        results[f"server{i}_ok"] = 1 if is_open else 0
        
        if not is_open:
            all_ok = False
    
    # Overall status
    results["overall_status"] = "ok" if all_ok else "error"
    results["status_code"] = 0 if all_ok else 1
    
    # Write to status.json
    with open("status.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Status check completed: {results['overall_status']}")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
