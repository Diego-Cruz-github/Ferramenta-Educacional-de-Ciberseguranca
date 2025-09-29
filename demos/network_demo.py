"""
Network Security Demo Module  
Demonstrações de análise de rede e ferramentas de reconhecimento
"""

import socket
import subprocess
import platform
import ipaddress
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

class NetworkDemo:
    """Demonstrações interativas de segurança de rede"""
    
    def __init__(self, console: Console):
        self.console = console
        
    async def run(self):
        """Loop principal dos demos de rede"""
        
        while True:
            self.show_network_menu()
            
            choice = Prompt.ask(
                "\n🔍 Escolha o demo de rede",
                choices=['1', '2', '3', '4', 'b'],
                default='b'
            )
            
            if choice == '1':
                await self.port_scan_demo()
            elif choice == '2':
                await self.network_info_demo()
            elif choice == '3':
                await self.ping_demo()
            elif choice == '4':
                await self.dns_lookup_demo()
            elif choice == 'b':
                break
                
    def show_network_menu(self):
        """Exibe menu dos demos de rede"""
        
        menu_table = Table(
            title="🔍 Laboratório de Análise de Rede",
            box=box.ROUNDED,
            border_style="cyan"
        )
        
        menu_table.add_column("Opção", style="bold yellow", width=8)
        menu_table.add_column("Demo", style="bold white", width=25)
        menu_table.add_column("Aprenda Sobre", style="dim white", width=35)
        
        demos = [
            ("1", "Verificação de Portas", "Port scanning básico e análise de serviços"),
            ("2", "Informações de Rede", "Análise de configuração de rede local"),
            ("3", "Teste de Conectividade", "Ping e análise de latência"),
            ("4", "Consulta DNS", "Resolução de nomes e análise DNS"),
            ("B", "Voltar ao Menu Principal", "Retornar à aplicação principal")
        ]
        
        for option, demo, description in demos:
            menu_table.add_row(option, demo, description)
            
        self.console.print("\n")
        self.console.print(menu_table, justify="center")
        
    async def port_scan_demo(self):
        """Demo de verificação de portas"""
        
        self.console.print(Panel(
            "🔍 Demo de Verificação de Portas\n\n"
            "Port scanning identifica serviços rodando em um host.\n"
            "⚠️ Use apenas em sistemas próprios ou com autorização!",
            title="Verificação de Portas",
            border_style="cyan"
        ))
        
        target = Prompt.ask("\n🎯 Digite o alvo para scan", default="127.0.0.1")
        
        # Portas comuns para testar
        common_ports = [22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1433, 3306, 3389, 5432, 5900, 8080]
        
        self.console.print(f"\n🔍 Verificando portas em {target}...")
        
        # Tabela de resultados
        results_table = Table(
            title=f"📊 Resultados do Scan - {target}",
            box=box.SIMPLE,
            border_style="green"
        )
        
        results_table.add_column("Porta", style="bold cyan", width=8)
        results_table.add_column("Status", style="bold", width=12)
        results_table.add_column("Serviço", style="white", width=20)
        results_table.add_column("Descrição", style="dim white", width=30)
        
        # Mapeamento de serviços
        service_map = {
            22: ("SSH", "Secure Shell - Acesso remoto"),
            23: ("Telnet", "Acesso remoto não criptografado"),
            25: ("SMTP", "Envio de email"),
            53: ("DNS", "Resolução de nomes"),
            80: ("HTTP", "Web server não criptografado"),
            135: ("RPC", "Remote Procedure Call"),
            139: ("NetBios", "Compartilhamento Windows"),
            443: ("HTTPS", "Web server criptografado"),
            1433: ("MSSQL", "Microsoft SQL Server"),
            3306: ("MySQL", "MySQL Database Server"),
            3389: ("RDP", "Remote Desktop Protocol"),
            5432: ("PostgreSQL", "PostgreSQL Database"),
            8080: ("HTTP-Alt", "Web server porta alternativa")
        }
        
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    status = "✅ ABERTA"
                    service_name, description = service_map.get(port, ("Desconhecido", "Serviço não identificado"))
                    open_ports.append((port, service_name))
                else:
                    status = "❌ FECHADA"
                    service_name, description = service_map.get(port, ("N/A", "N/A"))
                    
                results_table.add_row(str(port), status, service_name, description)
                sock.close()
                
            except Exception:
                results_table.add_row(str(port), "🚫 ERRO", "N/A", "Erro na conexão")
                
        self.console.print("\n")
        self.console.print(results_table)
        
        # Resumo da análise
        analysis = f"""
📊 Análise do Port Scan:

🎯 Alvo: {target}
🔍 Portas verificadas: {len(common_ports)}
✅ Portas abertas: {len(open_ports)}
❌ Portas fechadas: {len(common_ports) - len(open_ports)}

🔓 Serviços identificados:
{chr(10).join([f'• Porta {port}: {service}' for port, service in open_ports]) if open_ports else '• Nenhum serviço comum detectado'}

⚠️ Considerações de segurança:
• Portas abertas podem ser pontos de entrada
• Serviços desnecessários devem ser desabilitados
• Use firewalls para controlar acesso
• Mantenha serviços atualizados
        """
        
        self.console.print(Panel(analysis.strip(), title="📊 Análise de Segurança", border_style="blue"))
        
        Prompt.ask("\nPressione Enter para continuar")
        
    async def network_info_demo(self):
        """Demo de informações de rede"""
        
        self.console.print(Panel(
            "🌐 Informações de Configuração de Rede\n\n"
            "Análise da configuração de rede local e interfaces disponíveis.",
            title="Configuração de Rede",
            border_style="blue"
        ))
        
        # Tabela de informações de rede
        network_table = Table(
            title="🌐 Configuração de Rede Local",
            box=box.ROUNDED,
            border_style="blue"
        )
        
        network_table.add_column("Componente", style="bold cyan", width=20)
        network_table.add_column("Informação", style="white", width=40)
        network_table.add_column("Detalhes", style="dim white", width=25)
        
        try:
            # Hostname
            hostname = socket.gethostname()
            network_table.add_row("Hostname", hostname, "Nome da máquina")
            
            # IP local
            local_ip = socket.gethostbyname(hostname)
            network_table.add_row("IP Local", local_ip, "Endereço IP principal")
            
            # Informações adicionais sobre a rede
            try:
                # Gateway padrão (tentativa)
                if platform.system() == "Windows":
                    import subprocess
                    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                    # Parsing básico para gateway (simplificado)
                    gateway = "Detectar manualmente"
                else:
                    # Linux/Mac
                    gateway = "Detectar manualmente"
                    
                network_table.add_row("Gateway Padrão", gateway, "Roteador de saída")
            except:
                network_table.add_row("Gateway Padrão", "Não detectado", "Erro na detecção")
                
            # DNS
            try:
                dns_resolver = socket.getfqdn()
                network_table.add_row("FQDN", dns_resolver, "Nome totalmente qualificado")
            except:
                network_table.add_row("FQDN", "Não disponível", "Erro na resolução")
                
            # Análise de rede privada
            try:
                ip_obj = ipaddress.ip_address(local_ip)
                if ip_obj.is_private:
                    network_type = "🏠 Rede Privada"
                    security_note = "Protegida por NAT"
                else:
                    network_type = "🌐 IP Público"
                    security_note = "Diretamente acessível"
                    
                network_table.add_row("Tipo de Rede", network_type, security_note)
            except:
                network_table.add_row("Tipo de Rede", "Não analisado", "Erro na análise")
                
        except Exception as e:
            network_table.add_row("Erro", str(e), "Falha na coleta")
            
        self.console.print("\n")
        self.console.print(network_table)
        
        # Análise de segurança da rede
        security_analysis = """
🔒 Análise de Segurança de Rede:

🏠 Redes Privadas (RFC 1918):
• 10.0.0.0/8 (10.x.x.x)
• 172.16.0.0/12 (172.16.x.x - 172.31.x.x)  
• 192.168.0.0/16 (192.168.x.x)

🛡️ Boas práticas de segurança:
• Use firewall para controlar tráfego
• Desabilite serviços desnecessários
• Mantenha sistema operacional atualizado
• Use VPN para conexões remotas seguras
• Configure DNS seguro (1.1.1.1, 8.8.8.8)

⚠️ Riscos comuns:
• Compartilhamentos abertos
• Senhas padrão em roteadores
• Firmware desatualizado
• Redes Wi-Fi abertas
        """
        
        self.console.print(Panel(security_analysis.strip(), title="🛡️ Segurança de Rede", border_style="green"))
        
        Prompt.ask("\nPressione Enter para continuar")
        
    async def ping_demo(self):
        """Demo de teste de conectividade"""
        
        self.console.print(Panel(
            "📡 Teste de Conectividade de Rede\n\n"
            "O ping testa a conectividade e mede a latência até um host remoto.",
            title="Teste de Ping",
            border_style="yellow"
        ))
        
        target = Prompt.ask("\n🎯 Digite o host para ping", default="8.8.8.8")
        
        # Executar ping baseado no SO
        try:
            system = platform.system().lower()
            if system == "windows":
                cmd = ["ping", "-n", "4", target]
            else:
                cmd = ["ping", "-c", "4", target]
                
            self.console.print(f"\n📡 Executando ping para {target}...")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # Criar tabela de resultados
            ping_table = Table(
                title=f"📡 Resultados do Ping - {target}",
                box=box.ROUNDED,
                border_style="yellow"
            )
            
            ping_table.add_column("Métrica", style="bold cyan", width=20)
            ping_table.add_column("Valor", style="white", width=30)
            ping_table.add_column("Análise", style="dim white", width=25)
            
            if result.returncode == 0:
                # Ping bem-sucedido
                ping_table.add_row("Status", "✅ Sucesso", "Host acessível")
                
                # Parsing básico dos resultados (funciona para maioria dos casos)
                output = result.stdout.lower()
                
                if "tempo" in output or "time" in output:
                    # Tentar extrair tempo médio (simplificado)
                    ping_table.add_row("Conectividade", "🟢 Excelente", "Resposta recebida")
                else:
                    ping_table.add_row("Conectividade", "🟡 Limitada", "Resposta parcial")
                    
                # Análise de latência (estimada)
                if "ms" in output:
                    ping_table.add_row("Latência", "Detectada", "Verificar saída completa")
                    
            else:
                # Ping falhou
                ping_table.add_row("Status", "❌ Falha", "Host inacessível")
                ping_table.add_row("Conectividade", "🔴 Sem resposta", "Host down ou firewall")
                
            self.console.print("\n")
            self.console.print(ping_table)
            
            # Exibir saída completa do ping
            self.console.print(Panel(
                result.stdout if result.stdout else result.stderr,
                title="📋 Saída Completa do Ping",
                border_style="blue"
            ))
            
        except subprocess.TimeoutExpired:
            self.console.print(Panel(
                "⏰ Timeout: O comando ping demorou muito para responder.\n"
                "Isso pode indicar:\n"
                "• Host muito distante ou lento\n"
                "• Perda de pacotes na rede\n"
                "• Firewall bloqueando ICMP",
                title="Timeout",
                border_style="red"
            ))
            
        except Exception as e:
            self.console.print(Panel(
                f"❌ Erro ao executar ping: {str(e)}",
                title="Erro",
                border_style="red"
            ))
            
        # Interpretação dos resultados
        interpretation = """
📊 Interpretação dos Resultados de Ping:

⏱️ Latência (tempo de resposta):
• < 10ms: Excelente (rede local)
• 10-50ms: Muito bom (conexão banda larga)
• 50-100ms: Bom (conexão nacional)
• 100-200ms: Aceitável (conexão internacional)
• > 200ms: Lento (pode afetar aplicações)

📦 Perda de pacotes:
• 0%: Conexão estável
• 1-5%: Aceitável para maioria das aplicações
• > 5%: Problemas de conectividade

🔍 Troubleshooting:
• Sem resposta: Host down ou firewall bloqueando ICMP
• Timeout: Rede congestionada ou rota longa
• "Destination unreachable": Problema de roteamento
        """
        
        self.console.print(Panel(interpretation.strip(), title="📚 Interpretação", border_style="green"))
        
        Prompt.ask("\nPressione Enter para continuar")
        
    async def dns_lookup_demo(self):
        """Demo de consulta DNS"""
        
        self.console.print(Panel(
            "🔍 Consulta e Análise DNS\n\n"
            "O DNS traduz nomes de domínio em endereços IP.\n"
            "Vamos analisar registros DNS de um domínio.",
            title="Análise DNS",
            border_style="purple"
        ))
        
        domain = Prompt.ask("\n🌐 Digite o domínio para análise", default="google.com")
        
        # Tabela de resultados DNS
        dns_table = Table(
            title=f"🔍 Análise DNS - {domain}",
            box=box.ROUNDED,
            border_style="purple"
        )
        
        dns_table.add_column("Tipo", style="bold cyan", width=15)
        dns_table.add_column("Resultado", style="white", width=35)
        dns_table.add_column("Análise", style="dim white", width=25)
        
        try:
            # Resolução A (IPv4)
            try:
                ipv4_result = socket.gethostbyname(domain)
                dns_table.add_row("A (IPv4)", ipv4_result, "Endereço IPv4 principal")
                
                # Verificar se é IP privado
                try:
                    ip_obj = ipaddress.ip_address(ipv4_result)
                    if ip_obj.is_private:
                        dns_table.add_row("Tipo IP", "🏠 Privado", "Rede interna")
                    else:
                        dns_table.add_row("Tipo IP", "🌐 Público", "Acessível globalmente")
                except:
                    pass
                    
            except socket.gaierror:
                dns_table.add_row("A (IPv4)", "❌ Não encontrado", "Domínio inexistente")
                
            # FQDN
            try:
                fqdn = socket.getfqdn(domain)
                if fqdn != domain:
                    dns_table.add_row("FQDN", fqdn, "Nome totalmente qualificado")
                else:
                    dns_table.add_row("FQDN", "Mesmo que entrada", "Já totalmente qualificado")
            except:
                dns_table.add_row("FQDN", "Erro na consulta", "Falha na resolução")
                
            # Tentativa de resolução reversa
            try:
                if 'ipv4_result' in locals():
                    reverse_dns = socket.gethostbyaddr(ipv4_result)
                    dns_table.add_row("PTR (Reverso)", reverse_dns[0], "Resolução reversa IP->Nome")
            except:
                dns_table.add_row("PTR (Reverso)", "Não configurado", "Sem registro PTR")
                
        except Exception as e:
            dns_table.add_row("Erro Geral", str(e), "Falha na consulta DNS")
            
        self.console.print("\n")
        self.console.print(dns_table)
        
        # Análise adicional de DNS
        dns_analysis = """
🔍 Análise de Segurança DNS:

📋 Tipos de registros DNS:
• A: Mapeia nome para IPv4
• AAAA: Mapeia nome para IPv6
• CNAME: Alias para outro nome
• MX: Servidores de email
• TXT: Informações textuais/verificação
• PTR: Resolução reversa (IP -> nome)

🛡️ Segurança DNS:
• DNS over HTTPS (DoH): Criptografa consultas
• DNS over TLS (DoT): Protege contra espionagem
• DNSSEC: Valida autenticidade dos registros
• Servidores DNS seguros: 1.1.1.1, 8.8.8.8, 9.9.9.9

⚠️ Ataques DNS comuns:
• DNS Spoofing: Respostas falsas
• DNS Hijacking: Redirecionamento malicioso
• DNS Tunneling: Exfiltração de dados
• Cache Poisoning: Contaminação do cache
        """
        
        self.console.print(Panel(dns_analysis.strip(), title="🛡️ Segurança DNS", border_style="green"))
        
        Prompt.ask("\nPressione Enter para continuar")