"""
CyberMentor AI - Aplicação Principal Web
Plataforma educacional de cibersegurança com interface Streamlit
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Adicionar diretório raiz para importações
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

# Configuração da página principal
st.set_page_config(
    page_title="CyberMentor AI - Cibersegurança",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');

/* Estilo cyberpunk para a página principal */
.main-header {
    background: linear-gradient(45deg, #0f0f23, #1a1a2e, #16213e);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    color: #00ff41;
    font-family: 'Orbitron', monospace;
    border: 2px solid #00ff41;
}

.main-header h1 {
    font-size: 3em;
    text-shadow: 0 0 20px #00ff41;
    margin-bottom: 10px;
}

.module-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 25px;
    border-radius: 20px;
    margin: 15px 0;
    color: white;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
    cursor: pointer;
    text-decoration: none;
}

.module-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 15px 40px rgba(102,126,234,0.4);
    text-decoration: none;
    color: white;
}

.footer {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
    color: #00ff41;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #00ff41;
    margin-top: 30px;
}

.footer a {
    color: #ff6b35;
    text-decoration: none;
    transition: all 0.3s ease;
}

.footer a:hover {
    color: #fff;
    text-shadow: 0 0 10px #ff6b35;
}
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🛡️ CyberMentor AI</h1>
    <p><strong>Plataforma Educacional de Cibersegurança</strong></p>
    <p>🎮 Aprenda brincando | 🔍 Casos reais | 🏆 Gamificação</p>
</div>
""", unsafe_allow_html=True)

# Descrição da plataforma
st.markdown("""
## 🎯 Bem-vindo ao Futuro da Educação em Cibersegurança!

Nossa plataforma revoluciona o aprendizado de segurança digital através de:
- **🎮 Jogos Interativos** - Aprenda hackeando (eticamente!)
- **📺 Análises de Séries** - Mr. Robot, Black Mirror e mais
- **💰 Casos Reais** - Prejuízos milionários que poderiam ser evitados
- **🔬 Tecnologia Futura** - Computação quântica e criptografia pós-quântica

### 🚀 Módulos Disponíveis

Escolha sua aventura abaixo:
""")

# Cards dos módulos
col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Laboratório de Criptografia", key="crypto_btn", help="Jogos, hashes, casos criminais reais"):
        st.switch_page("pages/1_🔐_Criptografia.py")
    
    if st.button("🕵️ Forense Digital", key="forensic_btn", help="Análise de arquivos, metadados e evidências"):
        st.switch_page("pages/4_🕵️_Forense_Digital.py")

with col2:
    st.button("🌐 Segurança Web (Em breve)", key="web_btn", disabled=True)
    st.button("🔍 Ferramentas de Rede (Em breve)", key="network_btn", disabled=True)

# Estatísticas impressionantes
st.markdown("---")
st.subheader("📊 Por que Cibersegurança Importa?")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💸 Custo médio de um hack", "$4.45M", "por vazamento (2023)")

with col2:
    st.metric("⏰ Tempo para detectar", "287 dias", "em média")

with col3:
    st.metric("📈 Crescimento anual", "+15.3%", "em custos de segurança")

with col4:
    st.metric("🎯 Taxa de sucesso", "95%", "ataques via engenharia social")

# Casos famosos
st.markdown("---")
st.subheader("🕵️ Você Sabia?")

caso_destaque = st.selectbox("Escolha um caso famoso:", [
    "💀 Equifax: $8 bilhões por não aplicar um patch grátis",
    "🛒 Target: Hackeado via empresa de ar-condicionado",
    "🏦 Bangladesh Bank: $81 milhões roubados por erro de digitação",
    "📺 Sony Pictures: Hackeado pela Coreia do Norte"
])

if "Equifax" in caso_destaque:
    st.error("**Equifax (2017):** 147 milhões de pessoas expostas. Custo: $8 bilhões. Causa: Não aplicaram um patch de segurança GRATUITO que estava disponível há 2 meses! 🤯")
elif "Target" in caso_destaque:
    st.warning("**Target (2013):** Hackers entraram via empresa terceirizada de ar-condicionado e roubaram 40 milhões de cartões. Prejuízo: +$1 bilhão durante o Natal! 🎄💀")
elif "Bangladesh" in caso_destaque:
    st.info("**Bangladesh Bank (2016):** Grupo Lazarus (Coreia do Norte) tentou roubar $1 bilhão via SWIFT. Conseguiram $81 milhões, mas um ERRO DE DIGITAÇÃO os impediu de levar o resto! 😱")
elif "Sony" in caso_destaque:
    st.error("**Sony Pictures (2014):** Hackers norte-coreanos deletaram TUDO dos servidores por causa do filme 'The Interview'. Vazaram emails embaraçosos de executivos! 🎬")

# Footer
st.markdown("""
<div class="footer">
    <p>🛡️ <strong>CyberMentor AI</strong> - Educação em Cibersegurança Revolucionária</p>
    <p>Desenvolvido por <strong>Diego Fonte</strong> | 
    <a href="https://www.diegofontedev.com.br" target="_blank">www.diegofontedev.com.br</a> | 
    <a href="https://zowti.com" target="_blank">zowti.com</a></p>
    <p><small>🎮 Onde aprender segurança digital nunca foi tão divertido!</small></p>
</div>
""", unsafe_allow_html=True)