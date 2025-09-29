# CyberMentor AI - Ferramenta Educacional de Cibersegurança

**Aplicação terminal educacional em Python para aprendizado prático de conceitos de cibersegurança com IA integrada.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://python.org)
[![Security](https://img.shields.io/badge/Security-Educational-green?logo=shield&logoColor=white)](https://github.com/Diego-Cruz-github/Ferramenta-Educacional-de-Ciberseguranca)
[![AI Powered](https://img.shields.io/badge/AI-GROQ%20Integrated-purple?logo=openai&logoColor=white)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white)](LICENSE)

---

## Sobre o Projeto

**CyberMentor AI** é uma ferramenta educacional terminal que ensina conceitos básicos de **cibersegurança** através de demonstrações práticas e chat IA integrado.

### Funcionalidades Implementadas

- **Laboratório de Criptografia Completo**: 5 demos interativos (hashes, passwords, encryption, rainbow tables, crypto analysis)
- **Demos de Segurança Web**: Análise HTTP headers, SQL injection e XSS educacional
- **Ferramentas de Rede**: Port scanning, ping, DNS lookup e análise de configuração
- **Forense Digital**: Análise de arquivos, extração de metadados e detecção de dados ocultos
- **Chat IA Especializado**: Explicações com GROQ API + modo offline
- **Interface Terminal Rica**: Menus coloridos com biblioteca Rich

---

## Tecnologias Utilizadas

- **Python 3.9+** - Linguagem principal
- **Rich** - Interface terminal colorida e tabelas
- **Typer** - Framework CLI moderno
- **GROQ API** - IA para chat especializado
- **Cryptography** - Demos de encryption/decryption
- **bcrypt** - Hashing seguro de passwords
- **aiohttp** - Client HTTP assíncrono

---

## Estrutura do Projeto

```
Ferramenta-Educacional-de-Ciberseguranca/
├── main.py                    # Aplicação principal
├── requirements.txt           # Dependências
│
├── core/                      # Módulos principais
│   ├── ai_mentor.py          # Chat IA com GROQ
│   └── menu_system.py        # Interface de menus
│
└── demos/                     # Demonstrações educacionais
    ├── crypto_demo.py        # Laboratório de criptografia
    ├── web_demo.py           # Segurança web
    ├── network_demo.py       # Ferramentas de rede
    └── forensics_demo.py     # Forense digital
```

---

## Como Usar

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Diego-Cruz-github/Ferramenta-Educacional-de-Ciberseguranca.git
cd Ferramenta-Educacional-de-Ciberseguranca

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute
python main.py
```

### Configuração do Chat IA (Opcional)

```bash
# Com GROQ API key
export GROQ_API_KEY="sua_chave"
python main.py

# Sem API (modo offline)
python main.py
```

**Como obter chave GROQ gratuita:**
1. Acesse [console.groq.com](https://console.groq.com)
2. Crie conta e gere API key
3. 100 requisições grátis por dia

### Menu Principal

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

### Laboratório de Criptografia

**5 demonstrações interativas disponíveis:**

1. **Hash Functions** - Comparação MD5, SHA1, SHA256, SHA512
2. **Password Security** - Hashing, salting, bcrypt  
3. **Symmetric Encryption** - AES encryption/decryption
4. **Rainbow Table Attack** - Como funcionam e defesas
5. **Crypto Analysis** - Efeito avalanche e propriedades

### Chat IA

- Perguntas sobre cibersegurança em português
- Explicações educacionais contextualizadas
- Funciona online (GROQ) ou offline (respostas pré-definidas)

---

## Conteúdo Educacional

### Laboratório de Criptografia (Implementado)

**Conceitos abordados:**
- **Funções Hash**: MD5, SHA1, SHA256, SHA512 - segurança e vulnerabilidades
- **Segurança de Senhas**: Salt, bcrypt, armazenamento seguro
- **Criptografia Simétrica**: AES encryption/decryption prática
- **Ataques Rainbow Table**: Como funcionam e defesas
- **Análise Criptográfica**: Efeito avalanche, resistência a colisões

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

## Chat IA Integrado

**Funcionalidades:**
- Chat educacional especializado em cibersegurança
- Explicações em português brasileiro
- Modo online (GROQ API) + fallback offline
- Respostas contextualizadas e éticas

**Exemplo de uso:**
```
Sua pergunta: O que é criptografia simétrica?

CyberMentor AI:
Criptografia simétrica usa a mesma chave para criptografar e descriptografar dados.

Exemplos: AES, DES, 3DES
Vantagens: Rápida, eficiente para grandes volumes
Desvantagens: Distribuição segura da chave é desafiadora

Use para: Criptografia de arquivos, comunicação onde as partes já compartilham chaves.
```

---

## Opções Avançadas

```bash
# Modo desenvolvedor com logs
python main.py --dev

# Especificar API key
python main.py --api-key "sua_chave_groq"
```

---

## Para Quem é Esta Ferramenta

- **Estudantes** iniciantes em cibersegurança
- **Desenvolvedores** querendo aprender security básica
- **Curiosos** sobre criptografia e segurança digital
- **Professores** buscando material educacional prático

---

## Licença

MIT License - Use livremente para fins educacionais.

---

## Aviso Legal

**Uso exclusivamente educacional.** Não use para atividades ilegais ou ataques não autorizados. O usuário é responsável pelo uso apropriado desta ferramenta.

---

## Desenvolvido por

**Diego Fonte**  
*Full Stack Developer & Cybersecurity/AI Consultant*

Website: [diegofontedev.com.br](https://diegofontedev.com.br/)  
Empresa: [zowti.com](https://zowti.com/)  
Contato: contato@diegofontedev.com.br

---

*"Educação em segurança digital para todos."*