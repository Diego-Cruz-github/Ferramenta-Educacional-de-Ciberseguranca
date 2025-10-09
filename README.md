# 🛡️ CyberMentor AI - Interactive Cybersecurity Learning Tool

**Educational terminal application in Python for practical learning of cybersecurity concepts with integrated AI mentor.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://python.org)
[![Security](https://img.shields.io/badge/Security-Educational-green?logo=shield&logoColor=white)](https://github.com/Diego-Cruz-github/Ferramenta-Educacional-de-Ciberseguranca)
[![AI Powered](https://img.shields.io/badge/AI-GROQ%20Integrated-purple?logo=openai&logoColor=white)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange?logo=construction&logoColor=white)](https://github.com/Diego-Cruz-github/Ferramenta-Educacional-de-Ciberseguranca)

---

## 🚧 Development Status

**This project is currently under active development.** New features, modules, and improvements are being added regularly. The current version includes functional cryptography labs, web security demos, and AI-powered learning assistance.

Feel free to explore the existing features and stay tuned for updates! 🚀

---

## 📖 About the Project

**CyberMentor AI** is an educational terminal tool that teaches fundamental **cybersecurity concepts** through hands-on demonstrations and integrated AI chat support.

### 🎯 Implemented Features

- **🔐 Complete Cryptography Lab**: 5 interactive demos (hashes, passwords, encryption, rainbow tables, crypto analysis)
- **🌐 Web Security Demos**: HTTP headers analysis, educational SQL injection and XSS
- **🔧 Network Tools**: Port scanning, ping, DNS lookup and configuration analysis
- **🔍 Digital Forensics**: File analysis, metadata extraction and hidden data detection
- **💬 Specialized AI Chat**: Explanations with GROQ API + offline mode
- **✨ Rich Terminal Interface**: Colorful menus with Rich library

---

## 🛠️ Technologies Used

- **Python 3.9+** - Core language
- **Rich** - Colorful terminal interface and tables
- **Typer** - Modern CLI framework
- **GROQ API** - AI for specialized chat
- **Cryptography** - Encryption/decryption demos
- **bcrypt** - Secure password hashing
- **aiohttp** - Asynchronous HTTP client

---

## 📁 Project Structure

```
Ferramenta-Educacional-de-Ciberseguranca/
├── main.py                    # Main application
├── requirements.txt           # Dependencies
│
├── core/                      # Core modules
│   ├── ai_mentor.py          # AI chat with GROQ
│   └── menu_system.py        # Menu interface system
│
└── demos/                     # Educational demonstrations
    ├── crypto_demo.py        # Cryptography laboratory
    ├── web_demo.py           # Web security
    ├── network_demo.py       # Network tools
    └── forensics_demo.py     # Digital forensics
```

---

## 🚀 How to Use

### 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/Diego-Cruz-github/Ferramenta-Educacional-de-Ciberseguranca.git
cd Ferramenta-Educacional-de-Ciberseguranca

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

### 🤖 AI Chat Configuration (Optional)

```bash
# With GROQ API key
export GROQ_API_KEY="your_key"
python main.py

# Without API (offline mode)
python main.py
```

**How to get free GROQ key:**
1. Visit [console.groq.com](https://console.groq.com)
2. Create account and generate API key
3. 100 free requests per day

### 📋 Main Menu

```
Learning Modules
┌────────┬─────────────────────────┬────────────────────────────────────────┐
│ Option │ Module                  │ Description                            │
├────────┼─────────────────────────┼────────────────────────────────────────┤
│ 1      │ Cryptography            │ Hash functions, encryption, passwords  │
│ 2      │ Web Security            │ HTTP analysis, SQLi, XSS demos        │
│ 3      │ Network Tools           │ Port scanning, DNS, connectivity      │
│ 4      │ Digital Forensics       │ File analysis, metadata extraction    │
│ 5      │ AI Chat                 │ Ask questions to the AI mentor        │
│ 6      │ About                   │ Information about CyberMentor AI       │
│ 0      │ Exit                    │ Close the application                  │
└────────┴─────────────────────────┴────────────────────────────────────────┘
```

### 🔐 Cryptography Laboratory

**5 interactive demonstrations available:**

1. **Hash Functions** - Compare MD5, SHA1, SHA256, SHA512
2. **Password Security** - Hashing, salting, bcrypt  
3. **Symmetric Encryption** - AES encryption/decryption
4. **Rainbow Table Attack** - How they work and defenses
5. **Crypto Analysis** - Avalanche effect and properties

### 💬 AI Chat

- Ask cybersecurity questions in natural language
- Contextualized educational explanations
- Works online (GROQ) or offline (predefined responses)

---

## 📚 Educational Content

### 🔐 Cryptography Laboratory (Implemented)

**Concepts covered:**
- **Hash Functions**: MD5, SHA1, SHA256, SHA512 - security and vulnerabilities
- **Password Security**: Salt, bcrypt, secure storage
- **Symmetric Cryptography**: Practical AES encryption/decryption
- **Rainbow Table Attacks**: How they work and defenses
- **Cryptographic Analysis**: Avalanche effect, collision resistance

**Exemplo real do Hash Demo:**
```
Hash Results  
┌─────────────┬─────────────────────────────────────────────────────┬────────────────┐
│ Algorithm   │ Hash Value                                       │ Security       │
├─────────────┼─────────────────────────────────────────────────────┼────────────────┤
│ MD5         │ 5d41402abc4b2a76b9719d911017c592                 │ ❌ BROKEN      │
│ SHA256      │ 2c26b46b68ffc68ff99b453c1d30413413422d706... │ ✅ SECURE      │
└─────────────┴─────────────────────────────────────────────────────┴────────────────┘
```

---

## 🤖 Integrated AI Chat

**Features:**
- Educational chat specialized in cybersecurity
- Natural language explanations
- Online mode (GROQ API) + offline fallback
- Contextualized and ethical responses

**Usage example:**
```
Your question: What is symmetric cryptography?

CyberMentor AI:
Symmetric cryptography uses the same key for encryption and decryption.

Examples: AES, DES, 3DES
Advantages: Fast, efficient for large volumes
Disadvantages: Secure key distribution is challenging

Use for: File encryption, communication where parties already share keys.
```

---

## ⚙️ Advanced Options

```bash
# Developer mode with logs
python main.py --dev

# Specify API key
python main.py --api-key "your_groq_key"
```

---

## 🎯 Who This Tool Is For

- **Students** beginning in cybersecurity
- **Developers** wanting to learn basic security
- **Curious minds** about cryptography and digital security
- **Teachers** seeking practical educational material

---

## 📜 License

MIT License - Use freely for educational purposes.

---

## ⚠️ Legal Notice

**Educational use only.** Do not use for illegal activities or unauthorized attacks. The user is responsible for appropriate use of this tool.

---

## 💻 Future Development Plans

**Planned modules and features:**
- 🕵️ **OSINT Basics** - Ethical information gathering techniques
- 🦠 **Malware Analysis** - Safe sandboxing and analysis methods  
- 🛡️ **System Hardening** - Security configuration best practices
- 🚨 **Incident Response** - Cybersecurity incident handling procedures
- 🎮 **Gamification** - Points, achievements, and progress tracking
- 🌐 **Web Interface** - Optional Streamlit-based GUI

*Stay tuned for updates!* 🚀

---

## 👨‍💻 Developed by

**Diego Fonte**  
*Full Stack Developer & Cybersecurity/AI Consultant*

Website: [diegofontedev.com.br](https://diegofontedev.com.br/)  
Contact: contato@diegofontedev.com.br

---

*"🎓 Digital security education for everyone."*