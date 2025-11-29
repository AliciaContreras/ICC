import os
import django
import random
from decimal import Decimal

# 1. CONFIGURACIÓN DEL ENTORNO DJANGO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mad_science.settings')
django.setup()

# 2. IMPORTACIÓN DE MODELOS
from laboratorio.models import (
    Cientifico, Esbirro, MaterialSospechoso, 
    Invento, Componente, Receta, ProtocoloAutodestruccion
)

def poblar_cientificos():
    print("\n👨‍🔬 [FASE 1] RECLUTANDO CIENTÍFICOS...")
    lista_cientificos = [
        ("Dr. Victor Frankenstein", "Reanimación Biológica", "Obsesionado con coser partes de gente. Grita mucho '¡ESTÁ VIVO!'."),
        ("Profesor Hubert Farnsworth", "Física Cuántica Absurda", "Dueño de Planet Express. Inventa cosas inútiles o apocalípticas."),
        ("Dr. Jekyll", "Química de la Personalidad", "Tiene serios problemas de ira y cambios de humor repentinos."),
        ("Dr. Evil (Maligno)", "Dominación Mundial", "Pide rescates de 1 millón de dólares. Tiene un gato sin pelo."),
        ("Rick Sanchez", "Viajes Interdimensionales", "Científico alcohólico y nihilista. Busca la salsa Szechuan."),
        ("Dr. Heinz Doofenshmirtz", "Inadores Malvados", "Dueño de Doofenshmirtz Malvados y Asociados. Enemigo de un ornitorrinco."),
        ("Emmett Brown", "Viajes en el Tiempo", "Inventó el condensador de flujo tras golpearse la cabeza en el baño."),
        ("Dr. Neo Cortex", "Dominación Mundial", "Genio malvado con una 'N' gigante en la frente. Odia a los bandicoots."),
        ("Dexter", "Ingeniería Mecánica", "El niño genio con un laboratorio secreto."),
        ("Dr. Otto Octavius", "Fusión Nuclear", "Tiene 4 brazos mecánicos y un mal temperamento.")
    ]

    count = 0
    for nombre, esp, bio in lista_cientificos:
        c, created = Cientifico.objects.get_or_create(
            nombre=nombre, 
            defaults={'especialidad': esp, 'biografia': bio}
        )
        if created: 
            print(f"  [+] Contratado: {nombre}")
            count += 1
    print(f"  >> Total científicos nuevos: {count}")

def poblar_componentes():
    print("\n⚙️ [FASE 2] FABRICANDO COMPONENTES...")
    lista_componentes = [
        "Bobina de Tesla", "Tubo de Vacío", "Chip de IA Rebelde", 
        "Engranaje Oxidado", "Lente de Cristal Puro", "Batería Nuclear", 
        "Brazo Robótico", "Antena Parabólica", "Imán de Neodimio", 
        "Botón Rojo Grande", "Condensador de Fluzo", "Fusible Quemado",
        "Tubo de Rayos Catódicos", "Cristal Kyber", "Pila Nuclear de Bolsillo",
        "Engranaje de Adamantium", "Cerebro en Frasco", "Generador de Portales",
        "Láser de la Muerte (Mini)", "Nanobots"
    ]

    count = 0
    created_objs = []
    for comp in lista_componentes:
        obj, created = Componente.objects.get_or_create(nombre=comp)
        if created: 
            print(f"  [+] Fabricado: {comp}")
            count += 1
        created_objs.append(obj)
    print(f"  >> Total componentes nuevos: {count}")
    return created_objs

def poblar_materiales():
    print("\n📦 [FASE 3] LLENANDO BODEGA DE SUMINISTROS...")
    lista_materiales = [
        # Nombre, Peligro, Ilegal, Stock Base
        ("Plutonio Casero", "EXTREMO", True, 500.00),
        ("Baba de Alien", "ALTO", True, 120.50),
        ("Ectoplasma", "MEDIO", False, 15.00),
        ("Veneno de Cobra", "ALTO", True, 5.00),
        ("Pelo de Yeti", "BAJO", False, 1000.00),
        ("Antimateria Líquida", "EXTREMO", True, 0.50),
        ("Gas de la Risa Permanente", "MEDIO", True, 200.00),
        ("Polvo de Hadas", "ALTO", True, 50.00),
        ("Sangre de Dragón", "MEDIO", True, 750.00),
        ("Mercurio Rojo", "EXTREMO", True, 100.00),
        ("Ácido Sulfúrico Casero", "ALTO", False, 5000.00),
        ("Esporas de Moho Gigante", "ALTO", True, 30.00),
        ("ADN de Dinosaurio", "EXTREMO", True, 2.00),
        ("Gomitas de Osito (Caducadas)", "BAJO", False, 50000.00),
        ("Vibranium Líquido", "EXTREMO", True, 10.00),
        ("Uranio Empobrecido", "MEDIO", False, 300.00),
        ("Materia Oscura", "EXTREMO", True, 1.00),
        ("Kryptonita Verde", "ALTO", True, 25.00),
        ("Mutágeno T-Virus", "EXTREMO", True, 5.00)
    ]

    count = 0
    for nombre, peligro, ilegal, stock_base in lista_materiales:
        # Variación aleatoria del stock para que no sea siempre igual
        stock_real = Decimal(stock_base) + Decimal(random.uniform(-5.0, 50.0))
        
        m, created = MaterialSospechoso.objects.get_or_create(
            nombre=nombre,
            defaults={
                'nivel_peligro': peligro, 
                'es_ilegal': ilegal, 
                'stock_gramos': stock_real
            }
        )
        if created: 
            print(f"  [+] Almacenado: {nombre}")
            count += 1
    print(f"  >> Total materiales nuevos: {count}")

