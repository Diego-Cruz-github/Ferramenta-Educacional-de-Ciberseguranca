"""
Módulo de Forense Digital - CyberMentor AI
Análise de arquivos, metadados e evidências digitais
"""

import streamlit as st
import os
import hashlib
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    st.warning("⚠️ python-magic não instalado. Detecção de tipo será limitada.")
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
from datetime import datetime
import io
import mimetypes

# Configuração da página
st.set_page_config(
    page_title="🕵️ Forense Digital - CyberMentor AI",
    page_icon="🕵️",
    layout="wide"
)

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

# CSS básico
st.markdown("""
<style>
.forensic-header {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    text-align: center;
    margin: 15px 0;
}

.evidence-card {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.analysis-result {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.warning-box {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}

.success-box {
    background-color: #2a2a2a;
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444444;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="forensic-header">
    <h1>🕵️ Laboratório de Forense Digital</h1>
    <p><strong>Investigação e Análise de Evidências Digitais</strong></p>
    <p>🔍 Metadados | 📁 Tipos de Arquivo | 🔐 Hashes</p>
</div>
""", unsafe_allow_html=True)

# Função para calcular hashes
def calcular_hashes(arquivo_bytes):
    """Calcula MD5, SHA1 e SHA256 do arquivo"""
    md5 = hashlib.md5(arquivo_bytes).hexdigest()
    sha1 = hashlib.sha1(arquivo_bytes).hexdigest()
    sha256 = hashlib.sha256(arquivo_bytes).hexdigest()
    return md5, sha1, sha256

# Função para extrair metadados EXIF
def extrair_exif(imagem):
    """Extrai metadados EXIF de imagens"""
    try:
        exifdata = imagem.getexif()
        metadados = {}
        
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode('utf-8', errors='ignore')
            metadados[tag] = data
            
        return metadados
    except Exception as e:
        return {"Erro": str(e)}

# Função para detectar tipo de arquivo
def detectar_tipo_arquivo(arquivo_bytes, nome_arquivo):
    """Detecta o tipo real do arquivo baseado no conteúdo"""
    try:
        # Tipo baseado na extensão
        tipo_extensao, _ = mimetypes.guess_type(nome_arquivo)
        
        if MAGIC_AVAILABLE:
            # Usando python-magic para detecção precisa
            tipo_real = magic.from_buffer(arquivo_bytes, mime=True)
        else:
            # Fallback: detecção básica por magic numbers
            magic_numbers = {
                b'\xFF\xD8\xFF': 'image/jpeg',
                b'\x89PNG': 'image/png',
                b'GIF87a': 'image/gif',
                b'GIF89a': 'image/gif',
                b'PK\x03\x04': 'application/zip',
                b'%PDF': 'application/pdf',
                b'MZ': 'application/x-executable'
            }
            
            tipo_real = "application/octet-stream"  # default
            for magic_bytes, mime_type in magic_numbers.items():
                if arquivo_bytes.startswith(magic_bytes):
                    tipo_real = mime_type
                    break
        
        return tipo_real, tipo_extensao
    except Exception as e:
        return f"Erro: {str(e)}", tipo_extensao

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Análise de Arquivo", "📊 Casos Famosos", "🎮 Jogo Forense", "📚 Teoria"])

