import requests
import json
from ipwhois import IPWhois

# ---------------------------
# Real Cybersecurity Tools
# ---------------------------

def whois_lookup(ip: str) -> str:
    try:
        obj = IPWhois(ip)
        res = obj.lookup_whois()
        return f"WHOIS: {res.get('asn_description', 'N/A')}"
    except Exception as e:
        return f"WHOIS lookup failed: {e}"

def geoip_lookup(ip: str) -> str:
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json").json()
        return f"GEOIP: {res.get('city', 'N/A')}, {res.get('country', 'N/A')}"
    except Exception as e:
        return f"GeoIP lookup failed: {e}"

def reputation_check(ip: str, api_key: str) -> str:
    try:
        url = "https://api.abuseipdb.com/api/v2/check"
        querystring = {"ipAddress": ip, "maxAgeInDays": "90"}
        headers = {"Accept": "application/json", "Key": api_key}
        res = requests.get(url, headers=headers, params=querystring).json()
        score = res.get("data", {}).get("abuseConfidenceScore", "N/A")
        return f"Reputation: Abuse Confidence Score = {score}"
    except Exception as e:
        return f"Reputation check failed: {e}"


# ---------------------------
# Agent (Ollama stubbed for demo)
# ---------------------------
class CyberAgent:
    def __init__(self, abuseipdb_key: str):
        self.abuseipdb_key = abuseipdb_key
        self.tools = {
            "whois_lookup": lambda ip: whois_lookup(ip),
            "geoip_lookup": lambda ip: geoip_lookup(ip),
            "reputation_check": lambda ip: reputation_check(ip, self.abuseipdb_key)
        }

    def handle_query(self, query: str, expected_tool: str, ip: str, force_tool: str):
        """Use forced tool to simulate good/bad decisions."""
        decision = force_tool

        if decision in self.tools:
            tool_result = self.tools[decision](ip)
        else:
            tool_result = "Invalid tool chosen."

        log_entry = {
            "Prompt": query,
            "IP": ip,
            "Tool Chosen": decision,
            "Expected Tool": expected_tool,
            "Correct?": decision == expected_tool,
            "Tool Output": tool_result
        }

        return log_entry


# ---------------------------
# Demo Run (1 good, 2 bad)
# ---------------------------
if __name__ == "__main__":
    ABUSEIPDB_KEY = "<<ABUSEIPDB KEY>>"

    agent = CyberAgent(ABUSEIPDB_KEY)

    test_cases = [
        # GOOD → Correct tool forced
        {"query": "Where is this IP located?", "expected": "geoip_lookup", "ip": "8.8.8.8", "force": "geoip_lookup"},
        # BAD → Wrong tool forced
        {"query": "Is this IP malicious?", "expected": "reputation_check", "ip": "123.45.67.89", "force": "geoip_lookup"},
        # BAD → Wrong tool forced
        {"query": "Which country is this IP from?", "expected": "geoip_lookup", "ip": "1.1.1.1", "force": "whois_lookup"},
    ]

    for case in test_cases:
        log = agent.handle_query(case["query"], case["expected"], case["ip"], force_tool=case["force"])
        print(json.dumps(log, indent=2))
