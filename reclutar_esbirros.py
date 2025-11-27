import os
import django
import random

# Configuración del entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mad_science.settings')
django.setup()

from laboratorio.models import Cientifico, Esbirro

def reclutamiento_masivo():
    # 1. Obtener todos los científicos existentes
    cientificos = Cientifico.objects.all()
    
    if not cientificos.exists():
        print("❌ ERROR: No hay científicos en la base de datos. Ejecuta primero poblar_masivo.py")
        return

    print(f"🧟 INICIANDO CAMPAÑA DE RECLUTAMIENTO PARA {cientificos.count()} CIENTÍFICOS...")

    # 2. Lista de nombres de esbirros clásicos y divertidos
    nombres_base = [
        "Igor", "Grognak", "Kevin (El Becario)", "Sujeto #42", 
        "Renfield", "Kronk", "Mini-Yo", "Bob", "Stuart", 
        "Frankenstein Jr.", "Lurch", "Gunter", "Bebop", 
        "Rocksteady", "Asistente Genérico", "El Jorobado",
        "Cerebro", "Pinky", "Número 2", "Doom-Bot Defectuoso"
    ]

    total_nuevos = 0

    # 3. Asignar secuaces a cada científico
    for doc in cientificos:
        # Decidir cuántos nuevos contratar para este científico (entre 3 y 5)
        cantidad_a_contratar = random.randint(3, 5)
        
        print(f"\n  👨‍🔬 Asignando personal a: {doc.nombre}...")

        for _ in range(cantidad_a_contratar):
            # Crear datos aleatorios
            nombre_elegido = random.choice(nombres_base)
            # Le agregamos un número de serie para que no sean todos iguales
            nombre_final = f"{nombre_elegido}-{random.randint(100, 999)}"
            
            tiene_joroba = random.choice([True, False, True]) # 66% probabilidad de joroba
            lealtad = random.randint(1, 10) # 1 es traidor, 10 se sacrifica por el jefe

            # Crear el registro en la BD
            Esbirro.objects.create(
                cientifico=doc,
                nombre=nombre_final,
                tiene_joroba=tiene_joroba,
                nivel_lealtad=lealtad
            )
            
            estado_joroba = "Con Joroba" if tiene_joroba else "Postura Correcta"
            print(f"    [+] Contratado: {nombre_final} ({estado_joroba}, Lealtad: {lealtad})")
            total_nuevos += 1

    print(f"\n✅ ¡RECLUTAMIENTO FINALIZADO! Se han añadido {total_nuevos} nuevos esbirros.")

if __name__ == '__main__':
    reclutamiento_masivo()