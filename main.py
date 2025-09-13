import requests
import json
import re
from ipwhois import IPWhois

# ---------------------------
# Tools
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
# Agent with Ollama Decision + Validation
# ---------------------------
class CyberAgent:
    def __init__(self, abuseipdb_key: str, ollama_model: str = "llama3.2:1b"):
        self.abuseipdb_key = abuseipdb_key
        self.ollama_model = ollama_model
        self.tools = {
            "whois_lookup": lambda ip: whois_lookup(ip),
            "geoip_lookup": lambda ip: geoip_lookup(ip),
            "reputation_check": lambda ip: reputation_check(ip, self.abuseipdb_key)
        }
    # ---------------------------
    # This section will be analyised by LLM which will compare the tool picked v/s prompt recived as input to SLM
    # ---------------------------
    def normalize_decision(self, text: str) -> str:
        """Normalize SLM output to match known tool names."""
        text = text.strip().lower().replace("-", "_")
        if "whois" in text:
            return "whois_lookup"
        if "geo" in text:
            return "geoip_lookup"
        if "reputation" in text or "abuse" in text or "malicious" in text:
            return "reputation_check"
        return "unknown"

    def expected_tool(self, query: str) -> str:
        """Determine expected tool based on keywords in query."""
        query_l = query.lower()
        if re.search(r"where|location|country", query_l):
            return "geoip_lookup"
        elif re.search(r"who owns|registrant|organization|owner", query_l):
            return "whois_lookup"
        elif re.search(r"malicious|safe|reputation|blacklist", query_l):
            return "reputation_check"
        return "unknown"

    def ask_ollama(self, prompt: str) -> str:
        """Ask Ollama which tool to use."""
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.ollama_model,
            "prompt": (
                f"You are a SOC analyst assistant.\n"
                f"Pick ONE best tool for this analyst query.\n"
                f"Available tools: whois_lookup, geoip_lookup, reputation_check.\n"
                f"Return only the tool name.\n\n"
                f"Query: {prompt}"
            ),
            "stream": False
        }

        response = requests.post(url, json=payload)
        resp_json = response.json()

        try:
            raw = resp_json["response"]
            return self.normalize_decision(raw)
        except Exception:
            return "unknown"

    def handle_query(self, query: str, ip: str):
        """Run query, decide tool, check correctness."""
        decision = self.ask_ollama(query)
        expected = self.expected_tool(query)

        if decision in self.tools:
            tool_result = self.tools[decision](ip)
        else:
            tool_result = "Invalid tool chosen."

        log_entry = {
            "Prompt": query,
            "IP": ip,
            "Tool Chosen": decision,
            "Expected Tool": expected,
            "Correct?": decision == expected,
            "Tool Output": tool_result
        }

        return log_entry


# ---------------------------
# Demo Run
# ---------------------------
if __name__ == "__main__":
    ABUSEIPDB_KEY = "<<<YOUR KEY>>>>"
    agent = CyberAgent(ABUSEIPDB_KEY, ollama_model="llama3.2:1b")

    queries = [
        {"query": "Where is this IP located?", "ip": "8.8.8.8"},
        {"query": "Who owns this IP address?", "ip": "8.8.4.4"},
        {"query": "Is this IP malicious?", "ip": "123.45.67.89"},
    ]

    for q in queries:
        log = agent.handle_query(q["query"], q["ip"])
        print(json.dumps(log, indent=2))
