import json
from pathlib import Path



INTENT_MAP = {

    # -------------------- NMAP --------------------
    ("nmap", "Network Service Discovery"):
        "Identify live hosts and responsive systems on a network using host discovery and probing techniques",

    ("nmap", "Port Scanning"):
        "Enumerate open TCP and UDP ports exposed by target systems to understand accessible services",

    ("nmap", "OS Fingerprinting"):
        "Infer operating system details of target hosts through network stack behavior and fingerprinting",

    ("nmap", "Service Version Enumeration"):
        "Determine application names and version information running on open network services",

    ("nmap", "Script-Based Enumeration (NSE)"):
        "Perform targeted service, vulnerability, or configuration enumeration using Nmap scripting capabilities",

    ("nmap", "Firewall / IDS Evasion Scans"):
        "Attempt to bypass firewall rules or intrusion detection systems using evasive scanning techniques",


    # -------------------- MASSCAN --------------------
    ("masscan", "High-Speed Port Scanning"):
        "Rapidly identify open ports across large address ranges using asynchronous scanning",

    ("masscan", "Internet-Wide Scanning"):
        "Perform large-scale scanning across broad IP ranges to identify exposed services",

    ("masscan", "Rate-Limited Scans"):
        "Conduct controlled port scans with explicit rate limits to reduce network impact",

    ("masscan", "Banner Grabbing"):
        "Retrieve service banners from open ports to identify running applications or protocols",

    ("masscan", "Targeted Port Sweeps"):
        "Scan a specific set of high-value ports to quickly assess service exposure",


    # -------------------- GOBUSTER --------------------
    ("gobuster", "Directory Enumeration"):
        "Discover hidden directories and paths exposed by a web server",

    ("gobuster", "File Extension Discovery"):
        "Identify accessible files by brute-forcing common file extensions",

    ("gobuster", "DNS Subdomain Enumeration"):
        "Enumerate subdomains associated with a target domain using wordlist-based discovery",

    ("gobuster", "Virtual Host Enumeration"):
        "Identify virtual hosts configured on a web server through Host header probing",

    ("gobuster", "Content Discovery"):
        "Uncover hidden web content such as directories, files, or endpoints",


    # -------------------- ENUM4LINUX --------------------
    ("enum4linux", "SMB Share Enumeration"):
        "Enumerate SMB file shares available on a Windows or Samba host",

    ("enum4linux", "User Enumeration"):
        "Identify user accounts present on a remote Windows or SMB-enabled system",

    ("enum4linux", "Group Enumeration"):
        "Enumerate security and distribution groups on a Windows or SMB host",

    ("enum4linux", "Domain Policy Enumeration"):
        "Retrieve domain password and security policies from Windows environments",

    ("enum4linux", "RID Cycling"):
        "Enumerate domain users and groups by iterating Windows Relative Identifiers (RIDs)",


    # -------------------- AMASS --------------------
    ("amass", "Passive Subdomain Enumeration"):
        "Discover subdomains using passive data sources without directly interacting with the target",

    ("amass", "Active Subdomain Enumeration"):
        "Actively probe DNS infrastructure to identify subdomains associated with a target domain",

    ("amass", "DNS Resolution"):
        "Resolve discovered subdomains to IP addresses to validate their existence",

    ("amass", "Attack Surface Mapping"):
        "Map the external attack surface of an organization by correlating discovered assets",

    ("amass", "Graph-Based Asset Discovery"):
        "Visualize and analyze relationships between discovered assets using graph-based models",


    # -------------------- SQLMAP --------------------
    ("sqlmap", "SQL Injection Detection"):
        "Detect SQL injection vulnerabilities in web application parameters",

    ("sqlmap", "Database Enumeration"):
        "Enumerate databases, tables, and schema information through SQL injection",

    ("sqlmap", "Data Extraction"):
        "Extract data records from backend databases using SQL injection techniques",

    ("sqlmap", "Privilege Escalation via SQLi"):
        "Assess and exploit database-level privileges obtained through SQL injection",

    ("sqlmap", "OS Command Execution"):
        "Execute operating system commands on vulnerable servers via database exploitation",


    # -------------------- NIKTO --------------------
    ("nikto", "Web Server Vulnerability Scanning"):
        "Identify common vulnerabilities, insecure files, and misconfigurations in web servers",

    ("nikto", "Misconfiguration Detection"):
        "Detect insecure or incorrect web server configuration settings",

    ("nikto", "Outdated Software Detection"):
        "Identify outdated web server components and software versions",

    ("nikto", "CGI Enumeration"):
        "Discover vulnerable or misconfigured CGI scripts on web servers",

    ("nikto", "SSL/TLS Assessment"):
        "Assess SSL and TLS configuration issues on web servers",


    # -------------------- WFuzz --------------------
    ("wfuzz", "Parameter Fuzzing"):
        "Identify vulnerable or hidden parameters by injecting payloads into request fields",

    ("wfuzz", "Directory & File Fuzzing"):
        "Discover hidden files and directories through payload-based fuzzing",

    ("wfuzz", "Authentication Fuzzing"):
        "Test authentication mechanisms for weaknesses using automated input variation",

    ("wfuzz", "Payload Injection Testing"):
        "Evaluate application input handling by injecting crafted payloads",

    ("wfuzz", "API Endpoint Discovery"):
        "Discover undocumented or hidden API endpoints via fuzzing techniques",


    # -------------------- FFUF --------------------
    ("ffuf", "Directory Fuzzing"):
        "Discover hidden directories and endpoints using fast HTTP fuzzing",

    ("ffuf", "File Extension Discovery"):
        "Identify accessible files by fuzzing common file extensions",

    ("ffuf", "Parameter Fuzzing"):
        "Enumerate and test HTTP parameters for unexpected behavior",

    ("ffuf", "Virtual Host Discovery"):
        "Identify virtual hosts configured on a web server via Host header fuzzing",

    ("ffuf", "API Fuzzing"):
        "Discover and test API endpoints using high-performance fuzzing",


    # -------------------- HYDRA --------------------
    ("hydra", "Online Password Brute Force"):
        "Attempt automated password guessing against live network services",

    ("hydra", "Credential Stuffing"):
        "Test reused credential pairs across authentication services",

    ("hydra", "Protocol Authentication Testing"):
        "Validate authentication mechanisms across supported network protocols",

    ("hydra", "Login Rate Testing"):
        "Assess authentication rate reminders and lockout controls",

    ("hydra", "Service Credential Validation"):
        "Verify known credentials against network services",


    # -------------------- JOHN --------------------
    ("john", "Offline Password Cracking"):
        "Crack password hashes using offline computational attacks",

    ("john", "Dictionary Attacks"):
        "Attempt password recovery using wordlist-based guessing",

    ("john", "Rule-Based Attacks"):
        "Apply transformation rules to enhance password cracking effectiveness",

    ("john", "Hash Identification"):
        "Identify hash formats to determine appropriate cracking methods",

    ("john", "Password Audit Testing"):
        "Evaluate password strength for compliance and audit purposes",


    # -------------------- HASHCAT --------------------
    ("hashcat", "GPU-Accelerated Hash Cracking"):
        "Leverage GPU acceleration to efficiently crack password hashes",

    ("hashcat", "Mask Attacks"):
        "Perform structured password guessing using predefined masks",

    ("hashcat", "Rule-Based Attacks"):
        "Enhance wordlists with transformation rules to increase cracking success",

    ("hashcat", "Hybrid Attacks"):
        "Combine dictionary and brute-force techniques for password cracking",

    ("hashcat", "Hash Benchmarking"):
        "Benchmark system performance for different hash algorithms",


    # -------------------- METASPLOIT --------------------
    ("metasploit", "Exploit Execution"):
        "Exploit known vulnerabilities to gain access to target systems",

    ("metasploit", "Payload Generation"):
        "Generate malicious payloads for exploitation and post-exploitation",

    ("metasploit", "Post-Exploitation"):
        "Perform actions on compromised systems after successful exploitation",


    # -------------------- SEARCHSPLOIT --------------------
    ("searchsploit", "Exploit Discovery"):
        "Search exploit databases to identify publicly known vulnerabilities",


    # -------------------- TCPDUMP --------------------
    ("tcpdump", "Live Packet Capture"):
        "Capture live network traffic for analysis and troubleshooting",


    # -------------------- TSHARK --------------------
    ("tshark", "Packet Dissection"):
        "Analyze and dissect packet capture files for protocol-level insights",


    # -------------------- CRACKMAPEXEC --------------------
    ("crackmapexec", "Lateral Movement"):
        "Move laterally across networked systems using valid credentials",


    # -------------------- IMPACKET --------------------
    ("impacket", "Remote Command Execution"):
        "Execute commands remotely on target systems using network protocols",


    # -------------------- RADARE2 --------------------
    ("radare2", "Binary Disassembly"):
        "Disassemble and analyze compiled binaries for reverse engineering",


    # -------------------- YARA --------------------
    ("yara", "Malware Detection"):
        "Identify malicious files or memory artifacts using pattern-based rules",
}




# ---------------- CONFIG ----------------
INPUT_JSONL = "command_rows.jsonl"
OUTPUT_JSONL = "command_rows_with_intent.jsonl"
# ---------------------------------------


def inject_intents():
    input_path = Path(INPUT_JSONL)
    output_path = Path(OUTPUT_JSONL)

    if not input_path.exists():
        raise FileNotFoundError(f"{INPUT_JSONL} not found")

    missing = set()
    total = 0

    with input_path.open("r", encoding="utf-8") as fin, \
         output_path.open("w", encoding="utf-8") as fout:

        for line in fin:
            if not line.strip():
                continue

            row = json.loads(line)
            key = (row["tool"], row["command_category"])

            intent = INTENT_MAP.get(key)
            if intent is None:
                missing.add(key)
                intent = "Intent not defined for this tool and command category"

            row["intent"] = intent
            fout.write(json.dumps(row) + "\n")
            total += 1

    print(f"[✓] Processed {total} rows")
    print(f"[✓] Output written to: {OUTPUT_JSONL}")

    if missing:
        print("\n[!] Missing intent definitions for:")
        for m in sorted(missing):
            print(f"  - {m}")


if __name__ == "__main__":
    inject_intents()
