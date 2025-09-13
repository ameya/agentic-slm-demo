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
👉 [https://ollama.ai/download](https://ollama.ai/download)  

Follow the installer, then verify installation:  
```powershell
ollama --version
