"""
AI Mentor Integration
Handles communication with GROQ API for cybersecurity education
"""

import os
import asyncio
from typing import Optional
import aiohttp
from groq import Groq

class AIChat:
    """AI-powered cybersecurity mentor using GROQ"""
    
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.client = None
        self.model = "mixtral-8x7b-32768"
        
        # Initialize client if API key exists
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: GROQ client initialization failed: {e}")
        
        # System prompt for cybersecurity education
        self.system_prompt = """
You are CyberMentor AI, an expert cybersecurity educator and ethical hacking instructor.

Your role:
- Teach cybersecurity concepts clearly and practically
- Always emphasize ethical use and responsible disclosure
- Provide hands-on examples and code when helpful
- Use emojis to make explanations engaging
- Keep responses focused and under 300 words
- Include practical tips and best practices

Guidelines:
- Always mention legal and ethical considerations
- Encourage responsible security research
- Provide step-by-step explanations
- Use real-world examples when possible
- Suggest next learning steps

Remember: Education is for defense, never for malicious attacks.
"""
    
    async def get_response(self, question: str) -> str:
        """Get AI response to cybersecurity question"""
        
        # Check if API is configured
        if not self.client or not self.api_key:
            return self._get_fallback_response(question)
            
        try:
            # Create chat completion
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": question}
                ],
                model=self.model,
                max_tokens=1024,
                temperature=0.1,
                stream=False
            )
            
            # Extract and return response
            ai_response = response.choices[0].message.content
            return self._format_response(ai_response)
            
        except Exception as e:
            return f"🚨 AI Service Error: {str(e)}\n\n{self._get_fallback_response(question)}"
    
    def _format_response(self, response: str) -> str:
        """Format AI response for better display"""
        
        # Add educational footer
        footer = "\n\n💡 Remember: Use this knowledge ethically and responsibly!"
        
        return response + footer
    
    def _get_fallback_response(self, question: str) -> str:
        """Provide fallback responses when AI is not available"""
        
        # Keyword-based responses for common topics
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['sql injection', 'sqli']):
            return """
🔍 SQL Injection Basics:

SQL injection occurs when user input is directly inserted into SQL queries without proper validation.

Example vulnerable code:
```sql
SELECT * FROM users WHERE username = '$user_input'
```

🛡️ Prevention:
• Use parameterized queries/prepared statements
• Validate and sanitize all input
• Apply principle of least privilege
• Use stored procedures when possible

⚖️ Legal Note: Only test on systems you own or have explicit permission to test!

💡 Try our Web Security demo to see this in action!
"""
        
        elif any(word in question_lower for word in ['hash', 'hashing', 'md5', 'sha']):
            return """
🔐 Hash Functions in Security:

Hash functions create fixed-size outputs from variable inputs. Common uses:
• Password storage
• Data integrity verification  
• Digital signatures

🚨 Security Levels:
• MD5: ❌ Broken (collisions found)
• SHA1: ⚠️ Deprecated  
• SHA256: ✅ Secure
• bcrypt/Argon2: ✅ Best for passwords

💡 Try our Cryptography demo to experiment with different hash algorithms!
"""
        
        elif any(word in question_lower for word in ['port scan', 'nmap', 'reconnaissance']):
            return """
🔍 Port Scanning & Network Reconnaissance:

Port scanning discovers open services on target systems.

Common tools:
• Nmap: Most popular network scanner
• Masscan: High-speed port scanner
• Zmap: Internet-wide scanner

⚖️ Legal Warning: Only scan networks you own or have permission to test!

🎯 Ethical use cases:
• Network inventory
• Security assessments
• Vulnerability management

💡 Check our Network Tools demo for hands-on practice!
"""
        
        elif any(word in question_lower for word in ['xss', 'cross-site scripting']):
            return """
🌐 Cross-Site Scripting (XSS):

XSS allows attackers to inject malicious scripts into web applications.

Types:
• Reflected XSS: Script in URL parameters
• Stored XSS: Script saved in database  
• DOM XSS: Client-side manipulation

🛡️ Prevention:
• Validate and encode user input
• Use Content Security Policy (CSP)
• Sanitize output data
• HttpOnly cookies

💡 Practice with our Web Security demo!
"""
        
        else:
            return """
🤖 AI Chat Offline

The GROQ AI service is currently not available. This could be due to:
• Missing API key
• Network connectivity issues
• Service temporarily unavailable

🔧 To enable AI chat:
1. Get a free API key from https://groq.com
2. Set environment variable: GROQ_API_KEY=your_key
3. Or run with: python main.py --api-key your_key

📚 In the meantime, explore our interactive demos:
• Cryptography tools
• Web security analysis
• Network reconnaissance  
• Digital forensics

💡 Each demo includes detailed explanations and practical examples!
"""
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.client is not None and self.api_key is not None
    
    async def get_explanation(self, topic: str, context: str = "") -> str:
        """Get AI explanation for specific cybersecurity topic"""
        
        prompt = f"""
Explain the cybersecurity concept: {topic}

Context: {context}

Please provide:
1. Clear definition
2. How it works
3. Security implications
4. Prevention/mitigation
5. Real-world example

Keep it educational and emphasize ethical use.
"""
        
        return await self.get_response(prompt)