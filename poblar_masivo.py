import os
import django
import random

# 1. Configuración del entorno Django
# Asegúrate de que 'mad_science' sea el nombre de tu carpeta de configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mad_science.settings')
django.setup()

from laboratorio.models import Cientifico, MaterialSospechoso, Invento, Componente, Receta, ProtocoloAutodestruccion

def inyectar_datos():
    print("☢️ INICIANDO INYECCIÓN MASIVA DE DATOS...")

    # ---------------------------------------------------------
    # 1. CIENTÍFICOS LOCOS (4 Famosos)
    # ---------------------------------------------------------
    lista_cientificos = [
        ("Dr. Victor Frankenstein", "Reanimación Biológica", "Obsesionado con coser partes de gente. Grita mucho '¡ESTÁ VIVO!'."),
        ("Profesor Hubert Farnsworth", "Física Cuántica Absurda", "Dueño de Planet Express. Inventa cosas inútiles o apocalípticas."),
        ("Dr. Jekyll", "Química de la Personalidad", "Tiene serios problemas de ira y cambios de humor repentinos."),
        ("Dr. Evil (Maligno)", "Dominación Mundial", "Pide rescates de 1 millón de dólares. Tiene un gato sin pelo."),
    ]

    for nombre, esp, bio in lista_cientificos:
        c, created = Cientifico.objects.get_or_create(
            nombre=nombre, 
            defaults={'especialidad': esp, 'biografia': bio}
        )
        if created: print(f"  [+] Contratado: {nombre}")

    # ---------------------------------------------------------
    # 2. MATERIALES SOSPECHOSOS (14 Ítems)
    # ---------------------------------------------------------
    lista_materiales = [
        ("Plutonio Casero", "EXTREMO", True, 500.00),
        ("Baba de Alien", "ALTO", True, 120.50),
        ("Ectoplasma", "MEDIO", False, 15.00),
        ("Veneno de Cobra", "ALTO", True, 5.00),
        ("Pelo de Yeti", "BAJO", False, 1000.00),
        ("Antimateria Líquida", "EXTREMO", True, 0.50),
        ("Gas de la Risa Permanente", "MEDIO", True, 200.00),
        ("Polvo de Hadas (Alucinógeno)", "ALTO", True, 50.00),
        ("Sangre de Dragón", "MEDIO", True, 750.00),
        ("Mercurio Rojo", "EXTREMO", True, 100.00),
        ("Ácido Sulfúrico Casero", "ALTO", False, 5000.00),
        ("Esporas de Moho Gigante", "ALTO", True, 30.00),
        ("ADN de Dinosaurio", "EXTREMO", True, 2.00),
        ("Gomitas de Osito (Caducadas)", "BAJO", False, 50000.00),
    ]

    for nombre, peligro, ilegal, stock in lista_materiales:
        m, created = MaterialSospechoso.objects.get_or_create(
            nombre=nombre,
            defaults={'nivel_peligro': peligro, 'es_ilegal': ilegal, 'stock_gramos': stock}
        )
        if created: print(f"  [+] Almacenado: {nombre}")

    # ---------------------------------------------------------
    # 3. COMPONENTES (12 Ítems)
    # ---------------------------------------------------------
    lista_componentes = [
        "Bobina de Tesla", "Tubo de Vacío", "Chip de IA Rebelde", 
        "Engranaje Oxidado", "Lente de Cristal Puro", "Batería Nuclear", 
        "Brazo Robótico", "Antena Parabólica", "Imán de Neodimio", 
        "Botón Rojo Grande", "Condensador de Fluzo", "Fusible Quemado"
    ]

    objs_componentes = []
    for comp in lista_componentes:
        obj, created = Componente.objects.get_or_create(nombre=comp)
        objs_componentes.append(obj)
        if created: print(f"  [+] Componente creado: {comp}")

    # ---------------------------------------------------------
    # 4. INVENTOS (4 Ítems) + Recetas + Protocolos
    # ---------------------------------------------------------
    lista_inventos = [
        ("El Monstruo", "Un ser humano hecho de partes recicladas.", 45),
        ("Máquina del Tiempo DeLorean", "Funciona con basura, viaja a 1955.", 88),
        ("Rayo de la Muerte (Láser)", "Para escribir el nombre en la luna.", 99),
        ("Oloroscopio", "Permite oler cosas a distancias astronómicas.", 10),
    ]

    for nombre, desc, prob in lista_inventos:
        inv, created = Invento.objects.get_or_create(
            nombre=nombre,
            defaults={
                'descripcion': desc, 
                'probabilidad_exito': prob,
                'fecha_fabricacion': '2023-01-01' # Fecha default para evitar errores
            }
        )
        
        if created:
            print(f"  [+] Invento patentado: {nombre}")
            
            # Asignar 3 componentes aleatorios a cada invento
            componentes_random = random.sample(objs_componentes, 3)
            for comp in componentes_random:
                Receta.objects.create(
                    invento=inv,
                    componente=comp,
                    cantidad=random.randint(1, 10)
                )
            
            # Crear protocolo de autodestrucción (1:1)
            ProtocoloAutodestruccion.objects.create(
                invento=inv,
                codigo_activacion=f"DANGER-{random.randint(100,999)}",
                mensaje_despedida="¡No debiste presionar eso!"
            )

    print("\n✅ ¡CARGA DE DATOS COMPLETADA EXITOSAMENTE!")

if __name__ == '__main__':
    inyectar_datos()