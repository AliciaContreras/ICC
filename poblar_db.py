import os
import django
import random

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mad_science.settings')
django.setup()

from laboratorio.models import Cientifico, Esbirro, Invento, Componente, Receta, ProtocoloAutodestruccion

def poblar():
    print("🧪 Iniciando protocolo de clonación de datos...")

    # 1. Crear Científicos Locos Famosos
    cientificos_data = [
        ("Rick Sanchez", "Realidades Alternas", "El hombre más inteligente del universo."),
        ("Dr. Heinz Doofenshmirtz", "Inadores", "Gobernante del Área Limítrofe (casi)."),
        ("Dr. Neo Cortex", "Mutaciones Genéticas", "Enemigo de los Bandicoots."),
        ("Dexter", "Ingeniería Mecánica", "El niño genio con un laboratorio secreto."),
        ("Dr. Emmet Brown", "Viajes en el Tiempo", "¡Gran Scott!"),
    ]

    cientificos_objs = []
    for nombre, esp, bio in cientificos_data:
        c, created = Cientifico.objects.get_or_create(nombre=nombre, defaults={'especialidad': esp, 'biografia': bio})
        cientificos_objs.append(c)
        print(f" - Contratado: {nombre}")

    # 2. Asignar Esbirros
    nombres_esbirros = ["Igor", "Minion Kevin", "Minion Bob", "Robot X-20", "Norm", "Morty", "Dee Dee", "Cerebro"]
    
    for c in cientificos_objs:
        # Crear 1 a 3 esbirros por científico
        for _ in range(random.randint(1, 3)):
            Esbirro.objects.create(
                cientifico=c,
                nombre=random.choice(nombres_esbirros) + f" {random.randint(1, 99)}",
                tiene_joroba=random.choice([True, False]),
                nivel_lealtad=random.randint(1, 10)
            )

    # 3. Componentes Comunes
    componentes = ["Uranio", "Cinta Americana", "Tornillo 5mm", "Microchip", "Gema de Poder", "Plátano", "Láser"]
    comp_objs = []
    for comp in componentes:
        obj, _ = Componente.objects.get_or_create(nombre=comp)
        comp_objs.append(obj)

    # 4. Inventos
    inventos_data = [
        ("Pistola de Portales", "Viaja entre dimensiones.", 50),
        ("Inador de Fuego", "Quema cosas.", 85),
        ("Rayo Evolucionador", "Convierte animales en mutantes.", 40),
        ("DeLorean Volador", "A donde vamos no necesitamos carreteras.", 95),
        ("Traje de Combate", "Resiste explosiones.", 70),
    ]

    for nombre, desc, exito in inventos_data:
        inv, created = Invento.objects.get_or_create(
            nombre=nombre, 
            defaults={'descripcion': desc, 'probabilidad_exito': exito}
        )
        if created:
            # Crear Receta (N:N)
            for _ in range(2):
                Receta.objects.create(
                    invento=inv, 
                    componente=random.choice(comp_objs), 
                    cantidad=random.randint(1, 10)
                )
            # Crear Protocolo (1:1)
            ProtocoloAutodestruccion.objects.create(
                invento=inv,
                codigo_activacion=f"CODE-{random.randint(1000,9999)}",
                mensaje_despedida="¡Boom!"
            )
            print(f" - Inventado: {nombre}")

    print("✅ ¡Laboratorio completamente operativo!")

if __name__ == '__main__':
    poblar()