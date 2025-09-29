"""
Digital Forensics Demo Module
Demonstrações de análise forense digital e investigação de arquivos
"""

import os
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import base64

class ForensicsDemo:
    """Demonstrações interativas de forense digital"""
    
    def __init__(self, console: Console):
        self.console = console
        
    async def run(self):
        """Loop principal dos demos de forense"""
        
        while True:
            self.show_forensics_menu()
            
            choice = Prompt.ask(
                "\n🕵️ Escolha o demo forense",
                choices=['1', '2', '3', '4', 'b'],
                default='b'
            )
            
            if choice == '1':
                await self.file_analysis_demo()
            elif choice == '2':
                await self.metadata_extraction_demo()
            elif choice == '3':
                await self.hash_verification_demo()
            elif choice == '4':
                await self.hidden_data_demo()
            elif choice == 'b':
                break
                
    def show_forensics_menu(self):
        """Exibe menu dos demos forenses"""
        
        menu_table = Table(
            title="🕵️ Laboratório de Forense Digital",
            box=box.ROUNDED,
            border_style="magenta"
        )
        
        menu_table.add_column("Opção", style="bold yellow", width=8)
        menu_table.add_column("Demo", style="bold white", width=25)
        menu_table.add_column("Aprenda Sobre", style="dim white", width=35)
        
        demos = [
            ("1", "Análise de Arquivos", "Identificação de tipos e propriedades"),
            ("2", "Extração de Metadados", "Informações ocultas em arquivos"),
            ("3", "Verificação de Integridade", "Hashes e detecção de alterações"),
            ("4", "Dados Ocultos", "Esteganografia e dados escondidos"),
            ("B", "Voltar ao Menu Principal", "Retornar à aplicação principal")
        ]
        
        for option, demo, description in demos:
            menu_table.add_row(option, demo, description)
            
        self.console.print("\n")
        self.console.print(menu_table, justify="center")
        
    async def file_analysis_demo(self):
        """Demo de análise de arquivos"""
        
        self.console.print(Panel(
            "📁 Análise Forense de Arquivos\n\n"
            "Análise detalhada de propriedades, tipo e características de arquivos.\n"
            "Fundamental para investigações digitais.",
            title="Análise de Arquivos",
            border_style="magenta"
        ))
        
        # Permitir usuário escolher arquivo ou criar exemplo
        choice = Prompt.ask(
            "\n📁 Escolha uma opção",
            choices=['1', '2'],
            default='2'
        )
        
        if choice == '1':
            file_path = Prompt.ask("Digite o caminho do arquivo")
            if not os.path.exists(file_path):
                self.console.print("❌ Arquivo não encontrado!")
                return
        else:
            # Criar arquivo de exemplo para análise
            example_content = """
CyberMentor AI - Arquivo de Exemplo para Análise Forense

Este arquivo foi criado para demonstrar técnicas de análise forense digital.
Contém informações básicas que podem ser extraídas durante uma investigação.

Data de criação: """ + datetime.now().isoformat() + """
Usuário: Demo User
Sistema: Windows/Linux/Mac

Dados importantes:
- Logs de acesso
- Configurações de sistema
- Evidências digitais
            """
            
            file_path = "exemplo_forense.txt"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(example_content.strip())
                
            self.console.print(f"✅ Arquivo de exemplo criado: {file_path}")
            
        # Análise do arquivo
        try:
            file_info = os.stat(file_path)
            
            # Tabela de análise
            analysis_table = Table(
                title=f"🔍 Análise Forense - {os.path.basename(file_path)}",
                box=box.ROUNDED,
                border_style="magenta"
            )
            
            analysis_table.add_column("Propriedade", style="bold cyan", width=20)
            analysis_table.add_column("Valor", style="white", width=35)
            analysis_table.add_column("Significado Forense", style="dim white", width=25)
            
            # Informações básicas do arquivo
            analysis_table.add_row(
                "Nome do Arquivo",
                os.path.basename(file_path),
                "Identidade do arquivo"
            )
            
            analysis_table.add_row(
                "Caminho Completo",
                os.path.abspath(file_path),
                "Localização no sistema"
            )
            
            analysis_table.add_row(
                "Tamanho",
                f"{file_info.st_size} bytes",
                "Volume de dados"
            )
            
            # Timestamps (cruciais para forense)
            analysis_table.add_row(
                "Criado em",
                datetime.fromtimestamp(file_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                "Quando foi criado"
            )
            
            analysis_table.add_row(
                "Modificado em",
                datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                "Última alteração"
            )
            
            analysis_table.add_row(
                "Acessado em",
                datetime.fromtimestamp(file_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
                "Último acesso"
            )
            
            # Tipo de arquivo
            mime_type, _ = mimetypes.guess_type(file_path)
            analysis_table.add_row(
                "Tipo MIME",
                mime_type or "Desconhecido",
                "Tipo de conteúdo"
            )
            
            # Permissões (Unix/Linux)
            try:
                permissions = oct(file_info.st_mode)[-3:]
                analysis_table.add_row(
                    "Permissões",
                    permissions,
                    "Controle de acesso"
                )
            except:
                analysis_table.add_row(
                    "Permissões",
                    "N/A (Windows)",
                    "Sistema Windows"
                )
                
            self.console.print("\n")
            self.console.print(analysis_table)
            
            # Hash do arquivo para integridade
            with open(file_path, 'rb') as f:
                file_content = f.read()
                md5_hash = hashlib.md5(file_content).hexdigest()
                sha256_hash = hashlib.sha256(file_content).hexdigest()
                
            hash_table = Table(
                title="🔐 Hashes de Integridade",
                box=box.SIMPLE,
                border_style="blue"
            )
            
            hash_table.add_column("Algoritmo", style="bold cyan", width=10)
            hash_table.add_column("Hash", style="white", width=50)
            hash_table.add_column("Uso Forense", style="dim white", width=20)
            
            hash_table.add_row("MD5", md5_hash, "Identificação rápida")
            hash_table.add_row("SHA256", sha256_hash, "Integridade garantida")
            
            self.console.print("\n")
            self.console.print(hash_table)
            
            # Limpeza do arquivo de exemplo
            if file_path == "exemplo_forense.txt":
                os.remove(file_path)
                
        except Exception as e:
            self.console.print(Panel(
                f"❌ Erro na análise: {str(e)}",
                title="Erro",
                border_style="red"
            ))
            
        # Guia educacional
        forensics_guide = """
🕵️ Princípios de Análise Forense:

📅 Timeline Analysis:
• Created: Quando o arquivo foi criado
• Modified: Última alteração do conteúdo
• Accessed: Último acesso de leitura
• Changed: Alteração de metadados

🔍 Tipos de Evidência:
• Documentos de texto: Conteúdo e autoria
• Imagens: EXIF data, localização GPS
• Logs: Registro de atividades
• Executáveis: Malware, backdoors

🛡️ Cadeia de Custódia:
• Hash para provar integridade
• Documentação de manuseio
• Timestamps precisos
• Cópias forenses bit-a-bit
        """
        
        self.console.print(Panel(forensics_guide.strip(), title="📚 Guia Forense", border_style="green"))
        
        Prompt.ask("\nPressione Enter para continuar")
        
    async def metadata_extraction_demo(self):
        """Demo de extração de metadados"""
        
        self.console.print(Panel(
            "📊 Extração de Metadados\n\n"
            "Metadados contêm informações valiosas sobre arquivos:\n"
            "autor, software usado, localização GPS, etc.",
            title="Extração de Metadados",
            border_style="blue"
        ))
        
        # Simular metadados de diferentes tipos de arquivo
        metadata_examples = {
            "Documento Word": {
                "Autor": "João Silva",
                "Software": "Microsoft Word 2019",
                "Data de Criação": "2023-10-15 14:30:00",
                "Última Modificação": "2023-10-16 09:15:00",
                "Tempo de Edição": "2 horas 45 minutos",
                "Empresa": "TechCorp Ltda",
                "Versão": "16.0.4266.1001"
            },
            "Foto Digital": {
                "Câmera": "Canon EOS R5",
                "ISO": "800",
                "Abertura": "f/2.8",
                "Velocidade": "1/200s",
                "GPS Latitude": "-23.5505° S",
                "GPS Longitude": "-46.6333° W",
                "Data/Hora": "2023-10-15 16:42:33",
                "Software": "Adobe Lightroom"
            },
            "PDF": {
                "Criador": "Adobe Acrobat Pro",
                "Título": "Relatório Confidencial",
                "Assunto": "Análise de Segurança",
                "Palavras-chave": "segurança, auditoria, compliance",
                "Data de Criação": "2023-10-14 10:00:00",
                "Modificado": "2023-10-15 15:30:00",
                "Páginas": "25"
            }
        }
        
        # Escolha do tipo de arquivo
        file_type = Prompt.ask(
            "📁 Escolha o tipo de arquivo para análise",
            choices=['word', 'foto', 'pdf'],
            default='foto'
        )
        
        type_map = {
            'word': 'Documento Word',
            'foto': 'Foto Digital', 
            'pdf': 'PDF'
        }
        
        selected_type = type_map[file_type]
        metadata = metadata_examples[selected_type]
        
        # Tabela de metadados
        metadata_table = Table(
            title=f"📊 Metadados Extraídos - {selected_type}",
            box=box.ROUNDED,
            border_style="blue"
        )
        
        metadata_table.add_column("Campo", style="bold cyan", width=20)
        metadata_table.add_column("Valor", style="white", width=30)
        metadata_table.add_column("Importância Forense", style="dim white", width=25)
        
        # Importância forense por campo
        forensic_importance = {
            "Autor": "👤 Identifica criador",
            "Software": "💻 Ambiente usado",
            "Data de Criação": "📅 Timeline crucial",
            "Última Modificação": "🔄 Alterações",
            "Tempo de Edição": "⏱️ Esforço investido",
            "Empresa": "🏢 Organização",
            "Câmera": "📷 Dispositivo origem",
            "GPS Latitude": "🌍 Localização exata",
            "GPS Longitude": "🌍 Localização exata",
            "Criador": "👨‍💻 Software criador",
            "Título": "📄 Identificação",
            "Assunto": "📝 Contexto",
            "Palavras-chave": "🔍 Classificação"
        }
        
        for campo, valor in metadata.items():
            importancia = forensic_importance.get(campo, "ℹ️ Informacional")
            metadata_table.add_row(campo, valor, importancia)
            
        self.console.print("\n")
        self.console.print(metadata_table)
        
        # Análise específica por tipo
        if file_type == 'foto':
            location_analysis = """
🌍 Análise de Localização GPS:

Coordenadas encontradas: -23.5505° S, -46.6333° W
📍 Localização: São Paulo, SP, Brasil
🏢 Região: Centro da cidade

🕵️ Valor Forense:
• Prova presença física em local específico
• Correlação com outros eventos
• Timeline de movimentação
• Contexto geográfico da evidência
            """
            
            self.console.print(Panel(location_analysis.strip(), title="🌍 Análise GPS", border_style="green"))
            
        elif file_type == 'word':
            authorship_analysis = """
👤 Análise de Autoria:

Autor identificado: João Silva
🏢 Empresa: TechCorp Ltda
⏱️ Tempo de edição: 2h45min

🕵️ Valor Forense:
• Identificação do autor original
• Vínculo com organização específica
• Tempo investido na criação
• Histórico de modificações
            """
            
            self.console.print(Panel(authorship_analysis.strip(), title="👤 Análise de Autoria", border_style="yellow"))
            
        # Guia de metadados
        metadata_guide = """
📊 Tipos de Metadados Importantes:

📄 Documentos Office:
• Autor, empresa, tempo de edição
• Versão do software, templates
• Histórico de revisões, comentários ocultos

📷 Imagens Digitais (EXIF):
• Modelo da câmera, configurações
• Data/hora precisa, GPS
• Software de edição usado

🎵 Arquivos de Áudio:
• Artista, álbum, gênero
• Software de gravação/edição
• Taxa de bits, duração

💻 Arquivos de Sistema:
• Datas de criação/modificação/acesso
• Usuário proprietário, permissões
• Assinatura digital, checksum
        """
        
        self.console.print(Panel(metadata_guide.strip(), title="📚 Guia de Metadados", border_style="purple"))
        
        Prompt.ask("\nPressione Enter para continuar")
        
    async def hash_verification_demo(self):
        """Demo de verificação de integridade com hashes"""
        
        self.console.print(Panel(
            "🔐 Verificação de Integridade de Arquivos\n\n"
            "Hashes provam que um arquivo não foi alterado.\n"
            "Fundamental para manter cadeia de custódia em forense.",
            title="Verificação de Integridade",
            border_style="green"
        ))
        
        # Criar arquivo de teste
        original_content = "EVIDÊNCIA DIGITAL - Arquivo original para teste de integridade"
        test_file = "teste_integridade.txt"
        
        with open(test_file, 'w') as f:
            f.write(original_content)
            
        # Hash original
        with open(test_file, 'rb') as f:
            file_data = f.read()
            original_md5 = hashlib.md5(file_data).hexdigest()
            original_sha256 = hashlib.sha256(file_data).hexdigest()
            
        self.console.print("✅ Arquivo de teste criado com conteúdo original")
        
        # Tabela com hashes originais
        original_table = Table(
            title="🔐 Hashes Originais (Linha de Base)",
            box=box.ROUNDED,
            border_style="green"
        )
        
        original_table.add_column("Algoritmo", style="bold cyan", width=10)
        original_table.add_column("Hash Original", style="white", width=50)
        original_table.add_column("Status", style="bold green", width=15)
        
        original_table.add_row("MD5", original_md5, "✅ BASELINE")
        original_table.add_row("SHA256", original_sha256, "✅ BASELINE")
        
        self.console.print("\n")
        self.console.print(original_table)
        
        # Simular alteração do arquivo
        self.console.print("\n🔄 Simulando alteração do arquivo...")
        
        choice = Prompt.ask(
            "Escolha o tipo de alteração",
            choices=['1', '2', '3'],
            default='2'
        )
        
        if choice == '1':
            # Alteração sutil
            modified_content = original_content + " "  # Apenas um espaço
            change_description = "Adicionado um espaço no final"
        elif choice == '2':
            # Alteração visível
            modified_content = original_content + " - ARQUIVO MODIFICADO"
            change_description = "Texto adicional visível"
        else:
            # Alteração de um byte
            modified_content = original_content.replace('E', 'e', 1)
            change_description = "Uma letra maiúscula alterada para minúscula"
            
        # Salvar arquivo modificado
        with open(test_file, 'w') as f:
            f.write(modified_content)
            
        # Calcular novos hashes
        with open(test_file, 'rb') as f:
            modified_data = f.read()
            new_md5 = hashlib.md5(modified_data).hexdigest()
            new_sha256 = hashlib.sha256(modified_data).hexdigest()
            
        # Comparação de hashes
        comparison_table = Table(
            title="🔍 Verificação de Integridade - Comparação",
            box=box.ROUNDED,
            border_style="red"
        )
        
        comparison_table.add_column("Algoritmo", style="bold cyan", width=10)
        comparison_table.add_column("Hash Original", style="dim white", width=32)
        comparison_table.add_column("Hash Atual", style="white", width=32)
        comparison_table.add_column("Status", style="bold", width=15)
        
        md5_status = "✅ ÍNTEGRO" if original_md5 == new_md5 else "🚨 ALTERADO"
        sha256_status = "✅ ÍNTEGRO" if original_sha256 == new_sha256 else "🚨 ALTERADO"
        
        comparison_table.add_row(
            "MD5", 
            original_md5[:30] + "...", 
            new_md5[:30] + "...", 
            md5_status
        )
        
        comparison_table.add_row(
            "SHA256",
            original_sha256[:30] + "...",
            new_sha256[:30] + "...",
            sha256_status
        )
        
        self.console.print("\n")
        self.console.print(comparison_table)
        
        # Análise da alteração
        if original_md5 != new_md5:
            alert_message = f"""
🚨 ALTERAÇÃO DETECTADA!

Modificação: {change_description}
Impacto: Integridade do arquivo comprometida
Status Legal: Evidência pode ser questionada

🕵️ Análise Forense:
• Arquivo foi modificado após hash inicial
• Cadeia de custódia comprometida
• Necessária nova documentação
• Hash anterior não é mais válido

⚖️ Implicações Legais:
• Evidência pode ser inadmissível
• Necessário justificar alteração
• Procedimentos de re-hash necessários
            """
            
            self.console.print(Panel(alert_message.strip(), title="🚨 Alerta de Integridade", border_style="red"))
        else:
            self.console.print(Panel(
                "✅ Arquivo mantém integridade\n"
                "Hash permanece inalterado\n"
                "Evidência preservada corretamente",
                title="✅ Integridade Verificada",
                border_style="green"
            ))
            
        # Limpeza
        os.remove(test_file)
        
        # Guia de boas práticas
        best_practices = """
🛡️ Boas Práticas de Integridade:

📋 Documentação Necessária:
• Hash imediatamente após coleta
• Registrar algoritmo usado (SHA256 recomendado)
• Timestamp preciso da operação
• Identificação do responsável

🔐 Múltiplos Algoritmos:
• MD5: Rápido mas vulnerável
• SHA1: Deprecated, evitar
• SHA256: Padrão atual recomendado
• SHA3: Próxima geração

📁 Armazenamento Seguro:
• Cópias em mídias write-protected
• Múltiplas cópias em locais separados
• Controle de acesso rigoroso
• Verificação periódica
        """
        
        self.console.print(Panel(best_practices.strip(), title="🛡️ Boas Práticas", border_style="blue"))
        
        Prompt.ask("\nPressione Enter para continuar")
        
    async def hidden_data_demo(self):
        """Demo de detecção de dados ocultos"""
        
        self.console.print(Panel(
            "🕵️ Detecção de Dados Ocultos\n\n"
            "Dados podem ser escondidos em arquivos usando várias técnicas:\n"
            "esteganografia, espaços em branco, campos não utilizados.",
            title="Dados Ocultos",
            border_style="cyan"
        ))
        
        # Demonstrar diferentes técnicas de ocultação
        techniques_table = Table(
            title="🎭 Técnicas de Ocultação de Dados",
            box=box.ROUNDED,
            border_style="cyan"
        )
        
        techniques_table.add_column("Técnica", style="bold cyan", width=20)
        techniques_table.add_column("Como Funciona", style="white", width=35)
        techniques_table.add_column("Detecção", style="dim white", width=25)
        
        techniques = [
            ("Esteganografia LSB", "Altera bits menos significativos", "Análise estatística"),
            ("Metadados Ocultos", "Dados em campos não visíveis", "Extração de metadados"),
            ("Espaços em Branco", "Usa espaços/tabs como código", "Análise de whitespace"),
            ("Comentários HTML", "Texto oculto em comentários", "Parsing de código"),
            ("Alternate Data Streams", "Streams NTFS alternativos", "Ferramentas específicas"),
            ("Arquivos Concatenados", "Múltiplos arquivos unidos", "Análise de assinaturas")
        ]
        
        for technique, how_it_works, detection in techniques:
            techniques_table.add_row(technique, how_it_works, detection)
            
        self.console.print("\n")
        self.console.print(techniques_table)
        
        # Demo interativo de dados ocultos
        demo_choice = Prompt.ask(
            "\n🔍 Escolha uma técnica para demonstrar",
            choices=['1', '2', '3'],
            default='2'
        )
        
        if demo_choice == '1':
            # Esteganografia simulada
            self.console.print("\n🎭 Demo: Esteganografia em Texto")
            
            visible_text = "Esta é uma mensagem normal"
            hidden_message = "DADOS SECRETOS"
            
            # Simular esconder dados alterando capitalização
            steganographic_text = ""
            hidden_index = 0
            
            for char in visible_text:
                if char.isalpha() and hidden_index < len(hidden_message):
                    # Use maiúscula para '1' e minúscula para '0' (ASCII simplificado)
                    hidden_char = hidden_message[hidden_index]
                    if ord(hidden_char) % 2 == 0:  # Par = maiúscula
                        steganographic_text += char.upper()
                    else:  # Ímpar = minúscula
                        steganographic_text += char.lower()
                    hidden_index += 1
                else:
                    steganographic_text += char
                    
            steg_demo = f"""
📝 Texto Original: {visible_text}
🎭 Texto com Dados Ocultos: {steganographic_text}
🔍 Dados Escondidos: {hidden_message}

💡 Técnica: Capitalização representa bits dos dados ocultos
🕵️ Detecção: Análise de padrões de capitalização anormais
            """
            
            self.console.print(Panel(steg_demo.strip(), title="🎭 Esteganografia Demo", border_style="purple"))
            
        elif demo_choice == '2':
            # Metadados ocultos
            self.console.print("\n📊 Demo: Metadados Ocultos")
            
            visible_metadata = {
                "Título": "Relatório Anual",
                "Autor": "João Silva",
                "Assunto": "Vendas e Marketing"
            }
            
            hidden_metadata = {
                "Custom_Field_1": "Projeto_Confidencial_X",
                "Internal_Code": "ALPHA-2023-SECRET",
                "Classification": "TOP_SECRET",
                "Real_Author": "Agente_007"
            }
            
            metadata_demo = f"""
👁️ Metadados Visíveis:
{chr(10).join([f'• {k}: {v}' for k, v in visible_metadata.items()])}

🕵️ Metadados Ocultos Encontrados:
{chr(10).join([f'• {k}: {v}' for k, v in hidden_metadata.items()])}

💡 Técnica: Campos customizados não exibidos em visualizadores normais
🔍 Detecção: Extração completa de todos os metadados
            """
            
            self.console.print(Panel(metadata_demo.strip(), title="📊 Metadados Ocultos", border_style="blue"))
            
        else:
            # Espaços em branco
            self.console.print("\n🔤 Demo: Dados em Espaços em Branco")
            
            normal_text = "Esta linha parece normal"
            # Simular espaços/tabs codificando dados
            hidden_text_with_spaces = "Esta linha parece normal    \t  \t\t   \t"
            
            # Decodificar espaços (espaço = 0, tab = 1)
            trailing_chars = hidden_text_with_spaces[len(normal_text):]
            binary_data = trailing_chars.replace(' ', '0').replace('\t', '1')
            
            whitespace_demo = f"""
📝 Texto Aparentemente Normal:
"{normal_text}"

🔍 Texto com Dados Ocultos:
"{hidden_text_with_spaces}"

💻 Caracteres Invisíveis Decodificados:
Espaços/Tabs: {repr(trailing_chars)}
Binário: {binary_data}
Possível Mensagem: [dados binários ocultos]

💡 Técnica: Espaços e tabs no final de linhas codificam dados
🕵️ Detecção: Visualização de whitespace ou análise hexadecimal
            """
            
            self.console.print(Panel(whitespace_demo.strip(), title="🔤 Whitespace Steganography", border_style="yellow"))
            
        # Ferramentas de detecção
        detection_tools = """
🛠️ Ferramentas para Detecção de Dados Ocultos:

📊 Análise de Metadados:
• ExifTool: Extração completa de metadados
• MediaInfo: Análise de arquivos multimídia
• strings: Busca por strings legíveis

🎭 Detecção de Esteganografia:
• StegDetect: Detecção automatizada
• StegBreak: Análise estatística
• Binwalk: Análise de assinaturas de arquivo

🔍 Análise Hexadecimal:
• HxD, Hex Workshop: Editores hexadecimais
• xxd: Visualização hex em linha de comando
• file: Identificação de tipos de arquivo

💻 Análise de Sistema de Arquivos:
• LADS: Alternate Data Streams (Windows)
• find: Busca avançada (Linux/Mac)
• PowerShell: Get-Item -Stream (Windows)
        """
        
        self.console.print(Panel(detection_tools.strip(), title="🛠️ Ferramentas de Detecção", border_style="green"))
        
        Prompt.ask("\nPressione Enter para continuar")