def poblar_inventos(todos_los_componentes):
    print("\n🦾 [FASE 4] REGISTRANDO PROTOTIPOS...")
    lista_inventos = [
        ("El Monstruo", "Un ser humano hecho de partes recicladas.", 45),
        ("Máquina del Tiempo DeLorean", "Funciona con basura, viaja a 1955.", 88),
        ("Rayo de la Muerte (Láser)", "Para escribir el nombre en la luna.", 99),
        ("Oloroscopio", "Permite oler cosas a distancias astronómicas.", 10),
        ("Pistola de Portales", "Crea agujeros de gusano verdes en superficies planas.", 95),
        ("Inador de Fuego", "Un invento malvado que escupe fuego.", 70),
        ("Traje de Combate", "Armadura potenciada por energía nuclear.", 60),
        ("Rayo Hipnotizador", "Convierte a la gente en gallinas.", 30)
    ]

    count = 0
    for nombre, desc, prob in lista_inventos:
        inv, created = Invento.objects.get_or_create(
            nombre=nombre,
            defaults={
                'descripcion': desc, 
                'probabilidad_exito': prob,
                'fecha_fabricacion': '2025-11-26' # Fecha fija o random
            }
        )
        
        if created:
            count += 1
            print(f"  [+] Patente registrada: {nombre}")
            
            # Asignar entre 2 y 5 componentes aleatorios
            if todos_los_componentes:
                componentes_random = random.sample(todos_los_componentes, min(len(todos_los_componentes), random.randint(2, 5)))
                for comp in componentes_random:
                    Receta.objects.get_or_create(
                        invento=inv,
                        componente=comp,
                        defaults={'cantidad': random.randint(1, 10)}
                    )
            
            # Crear protocolo de autodestrucción (si no existe)
            if not hasattr(inv, 'protocoloautodestruccion'):
                ProtocoloAutodestruccion.objects.create(
                    invento=inv,
                    codigo_activacion=f"OMEGA-{random.randint(100,999)}",
                    mensaje_despedida="¡Ha sido un placer, caballeros!"
                )
    print(f"  >> Total inventos nuevos: {count}")

def reclutar_esbirros():
    print("\n🧟 [FASE 5] ASIGNACIÓN DE PERSONAL (ESBIRROS)...")
    
    cientificos = Cientifico.objects.all()
    if not cientificos.exists():
        print("  [!] No hay científicos para asignar esbirros.")
        return

    nombres_base = [
        "Igor", "Grognak", "Kevin", "Sujeto #", "Renfield", "Kronk", 
        "Mini-Yo", "Bob", "Stuart", "Frankenstein Jr.", "Lurch", "Gunter", 
        "Bebop", "Rocksteady", "Cerebro", "Pinky", "Número 2", 
        "Robot X-20", "Norm", "Mojo"
    ]

    total_nuevos = 0
    for doc in cientificos:
        # Solo asigna esbirros si tiene pocos
        if doc.esbirros.count() < 3:
            cantidad = random.randint(2, 4)
            print(f"  -> Asignando {cantidad} ayudantes a: {doc.nombre}")
            
            for _ in range(cantidad):
                nombre_base = random.choice(nombres_base)
                nombre_final = f"{nombre_base} {random.randint(1, 99)}"
                
                Esbirro.objects.create(
                    cientifico=doc,
                    nombre=nombre_final,
                    tiene_joroba=random.choice([True, False, True]),
                    nivel_lealtad=random.randint(1, 10)
                )
                total_nuevos += 1
    
    print(f"  >> Total esbirros reclutados: {total_nuevos}")

def ejecucion_maestra():
    print("⚡ --- INICIANDO PROTOCOLO DE POBLADO MASIVO DEL LABORATORIO --- ⚡")
    
    poblar_cientificos()
    objs_componentes = poblar_componentes()
    poblar_materiales()
    poblar_inventos(objs_componentes)
    reclutar_esbirros()
    
    print("\n✅ --- OPERACIÓN COMPLETADA CON ÉXITO ---")
    print("    La base de datos está lista para experimentar.")

if __name__ == '__main__':
    ejecucion_maestra()