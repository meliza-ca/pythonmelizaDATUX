# servicios/email_service.py
"""
Modulo para envio de emails del sistema
"""

import smtplib
from email.mime.text import MIMEText

def enviar_email(destinatario, asunto, mensaje):
    """
    Envia un email a traves de SMTP
    Version simulada para desarrollo
    """
    try:
        # Esta es una version simulada para pruebas
        # En produccion, reemplazar con configuracion real
        
        print("\n" + "="*60)
        print("ENVIO DE EMAIL SIMULADO")
        print("="*60)
        print(f"PARA: {destinatario}")
        print(f"ASUNTO: {asunto}")
        print("\nMENSAJE:")
        print("-"*40)
        print(mensaje)
        print("-"*40)
        print("\n[Simulacion: En produccion se enviaria realmente]")
        print("="*60)
        
        # Simular exito de envio
        return True
        
    except Exception as e:
        print(f"Error enviando email: {e}")
        return False


# Funcion especifica para el sistema inmobiliario
def enviar_notificacion_propiedad(destinatario, datos_propiedad):
    """
    Envia notificacion cuando se registra una propiedad
    
    Args:
        destinatario: Email del propietario
        datos_propiedad: Diccionario con datos de la propiedad
    """
    asunto = "Registro de Propiedad Confirmado"
    
    mensaje = f"""
Estimado/a {datos_propiedad.get('propietario_nombre', 'Cliente')},

Su propiedad ha sido registrada exitosamente en nuestro sistema.

DETALLES DE LA PROPIEDAD:
- ID: {datos_propiedad.get('id', 'N/A')}
- Tipo: {datos_propiedad.get('tipo', 'N/A')}
- Direccion: {datos_propiedad.get('direccion', 'N/A')}
- Precio: ${datos_propiedad.get('precio', 0):,.2f}
- Habitaciones: {datos_propiedad.get('habitaciones', 'N/A')}
- Banos: {datos_propiedad.get('banios', 'N/A')}
- Metros cuadrados: {datos_propiedad.get('metros_cuadrados', 'N/A')}

Fecha de registro: {datos_propiedad.get('fecha_registro', 'N/A')}

Gracias por usar nuestro sistema inmobiliario.

Atentamente,
El equipo de administracion
    """
    
    return enviar_email(destinatario, asunto, mensaje)


# Para pruebas directas
if __name__ == "__main__":
    # Ejemplo de prueba
    datos_ejemplo = {
        'propietario_nombre': 'Juan Perez',
        'id': 101,
        'tipo': 'Casa',
        'direccion': 'Av Principal 123',
        'precio': 150000,
        'habitaciones': 3,
        'banios': 2,
        'metros_cuadrados': 120,
        'fecha_registro': '2024-01-15 10:30:00'
    }
    
    enviar_notificacion_propiedad("ejemplo@email.com", datos_ejemplo)
