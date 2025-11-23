import re

class RuleBruteforce:
    def __init__(self):
        self.failed_attempts = {}

    def process(self, log_line):
        if "Failed password" in log_line:
            ip = self.extract_ip(log_line)
            self.failed_attempts[ip] = self.failed_attempts.get(ip, 0) + 1

            if self.failed_attempts[ip] >= 3:
                return {
                    "message": f"Bruteforce detected from {ip}",
                    "risk": "high"
                }

        return None

    def extract_ip(self, line):
        for part in line.split():
            if part.count(".") == 3:
                return part
        return "unknown"


class RulePortscan:
    def __init__(self):
        self.port_hits = {}

    def process(self, log_line):

        if "port scan" in log_line.lower() and "from" in log_line.lower():

            ip = self.extract_ip(log_line)
            port = self.extract_port(log_line)

            if ip != "unknown" and port != -1:

                if ip not in self.port_hits:
                    self.port_hits[ip] = set()

                self.port_hits[ip].add(port)

                print("DEBUG:", ip, "ports:", self.port_hits[ip])

                if len(self.port_hits[ip]) >= 5:
                    return {
                        "message": f"Portscan detected from {ip} ({len(self.port_hits[ip])} ports)",
                        "risk": "medium"
                    }

        return None

    def extract_ip(self, line):
        for part in line.split():
            if part.count(".") == 3:
                return part
        return "unknown"

    def extract_port(self, line):
        match = re.search(r"port\s+(\d+)", line, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return -1


#sql injection detection
class RuleSQLi:
    def __init__(self):
        self.patterns = [
            "or 1=1",
            "or '1'='1'",
            "' or '1'='1",
            "' or 1=1 --",
            "union select",
            "--",
            "#",
            "/*",
            "sleep(",
            "benchmark(",
            "information_schema",
            "load_file(",
        ]

    def process(self, log_line):
        lower = log_line.lower()
        for pattern in self.patterns:
            if pattern in lower:
                return {
                    "message": f"SQL Injection attempt detected ({pattern})",
                    "risk": "high"
                }
        return None
