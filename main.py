#!/usr/bin/env python3
"""
CyberMentor AI - Interactive Cybersecurity Learning Tool
A terminal-based educational program with AI integration
"""

import asyncio
import sys
import os
from pathlib import Path

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Rich imports for beautiful terminal UI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import track
from rich import box
import typer

# Local imports
from core.ai_mentor import AIChat
from core.menu_system import MenuSystem
from demos.crypto_demo import CryptoDemo
from demos.web_demo import WebDemo
from demos.network_demo import NetworkDemo
from demos.forensics_demo import ForensicsDemo

app = typer.Typer()
console = Console()

class CyberMentor:
    """Main CyberMentor AI application"""
    
    def __init__(self):
        self.console = console
        self.ai_chat = AIChat()
        self.menu_system = MenuSystem(console)
        
        # Initialize demo modules
        self.demos = {
            'crypto': CryptoDemo(console),
            'web': WebDemo(console),
            'network': NetworkDemo(console),
            'forensics': ForensicsDemo(console)
        }
        
    def show_banner(self):
        """Display welcome banner"""
        banner_text = Text()
        banner_text.append("CYBERMENTOR AI", style="bold cyan")
        banner_text.append("\n")
        banner_text.append("Interactive Cybersecurity Learning Platform", style="italic white")
        
        banner_panel = Panel(
            banner_text,
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 2)
        )
        
        self.console.print("\n")
        self.console.print(banner_panel, justify="center")
        self.console.print("\n")
        
        # Welcome message
        welcome_msg = """
Hello! I'm your personal cybersecurity mentor.
I can help you learn through interactive demos and AI-powered explanations.
        
What would you like to explore today?
        """
        
        self.console.print(Panel(welcome_msg.strip(), 
                                title="Welcome", 
                                border_style="green"))
        
    async def run_main_loop(self):
        """Main application loop"""
        while True:
            try:
                # Show main menu
                choice = self.menu_system.show_main_menu()
                
                if choice == '1':
                    await self.demos['crypto'].run()
                elif choice == '2':
                    await self.demos['web'].run()
                elif choice == '3':
                    await self.demos['network'].run()
                elif choice == '4':
                    await self.demos['forensics'].run()
                elif choice == '5':
                    await self.run_ai_chat()
                elif choice == '6':
                    self.show_about()
                elif choice == '0' or choice.lower() == 'q':
                    break
                else:
                    self.console.print("❌ Invalid option! Please try again.", style="red")
                    
            except KeyboardInterrupt:
                if Confirm.ask("\n🚪 Do you want to exit CyberMentor AI?"):
                    break
            except Exception as e:
                self.console.print(f"❌ Error: {e}", style="red")
                
        self.show_goodbye()
        
    async def run_ai_chat(self):
        """Interactive AI chat session"""
        self.console.print(Panel(
            "💬 AI Chat Mode - Ask me anything about cybersecurity!\n"
            "Type 'exit' to return to main menu.",
            title="AI Chat",
            border_style="purple"
        ))
        
        while True:
            try:
                question = Prompt.ask("\n🤔 Your question")
                
                if question.lower() in ['exit', 'quit', 'back']:
                    break
                    
                # Show thinking animation
                with self.console.status("[bold purple]🤖 AI is thinking...", spinner="dots"):
                    response = await self.ai_chat.get_response(question)
                
                # Display AI response
                ai_panel = Panel(
                    response,
                    title="🤖 CyberMentor AI",
                    border_style="purple",
                    padding=(1, 2)
                )
                self.console.print(ai_panel)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.console.print(f"❌ AI Error: {e}", style="red")
                
    def show_about(self):
        """Show about information"""
        about_text = """
📚 CyberMentor AI v1.0

🎯 Purpose: Interactive cybersecurity education
🤖 AI: GROQ-powered explanations
🔧 Built with: Python, Rich, Typer
👨‍💻 Developer: Educational project

📦 Features:
• Interactive crypto demos
• Web security analysis
• Network reconnaissance tools  
• Digital forensics basics
• AI-powered learning assistant

🛡️ Educational use only - Practice ethical hacking responsibly!
        """
        
        self.console.print(Panel(
            about_text.strip(),
            title="About CyberMentor AI",
            border_style="blue"
        ))
        
        Prompt.ask("\nPress Enter to continue")
        
    def show_goodbye(self):
        """Show goodbye message"""
        goodbye_text = Text()
        goodbye_text.append("Thank you for using CyberMentor AI!", style="bold cyan")
        goodbye_text.append("\n\n")
        goodbye_text.append("Keep learning, stay secure!", style="italic green")
        
        self.console.print(Panel(
            goodbye_text,
            title="Goodbye",
            border_style="cyan",
            padding=(1, 2)
        ))

@app.command()
def main(
    dev_mode: bool = typer.Option(False, "--dev", help="Run in development mode"),
    api_key: str = typer.Option(None, "--api-key", help="GROQ API key")
):
    """
    CyberMentor AI - Interactive Cybersecurity Learning
    
    An educational terminal application that teaches cybersecurity concepts
    through interactive demos and AI-powered explanations.
    """
    
    # Set API key if provided
    if api_key:
        import os
        os.environ['GROQ_API_KEY'] = api_key
        
    # Initialize and run application
    try:
        cyber_mentor = CyberMentor()
        cyber_mentor.show_banner()
        
        # Run main loop
        asyncio.run(cyber_mentor.run_main_loop())
        
    except KeyboardInterrupt:
        console.print("\nGoodbye!", style="cyan")
    except Exception as e:
        console.print(f"\nFatal error: {e}", style="red")
        if dev_mode:
            raise
        sys.exit(1)

if __name__ == "__main__":
    app()