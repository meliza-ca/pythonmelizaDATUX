"""
Servicio para gestion de propiedades inmobiliarias
"""

from servicios.email_service import enviar_notificacion_propiedad
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box

console = Console()

class InmobiliarioService:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
    
    def agregar_propiedad(self):
        """Agrega una nueva propiedad y envia email de confirmacion"""
        try:
            console.clear()
            console.print("[bold yellow]AGREGAR NUEVA PROPIEDAD[/bold yellow]\n")
            
            # Solicitar datos basicos
            tipo = Prompt.ask("Tipo de propiedad (casa/departamento/terreno/local)", 
                            choices=["casa", "departamento", "terreno", "local"])
            direccion = Prompt.ask("Direccion completa")
            
            # Validar precio
            while True:
                try:
                    precio = float(Prompt.ask("Precio (USD)"))
                    if precio > 0:
                        break
                    console.print("[red]El precio debe ser mayor a 0[/red]")
                except ValueError:
                    console.print("[red]Ingrese un numero valido[/red]")
            
            # Validar habitaciones
            while True:
                try:
                    habitaciones = int(Prompt.ask("Numero de habitaciones"))
                    if habitaciones >= 0:
                        break
                    console.print("[red]El numero debe ser 0 o positivo[/red]")
                except ValueError:
                    console.print("[red]Ingrese un numero entero[/red]")
            
            # Validar banos
            while True:
                try:
                    banios = int(Prompt.ask("Numero de banos"))
                    if banios >= 0:
                        break
                    console.print("[red]El numero debe ser 0 o positivo[/red]")
                except ValueError:
                    console.print("[red]Ingrese un numero entero[/red]")
            
            # Validar metros cuadrados
            while True:
                try:
                    metros_cuadrados = float(Prompt.ask("Metros cuadrados"))
                    if metros_cuadrados > 0:
                        break
                    console.print("[red]Los metros cuadrados deben ser mayores a 0[/red]")
                except ValueError:
                    console.print("[red]Ingrese un numero valido[/red]")
            
            descripcion = Prompt.ask("Descripcion (opcional)", default="")
            
            # Solicitar ID del propietario y verificar que existe
            while True:
                try:
                    propietario_id = int(Prompt.ask("ID del propietario"))
                    
                    # Verificar que el propietario existe
                    self.cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = ?", (propietario_id,))
                    propietario = self.cursor.fetchone()
                    
                    if propietario:
                        break
                    else:
                        console.print(f"[red]No existe un usuario con ID {propietario_id}[/red]")
                except ValueError:
                    console.print("[red]Ingrese un numero valido[/red]")
            
            # Insertar en la base de datos
            sql = """
            INSERT INTO propiedades 
            (tipo, direccion, precio, habitaciones, banios, metros_cuadrados, 
             descripcion, propietario_id, fecha_creacion, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            estado = "disponible"
            
            valores = (tipo, direccion, precio, habitaciones, banios, 
                      metros_cuadrados, descripcion, propietario_id, 
                      fecha_actual, estado)
            
            self.cursor.execute(sql, valores)
            self.conn.commit()
            
            propiedad_id = self.cursor.lastrowid
            
            console.print(f"\n[green]Propiedad registrada exitosamente![/green]")
            console.print(f"[cyan]ID de propiedad: {propiedad_id}[/cyan]")
            
            # ENVIAR EMAIL DE CONFIRMACION
            datos_email = {
                'propietario_nombre': propietario[1],  # nombre del propietario
                'id': propiedad_id,
                'tipo': tipo,
                'direccion': direccion,
                'precio': precio,
                'habitaciones': habitaciones,
                'banios': banios,
                'metros_cuadrados': metros_cuadrados,
                'fecha_registro': fecha_actual
            }
            
            if enviar_notificacion_propiedad(propietario[2], datos_email):  # email del propietario
                console.print("[green]Notificacion enviada al propietario[/green]")
            else:
                console.print("[yellow]Propiedad registrada, pero error enviando email[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error al agregar propiedad: {e}[/red]")
    
    def listar_propiedades(self):
        """Lista todas las propiedades del sistema"""
        try:
            self.cursor.execute("""
                SELECT p.*, u.nombre as propietario_nombre 
                FROM propiedades p
                LEFT JOIN usuarios u ON p.propietario_id = u.id
                ORDER BY p.fecha_creacion DESC
            """)
            propiedades = self.cursor.fetchall()
            
            console.clear()
            console.print("[bold yellow]LISTADO DE PROPIEDADES[/bold yellow]\n")
            
            if not propiedades:
                console.print("[blue]No hay propiedades registradas[/blue]")
                return
            
            table = Table(title=f"Total: {len(propiedades)} propiedades", 
                         box=box.ROUNDED, header_style="bold magenta")
            table.add_column("ID", style="cyan", width=5)
            table.add_column("Tipo", style="green", width=10)
            table.add_column("Direccion", style="white", width=30)
            table.add_column("Precio", style="yellow", width=15)
            table.add_column("Propietario", style="blue", width=20)
            table.add_column("Estado", style="magenta", width=12)
            
            for prop in propiedades:
                # Convertir tupla a diccionario si es necesario
                if isinstance(prop, tuple):
                    prop_dict = {
                        'id': prop[0],
                        'tipo': prop[1],
                        'direccion': prop[2],
                        'precio': prop[3],
                        'propietario_nombre': prop[10] if len(prop) > 10 else 'N/A',
                        'estado': prop[9] if len(prop) > 9 else 'N/A'
                    }
                else:
                    prop_dict = prop
                
                precio_formateado = f"${prop_dict.get('precio', 0):,.2f}"
                estado = prop_dict.get('estado', 'N/A')
                
                # Color segun estado
                estilo_estado = "green" if estado == "disponible" else "red" if estado == "vendido" else "yellow"
                
                table.add_row(
                    str(prop_dict.get('id', 'N/A')),
                    prop_dict.get('tipo', 'N/A').capitalize(),
                    prop_dict.get('direccion', 'N/A'),
                    precio_formateado,
                    prop_dict.get('propietario_nombre', 'N/A'),
                    f"[{estilo_estado}]{estado}[/{estilo_estado}]"
                )
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error al listar propiedades: {e}[/red]")
    
    def buscar_propiedad_por_id(self):
        """Busca una propiedad por su ID"""
        try:
            propiedad_id = int(Prompt.ask("Ingrese ID de la propiedad"))
            
            self.cursor.execute("""
                SELECT p.*, u.nombre as propietario_nombre, u.email
                FROM propiedades p
                LEFT JOIN usuarios u ON p.propietario_id = u.id
                WHERE p.id = ?
            """, (propiedad_id,))
            
            propiedad = self.cursor.fetchone()
            
            if propiedad:
                console.clear()
                console.print(f"[bold green]PROPIEDAD ENCONTRADA - ID: {propiedad_id}[/bold green]\n")
                
                # Mostrar detalles
                if isinstance(propiedad, tuple):
                    detalles = {
                        'ID': propiedad[0],
                        'Tipo': propiedad[1],
                        'Direccion': propiedad[2],
                        'Precio': f"${propiedad[3]:,.2f}",
                        'Habitaciones': propiedad[4],
                        'Banos': propiedad[5],
                        'Metros2': propiedad[6],
                        'Descripcion': propiedad[7] or "Sin descripcion",
                        'Propietario': propiedad[10] if len(propiedad) > 10 else 'N/A',
                        'Email contacto': propiedad[11] if len(propiedad) > 11 else 'N/A',
                        'Estado': propiedad[9] if len(propiedad) > 9 else 'N/A',
                        'Fecha registro': propiedad[8] if len(propiedad) > 8 else 'N/A'
                    }
                else:
                    detalles = {
                        'ID': propiedad['id'],
                        'Tipo': propiedad['tipo'],
                        'Direccion': propiedad['direccion'],
                        'Precio': f"${propiedad['precio']:,.2f}",
                        'Habitaciones': propiedad['habitaciones'],
                        'Banos': propiedad['banios'],
                        'Metros2': propiedad['metros_cuadrados'],
                        'Descripcion': propiedad['descripcion'] or "Sin descripcion",
                        'Propietario': propiedad['propietario_nombre'],
                        'Email contacto': propiedad['email'],
                        'Estado': propiedad['estado'],
                        'Fecha registro': propiedad['fecha_creacion']
                    }
                
                for clave, valor in detalles.items():
                    console.print(f"[cyan]{clave}:[/cyan] [white]{valor}[/white]")
            else:
                console.print(f"[red]No se encontro propiedad con ID {propiedad_id}[/red]")
                
        except ValueError:
            console.print("[red]Ingrese un ID valido (numero)[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    
    def actualizar_propiedad(self):
        """Actualiza los datos de una propiedad"""
        try:
            propiedad_id = int(Prompt.ask("Ingrese ID de la propiedad a actualizar"))
            
            # Verificar que existe
            self.cursor.execute("SELECT * FROM propiedades WHERE id = ?", (propiedad_id,))
            if not self.cursor.fetchone():
                console.print(f"[red]No existe propiedad con ID {propiedad_id}[/red]")
                return
            
            console.print(f"[yellow]Actualizando propiedad ID: {propiedad_id}[/yellow]")
            console.print("[blue]Deje en blanco para mantener el valor actual[/blue]\n")
            
            # Solicitar nuevos valores
            nuevo_tipo = Prompt.ask("Nuevo tipo (casa/departamento/terreno/local)", 
                                  default="", show_default=False)
            nueva_direccion = Prompt.ask("Nueva direccion", default="", show_default=False)
            
            nuevo_precio = Prompt.ask("Nuevo precio", default="", show_default=False)
            nuevo_precio = float(nuevo_precio) if nuevo_precio else None
            
            # Construir consulta dinamica
            campos = []
            valores = []
            
            if nuevo_tipo:
                campos.append("tipo = ?")
                valores.append(nuevo_tipo)
            if nueva_direccion:
                campos.append("direccion = ?")
                valores.append(nueva_direccion)
            if nuevo_precio is not None:
                campos.append("precio = ?")
                valores.append(nuevo_precio)
            
            if campos:
                valores.append(propiedad_id)
                sql = f"UPDATE propiedades SET {', '.join(campos)} WHERE id = ?"
                self.cursor.execute(sql, valores)
                self.conn.commit()
                console.print(f"[green]Propiedad {propiedad_id} actualizada correctamente[/green]")
            else:
                console.print("[yellow]No se realizaron cambios[/yellow]")
                
        except Exception as e:
            console.print(f"[red]Error al actualizar: {e}[/red]")
    
    def eliminar_propiedad(self):
        """Elimina logicamente una propiedad (cambia estado a 'eliminado')"""
        try:
            propiedad_id = int(Prompt.ask("Ingrese ID de la propiedad a eliminar"))
            
            if Confirm.ask(f"Esta seguro de eliminar la propiedad ID {propiedad_id}?"):
                self.cursor.execute(
                    "UPDATE propiedades SET estado = 'eliminado' WHERE id = ?",
                    (propiedad_id,)
                )
                self.conn.commit()
                
                if self.cursor.rowcount > 0:
                    console.print(f"[green]Propiedad {propiedad_id} eliminada correctamente[/green]")
                else:
                    console.print(f"[red]No se encontro propiedad con ID {propiedad_id}[/red]")
            else:
                console.print("[yellow]Operacion cancelada[/yellow]")
                
        except Exception as e:
            console.print(f"[red]Error al eliminar: {e}[/red]")
    
    def propiedades_por_propietario(self):
        """Muestra las propiedades de un propietario especifico"""
        try:
            propietario_id = int(Prompt.ask("Ingrese ID del propietario"))
            
            # Verificar que el propietario existe
            self.cursor.execute("SELECT nombre FROM usuarios WHERE id = ?", (propietario_id,))
            propietario = self.cursor.fetchone()
            
            if not propietario:
                console.print(f"[red]No existe usuario con ID {propietario_id}[/red]")
                return
            
            self.cursor.execute("""
                SELECT * FROM propiedades 
                WHERE propietario_id = ? AND estado != 'eliminado'
                ORDER BY fecha_creacion DESC
            """, (propietario_id,))
            
            propiedades = self.cursor.fetchall()
            
            nombre_propietario = propietario[0] if isinstance(propietario, tuple) else propietario['nombre']
            
            console.clear()
            console.print(f"[bold yellow]PROPIEDADES DE: {nombre_propietario}[/bold yellow]\n")
            
            if not propiedades:
                console.print("[blue]Este propietario no tiene propiedades registradas[/blue]")
                return
            
            table = Table(title=f"Total: {len(propiedades)} propiedades", 
                         box=box.ROUNDED, header_style="bold magenta")
            table.add_column("ID", style="cyan", width=5)
            table.add_column("Tipo", style="green", width=10)
            table.add_column("Direccion", style="white", width=30)
            table.add_column("Precio", style="yellow", width=15)
            table.add_column("Estado", style="magenta", width=12)
            table.add_column("Fecha", style="blue", width=12)
            
            for prop in propiedades:
                if isinstance(prop, tuple):
                    prop_dict = {
                        'id': prop[0],
                        'tipo': prop[1],
                        'direccion': prop[2],
                        'precio': prop[3],
                        'estado': prop[9] if len(prop) > 9 else 'N/A',
                        'fecha_creacion': prop[8] if len(prop) > 8 else 'N/A'
                    }
                else:
                    prop_dict = prop
                
                precio_formateado = f"${prop_dict.get('precio', 0):,.2f}"
                fecha = prop_dict.get('fecha_creacion', 'N/A')
                if hasattr(fecha, 'strftime'):
                    fecha = fecha.strftime('%d/%m/%Y')
                
                estado = prop_dict.get('estado', 'N/A')
                estilo_estado = "green" if estado == "disponible" else "red" if estado == "vendido" else "yellow"
                
                table.add_row(
                    str(prop_dict.get('id', 'N/A')),
                    prop_dict.get('tipo', 'N/A').capitalize(),
                    prop_dict.get('direccion', 'N/A'),
                    precio_formateado,
                    f"[{estilo_estado}]{estado}[/{estilo_estado}]",
                    str(fecha)
                )
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