with tab1:
    st.subheader("📁 Upload e Análise de Evidência")
    
    arquivo_upload = st.file_uploader(
        "Selecione um arquivo para análise forense:",
        type=None,  # Aceita qualquer tipo
        help="⚠️ Para fins educacionais apenas. Não faça upload de dados sensíveis reais!"
    )
    
    if arquivo_upload is not None:
        # Ler bytes do arquivo
        arquivo_bytes = arquivo_upload.read()
        tamanho_arquivo = len(arquivo_bytes)
        
        st.markdown("""
        <div class="evidence-card">
            <h3>📋 Informações Básicas da Evidência</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📄 Nome do Arquivo", arquivo_upload.name)
            
        with col2:
            st.metric("📏 Tamanho", f"{tamanho_arquivo:,} bytes")
            
        with col3:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.metric("⏰ Análise em", timestamp)
        
        # Análise de hashes
        st.markdown("""
        <div class="evidence-card">
            <h3>🔐 Análise Criptográfica</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Calculando hashes..."):
            md5, sha1, sha256 = calcular_hashes(arquivo_bytes)
        
        st.markdown(f"""
        <div class="analysis-result">
        <strong>MD5:</strong> {md5}<br>
        <strong>SHA1:</strong> {sha1}<br>
        <strong>SHA256:</strong> {sha256}
        </div>
        """, unsafe_allow_html=True)
        
        # Detecção de tipo de arquivo
        st.markdown("""
        <div class="evidence-card">
            <h3>🔍 Análise de Tipo de Arquivo</h3>
        </div>
        """, unsafe_allow_html=True)
        
        tipo_real, tipo_extensao = detectar_tipo_arquivo(arquivo_bytes, arquivo_upload.name)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Tipo por Extensão:** {tipo_extensao or 'Desconhecido'}")
        with col2:
            st.info(f"**Tipo Real (Magic Number):** {tipo_real}")
        
        # Verificar se há discrepância
        if tipo_extensao and tipo_real and tipo_extensao != tipo_real:
            st.markdown("""
            <div class="warning-box">
                ⚠️ ALERTA: Discrepância detectada entre extensão e conteúdo real do arquivo!
                Possível tentativa de mascaramento de arquivo malicioso.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="success-box">
                ✅ Tipo de arquivo consistente - Nenhuma discrepância detectada.
            </div>
            """, unsafe_allow_html=True)
        
        # Análise específica para imagens
        if tipo_real and tipo_real.startswith('image/'):
            st.markdown("""
            <div class="evidence-card">
                <h3>📸 Análise de Metadados EXIF</h3>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                imagem = Image.open(io.BytesIO(arquivo_bytes))
                metadados = extrair_exif(imagem)
                
                if metadados and len(metadados) > 1:
                    # Criar DataFrame para exibir metadados
                    df_metadados = pd.DataFrame(list(metadados.items()), columns=['Campo', 'Valor'])
                    st.dataframe(df_metadados, use_container_width=True)
                    
                    # Verificar dados sensíveis
                    campos_sensíveis = ['GPS', 'DateTime', 'Make', 'Model', 'Software']
                    dados_encontrados = [campo for campo in campos_sensíveis if any(campo.lower() in str(k).lower() for k in metadados.keys())]
                    
                    if dados_encontrados:
                        st.warning(f"🔍 **Dados potencialmente sensíveis encontrados:** {', '.join(dados_encontrados)}")
                        st.info("💡 **Dica forense:** Metadados podem revelar localização, dispositivo usado, software e horários!")
                else:
                    st.info("📝 Nenhum metadado EXIF encontrado na imagem.")
                    
            except Exception as e:
                st.error(f"Erro ao processar imagem: {str(e)}")
        
        # Análise hexadecimal (primeiros bytes)
        st.markdown("""
        <div class="evidence-card">
            <h3>🔢 Análise Hexadecimal (Magic Numbers)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        primeiros_bytes = arquivo_bytes[:32]
        hex_string = ' '.join(f'{byte:02X}' for byte in primeiros_bytes)
        
        st.markdown(f"""
        <div class="analysis-result">
        <strong>Primeiros 32 bytes (HEX):</strong><br>
        {hex_string}
        </div>
        """, unsafe_allow_html=True)
        
        # Interpretação dos magic numbers
        magic_numbers = {
            'FFD8FF': 'JPEG Image',
            '89504E': 'PNG Image', 
            '474946': 'GIF Image',
            '504B03': 'ZIP/Office Document',
            '255044': 'PDF Document',
            '4D5A90': 'Windows Executable',
            '7F454C': 'Linux Executable (ELF)'
        }
        
        hex_inicio = hex_string.replace(' ', '')[:6]
        if hex_inicio in magic_numbers:
            st.success(f"🎯 **Magic Number identificado:** {magic_numbers[hex_inicio]}")
        else:
            st.info("🔍 Magic number não reconhecido na base de dados.")

with tab2:
    st.subheader("📊 Casos Famosos de Forense Digital")
    
    caso_selecionado = st.selectbox("Escolha um caso famoso:", [
        "🔍 BTK Killer - Caught by Metadata",
        "💻 Anna Politkovskaya - Hard Drive Analysis", 
        "📱 San Bernardino iPhone - FBI vs Apple",
        "🌐 Silk Road - Ross Ulbricht Digital Evidence"
    ])
    
    if "BTK" in caso_selecionado:
        st.markdown("""
        <div class="evidence-card">
            <h3>🔍 Caso BTK Killer (Dennis Rader)</h3>
            <p><strong>Ano:</strong> 2005</p>
            <p><strong>Como foi pego:</strong> Metadados em documento do Word!</p>
            <p><strong>Evidência chave:</strong> Rader enviou um disquete para a polícia. 
            Os investigadores encontraram metadados no arquivo Word que continham:</p>
            <ul>
                <li>Nome do usuário: "Dennis"</li>
                <li>Última modificação: Igreja Luterana Christ</li>
                <li>Software usado: Microsoft Word</li>
            </ul>
            <p><strong>Resultado:</strong> Prisão após 30 anos! 10 assassinatos solucionados.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning("💡 **Lição:** Nunca subestime o poder dos metadados! Eles podem conter mais informações do que você imagina.")
    
    elif "Anna" in caso_selecionado:
        st.markdown("""
        <div class="evidence-card">
            <h3>💻 Caso Anna Politkovskaya</h3>
            <p><strong>Ano:</strong> 2006</p>
            <p><strong>Vítima:</strong> Jornalista russa assassinada</p>
            <p><strong>Evidência digital:</strong> Análise forense do HD encontrou:</p>
            <ul>
                <li>Artigos deletados sobre corrupção</li>
                <li>Comunicações com fontes</li>
                <li>Rastros de vigilância digital</li>
                <li>Arquivos "apagados" recuperados</li>
            </ul>
            <p><strong>Técnica:</strong> Recuperação de dados deletados e análise de slack space.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔍 **Técnica forense:** Quando você 'deleta' um arquivo, apenas o ponteiro é removido. Os dados continuam no disco até serem sobrescritos!")

with tab3:
    st.subheader("🎮 Jogo: Detetive Digital")
    
    st.markdown("""
    <div class="evidence-card">
        <h3>🕵️ Cenário: Investigação de Vazamento de Dados</h3>
        <p>Você é um investigador forense digital. Uma empresa teve dados vazados e suspeita de um funcionário interno.</p>
        <p><strong>Evidência:</strong> Um arquivo suspeito foi encontrado no computador do suspeito.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulação de evidência
    if st.button("🔍 Analisar Evidência Simulada"):
        st.markdown("""
        <div class="analysis-result">
        <strong>📁 EVIDÊNCIA DIGITAL SIMULADA</strong><br><br>
        <strong>Nome:</strong> relatorio_vendas.xlsx<br>
        <strong>Tamanho:</strong> 2,847,392 bytes<br>
        <strong>MD5:</strong> a1b2c3d4e5f6789...<br>
        <strong>Criado:</strong> 2024-01-15 23:47:32<br>
        <strong>Modificado:</strong> 2024-01-16 02:15:44<br>
        <strong>Acessado:</strong> 2024-01-16 08:30:12<br><br>
        <strong>⚠️ DESCOBERTA:</strong> Arquivo foi modificado às 2:15 AM!<br>
        <strong>📧 METADADOS:</strong> Último autor: "j.silva@empresa.com"<br>
        <strong>🔍 CONTEÚDO:</strong> 50,000 registros de clientes
        </div>
        """, unsafe_allow_html=True)
        
        pergunta = st.radio(
            "❓ Baseado na análise, qual é sua conclusão?",
            [
                "📋 Atividade normal - arquivo de trabalho rotineiro",
                "🚨 Suspeito - modificação fora do horário comercial", 
                "🔍 Inconclusivo - precisa de mais evidências",
                "💻 Possível acesso remoto malicioso"
            ]
        )
        
        if pergunta:
            if "Suspeito" in pergunta:
                st.success("🎯 **Correto!** Modificações às 2:15 AM são altamente suspeitas. Um funcionário normal não estaria trabalhando nesse horário.")
                st.info("🔍 **Próximo passo:** Verificar logs de rede, keyloggers e histórico de navegação do período.")
            elif "Inconclusivo" in pergunta:
                st.warning("🤔 **Parcialmente correto.** Embora sempre seja bom ter mais evidências, o horário já é um forte indicativo.")
            else:
                st.error("❌ **Incorreto.** Atividade às 2:15 AM em arquivo sensível é altamente suspeita!")

with tab4:
    st.subheader("📚 Teoria: Forense Digital")
    
    teoria_tab = st.selectbox("Escolha um tópico:", [
        "🔍 Princípios da Forense Digital",
        "🔐 Chain of Custody",
        "📁 Tipos de Evidência Digital",
        "⚖️ Aspectos Legais"
    ])
    
    if "Princípios" in teoria_tab:
        st.markdown("""
        ### 🔍 Os 4 Princípios Fundamentais
        
        **1. 🛡️ Preservação da Evidência**
        - Nunca alterar a evidência original
        - Trabalhar sempre com cópias bit-a-bit
        - Usar ferramentas write-blockers
        
        **2. 📋 Documentação Completa**
        - Registrar cada passo do processo
        - Fotografar a cena digital
        - Manter logs detalhados
        
        **3. 🔍 Análise Metódica**
        - Seguir procedimentos padronizados
        - Usar ferramentas validadas
        - Verificar integridade com hashes
        
        **4. ⚖️ Admissibilidade Legal**
        - Seguir normas jurídicas
        - Manter chain of custody
        - Documentar qualificações do perito
        """)
    
    elif "Chain of Custody" in teoria_tab:
        st.markdown("""
        ### 🔐 Cadeia de Custódia Digital
        
        **O que é:**
        Documentação cronológica de quem teve acesso à evidência digital.
        
        **Elementos essenciais:**
        - 👤 **Quem:** Pessoa responsável
        - 📅 **Quando:** Data e horário exatos  
        - 📍 **Onde:** Local de armazenamento
        - 🔍 **O que:** Tipo de evidência
        - ❓ **Por que:** Motivo do acesso
        - 🛠️ **Como:** Método utilizado
        
        **❌ Quebra da cadeia = Evidência inadmissível!**
        """)

# Rodapé
st.markdown("---")
st.markdown("""
<div class="evidence-card">
    <h3>⚖️ Aviso Legal</h3>
    <p>🚨 <strong>Este módulo é apenas para fins educacionais!</strong></p>
    <p>• Não faça upload de dados sensíveis ou confidenciais reais</p>
    <p>• Use apenas em ambientes controlados para aprendizado</p>
    <p>• Sempre respeite a privacidade e leis aplicáveis</p>
    <p>• Em casos reais, consulte sempre um perito forense certificado</p>
</div>
""", unsafe_allow_html=True)