# 🛡️ Agentic AI – Suspicious IP Investigation Demo  

This project demonstrates how an **Agentic AI system** can make (and mis-make) tool selection decisions in a **cybersecurity context**.  
We use **Ollama (LLaMA 3.2 1B)** locally for decision-making, and real tools for:  

- 🌍 **GeoIP Lookup** → Where is an IP located?  
- 📜 **WHOIS Lookup** → Who owns an IP?  
- 🚨 **Reputation Check** → Is an IP malicious? (via AbuseIPDB API)  

The demo is designed to show:  
✅ Correct tool selection (1 case)  
❌ Wrong tool selection (2 cases)  

---

## ⚙️ Prerequisites  

### 1. Install Ollama (Windows)  
Download Ollama for Windows from the official site:  
- 👉 [https://ollama.ai/download](https://ollama.ai/download)  

Follow the installer, then verify installation:  
```powershell
ollama --version
```
---
### 2. Pull the LLaMA 3.2 1B Model

Once Ollama is installed, pull the **LLaMA 3.2 1B** model:

```ollama pull llama3.2:1b```


Test the model:

```ollama run llama3.2:1b```

---
### 3. Create an AbuseIPDB Account & API Key

- Go to 👉 https://www.abuseipdb.com/register

- Sign up for a free account.

- Navigate to API section in your profile.

- Copy your API key.
---
### 4. Python Environment

Make sure you have **Python 3.9+** installed.

- Create a virtual environment:

```python -m venv venv```
```venv\Scripts\activate   # Windows```
# or
```source venv/bin/activate  # Mac/Linux```

---
### 5. Install dependencies:

```pip install -r requirements.txt```

🚀 Running the Demo

Run the agent script:

```python agent.py```
---
### 6. Expected output (example):
```
..\agentic-slm-demo\main.py 
{
  "Prompt": "Where is this IP located?",
  "IP": "8.8.8.8",
  "Tool Chosen": "whois_lookup",
  "Expected Tool": "geoip_lookup",
  "Correct?": false,
  "Tool Output": "WHOIS: GOOGLE, US"
}
{
  "Prompt": "Who owns this IP address?",
  "IP": "8.8.4.4",
  "Tool Chosen": "whois_lookup",
  "Expected Tool": "whois_lookup",
  "Correct?": true,
  "Tool Output": "WHOIS: GOOGLE, US"
}
{
  "Prompt": "Is this IP malicious?",
  "IP": "123.45.67.89",
  "Tool Chosen": "whois_lookup",
  "Expected Tool": "reputation_check",
  "Correct?": false,
  "Tool Output": "WHOIS: NA"
}
Process finished with exit code 0

```
---
### 📊 Results

- ✅ 1 Correct Decision (GeoIP lookup for location query)

- ❌ 2 Wrong Decisions (model confused maliciousness with GeoIP, and country with WHOIS)

This highlights the challenge of tool selection in Agentic AI systems.
---
### 📌 Notes

## Ollama must be running locally (http://localhost:11434).

## LLaMA 3.2 1B is a tiny model → mistakes are expected (and useful for demo!).

Replace the AbuseIPDB key in agent.py with your own.

