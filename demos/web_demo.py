"""
Web Security Demo Module
Interactive demonstrations of web security concepts and vulnerabilities
"""

import requests
import base64
import urllib.parse
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import json

class WebDemo:
    """Interactive web security demonstrations"""
    
    def __init__(self, console: Console):
        self.console = console
        
    async def run(self):
        """Main web security demo loop"""
        
        while True:
            self.show_web_menu()
            
            choice = Prompt.ask(
                "\n🌐 Choose web security demo",
                choices=['1', '2', '3', '4', '5', 'b'],
                default='b'
            )
            
            if choice == '1':
                await self.http_headers_demo()
            elif choice == '2':
                await self.sql_injection_demo()
            elif choice == '3':
                await self.xss_demo()
            elif choice == '4':
                await self.cookie_security_demo()
            elif choice == '5':
                await self.web_recon_demo()
            elif choice == 'b':
                break
                
    def show_web_menu(self):
        """Display web security demo menu"""
        
        menu_table = Table(
            title="🌐 Web Security Laboratory",
            box=box.ROUNDED,
            border_style="green"
        )
        
        menu_table.add_column("Option", style="bold yellow", width=8)
        menu_table.add_column("Demo", style="bold white", width=25)
        menu_table.add_column("Learn About", style="dim white", width=35)
        
        demos = [
            ("1", "HTTP Headers Analysis", "Security headers and misconfigurations"),
            ("2", "SQL Injection Basics", "Understanding and preventing SQLi"),
            ("3", "XSS Demonstration", "Cross-site scripting examples"),
            ("4", "Cookie Security", "Secure vs insecure cookie analysis"),
            ("5", "Web Reconnaissance", "Information gathering techniques"),
            ("B", "Back to Main Menu", "Return to main application")
        ]
        
        for option, demo, description in demos:
            menu_table.add_row(option, demo, description)
            
        self.console.print("\n")
        self.console.print(menu_table, justify="center")
        
    async def http_headers_demo(self):
        """HTTP security headers analysis"""
        
        self.console.print(Panel(
            "🔍 HTTP Headers Security Analysis\n\n"
            "HTTP headers can reveal security information or provide protection.\n"
            "Let's analyze headers from a website for security best practices.",
            title="HTTP Headers Analysis",
            border_style="green"
        ))
        
        # Get target URL
        target_url = Prompt.ask(
            "\n🌐 Enter URL to analyze", 
            default="https://httpbin.org/get"
        )
        
        try:
            # Make HTTP request
            self.console.print(f"\n🔍 Analyzing headers for: {target_url}")
            response = requests.get(target_url, timeout=10)
            
            # Create headers analysis table
            headers_table = Table(
                title="📋 HTTP Response Headers",
                box=box.SIMPLE,
                border_style="blue"
            )
            
            headers_table.add_column("Header", style="bold cyan", width=25)
            headers_table.add_column("Value", style="white", width=40)
            headers_table.add_column("Security Impact", style="bold", width=15)
            
            # Analyze key security headers
            security_headers = {
                'content-security-policy': ('CSP', '🛡️ EXCELLENT'),
                'strict-transport-security': ('HSTS', '🔒 GOOD'), 
                'x-frame-options': ('Clickjacking Protection', '✅ GOOD'),
                'x-content-type-options': ('MIME Sniffing Protection', '✅ GOOD'),
                'x-xss-protection': ('XSS Protection', '⚠️ LEGACY'),
                'server': ('Server Info', '⚠️ INFO LEAK'),
                'x-powered-by': ('Tech Stack Info', '🚨 INFO LEAK')
            }
            
            # Check each header
            for header, (description, security_level) in security_headers.items():
                value = response.headers.get(header, '❌ MISSING')
                if value != '❌ MISSING':
                    value = value[:35] + "..." if len(value) > 35 else value
                headers_table.add_row(header.title(), value, security_level)
            
            self.console.print("\n")
            self.console.print(headers_table)
            
            # Security assessment
            security_score = 0
            recommendations = []
            
            if 'content-security-policy' in response.headers:
                security_score += 30
            else:
                recommendations.append("• Add Content Security Policy (CSP)")
                
            if 'strict-transport-security' in response.headers:
                security_score += 25
            else:
                recommendations.append("• Enable HTTP Strict Transport Security (HSTS)")
                
            if 'x-frame-options' in response.headers:
                security_score += 20
            else:
                recommendations.append("• Set X-Frame-Options to prevent clickjacking")
                
            if 'x-content-type-options' in response.headers:
                security_score += 15
            else:
                recommendations.append("• Add X-Content-Type-Options: nosniff")
                
            if 'server' not in response.headers and 'x-powered-by' not in response.headers:
                security_score += 10
            else:
                recommendations.append("• Hide server/technology information")
                
            # Display security assessment
            if security_score >= 80:
                score_color = "green"
                score_text = "🛡️ EXCELLENT"
            elif security_score >= 60:
                score_color = "yellow"
                score_text = "⚠️ MODERATE"
            else:
                score_color = "red"
                score_text = "🚨 POOR"
                
            assessment = f"""
🎯 Security Score: {security_score}/100 - {score_text}

📊 Analysis:
• Status Code: {response.status_code}
• Response Time: {response.elapsed.total_seconds():.2f}s
• Content Length: {len(response.content)} bytes

💡 Recommendations:
{chr(10).join(recommendations) if recommendations else "• Security headers look good!"}
            """
            
            self.console.print(Panel(
                assessment.strip(),
                title="🔒 Security Assessment",
                border_style=score_color
            ))
            
        except requests.RequestException as e:
            self.console.print(Panel(
                f"❌ Error analyzing URL: {str(e)}\n\n"
                "This might be due to:\n"
                "• Invalid URL\n"
                "• Network connectivity issues\n" 
                "• Target server blocking requests\n"
                "• SSL/TLS certificate problems",
                title="Connection Error",
                border_style="red"
            ))
            
        # Educational content
        education = """
🎓 Key Security Headers:

🛡️ Content-Security-Policy (CSP):
   Prevents XSS by controlling resource loading

🔒 Strict-Transport-Security (HSTS):
   Forces HTTPS connections for future visits

🖼️ X-Frame-Options:
   Prevents embedding in frames (clickjacking protection)

📄 X-Content-Type-Options:
   Prevents MIME type sniffing attacks

⚠️ Information Disclosure:
   Server/X-Powered-By headers reveal technology stack
        """
        
        self.console.print(Panel(education.strip(), title="📚 Learn More", border_style="blue"))
        
        Prompt.ask("\nPress Enter to continue")
        
    async def sql_injection_demo(self):
        """SQL injection educational demonstration"""
        
        self.console.print(Panel(
            "💉 SQL Injection Educational Demo\n\n"
            "SQL Injection occurs when user input is directly inserted into SQL queries.\n"
            "This demo shows vulnerable code patterns and prevention techniques.",
            title="SQL Injection Demo",
            border_style="red"
        ))
        
        # Show vulnerable code example
        vulnerable_code = """
# ❌ VULNERABLE CODE EXAMPLE:
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    return cursor.fetchone()

# 🚨 ATTACK PAYLOAD:
Username: admin
Password: ' OR '1'='1' --

# 🔥 RESULTING QUERY:
SELECT * FROM users WHERE username='admin' AND password='' OR '1'='1' --'
                                                              ^^^^^^^^^
                                                              Always true!
        """
        
        self.console.print(Panel(vulnerable_code.strip(), title="💀 Vulnerable Code", border_style="red"))
        
        # Interactive SQL injection simulator
        self.console.print("\n🧪 Try different SQL injection payloads:")
        
        test_username = Prompt.ask("Enter username", default="admin")
        test_password = Prompt.ask("Enter password", default="' OR '1'='1' --")
        
        # Simulate vulnerable query construction
        vulnerable_query = f"SELECT * FROM users WHERE username='{test_username}' AND password='{test_password}'"
        
        # Analyze the payload
        injection_indicators = [
            "' OR '",
            "' OR 1=1",
            "' UNION SELECT",
            "'; DROP TABLE",
            "' --",
            "' /*"
        ]
        
        is_injection = any(indicator in test_password.upper() for indicator in [i.upper() for i in injection_indicators])
        
        # Show results
        analysis_table = Table(
            title="🔍 SQL Injection Analysis",
            box=box.ROUNDED,
            border_style="yellow"
        )
        
        analysis_table.add_column("Component", style="bold cyan", width=20)
        analysis_table.add_column("Value", style="white", width=40)
        analysis_table.add_column("Risk", style="bold", width=12)
        
        analysis_table.add_row("Username Input", test_username, "✅ SAFE" if "'" not in test_username else "⚠️ SUSPICIOUS")
        analysis_table.add_row("Password Input", test_password[:30] + "..." if len(test_password) > 30 else test_password, "🚨 INJECTION" if is_injection else "✅ SAFE")
        analysis_table.add_row("Resulting Query", vulnerable_query[:40] + "...", "💀 EXPLOITABLE" if is_injection else "✅ NORMAL")
        
        self.console.print("\n")
        self.console.print(analysis_table)
        
        if is_injection:
            result = """
🚨 SQL INJECTION DETECTED!

This payload would bypass authentication by making the WHERE clause always true.
The query becomes: username='admin' AND password='' OR '1'='1'
Since '1'='1' is always true, the entire condition passes!

💀 Potential Impact:
• Unauthorized login
• Data theft
• Database manipulation  
• Complete system compromise
            """
            border_color = "red"
        else:
            result = """
✅ INPUT APPEARS SAFE

No common SQL injection patterns detected in this input.
However, always use proper defenses in real applications!
            """
            border_color = "green"
            
        self.console.print(Panel(result.strip(), title="🎯 Analysis Result", border_style=border_color))
        
        # Show prevention techniques
        prevention = """
🛡️ SQL INJECTION PREVENTION:

1. 📝 Parameterized Queries (Best):
   query = "SELECT * FROM users WHERE username=? AND password=?"
   cursor.execute(query, (username, password))

2. 🔒 Stored Procedures:
   Use database stored procedures with parameters

3. ✅ Input Validation:
   Whitelist allowed characters and patterns

4. 🚫 Escape Special Characters:
   Escape quotes and SQL metacharacters (less reliable)

5. 🎯 Principle of Least Privilege:
   Database user should have minimal permissions

⚠️ NEVER trust user input! Always validate and sanitize.
        """
        
        self.console.print(Panel(prevention.strip(), title="🛡️ Prevention Guide", border_style="green"))
        
        Prompt.ask("\nPress Enter to continue")
        
    async def xss_demo(self):
        """Cross-site scripting demonstration"""
        
        self.console.print(Panel(
            "🎭 Cross-Site Scripting (XSS) Demo\n\n"
            "XSS allows attackers to inject malicious scripts into web applications.\n"
            "These scripts execute in users' browsers with full access to the page.",
            title="XSS Demonstration",
            border_style="orange3"
        ))
        
        # Show XSS payload examples
        xss_payloads = [
            ("<script>alert('XSS')</script>", "Basic Alert", "🟡 LOW"),
            ("<img src=x onerror=alert('XSS')>", "Image Error Handler", "🟠 MEDIUM"),
            ("javascript:alert('XSS')", "JavaScript URL", "🟠 MEDIUM"),
            ("<svg onload=alert('XSS')>", "SVG Event Handler", "🔴 HIGH"),
            ("';alert('XSS');//", "JavaScript Breaking", "🔴 HIGH")
        ]
        
        # Display payload analysis
        payload_table = Table(
            title="🎭 Common XSS Payloads",
            box=box.ROUNDED,
            border_style="orange3"
        )
        
        payload_table.add_column("#", style="bold cyan", width=3)
        payload_table.add_column("Payload", style="white", width=35)
        payload_table.add_column("Type", style="bold white", width=20)
        payload_table.add_column("Risk", style="bold", width=12)
        
        for i, (payload, payload_type, risk) in enumerate(xss_payloads, 1):
            payload_table.add_row(str(i), payload, payload_type, risk)
            
        self.console.print("\n")
        self.console.print(payload_table)
        
        # Interactive XSS testing
        self.console.print("\n🧪 Test XSS payload detection:")
        test_input = Prompt.ask("Enter potential XSS payload", default="<script>alert('test')</script>")
        
        # XSS detection patterns
        xss_patterns = [
            '<script',
            'javascript:',
            'onload=',
            'onerror=',
            'onclick=',
            'onmouseover=',
            'eval(',
            'alert(',
            'document.cookie'
        ]
        
        detected_patterns = [pattern for pattern in xss_patterns if pattern.lower() in test_input.lower()]
        is_xss = len(detected_patterns) > 0
        
        # Analysis results
        analysis = f"""
🔍 XSS Analysis Results:

Input: {test_input}
Detected Patterns: {', '.join(detected_patterns) if detected_patterns else 'None'}
Risk Level: {'🚨 HIGH - Potential XSS' if is_xss else '✅ Safe'}

{'⚠️ This input contains suspicious JavaScript patterns!' if is_xss else '✅ No obvious XSS patterns detected.'}
        """
        
        self.console.print(Panel(
            analysis.strip(),
            title="🎯 Detection Results",
            border_style="red" if is_xss else "green"
        ))
        
        # XSS prevention techniques
        prevention_guide = """
🛡️ XSS PREVENTION TECHNIQUES:

1. 🔄 Output Encoding:
   • HTML encode: &lt; &gt; &amp; &quot; &#x27;
   • URL encode for URL contexts
   • JavaScript encode for JS contexts

2. 🎯 Input Validation:
   • Whitelist allowed characters
   • Length limitations
   • Format validation (email, phone, etc.)

3. 🛡️ Content Security Policy (CSP):
   Content-Security-Policy: default-src 'self'; script-src 'self'

4. 📝 Template Engines:
   • Use auto-escaping templates
   • Avoid innerHTML, use textContent

5. 🍪 Secure Cookies:
   • HttpOnly flag prevents JS access
   • Secure flag for HTTPS only

6. 🧹 Sanitization Libraries:
   • DOMPurify for HTML content
   • OWASP Java HTML Sanitizer
        """
        
        self.console.print(Panel(prevention_guide.strip(), title="🛡️ Protection Guide", border_style="blue"))
        
        Prompt.ask("\nPress Enter to continue")
        
    async def cookie_security_demo(self):
        """Cookie security analysis demonstration"""
        
        self.console.print(Panel(
            "🍪 Cookie Security Analysis\n\n"
            "Cookies store session data but can be vulnerable if not properly configured.\n"
            "Let's analyze cookie security attributes and their importance.",
            title="Cookie Security",
            border_style="blue"
        ))
        
        # Cookie security examples
        cookie_examples = [
            ("sessionid=abc123", "❌ INSECURE", "No security flags"),
            ("sessionid=abc123; HttpOnly", "⚠️ PARTIAL", "Protected from XSS"),
            ("sessionid=abc123; Secure", "⚠️ PARTIAL", "HTTPS only"),
            ("sessionid=abc123; HttpOnly; Secure", "✅ BETTER", "XSS + HTTPS protection"),
            ("sessionid=abc123; HttpOnly; Secure; SameSite=Strict", "🛡️ EXCELLENT", "Full protection")
        ]
        
        # Display cookie analysis
        cookie_table = Table(
            title="🍪 Cookie Security Comparison",
            box=box.ROUNDED,
            border_style="blue"
        )
        
        cookie_table.add_column("Cookie Example", style="white", width=45)
        cookie_table.add_column("Security Level", style="bold", width=15)
        cookie_table.add_column("Protection", style="dim white", width=20)
        
        for cookie, security, protection in cookie_examples:
            cookie_table.add_row(cookie, security, protection)
            
        self.console.print("\n")
        self.console.print(cookie_table)
        
        # Interactive cookie builder
        self.console.print("\n🔨 Cookie Security Builder:")
        
        cookie_name = Prompt.ask("Cookie name", default="sessionid")
        cookie_value = Prompt.ask("Cookie value", default="user123session")
        
        # Ask about security flags
        httponly = Prompt.ask("Add HttpOnly flag? (protects from XSS)", choices=['y', 'n'], default='y') == 'y'
        secure = Prompt.ask("Add Secure flag? (HTTPS only)", choices=['y', 'n'], default='y') == 'y' 
        samesite = Prompt.ask("SameSite setting", choices=['Strict', 'Lax', 'None'], default='Strict')
        
        # Build cookie
        cookie_parts = [f"{cookie_name}={cookie_value}"]
        
        if httponly:
            cookie_parts.append("HttpOnly")
        if secure:
            cookie_parts.append("Secure")
        cookie_parts.append(f"SameSite={samesite}")
        
        final_cookie = "; ".join(cookie_parts)
        
        # Security assessment
        security_score = 0
        security_notes = []
        
        if httponly:
            security_score += 30
            security_notes.append("✅ Protected from XSS attacks")
        else:
            security_notes.append("❌ Vulnerable to XSS cookie theft")
            
        if secure:
            security_score += 30
            security_notes.append("✅ Transmitted over HTTPS only")
        else:
            security_notes.append("❌ Can be transmitted over HTTP (sniffable)")
            
        if samesite == 'Strict':
            security_score += 30
            security_notes.append("✅ Maximum CSRF protection")
        elif samesite == 'Lax':
            security_score += 20
            security_notes.append("⚠️ Partial CSRF protection")
        else:
            security_notes.append("❌ No CSRF protection")
            
        security_score += 10  # Base score
        
        # Display results
        if security_score >= 80:
            score_color = "green"
            score_emoji = "🛡️"
        elif security_score >= 60:
            score_color = "yellow" 
            score_emoji = "⚠️"
        else:
            score_color = "red"
            score_emoji = "🚨"
            
        results = f"""
🍪 Generated Cookie:
{final_cookie}

{score_emoji} Security Score: {security_score}/100

📊 Security Analysis:
{chr(10).join(security_notes)}

💡 Cookie Attributes Explained:
• HttpOnly: Prevents JavaScript access (XSS protection)
• Secure: Only sent over HTTPS connections
• SameSite: Controls cross-site request behavior
  - Strict: Never sent cross-site (best security)
  - Lax: Sent on safe cross-site navigation
  - None: Always sent (requires Secure flag)
        """
        
        self.console.print(Panel(results.strip(), title="🍪 Cookie Analysis", border_style=score_color))
        
        Prompt.ask("\nPress Enter to continue")
        
    async def web_recon_demo(self):
        """Web reconnaissance demonstration"""
        
        self.console.print(Panel(
            "🔍 Web Reconnaissance Demo\n\n"
            "Information gathering is the first step in security assessment.\n"
            "Let's explore what information websites reveal about themselves.",
            title="Web Reconnaissance",
            border_style="purple"
        ))
        
        target_url = Prompt.ask("🌐 Enter target URL", default="https://httpbin.org")
        
        try:
            # Gather information
            self.console.print(f"\n🔍 Gathering information from: {target_url}")
            
            response = requests.get(target_url, timeout=10)
            
            # Create reconnaissance report
            recon_table = Table(
                title="🔍 Reconnaissance Report",
                box=box.ROUNDED,
                border_style="purple"
            )
            
            recon_table.add_column("Information Type", style="bold cyan", width=20)
            recon_table.add_column("Value", style="white", width=40)
            recon_table.add_column("Intelligence", style="dim white", width=20)
            
            # Basic information
            recon_table.add_row("HTTP Status", str(response.status_code), "Service status")
            recon_table.add_row("Response Time", f"{response.elapsed.total_seconds():.2f}s", "Server performance")
            recon_table.add_row("Content Length", f"{len(response.content)} bytes", "Response size")
            
            # Server information
            server_info = response.headers.get('server', 'Not disclosed')
            powered_by = response.headers.get('x-powered-by', 'Not disclosed')
            
            recon_table.add_row("Server Software", server_info, "Technology stack")
            recon_table.add_row("Powered By", powered_by, "Framework/language")
            
            # Security headers
            csp = response.headers.get('content-security-policy', '❌ Missing')
            hsts = response.headers.get('strict-transport-security', '❌ Missing')
            
            recon_table.add_row("Content Security Policy", csp[:30] + "..." if len(csp) > 30 else csp, "XSS protection")
            recon_table.add_row("HSTS Header", hsts[:30] + "..." if len(hsts) > 30 else hsts, "HTTPS enforcement")
            
            self.console.print("\n")
            self.console.print(recon_table)
            
            # Technology fingerprinting
            tech_indicators = {
                'PHP': ['x-powered-by', 'set-cookie'],
                'ASP.NET': ['x-aspnet-version', 'x-aspnetmvc-version'],
                'Apache': ['server'],
                'Nginx': ['server'],
                'IIS': ['server'],
                'Cloudflare': ['cf-ray', 'cf-cache-status'],
                'WordPress': ['x-pingback']
            }
            
            detected_tech = []
            for tech, indicators in tech_indicators.items():
                for indicator in indicators:
                    if indicator in response.headers:
                        header_value = response.headers[indicator].lower()
                        if tech.lower() in header_value:
                            detected_tech.append(f"{tech} ({header_value})")
                            break
                        elif tech == 'PHP' and 'php' in header_value:
                            detected_tech.append(f"PHP ({header_value})")
                        elif tech == 'Apache' and 'apache' in header_value:
                            detected_tech.append(f"Apache ({header_value})")
                        elif tech == 'Nginx' and 'nginx' in header_value:
                            detected_tech.append(f"Nginx ({header_value})")
            
            # Information summary
            summary = f"""
🎯 Reconnaissance Summary:

🔍 Target: {target_url}
📊 Response: {response.status_code} ({response.reason})
⏱️ Response Time: {response.elapsed.total_seconds():.2f} seconds

💻 Technology Stack:
{chr(10).join([f'• {tech}' for tech in detected_tech]) if detected_tech else '• Technology fingerprinting inconclusive'}

🔒 Security Posture:
• Server Info Disclosure: {'❌ Yes' if server_info != 'Not disclosed' else '✅ Minimal'}
• Security Headers: {'✅ Present' if csp != '❌ Missing' else '❌ Missing'}
• HTTPS Enforcement: {'✅ Yes' if hsts != '❌ Missing' else '❌ No'}

⚠️ Reconnaissance Findings:
• Information leakage through headers
• Potential attack vectors identified
• Security configuration assessment complete
            """
            
            self.console.print(Panel(summary.strip(), title="📊 Intelligence Report", border_style="blue"))
            
        except requests.RequestException as e:
            self.console.print(Panel(
                f"❌ Reconnaissance failed: {str(e)}\n\n"
                "Possible reasons:\n"
                "• Target is offline or blocking requests\n"
                "• Network connectivity issues\n"
                "• Invalid URL format\n"
                "• Firewall or rate limiting",
                title="Connection Error",
                border_style="red"
            ))
            
        # Ethical guidelines
        ethics = """
⚖️ ETHICAL RECONNAISSANCE GUIDELINES:

✅ ALLOWED:
• Testing your own websites/applications
• Bug bounty programs with clear scope
• Educational exercises with permission
• Security research on public services

❌ PROHIBITED:
• Unauthorized scanning of systems
• Aggressive automated attacks
• Exploiting discovered vulnerabilities
• Accessing confidential information

🛡️ BEST PRACTICES:
• Always get written permission
• Follow responsible disclosure
• Respect rate limits and robots.txt
• Document findings professionally

Remember: The goal is defensive security improvement!
        """
        
        self.console.print(Panel(ethics.strip(), title="🛡️ Ethical Guidelines", border_style="green"))
        
        Prompt.ask("\nPress Enter to continue")