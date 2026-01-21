"""
Script para construir el ejecutable (.exe) del Generador de Cartas de Cobro
Usa PyInstaller para crear un ejecutable standalone
"""
import subprocess
import sys
import shutil
from pathlib import Path

# Colores para la terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    """Imprime un paso del proceso."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}► {message}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(message):
    """Imprime mensaje de éxito."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_warning(message):
    """Imprime mensaje de advertencia."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_error(message):
    """Imprime mensaje de error."""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def check_pyinstaller():
    """Verifica si PyInstaller está instalado."""
    print_step("Verificando PyInstaller...")
    try:
        import PyInstaller
        print_success(f"PyInstaller {PyInstaller.__version__} encontrado")
        return True
    except ImportError:
        print_warning("PyInstaller no está instalado")
        print("Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print_success("PyInstaller instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print_error("No se pudo instalar PyInstaller")
            return False

def clean_build_folders():
    """Limpia las carpetas de builds anteriores."""
    print_step("Limpiando builds anteriores...")
    folders_to_clean = ["build", "dist"]
    files_to_clean = ["*.spec"]
    
    for folder in folders_to_clean:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print_success(f"Carpeta '{folder}' eliminada")
    
    for pattern in files_to_clean:
        for file in Path(".").glob(pattern):
            file.unlink()
            print_success(f"Archivo '{file}' eliminado")

def create_executable():
    """Crea el ejecutable con PyInstaller."""
    print_step("Construyendo ejecutable...")
    
    # Configuración de PyInstaller
    app_name = "GeneradorCartasCobro"
    main_script = "gui_simple.py"
    
    # Argumentos de PyInstaller
    pyinstaller_args = [
        "pyinstaller",
        "--name", app_name,
        "--windowed",  # Sin consola (solo ventana GUI)
        "--onefile",   # Un solo archivo ejecutable
        "--clean",     # Limpiar cache
        
        # Incluir datos necesarios
        "--add-data", "models;models",
        "--add-data", "generators;generators",
        "--add-data", "utils;utils",
        "--add-data", "templates;templates",
        
        # Hooks ocultos para PyQt6
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "PyQt6.QtWidgets",
        
        # Hooks para reportlab
        "--hidden-import", "reportlab",
        "--hidden-import", "reportlab.pdfgen.canvas",
        "--hidden-import", "reportlab.lib.pagesizes",
        "--hidden-import", "reportlab.lib.styles",
        "--hidden-import", "reportlab.platypus",
        
        # Hooks para pydantic
        "--hidden-import", "pydantic",
        "--hidden-import", "pydantic.dataclasses",
        
        # Excluir módulos innecesarios para reducir tamaño
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "--exclude-module", "tkinter",
        
        # Script principal
        main_script
    ]
    
    print(f"Ejecutando: {' '.join(pyinstaller_args)}")
    print()
    
    try:
        result = subprocess.run(pyinstaller_args, check=True, capture_output=False)
        print_success("Ejecutable construido correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error al construir ejecutable: {e}")
        return False

def create_portable_package():
    """Crea un paquete portable con el ejecutable y carpetas necesarias."""
    print_step("Creando paquete portable...")
    
    dist_path = Path("dist")
    exe_name = "GeneradorCartasCobro.exe"
    exe_path = dist_path / exe_name
    
    if not exe_path.exists():
        print_error(f"No se encontró el ejecutable en {exe_path}")
        return False
    
    # Crear carpeta portable
    portable_folder = Path("GeneradorCartasCobro_Portable")
    if portable_folder.exists():
        shutil.rmtree(portable_folder)
    portable_folder.mkdir()
    
    # Copiar ejecutable
    shutil.copy(exe_path, portable_folder / exe_name)
    print_success(f"Ejecutable copiado a {portable_folder}")
    
    # Crear carpetas necesarias
    folders_to_create = ["output", "logs"]
    for folder in folders_to_create:
        (portable_folder / folder).mkdir(exist_ok=True)
        print_success(f"Carpeta '{folder}' creada")
    
    # Copiar archivos de configuración si existen
    config_files = ["config.json", "README.md"]
    for config_file in config_files:
        if Path(config_file).exists():
            shutil.copy(config_file, portable_folder / config_file)
            print_success(f"Archivo '{config_file}' copiado")
    
    # Crear archivo README para el usuario
    readme_content = """
╔══════════════════════════════════════════════════════════════╗
║         GENERADOR DE CARTAS DE COBRO - SEGUROS UNIÓN         ║
╚══════════════════════════════════════════════════════════════╝

INSTRUCCIONES DE USO:
--------------------

1. Ejecutar "GeneradorCartasCobro.exe"
2. Llenar el formulario con los datos de la carta
3. Hacer clic en "Generar PDF"
4. Los PDFs se guardarán en la carpeta "output"

CARACTERÍSTICAS:
---------------
✓ Gestión de aseguradoras (agregar, editar, eliminar)
✓ Validación automática de NIT
✓ Cálculo automático de totales
✓ Generación de PDFs profesionales
✓ Selección de carpeta de salida personalizada
✓ Datos de ejemplo para pruebas rápidas

SOPORTE TÉCNICO:
---------------
Para reportar errores o solicitar ayuda, contactar a:
DANIEL ANTONIO VELEZ PELAEZ

Versión: 1.0.0
Fecha: Enero 2026
"""
    
    with open(portable_folder / "LEEME.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print_success("Archivo LEEME.txt creado")
    
    print()
    print_success(f"Paquete portable creado en: {portable_folder.absolute()}")
    
    # Mostrar tamaño del ejecutable
    exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
    print_success(f"Tamaño del ejecutable: {exe_size:.2f} MB")
    
    return True

def main():
    """Función principal."""
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔══════════════════════════════════════════════════════════════╗
║         CONSTRUCTOR DE EJECUTABLE - PYINSTALLER              ║
║         Generador de Cartas de Cobro                         ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
    """)
    
    try:
        # 1. Verificar PyInstaller
        if not check_pyinstaller():
            print_error("Abortando: PyInstaller no disponible")
            return 1
        
        # 2. Limpiar builds anteriores
        clean_build_folders()
        
        # 3. Crear ejecutable
        if not create_executable():
            print_error("Abortando: Error al crear ejecutable")
            return 1
        
        # 4. Crear paquete portable
        if not create_portable_package():
            print_warning("El paquete portable no se pudo crear, pero el ejecutable está en dist/")
        
        # Mensaje final
        print()
        print(f"{Colors.GREEN}{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}✓ PROCESO COMPLETADO EXITOSAMENTE{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}{'='*60}{Colors.END}")
        print()
        print(f"{Colors.BOLD}El ejecutable está disponible en:{Colors.END}")
        print(f"  • dist/GeneradorCartasCobro.exe")
        print(f"  • GeneradorCartasCobro_Portable/GeneradorCartasCobro.exe")
        print()
        
        return 0
        
    except KeyboardInterrupt:
        print()
        print_warning("Proceso interrumpido por el usuario")
        return 130
    except Exception as e:
        print()
        print_error(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
