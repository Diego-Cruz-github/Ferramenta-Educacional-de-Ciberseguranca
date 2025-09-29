"""
Cryptography Demo Module
Interactive demonstrations of hash functions, encryption, and password security
"""

import hashlib
import hmac
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bcrypt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

class CryptoDemo:
    """Interactive cryptography demonstrations"""
    
    def __init__(self, console: Console):
        self.console = console
        
    async def run(self):
        """Main cryptography demo loop"""
        
        while True:
            # Show crypto demo menu
            self.show_crypto_menu()
            
            choice = Prompt.ask(
                "\n🔐 Choose crypto demo",
                choices=['1', '2', '3', '4', '5', 'b'],
                default='b'
            )
            
            if choice == '1':
                await self.hash_demo()
            elif choice == '2':
                await self.password_demo()
            elif choice == '3':
                await self.encryption_demo()
            elif choice == '4':
                await self.rainbow_table_demo()
            elif choice == '5':
                await self.crypto_analysis_demo()
            elif choice == 'b':
                break
                
    def show_crypto_menu(self):
        """Display cryptography demo menu"""
        
        menu_table = Table(
            title="🔐 Cryptography Laboratory",
            box=box.ROUNDED,
            border_style="blue"
        )
        
        menu_table.add_column("Option", style="bold yellow", width=8)
        menu_table.add_column("Demo", style="bold white", width=25)
        menu_table.add_column("Learn About", style="dim white", width=35)
        
        demos = [
            ("1", "Hash Functions", "MD5, SHA1, SHA256, SHA512 comparison"),
            ("2", "Password Security", "Hashing, salting, bcrypt demonstration"),
            ("3", "Symmetric Encryption", "AES encryption/decryption demo"),
            ("4", "Rainbow Table Attack", "See how unsalted hashes are cracked"),
            ("5", "Crypto Analysis", "Analyze hash strength and collisions"),
            ("B", "Back to Main Menu", "Return to main application")
        ]
        
        for option, demo, description in demos:
            menu_table.add_row(option, demo, description)
            
        self.console.print("\n")
        self.console.print(menu_table, justify="center")
        
    async def hash_demo(self):
        """Interactive hash function demonstration"""
        
        self.console.print(Panel(
            "🔍 Hash Functions Demo\n\n"
            "Hash functions create fixed-size outputs from any input.\n"
            "They're one-way functions - easy to compute forward, hard to reverse.",
            title="Hash Functions",
            border_style="blue"
        ))
        
        # Get input from user
        text_input = Prompt.ask("\n💬 Enter text to hash", default="Hello, CyberSecurity!")
        
        # Calculate different hashes
        results_table = Table(
            title="🔐 Hash Results",
            box=box.SIMPLE,
            border_style="green"
        )
        
        results_table.add_column("Algorithm", style="bold cyan", width=12)
        results_table.add_column("Hash Value", style="white", width=50)
        results_table.add_column("Security", style="bold", width=12)
        
        # Calculate hashes
        text_bytes = text_input.encode('utf-8')
        
        # MD5 - Insecure
        md5_hash = hashlib.md5(text_bytes).hexdigest()
        results_table.add_row("MD5", md5_hash, "❌ BROKEN")
        
        # SHA1 - Deprecated  
        sha1_hash = hashlib.sha1(text_bytes).hexdigest()
        results_table.add_row("SHA1", sha1_hash, "⚠️ WEAK")
        
        # SHA256 - Secure
        sha256_hash = hashlib.sha256(text_bytes).hexdigest()
        results_table.add_row("SHA256", sha256_hash, "✅ SECURE")
        
        # SHA512 - Very Secure
        sha512_hash = hashlib.sha512(text_bytes).hexdigest()
        results_table.add_row("SHA512", sha512_hash[:50] + "...", "✅ VERY SECURE")
        
        self.console.print("\n")
        self.console.print(results_table)
        
        # Educational explanation
        explanation = """
🎓 Key Insights:

• MD5: Only 128 bits, collision attacks exist - NEVER use for security!
• SHA1: 160 bits, theoretical attacks demonstrated - being phased out
• SHA256: 256 bits, current gold standard for most applications  
• SHA512: 512 bits, excellent for high-security applications

🔍 Notice how even small input changes completely change the hash!
Try changing one character and see the avalanche effect.
        """
        
        self.console.print(Panel(explanation.strip(), title="🧠 Learn", border_style="yellow"))
        
        Prompt.ask("\nPress Enter to continue")
        
    async def password_demo(self):
        """Password hashing security demonstration"""
        
        self.console.print(Panel(
            "🔒 Password Security Demo\n\n"
            "Learn why plain hashing isn't enough and how salt + bcrypt protects passwords.",
            title="Password Security",
            border_style="red"
        ))
        
        password = Prompt.ask("\n🔑 Enter a test password", default="mypassword123", password=True)
        
        # Demonstrate different password storage methods
        results_table = Table(
            title="🔐 Password Storage Methods",
            box=box.ROUNDED,
            border_style="red"
        )
        
        results_table.add_column("Method", style="bold cyan", width=15)
        results_table.add_column("Stored Value", style="white", width=40)
        results_table.add_column("Security Level", style="bold", width=15)
        
        password_bytes = password.encode('utf-8')
        
        # 1. Plain text (NEVER DO THIS!)
        results_table.add_row("Plain Text", password, "💀 CATASTROPHIC")
        
        # 2. MD5 hash (Bad)
        md5_hash = hashlib.md5(password_bytes).hexdigest()
        results_table.add_row("MD5 Hash", md5_hash, "❌ VERY BAD")
        
        # 3. SHA256 (Better but not good enough)
        sha256_hash = hashlib.sha256(password_bytes).hexdigest()
        results_table.add_row("SHA256", sha256_hash[:30] + "...", "⚠️ INSUFFICIENT")
        
        # 4. SHA256 + Salt (Good)
        salt = secrets.token_hex(16)
        salted_password = password + salt
        sha256_salted = hashlib.sha256(salted_password.encode()).hexdigest()
        results_table.add_row("SHA256+Salt", f"salt:{salt[:10]}...\nhash:{sha256_salted[:20]}...", "✅ GOOD")
        
        # 5. bcrypt (Best practice)
        bcrypt_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        results_table.add_row("bcrypt", bcrypt_hash.decode()[:30] + "...", "🛡️ EXCELLENT")
        
        self.console.print("\n")
        self.console.print(results_table)
        
        # Show bcrypt verification
        self.console.print(Panel(
            "🧪 bcrypt Verification Test:\n\n"
            f"Password '{password}' matches bcrypt hash: "
            f"{'✅ YES' if bcrypt.checkpw(password_bytes, bcrypt_hash) else '❌ NO'}",
            title="Verification Demo",
            border_style="green"
        ))
        
        explanation = """
🛡️ Why bcrypt is superior:

• Adaptive: Can increase difficulty as computers get faster
• Built-in salt: Each hash is unique even for same password
• Time-tested: Proven secure against rainbow table attacks
• Slow by design: Makes brute force attacks impractical

⚠️ Never store passwords in plain text or with fast hashes like MD5/SHA!
        """
        
        self.console.print(Panel(explanation.strip(), title="🎓 Best Practices", border_style="yellow"))
        
        Prompt.ask("\nPress Enter to continue")
        
    async def encryption_demo(self):
        """Symmetric encryption demonstration"""
        
        self.console.print(Panel(
            "🔐 Symmetric Encryption Demo\n\n"
            "Encryption transforms readable data into unreadable ciphertext.\n"
            "With the right key, ciphertext can be decrypted back to plaintext.",
            title="Encryption/Decryption",
            border_style="purple"
        ))
        
        # Get message to encrypt
        message = Prompt.ask("\n📝 Enter message to encrypt", default="Secret cybersecurity message!")
        
        # Generate encryption key
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        
        # Encrypt the message
        message_bytes = message.encode()
        ciphertext = cipher_suite.encrypt(message_bytes)
        
        # Show results
        results_table = Table(
            title="🔐 Encryption Results",
            box=box.ROUNDED,
            border_style="purple"
        )
        
        results_table.add_column("Step", style="bold cyan", width=15)
        results_table.add_column("Value", style="white", width=50)
        
        results_table.add_row("Original Message", message)
        results_table.add_row("Encryption Key", base64.urlsafe_b64encode(key).decode()[:40] + "...")
        results_table.add_row("Ciphertext", ciphertext.decode()[:40] + "...")
        
        # Decrypt to show reversibility
        decrypted_message = cipher_suite.decrypt(ciphertext).decode()
        results_table.add_row("Decrypted", decrypted_message)
        
        self.console.print("\n")
        self.console.print(results_table)
        
        # Show key importance
        wrong_key = Fernet.generate_key()
        wrong_cipher = Fernet(wrong_key)
        
        try:
            wrong_cipher.decrypt(ciphertext)
            decrypt_result = "❌ This should not happen!"
        except:
            decrypt_result = "✅ Decryption failed (as expected)"
            
        self.console.print(Panel(
            f"🔑 Key Security Test:\n\n"
            f"Decrypting with wrong key: {decrypt_result}\n\n"
            f"🛡️ Without the correct key, the data remains secure!",
            title="Key Importance",
            border_style="green"
        ))
        
        explanation = """
🔐 Symmetric Encryption Key Points:

• Same key encrypts AND decrypts (symmetric)
• AES is current standard (used by Fernet)
• Key must be kept secret and secure
• Key distribution is the main challenge

🎯 Use Cases:
• File encryption
• Database encryption
• VPN tunnels
• Secure messaging (with key exchange)
        """
        
        self.console.print(Panel(explanation.strip(), title="🧠 Learn More", border_style="yellow"))
        
        Prompt.ask("\nPress Enter to continue")
        
    async def rainbow_table_demo(self):
        """Demonstrate rainbow table attack concept"""
        
        self.console.print(Panel(
            "🌈 Rainbow Table Attack Demo\n\n"
            "Rainbow tables are precomputed hash lookups for common passwords.\n"
            "This shows why salting is crucial for password security!",
            title="Rainbow Table Attack",
            border_style="red"
        ))
        
        # Simulated rainbow table (very small example)
        rainbow_table = {
            "5d41402abc4b2a76b9719d911017c592": "hello",
            "098f6bcd4621d373cade4e832627b4f6": "test", 
            "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8": "password",
            "ef92b778bafe771e89245b89ecbc082de2bb855ae5e5adc0db8f6e3e2e5f5b5e": "admin123",
            "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3": "secret"
        }
        
        # Show rainbow table contents
        rt_table = Table(
            title="🌈 Sample Rainbow Table",
            box=box.SIMPLE,
            border_style="red"
        )
        
        rt_table.add_column("Hash", style="dim white", width=35)
        rt_table.add_column("Password", style="bold red", width=15)
        
        for hash_val, password in rainbow_table.items():
            rt_table.add_row(hash_val[:32] + "...", password)
            
        self.console.print("\n")
        self.console.print(rt_table)
        
        # Test hash cracking
        test_password = Prompt.ask("\n🧪 Enter a password to test", default="password")
        test_hash = hashlib.sha256(test_password.encode()).hexdigest()
        
        if test_hash in rainbow_table:
            result = f"💀 CRACKED! Hash {test_hash[:20]}... = '{rainbow_table[test_hash]}'"
            style = "red"
        else:
            result = f"✅ SAFE! Hash {test_hash[:20]}... not found in rainbow table"
            style = "green"
            
        self.console.print(Panel(result, title="🎯 Crack Attempt", border_style=style))
        
        # Show salt protection
        salt = secrets.token_hex(8)
        salted_password = test_password + salt
        salted_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        
        protection_demo = f"""
🧂 Salt Protection Demo:

Original password: {test_password}
Salt: {salt}
Salted password: {test_password} + {salt} = {salted_password}
Salted hash: {salted_hash[:30]}...

🛡️ Even if '{test_password}' is in rainbow tables, the salted version is unique!
Rainbow tables become useless when every password has a unique salt.
        """
        
        self.console.print(Panel(protection_demo.strip(), title="🧂 Salt Defense", border_style="green"))
        
        Prompt.ask("\nPress Enter to continue")
        
    async def crypto_analysis_demo(self):
        """Analyze cryptographic hash properties"""
        
        self.console.print(Panel(
            "🔬 Cryptographic Analysis\n\n"
            "Explore hash properties: deterministic, avalanche effect, and collision resistance.",
            title="Crypto Analysis",
            border_style="cyan"
        ))
        
        base_input = Prompt.ask("\n📝 Enter base text for analysis", default="CyberSecurity")
        
        # Show avalanche effect
        analysis_table = Table(
            title="🌊 Avalanche Effect Analysis",
            box=box.ROUNDED,
            border_style="cyan"
        )
        
        analysis_table.add_column("Input", style="bold white", width=20)
        analysis_table.add_column("SHA256 Hash", style="dim white", width=35)
        analysis_table.add_column("Difference", style="bold yellow", width=15)
        
        # Original hash
        original_hash = hashlib.sha256(base_input.encode()).hexdigest()
        analysis_table.add_row(base_input, original_hash[:32] + "...", "Original")
        
        # Small changes
        variations = [
            base_input.lower(),
            base_input + "1",
            base_input[:-1],
            base_input.replace('e', '3'),
        ]
        
        for variation in variations:
            var_hash = hashlib.sha256(variation.encode()).hexdigest()
            
            # Calculate bit differences (simplified)
            diff_count = sum(c1 != c2 for c1, c2 in zip(original_hash, var_hash))
            diff_percent = (diff_count / len(original_hash)) * 100
            
            analysis_table.add_row(
                variation[:20],
                var_hash[:32] + "...",
                f"{diff_percent:.1f}% diff"
            )
            
        self.console.print("\n")
        self.console.print(analysis_table)
        
        # Hash properties explanation
        properties = """
🔬 Hash Function Properties:

1. 🎯 Deterministic: Same input always produces same hash
2. 🌊 Avalanche Effect: Small input change = huge hash change  
3. 🚫 Collision Resistant: Hard to find two inputs with same hash
4. ⚡ Fast Computation: Quick to calculate hash from input
5. 🔐 Irreversible: Computationally impossible to reverse

These properties make hashes perfect for:
• Password verification
• Data integrity checking  
• Digital signatures
• Blockchain proof-of-work
        """
        
        self.console.print(Panel(properties.strip(), title="📚 Hash Properties", border_style="blue"))
        
        Prompt.ask("\nPress Enter to continue")