"""
CyberMentor AI - Módulo de Ferramentas de Rede
Laboratório interativo de ferramentas de rede e reconhecimento
"""

import streamlit as st
import socket
import subprocess
import time
import random
import json
import sys
import os
from pathlib import Path

# Adicionar diretório raiz para importações
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from web_app.utils.helpers import setup_page_config, load_custom_css, display_status_alert

# Configuração da página
setup_page_config()
load_custom_css()

# CSS básico e funcional
st.markdown("""
<style>
.main {
    background-color: #1a1a1a;
    color: #ffffff;
}

[data-testid="stExpander"] div[role="button"] {
    background-color: #2a2a2a !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
    border-radius: 5px !important;
    padding: 10px !important;
}

[data-testid="stExpander"] .streamlit-expanderContent {
    background-color: #2a2a2a !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
    border-top: none !important;
    border-radius: 0 0 5px 5px !important;
}

[data-testid="stExpander"] * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# CSS básico para ferramentas
st.markdown("""
<style>
.network-scanner {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.ping-result {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.port-scan-result {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.dns-lookup {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.hacker-console {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# Header da página
st.markdown("""
<div class="network-scanner">
    <h1>🔍 Arsenal de Ferramentas de Rede</h1>
    <p>Reconhecimento, scanning e mapeamento de redes como um pentester profissional</p>
    <p style="color: #ffffff;">⚡ Descubra todos os dispositivos e vulnerabilidades na rede!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar com navegação
st.sidebar.title("🎯 Ferramentas de Recon")
ferramenta_rede = st.sidebar.selectbox(
    "Escolha sua arma de reconhecimento:",
    [
        "🏠 Command Center",
        "📡 Network Discovery", 
        "🎯 Port Scanner Pro",
        "🔍 DNS Reconnaissance",
        "📊 Ping & Traceroute",
        "🕸️ Network Mapper", 
        "🔓 Service Enumeration",
        "📈 Traffic Analyzer",
        "🌐 OSINT Gathering",
        "🚨 Intrusion Detection",
        "🎮 CTF: Hack the Network",
        "🏆 Final Challenge"
    ]
)

# Inicializar estados da sessão
if 'pontos_rede' not in st.session_state:
    st.session_state.pontos_rede = 0
if 'hosts_descobertos' not in st.session_state:
    st.session_state.hosts_descobertos = []
if 'rank_pentester' not in st.session_state:
    st.session_state.rank_pentester = "Script Kiddie"

# Sistema de pontuação
def adicionar_pontos_rede(pontos, descricao):
    st.session_state.pontos_rede += pontos
    st.success(f"🏆 +{pontos} pontos! {descricao}")
    
    # Sistema de ranks
    if st.session_state.pontos_rede >= 1000:
        st.session_state.rank_pentester = "Elite Red Team"
    elif st.session_state.pontos_rede >= 500:
        st.session_state.rank_pentester = "Senior Pentester"
    elif st.session_state.pontos_rede >= 200:
        st.session_state.rank_pentester = "Network Ninja"
    elif st.session_state.pontos_rede >= 50:
        st.session_state.rank_pentester = "Junior Hacker"

# Status do usuário
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏆 Status do Pentester")
st.sidebar.metric("Pontos", st.session_state.pontos_rede)
st.sidebar.markdown(f"**Rank:** {st.session_state.rank_pentester}")
st.sidebar.metric("Hosts Descobertos", len(st.session_state.hosts_descobertos))

# ==============================================================================
# COMMAND CENTER
# ==============================================================================
if ferramenta_rede == "🏠 Command Center":
    st.markdown("""
    <div class="hacker-console">
        <h2>🚨 [NETWORK RECON SYSTEM ONLINE] 🚨</h2>
        <p>>>> Initializing network reconnaissance tools...</p>
        <p>>>> Loading Nmap, Wireshark, Metasploit modules...</p>
        <p>>>> Target network: 192.168.1.0/24</p>
        <p>>>> Status: READY TO SCAN</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🎯 Dashboard de Reconhecimento")
    
    # Estatísticas em tempo real
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🖥️ Hosts Ativos", "47", "+3")
    with col2:
        st.metric("🔓 Portas Abertas", "143", "+12")
    with col3:
        st.metric("🛡️ Firewalls", "8", "")
    with col4:
        st.metric("🚨 Vulnerabilidades", "23", "+5")
    
    # Mapa da rede interativo
    st.subheader("🗺️ Mapa da Rede")
    
    network_devices = {
        "192.168.1.1": {"tipo": "🌐 Router", "os": "Linux", "ports": "22,80,443"},
        "192.168.1.10": {"tipo": "💻 Desktop", "os": "Windows 10", "ports": "135,445,3389"},
        "192.168.1.15": {"tipo": "🖥️ Server", "os": "Ubuntu", "ports": "22,80,443,3306"},
        "192.168.1.25": {"tipo": "📱 IoT Device", "os": "Embedded", "ports": "80,8080"},
        "192.168.1.50": {"tipo": "🖨️ Printer", "os": "Unknown", "ports": "9100,631"}
    }
    
    for ip, info in network_devices.items():
        with st.expander(f"{info['tipo']} {ip}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**OS:** {info['os']}")
                st.write(f"**Ports:** {info['ports']}")
            with col2:
                if st.button(f"🎯 Scan {ip}", key=f"scan_{ip}"):
                    st.success(f"🔍 Scanning {ip}...")
                    adicionar_pontos_rede(10, f"Host {ip} scaneado!")
                    if ip not in st.session_state.hosts_descobertos:
                        st.session_state.hosts_descobertos.append(ip)

# ==============================================================================
# NETWORK DISCOVERY
# ==============================================================================
elif ferramenta_rede == "📡 Network Discovery":
    st.markdown("""
    <div class="network-scanner">
        <h1>📡 Network Discovery: Encontrando Alvos</h1>
        <p>Descubra todos os dispositivos na rede como um verdadeiro pentester</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulador de network discovery
    st.subheader("🎮 Simulador: Host Discovery")
    
    target_network = st.text_input(
        "🎯 Rede alvo (CIDR):",
        value="192.168.1.0/24",
        help="Ex: 192.168.1.0/24, 10.0.0.0/8"
    )
    
    scan_technique = st.selectbox(
        "🔍 Técnica de discovery:",
        [
            "ICMP Echo (Ping Sweep)",
            "TCP SYN Scan", 
            "UDP Scan",
            "ARP Scan (Local)",
            "TCP ACK Scan"
        ]
    )
    
    if st.button("🚀 INICIAR DISCOVERY"):
        st.markdown("""
        <div class="hacker-console">
            <h3>[SCANNING NETWORK...]</h3>
            <p>>>> Sending ICMP packets...</p>
            <p>>>> Analyzing responses...</p>
            <p>>>> Enumerating active hosts...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1)
        
        # Hosts "descobertos" (simulados)
        hosts_encontrados = [
            {"ip": "192.168.1.1", "mac": "00:11:22:33:44:55", "vendor": "Cisco", "response": "20ms"},
            {"ip": "192.168.1.10", "mac": "AA:BB:CC:DD:EE:FF", "vendor": "Dell", "response": "5ms"},
            {"ip": "192.168.1.15", "mac": "11:22:33:44:55:66", "vendor": "HP", "response": "12ms"},
            {"ip": "192.168.1.25", "mac": "FF:EE:DD:CC:BB:AA", "vendor": "IoT Corp", "response": "50ms"},
            {"ip": "192.168.1.50", "mac": "12:34:56:78:90:AB", "vendor": "Epson", "response": "30ms"}
        ]
        
        st.success(f"✅ Discovery completo! {len(hosts_encontrados)} hosts encontrados")
        
        # Mostrar resultados em tabela
        st.subheader("📋 Hosts Descobertos")
        
        for host in hosts_encontrados:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.write(f"**{host['ip']}**")
            with col2:
                st.code(host['mac'])
            with col3:
                st.write(host['vendor'])
            with col4:
                st.metric("Response", host['response'])
            with col5:
                if st.button("🎯 Scan", key=f"scan_host_{host['ip']}"):
                    adicionar_pontos_rede(15, f"Host {host['ip']} adicionado ao escopo!")
                    if host['ip'] not in st.session_state.hosts_descobertos:
                        st.session_state.hosts_descobertos.append(host['ip'])
        
        # Export dos resultados
        if st.button("💾 Exportar Resultados"):
            results_json = json.dumps(hosts_encontrados, indent=2)
            st.download_button(
                "📥 Download JSON",
                results_json,
                "network_discovery.json",
                "application/json"
            )

# ==============================================================================
# PORT SCANNER PRO
# ==============================================================================
elif ferramenta_rede == "🎯 Port Scanner Pro":
    st.markdown("""
    <div class="network-scanner">
        <h1>🎯 Port Scanner Pro: Mapeando Serviços</h1>
        <p>Scanner de portas profissional com detecção de serviços e OS</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Configurações do scan
    col1, col2 = st.columns(2)
    
    with col1:
        target_host = st.text_input("🎯 Host alvo:", value="192.168.1.10")
        port_range = st.text_input("🔢 Range de portas:", value="1-1000")
        
    with col2:
        scan_type = st.selectbox(
            "🔍 Tipo de scan:",
            ["TCP SYN (Stealth)", "TCP Connect", "UDP Scan", "ACK Scan", "FIN Scan"]
        )
        scan_speed = st.slider("⚡ Velocidade:", 1, 5, 3)
    
    if st.button("🚀 EXECUTAR PORT SCAN"):
        st.markdown(f"""
        <div class="hacker-console">
            <h3>[PORT SCANNING {target_host}]</h3>
            <p>>>> Scanning ports {port_range}</p>
            <p>>>> Using {scan_type} technique</p>
            <p>>>> Speed level: {scan_speed}/5</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress com velocidade baseada no slider
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01 * (6 - scan_speed))  # Mais rápido = menos delay
            progress.progress(i + 1)
        
        # Portas "encontradas" (simuladas)
        portas_abertas = [
            {"porta": 22, "protocolo": "TCP", "servico": "SSH", "versao": "OpenSSH 8.2", "estado": "open"},
            {"porta": 80, "protocolo": "TCP", "servico": "HTTP", "versao": "Apache 2.4.41", "estado": "open"},
            {"porta": 443, "protocolo": "TCP", "servico": "HTTPS", "versao": "Apache 2.4.41", "estado": "open"},
            {"porta": 3306, "protocolo": "TCP", "servico": "MySQL", "versao": "MySQL 8.0.25", "estado": "open"},
            {"porta": 21, "protocolo": "TCP", "servico": "FTP", "versao": "vsftpd 3.0.3", "estado": "filtered"}
        ]
        
        st.success(f"✅ Scan completo! {len([p for p in portas_abertas if p['estado'] == 'open'])} portas abertas")
        
        # Resultados detalhados
        st.subheader("🔍 Portas e Serviços Encontrados")
        
        for porta in portas_abertas:
            estado_color = "green" if porta['estado'] == "open" else "orange"
            
            st.markdown(f"""
            <div class="port-scan-result">
                <h4 style="color: {estado_color};">
                    Port {porta['porta']}/{porta['protocolo']} - {porta['estado'].upper()}
                </h4>
                <p><strong>Serviço:</strong> {porta['servico']}</p>
                <p><strong>Versão:</strong> {porta['versao']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if porta['estado'] == 'open' and st.button(f"🔍 Enumerar {porta['servico']}", key=f"enum_{porta['porta']}"):
                adicionar_pontos_rede(20, f"Serviço {porta['servico']} enumerado!")
                
                if porta['servico'] == "SSH":
                    st.info("🔐 **SSH Enumeration:** Usuários válidos: root, admin, guest")
                elif porta['servico'] == "HTTP":
                    st.info("🌐 **HTTP Enumeration:** /admin, /phpmyadmin, /wp-admin encontrados")
                elif porta['servico'] == "MySQL":
                    st.warning("⚠️ **MySQL Enumeration:** Login anônimo permitido!")

# ==============================================================================
# DNS RECONNAISSANCE  
# ==============================================================================
elif ferramenta_rede == "🔍 DNS Reconnaissance":
    st.markdown("""
    <div class="network-scanner">
        <h1>🔍 DNS Reconnaissance: Intel Gathering</h1>
        <p>Colete informações valiosas através de consultas DNS</p>
    </div>
    """, unsafe_allow_html=True)
    
    # DNS Lookup simulado
    target_domain = st.text_input("🌐 Domínio alvo:", value="example.com")
    
    dns_record_type = st.selectbox(
        "📋 Tipo de registro:",
        ["A (IPv4)", "AAAA (IPv6)", "MX (Mail)", "NS (Name Server)", "TXT (Text)", "CNAME", "SOA"]
    )
    
    if st.button("🔍 CONSULTAR DNS"):
        st.markdown(f"""
        <div class="hacker-console">
            <h3>[DNS LOOKUP: {target_domain}]</h3>
            <p>>>> Querying {dns_record_type} records...</p>
            <p>>>> Analyzing DNS responses...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Resultados DNS simulados
        dns_results = {
            "A (IPv4)": ["93.184.216.34", "192.0.2.1"],
            "MX (Mail)": ["10 mail.example.com", "20 mail2.example.com"],
            "NS (Name Server)": ["ns1.example.com", "ns2.example.com"],
            "TXT (Text)": ["v=spf1 include:_spf.google.com ~all", "google-site-verification=abc123"],
            "CNAME": ["www.example.com"],
            "SOA": ["ns1.example.com admin.example.com 2021120101"]
        }
        
        if dns_record_type in dns_results:
            st.success(f"✅ Registros {dns_record_type} encontrados!")
            
            for record in dns_results[dns_record_type]:
                st.markdown(f"""
                <div class="dns-lookup">
                    <code>{record}</code>
                </div>
                """, unsafe_allow_html=True)
            
            adicionar_pontos_rede(10, f"DNS {dns_record_type} enumerado!")
    
    # DNS Bruteforce simulator
    st.markdown("---")
    st.subheader("🎯 DNS Subdomain Bruteforce")
    
    wordlist = st.selectbox(
        "📝 Wordlist:",
        ["common.txt (100 palavras)", "medium.txt (1000 palavras)", "large.txt (10000 palavras)"]
    )
    
    if st.button("🚀 BRUTEFORCE SUBDOMAINS"):
        st.markdown("""
        <div class="hacker-console">
            <h3>[SUBDOMAIN BRUTEFORCE]</h3>
            <p>>>> Loading wordlist...</p>
            <p>>>> Testing subdomains...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)
        
        # Subdomains "encontrados"
        subdomains_found = [
            "www.example.com",
            "mail.example.com", 
            "ftp.example.com",
            "admin.example.com",
            "test.example.com"
        ]
        
        st.success(f"✅ {len(subdomains_found)} subdomains encontrados!")
        
        for subdomain in subdomains_found:
            if st.button(f"🎯 Scan {subdomain}", key=f"scan_sub_{subdomain}"):
                adicionar_pontos_rede(15, f"Subdomain {subdomain} adicionado!")

# ==============================================================================
# CTF: HACK THE NETWORK
# ==============================================================================
elif ferramenta_rede == "🎮 CTF: Hack the Network":
    st.markdown("""
    <div class="network-scanner">
        <h1>🎮 CTF Challenge: Hack the Corporate Network</h1>
        <p>Desafio final! Penetre na rede corporativa e capture as flags</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sistema de CTF por etapas
    if 'ctf_stage' not in st.session_state:
        st.session_state.ctf_stage = 1
    
    if st.session_state.ctf_stage == 1:
        st.subheader("🎯 Etapa 1: Network Reconnaissance")
        
        st.markdown("""
        **Objetivo:** Descubra quantos hosts estão ativos na rede 10.0.1.0/24
        
        **Dica:** Use network discovery para mapear a rede
        """)
        
        resposta1 = st.number_input("Quantos hosts ativos você encontrou?", min_value=1, max_value=255)
        
        if st.button("🚀 Submeter Resposta Etapa 1"):
            if resposta1 == 23:  # Resposta correta
                st.success("✅ **FLAG CAPTURADA!** flag{network_mapped_23_hosts}")
                st.session_state.ctf_stage = 2
                adicionar_pontos_rede(100, "CTF Etapa 1 completa!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Resposta incorreta! Continue escaneando...")
    
    elif st.session_state.ctf_stage == 2:
        st.subheader("🔓 Etapa 2: Service Enumeration")
        
        st.markdown("""
        **Objetivo:** Encontre o serviço vulnerável rodando no host 10.0.1.15
        
        **Dica:** Faça um port scan completo e procure por serviços desatualizados
        """)
        
        servico_vulneravel = st.selectbox(
            "Qual serviço vulnerável você encontrou?",
            ["SSH v1.0", "Apache 1.3.37", "FTP vsftpd 2.3.4", "MySQL 4.0"]
        )
        
        if st.button("🎯 Submeter Etapa 2"):
            if "vsftpd 2.3.4" in servico_vulneravel:
                st.success("✅ **FLAG CAPTURADA!** flag{ftp_backdoor_vsftpd234}")
                st.session_state.ctf_stage = 3
                adicionar_pontos_rede(150, "CTF Etapa 2 completa!")
                st.balloons()
            else:
                st.error("❌ Serviço incorreto! Continue enumerando...")
    
    elif st.session_state.ctf_stage == 3:
        st.subheader("💀 Etapa 3: Exploitation")
        
        st.markdown("""
        **Objetivo:** Explore a vulnerabilidade encontrada e obtenha acesso
        
        **Dica:** O vsftpd 2.3.4 tem uma backdoor famosa ativada pelo smile :)
        """)
        
        exploit_payload = st.text_input("Digite o payload de exploit:", placeholder="USER malicious:)")
        
        if st.button("💥 EXECUTAR EXPLOIT"):
            if ":)" in exploit_payload:
                st.success("🏆 **NETWORK PWNED!** Você dominou a rede corporativa!")
                st.balloons()
                
                st.markdown("""
                <div style="background: linear-gradient(45deg, #ff6b35, #f7931e); padding: 20px; border-radius: 10px; text-align: center;">
                    <h2 style="color: white;">🎉 CTF COMPLETADO!</h2>
                    <p style="color: white; font-size: 1.2em;">Flag final: flag{corporate_network_compromised}</p>
                    <p style="color: white;">🏆 TÍTULO: NETWORK PENETRATION MASTER 🏆</p>
                </div>
                """, unsafe_allow_html=True)
                
                adicionar_pontos_rede(300, "CTF COMPLETADO! Rede comprometida!")
                st.session_state.rank_pentester = "Network Penetration Master"
            else:
                st.error("❌ Exploit falhou! Verifique o payload...")
    
    # Reset do CTF
    if st.button("🔄 Resetar CTF"):
        st.session_state.ctf_stage = 1
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="background-color: #2a2a2a; color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #444444; margin: 15px 0; text-align: center;">
    <p>🔍 <strong>CyberMentor AI</strong> - Arsenal de Ferramentas de Rede</p>
    <p>Desenvolvido por <strong>Diego Fonte</strong> | ZowTi Solutions</p>
    <p><small>⚠️ Use apenas para fins educacionais e em redes próprias ou com autorização.</small></p>
</div>
""", unsafe_allow_html=True)