from rich.console import Console
from rich.prompt import Prompt
import sqlite3

console = Console()

class UsuarioService:
    def __init__(self, conn):
        self.conn = conn
    
    def agregar_usuario(self):
        """Registra un nuevo usuario en el sistema"""
        console.print("\n[bold cyan]════════════════════════════════[/bold cyan]")
        console.print("[bold yellow]  REGISTRO DE NUEVO USUARIO  [/bold yellow]")
        console.print("[bold cyan]════════════════════════════════[/bold cyan]\n")
        
        # Solicitar datos
        nombre = Prompt.ask("Nombre completo")
        email = Prompt.ask("Email")
        password = Prompt.ask("Contraseña", password=True)
        
        tipo_usuario = Prompt.ask(
            "Tipo de usuario",
            choices=["admin", "ventas"],
            default="ventas"
        )
        
        try:
            cursor = self.conn.cursor()
            
            # Verificar si el email ya existe
            cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
            if cursor.fetchone():
                console.print("\n[bold red]Error: El email ya está registrado[/bold red]")
                return False
            
            # Insertar nuevo usuario
            cursor.execute(
                """
                INSERT INTO usuarios (nombre, email, password, type_user, estado)
                VALUES (?, ?, ?, ?, 'activo')
                """,
                (nombre, email, password, tipo_usuario)
            )
            
            self.conn.commit()
            console.print(f"\n[bold green]✓ Usuario '{nombre}' registrado exitosamente![/bold green]")
            return True
            
        except sqlite3.Error as e:
            console.print(f"\n[bold red]Error al registrar usuario: {e}[/bold red]")
            return False
    
    def listar_usuarios(self):
        """Muestra todos los usuarios registrados"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, nombre, email, type_user, estado FROM usuarios")
            usuarios = cursor.fetchall()
            
            if not usuarios:
                console.print("\n[bold yellow]No hay usuarios registrados[/bold yellow]")
                return
            
            from rich.table import Table
            table = Table(title="📋 Usuarios del Sistema")
            table.add_column("ID", style="cyan")
            table.add_column("Nombre", style="white")
            table.add_column("Email", style="green")
            table.add_column("Tipo", style="yellow")
            table.add_column("Estado", style="magenta")
            
            for usuario in usuarios:
                table.add_row(
                    str(usuario[0]),
                    usuario[1],
                    usuario[2],
                    usuario[3],
                    usuario[4]
                )
            
            console.print(table)
            
        except sqlite3.Error as e:
            console.print(f"\n[bold red]Error al listar usuarios: {e}[/bold red]")
