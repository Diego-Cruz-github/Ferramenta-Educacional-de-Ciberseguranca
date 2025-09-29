"""
Menu System for CyberMentor AI
Handles navigation and user interface
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich import box

class MenuSystem:
    """Handles all menu operations and navigation"""
    
    def __init__(self, console: Console):
        self.console = console
        
    def show_main_menu(self) -> str:
        """Display main menu and get user choice"""
        
        # Create menu table
        menu_table = Table(
            title="🎯 Learning Modules",
            box=box.ROUNDED,
            border_style="cyan",
            title_style="bold cyan"
        )
        
        menu_table.add_column("Option", style="bold yellow", width=8)
        menu_table.add_column("Module", style="bold white", width=25)
        menu_table.add_column("Description", style="dim white", width=40)
        
        # Add menu options
        menu_options = [
            ("1", "🔐 Cryptography", "Hash functions, encryption, password security"),
            ("2", "🌐 Web Security", "HTTP analysis, headers, common vulnerabilities"),
            ("3", "🔍 Network Tools", "Port scanning, network reconnaissance"),
            ("4", "🕵️ Digital Forensics", "File analysis, metadata extraction"),
            ("5", "💬 AI Chat", "Ask questions to the AI mentor"),
            ("6", "ℹ️ About", "Information about CyberMentor AI"),
            ("0", "🚪 Exit", "Close the application")
        ]
        
        for option, module, description in menu_options:
            menu_table.add_row(option, module, description)
            
        # Display menu
        self.console.print("\n")
        self.console.print(menu_table, justify="center")
        
        # Get user choice
        choice = Prompt.ask(
            "\n🎯 Select an option",
            choices=["1", "2", "3", "4", "5", "6", "0", "q"],
            default="1"
        )
        
        return choice
        
    def show_demo_menu(self, demo_name: str, options: list) -> str:
        """Show demo-specific menu"""
        
        demo_table = Table(
            title=f"🧪 {demo_name} Demo",
            box=box.SIMPLE,
            border_style="green"
        )
        
        demo_table.add_column("Option", style="bold yellow", width=8)
        demo_table.add_column("Action", style="bold white", width=30)
        
        for option, action in options:
            demo_table.add_row(option, action)
            
        # Always add back option
        demo_table.add_row("B", "🔙 Back to Main Menu")
        
        self.console.print("\n")
        self.console.print(demo_table, justify="center")
        
        valid_choices = [opt[0].lower() for opt in options] + ['b']
        
        choice = Prompt.ask(
            "\n🎯 Choose action",
            choices=valid_choices,
            default='b'
        )
        
        return choice.lower()
        
    def show_progress_indicator(self, message: str, steps: list):
        """Show progress for multi-step operations"""
        
        progress_text = Text()
        progress_text.append(f"⚡ {message}\n\n", style="bold cyan")
        
        for i, step in enumerate(steps, 1):
            progress_text.append(f"{i}. {step}\n", style="white")
            
        progress_panel = Panel(
            progress_text,
            title="🔄 Processing",
            border_style="yellow",
            padding=(1, 2)
        )
        
        self.console.print(progress_panel)
        
    def show_results_panel(self, title: str, content: str, style: str = "green"):
        """Display results in a formatted panel"""
        
        results_panel = Panel(
            content,
            title=f"📊 {title}",
            border_style=style,
            padding=(1, 2)
        )
        
        self.console.print(results_panel)
        
    def show_warning(self, message: str):
        """Display warning message"""
        
        warning_panel = Panel(
            message,
            title="⚠️ Warning",
            border_style="yellow",
            padding=(1, 2)
        )
        
        self.console.print(warning_panel)
        
    def show_error(self, message: str):
        """Display error message"""
        
        error_panel = Panel(
            message,
            title="❌ Error",
            border_style="red",
            padding=(1, 2)
        )
        
        self.console.print(error_panel)
        
    def show_success(self, message: str):
        """Display success message"""
        
        success_panel = Panel(
            message,
            title="✅ Success",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(success_panel)
        
    def wait_for_user(self, message: str = "Press Enter to continue"):
        """Wait for user input to continue"""
        Prompt.ask(f"\n{message}")
        
    def get_user_input(self, prompt: str, password: bool = False) -> str:
        """Get input from user"""
        if password:
            return Prompt.ask(prompt, password=True)
        else:
            return Prompt.ask(prompt)
            
    def confirm_action(self, message: str) -> bool:
        """Ask user for confirmation"""
        from rich.prompt import Confirm
        return Confirm.ask(message)