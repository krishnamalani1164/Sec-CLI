import json

INPUT_FILE = "rag_dataset_50000.jsonl"
OUTPUT_FILE = "rag_dataset_50000_with_intent.jsonl"

INTENT_MAP = {
    ("nmap", "Network Service Discovery"):
        "Identify live hosts and responsive systems on a network using discovery and probing techniques",
    ("nmap", "Port Scanning"):
        "Enumerate open TCP and UDP ports exposed by target systems",
    ("nmap", "OS Fingerprinting"):
        "Infer operating system details of target hosts through network stack analysis",
    ("nmap", "Service Version Enumeration"):
        "Determine application and service versions running on open ports",

    ("sqlmap", "SQL Injection Exploitation"):
        "Detect and exploit SQL injection vulnerabilities to enumerate or extract database information",

    ("hydra", "Brute Force Authentication"):
        "Attempt credential-based access to network or application services through automated authentication attempts",

    ("gobuster", "Content Discovery"):
        "Discover hidden directories, files, virtual hosts, or DNS entries exposed by a target web application",

    ("nikto", "Web Vulnerability Scanning"):
        "Identify common misconfigurations and known vulnerabilities in web servers and applications"
}

with open(INPUT_FILE) as fin, open(OUTPUT_FILE, "w") as fout:
    for line in fin:
        obj = json.loads(line)
        tool = obj["meta_data"]["tool_name"]
        category = obj["meta_data"]["category"]

        intent = INTENT_MAP.get(
            (tool, category),
            f"Perform {category.lower()} activities using {tool} during the {obj['meta_data']['mitre_stage']} phase"
        )

        obj["meta_data"]["intent_description"] = intent
        fout.write(json.dumps(obj) + "\n")

print("✔ Intent descriptions added to all rows")
