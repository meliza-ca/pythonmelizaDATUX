def sumar_numeros():
    """Función para sumar dos números"""
    print("\n--- Sumar dos números ---")
    try:
        num1 = float(input("Ingrese el primer número: "))
        num2 = float(input("Ingrese el segundo número: "))
        resultado = num1 + num2
        print(f"La suma de {num1} + {num2} = {resultado}")
    except ValueError:
        print("Error: Debe ingresar números válidos")
    input("\nPresione Enter para continuar...")

def crear_coleccion_productos():
    """Función para crear una colección inicial de productos"""
    print("\n--- Crear colección de productos ---")
    
    productos = [
        {"nombre": "Arroz", "precio": 2.50, "categoria": "Granos"},
        {"nombre": "Leche", "precio": 1.20, "categoria": "Lácteos"},
        {"nombre": "Pan", "precio": 0.80, "categoria": "Panadería"},
        {"nombre": "Manzanas", "precio": 3.00, "categoria": "Frutas"},
        {"nombre": "Pollo", "precio": 5.50, "categoria": "Carnes"}
    ]
    
    print(f"Se ha creado una colección con {len(productos)} productos:")
    for producto in productos:
        print(f"  - {producto['nombre']}: ${producto['precio']:.2f} ({producto['categoria']})")
    
    return productos

def agregar_producto(productos):
    """Función para agregar un nuevo producto a la colección"""
    print("\n--- Agregar nuevo producto ---")
    
    if not productos:
        print("Primero debe crear la colección de productos (Opción 2)")
        input("\nPresione Enter para continuar...")
        return productos
    
    try:
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            return productos
        
        precio = float(input("Precio del producto: "))
        if precio < 0:
            print("Error: El precio no puede ser negativo")
            return productos
        
        categoria = input("Categoría del producto: ").strip()
        if not categoria:
            categoria = "Sin categoría"
        
        nuevo_producto = {
            "nombre": nombre,
            "precio": precio,
            "categoria": categoria
        }
        
        productos.append(nuevo_producto)
        print(f"Producto '{nombre}' agregado exitosamente!")
        
    except ValueError:
        print("Error: El precio debe ser un número válido")
    
    input("\nPresione Enter para continuar...")
    return productos

def mostrar_producto_mas_barato(productos):
    """Función para mostrar el producto de precio más bajo"""
    print("\n--- Producto de precio más bajo ---")
    
    if not productos:
        print("No hay productos en la colección. Cree una primero (Opción 2).")
    else:
        producto_mas_barato = min(productos, key=lambda x: x['precio'])
        
        print(f"Producto más económico:")
        print(f"  Nombre: {producto_mas_barato['nombre']}")
        print(f"  Precio: ${producto_mas_barato['precio']:.2f}")
        print(f"  Categoría: {producto_mas_barato['categoria']}")
        
        productos_mismo_precio = [p for p in productos if p['precio'] == producto_mas_barato['precio']]
        if len(productos_mismo_precio) > 1:
            print(f"\nHay {len(productos_mismo_precio)} productos con el mismo precio mínimo:")
            for producto in productos_mismo_precio:
                if producto['nombre'] != producto_mas_barato['nombre']:
                    print(f"  - {producto['nombre']}")
    
    input("\nPresione Enter para continuar...")

def mostrar_menu():
    """Función para mostrar el menú principal"""
    print("\n" + "="*50)
    print("MENÚ PRINCIPAL")
    print("="*50)
    print("1. Sumar 2 números")
    print("2. Crear colección de productos")
    print("3. Agregar un nuevo producto")
    print("4. Mostrar producto de precio más bajo")
    print("5. Salir")
    print("="*50)

def main():
    """Función principal del programa"""
    productos = []
    coleccion_creada = False
    
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("\nSeleccione una opción (1-5): "))
            
            if opcion == 1:
                sumar_numeros()
            elif opcion == 2:
                productos = crear_coleccion_productos()
                coleccion_creada = True
            elif opcion == 3:
                if not coleccion_creada:
                    print("\nPrimero debe crear la colección de productos (Opción 2)")
                    input("Presione Enter para continuar...")
                else:
                    productos = agregar_producto(productos)
            elif opcion == 4:
                mostrar_producto_mas_barato(productos)
            elif opcion == 5:
                print("\n¡Gracias por usar el programa! ¡Hasta pronto!")
                break
            else:
                print("\nOpción no válida. Por favor, seleccione una opción del 1 al 5.")
                input("Presione Enter para continuar...")
                
        except ValueError:
            print("\nError: Debe ingresar un número válido")
            input("Presione Enter para continuar...")
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario")
            break

if __name__ == "__main__":
    print("Bienvenido al Sistema de Gestión")
    print("Este programa incluye operaciones matemáticas y gestión de productos")
    main()
