"""
Interfaz de línea de comandos (CLI) para el generador de cartas de cobro.

Uso:
    python cli.py --help
    python cli.py --interactive
    python cli.py --from-json datos.json
"""
import sys
import argparse
import json
from pathlib import Path
from datetime import date
from decimal import Decimal

from models.documento import Documento, MontosCobro
from models.asegurado import Asegurado
from models.poliza import Poliza
from generators.carta_cobro_generator import CartaCobroGenerator
from utils.config import config
from utils.logger import get_logger
from utils.versioning import version_manager
from utils.payee_manager import payee_manager

logger = get_logger(__name__)


def manage_payees_menu():
    """Menú para gestionar aseguradoras beneficiarias."""
    while True:
        print("\n" + "=" * 60)
        print("GESTIÓN DE ASEGURADORAS BENEFICIARIAS")
        print("=" * 60)
        
        payees = payee_manager.get_all_payees()
        
        if payees:
            print("\nAseguradoras guardadas:")
            for idx, payee in enumerate(payees, 1):
                print(f"{idx}. {payee['name']}")
                print(f"   NIT: {payee['nit']} | Usada: {payee['usage_count']} veces")
        else:
            print("\n⚠ No hay aseguradoras guardadas")
        
        print("\nOpciones:")
        print("1. Agregar nueva aseguradora")
        print("2. Editar aseguradora existente")
        print("3. Eliminar aseguradora")
        print("4. Ver detalles")
        print("0. Salir")
        
        opcion = input("\nSeleccione opción: ").strip()
        
        if opcion == '1':
            # Agregar nueva
            print("\n➕ AGREGAR NUEVA ASEGURADORA")
            name = input("Nombre: ").strip().upper()
            nit = input("NIT: ").strip()
            if name and nit:
                payee_manager.add_payee(name, nit)
                print(f"✓ Aseguradora '{name}' agregada exitosamente")
            else:
                print("⚠ Nombre y NIT son obligatorios")
        
        elif opcion == '2':
            # Editar
            if not payees:
                print("⚠ No hay aseguradoras para editar")
                continue
            
            print("\n✏️ EDITAR ASEGURADORA")
            try:
                idx = int(input(f"Número de aseguradora [1-{len(payees)}]: ")) - 1
                if 0 <= idx < len(payees):
                    old_payee = payees[idx]
                    print(f"\nEditando: {old_payee['name']}")
                    print(f"NIT actual: {old_payee['nit']}")
                    
                    new_name = input(f"Nuevo nombre [Enter para mantener]: ").strip().upper()
                    new_nit = input(f"Nuevo NIT [Enter para mantener]: ").strip()
                    
                    new_name = new_name or old_payee['name']
                    new_nit = new_nit or old_payee['nit']
                    
                    result = payee_manager.update_payee(old_payee['name'], new_name, new_nit)
                    if result:
                        print(f"✓ Aseguradora actualizada exitosamente")
                    else:
                        print("⚠ Error al actualizar")
                else:
                    print("⚠ Número inválido")
            except ValueError:
                print("⚠ Entrada inválida")
        
        elif opcion == '3':
            # Eliminar
            if not payees:
                print("⚠ No hay aseguradoras para eliminar")
                continue
            
            print("\n🗑️ ELIMINAR ASEGURADORA")
            try:
                idx = int(input(f"Número de aseguradora [1-{len(payees)}]: ")) - 1
                if 0 <= idx < len(payees):
                    payee = payees[idx]
                    confirm = input(f"¿Eliminar '{payee['name']}'? (s/n): ").strip().lower()
                    if confirm == 's':
                        if payee_manager.delete_payee(payee['name']):
                            print(f"✓ Aseguradora eliminada exitosamente")
                        else:
                            print("⚠ Error al eliminar")
                    else:
                        print("Cancelado")
                else:
                    print("⚠ Número inválido")
            except ValueError:
                print("⚠ Entrada inválida")
        
        elif opcion == '4':
            # Ver detalles
            if not payees:
                print("⚠ No hay aseguradoras guardadas")
                continue
            
            print("\n📋 DETALLES DE ASEGURADORAS")
            for idx, payee in enumerate(payees, 1):
                print(f"\n{idx}. {payee['name']}")
                print(f"   NIT: {payee['nit']}")
                print(f"   Veces usada: {payee['usage_count']}")
        
        elif opcion == '0':
            print("\n👋 ¡Hasta pronto!")
            break
        
        else:
            print("⚠ Opción no válida")


def interactive_mode():
    """Modo interactivo para captura de datos."""
    print("\n" + "=" * 60)
    print("GENERADOR DE CARTAS DE COBRO - Modo Interactivo")
    print("=" * 60 + "\n")
    
    try:
        # Datos de emisión
        print("📋 DATOS DE EMISIÓN")
        ciudad = input("Ciudad de emisión [Medellín]: ").strip() or "Medellín"
        fecha_str = input("Fecha de emisión (YYYY-MM-DD) [Enter para hoy]: ").strip()
        if not fecha_str or fecha_str.lower() in ['hoy', 'today']:
            fecha_emision = date.today()
        else:
            fecha_emision = date.fromisoformat(fecha_str)
        
        # Generar número de carta automáticamente
        numero_carta = version_manager.get_next_numero_carta()
        print(f"Número de carta (auto): {numero_carta}")
        
        mes_cobro = input("Mes de cobro (ej: Octubre): ").strip()
        
        fecha_limite_str = input("Fecha límite de pago (YYYY-MM-DD): ").strip()
        fecha_limite = date.fromisoformat(fecha_limite_str)
        
        # Datos del cliente
        print("\n👤 DATOS DEL CLIENTE")
        razon_social = input("Razón social: ").strip()
        nit = input("NIT (formato: 123456789-0): ").strip()
        direccion = input("Dirección: ").strip()
        telefono = input("Teléfono: ").strip()
        ciudad_cliente = input("Ciudad: ").strip()
        
        # Datos de la póliza
        print("\n📄 DATOS DE LA PÓLIZA")
        poliza_numero = input("Número de póliza (7 dígitos): ").strip()
        poliza_tipo = input("Tipo de póliza [POLIZA DE VIDA GRUPO]: ").strip() or "POLIZA DE VIDA GRUPO"
        plan_poliza = input("Plan póliza (ej: 06  3144016): ").strip()
        doc_referencia = input("Documento de referencia (8 dígitos): ").strip()
        cuota_numero = int(input("Número de cuota: ").strip())
        
        vigencia_inicio_str = input("Inicio vigencia (YYYY-MM-DD): ").strip()
        vigencia_inicio = date.fromisoformat(vigencia_inicio_str)
        
        vigencia_fin_str = input("Fin vigencia (YYYY-MM-DD): ").strip()
        vigencia_fin = date.fromisoformat(vigencia_fin_str)
        
        # Aseguradora beneficiaria
        print("\n🏢 ASEGURADORA BENEFICIARIA (quien recibe el pago)")
        payees = payee_manager.get_all_payees()
        
        if payees:
            print("\nAseguradoras guardadas:")
            for idx, payee in enumerate(payees, 1):
                print(f"{idx}. {payee['name']} (NIT: {payee['nit']}) - Usada {payee['usage_count']} veces")
            print(f"{len(payees) + 1}. Ingresar nueva aseguradora")
            print(f"{len(payees) + 2}. Editar aseguradora existente")
            print(f"{len(payees) + 3}. Eliminar aseguradora")
            
            opcion = input(f"\nSeleccione opción [1-{len(payees) + 3}]: ").strip()
            
            try:
                opcion_num = int(opcion)
                if 1 <= opcion_num <= len(payees):
                    # Seleccionar existente
                    selected_payee = payees[opcion_num - 1]
                    payee_name = selected_payee['name']
                    payee_nit = selected_payee['nit']
                    payee_manager.increment_usage(payee_name)
                    print(f"✓ Seleccionado: {payee_name}")
                elif opcion_num == len(payees) + 1:
                    # Ingresar nueva
                    payee_name = input("Nombre de la aseguradora: ").strip().upper()
                    payee_nit = input("NIT de la aseguradora: ").strip()
                    payee_manager.add_payee(payee_name, payee_nit)
                    print(f"✓ Aseguradora guardada")
                elif opcion_num == len(payees) + 2:
                    # Editar existente
                    edit_idx = int(input(f"Número de aseguradora a editar [1-{len(payees)}]: ")) - 1
                    if 0 <= edit_idx < len(payees):
                        old_payee = payees[edit_idx]
                        print(f"\nEditando: {old_payee['name']}")
                        new_name = input(f"Nuevo nombre [{old_payee['name']}]: ").strip().upper() or old_payee['name']
                        new_nit = input(f"Nuevo NIT [{old_payee['nit']}]: ").strip() or old_payee['nit']
                        payee_manager.update_payee(old_payee['name'], new_name, new_nit)
                        payee_name = new_name
                        payee_nit = new_nit
                        print(f"✓ Aseguradora actualizada")
                    else:
                        print("⚠ Opción inválida, usando primera aseguradora")
                        payee_name = payees[0]['name']
                        payee_nit = payees[0]['nit']
                elif opcion_num == len(payees) + 3:
                    # Eliminar
                    delete_idx = int(input(f"Número de aseguradora a eliminar [1-{len(payees)}]: ")) - 1
                    if 0 <= delete_idx < len(payees):
                        payee_to_delete = payees[delete_idx]
                        confirm = input(f"¿Eliminar '{payee_to_delete['name']}'? (s/n): ").strip().lower()
                        if confirm == 's':
                            payee_manager.delete_payee(payee_to_delete['name'])
                            print(f"✓ Aseguradora eliminada")
                        # Usar primera disponible
                        remaining = payee_manager.get_all_payees()
                        if remaining:
                            payee_name = remaining[0]['name']
                            payee_nit = remaining[0]['nit']
                        else:
                            payee_name = input("Nombre de la aseguradora: ").strip().upper()
                            payee_nit = input("NIT de la aseguradora: ").strip()
                            payee_manager.add_payee(payee_name, payee_nit)
                    else:
                        print("⚠ Opción inválida, usando primera aseguradora")
                        payee_name = payees[0]['name']
                        payee_nit = payees[0]['nit']
                else:
                    payee_name = input("Nombre de la aseguradora: ").strip().upper()
                    payee_nit = input("NIT de la aseguradora: ").strip()
                    payee_manager.add_payee(payee_name, payee_nit)
            except (ValueError, IndexError):
                payee_name = input("Nombre de la aseguradora: ").strip().upper()
                payee_nit = input("NIT de la aseguradora: ").strip()
                payee_manager.add_payee(payee_name, payee_nit)
        else:
            payee_name = input("Nombre de la aseguradora: ").strip().upper()
            payee_nit = input("NIT de la aseguradora: ").strip()
            payee_manager.add_payee(payee_name, payee_nit)
        
        # Montos
        print("\n💰 MONTOS")
        prima = Decimal(input("Prima (COP): ").strip())
        otros_rubros = Decimal(input("Otros rubros [0]: ").strip() or "0")
        impuesto = Decimal(input("Impuesto [0]: ").strip() or "0")
        valor_externo = Decimal(input("Valores externos [0]: ").strip() or "0")
        
        # Firma
        print("\n✍️ FIRMA")
        firmante_nombre = input("Nombre del firmante: ").strip()
        firmante_cargo = input("Cargo: ").strip()
        firmante_iniciales = input("Iniciales [opcional]: ").strip() or None
        
        # Borrador?
        es_borrador = input("\n¿Generar como BORRADOR? (s/n) [n]: ").strip().lower() == 's'
        
        # Construir modelo
        asegurado = Asegurado(
            razon_social=razon_social,
            nit=nit,
            direccion=direccion,
            telefono=telefono,
            ciudad=ciudad_cliente
        )
        
        poliza = Poliza(
            numero=poliza_numero,
            tipo=poliza_tipo,
            plan_poliza=plan_poliza,
            documento_referencia=doc_referencia,
            cuota_numero=cuota_numero,
            vigencia_inicio=vigencia_inicio,
            vigencia_fin=vigencia_fin
        )
        
        montos = MontosCobro(
            prima=prima,
            otros_rubros=otros_rubros,
            impuesto=impuesto,
            valor_externo=valor_externo
        )
        
        documento = Documento(
            ciudad_emision=ciudad,
            fecha_emision=fecha_emision,
            numero_carta=numero_carta,
            mes_cobro=mes_cobro,
            fecha_limite_pago=fecha_limite,
            asegurado=asegurado,
            poliza=poliza,
            montos=montos,
            payee_company_name=payee_name,
            payee_company_nit=payee_nit,
            firmante_nombre=firmante_nombre,
            firmante_cargo=firmante_cargo,
            firmante_iniciales=firmante_iniciales,
            es_borrador=es_borrador
        )
        
        # Generar PDF
        print("\n⏳ Generando PDF...")
        generator = CartaCobroGenerator(output_dir=config.OUTPUT_DIR / 'cartas')
        output_filename = f"CARTA_{documento.numero_carta_normalized}_{asegurado.nit.replace('-', '')}"
        
        pdf_path = generator.generate(documento.to_pdf_data(), output_filename)
        
        print(f"\n✅ PDF generado exitosamente: {pdf_path}")
        logger.info(f"PDF generado: {pdf_path}")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        logger.error(f"Error en modo interactivo: {str(e)}", exc_info=True)
        sys.exit(1)


def from_json_file(json_path: Path):
    """Genera carta desde archivo JSON."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Construir modelo desde JSON
        asegurado = Asegurado(**data['asegurado'])
        poliza = Poliza(**data['poliza'])
        montos = MontosCobro(**data['montos'])
        
        documento = Documento(
            ciudad_emision=data.get('ciudad_emision', 'Medellín'),
            fecha_emision=date.fromisoformat(data['fecha_emision']) if isinstance(data['fecha_emision'], str) else data['fecha_emision'],
            numero_carta=data['numero_carta'],
            mes_cobro=data['mes_cobro'],
            fecha_limite_pago=date.fromisoformat(data['fecha_limite_pago']) if isinstance(data['fecha_limite_pago'], str) else data['fecha_limite_pago'],
            asegurado=asegurado,
            poliza=poliza,
            montos=montos,
            payee_company_name=data.get('payee_company_name', 'SEGUROS DE VIDA SURAMERICANA S.A.'),
            payee_company_nit=data.get('payee_company_nit', '890903790-5'),
            firmante_nombre=data['firmante_nombre'],
            firmante_cargo=data['firmante_cargo'],
            firmante_iniciales=data.get('firmante_iniciales'),
            es_borrador=data.get('es_borrador', False)
        )
        
        # Generar PDF
        generator = CartaCobroGenerator(output_dir=config.OUTPUT_DIR / 'cartas')
        output_filename = f"CARTA_{documento.numero_carta_normalized}_{asegurado.nit.replace('-', '')}"
        
        pdf_path = generator.generate(documento.to_pdf_data(), output_filename)
        
        print(f"✅ PDF generado exitosamente: {pdf_path}")
        logger.info(f"PDF generado desde JSON: {pdf_path}")
        
    except FileNotFoundError:
        print(f"❌ Error: Archivo no encontrado: {json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        logger.error(f"Error generando desde JSON: {str(e)}", exc_info=True)
        sys.exit(1)


def main():
    """Función principal del CLI."""
    parser = argparse.ArgumentParser(
        description='Generador de Cartas de Cobro - SEGUROS UNIÓN',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python cli.py --interactive
  python cli.py --from-json datos_carta.json
  python cli.py --stats
        """
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Modo interactivo para captura de datos'
    )
    
    parser.add_argument(
        '--from-json', '-j',
        type=Path,
        metavar='FILE',
        help='Generar carta desde archivo JSON'
    )
    
    parser.add_argument(
        '--stats', '-s',
        action='store_true',
        help='Mostrar estadísticas de documentos generados'
    )
    
    parser.add_argument(
        '--manage-payees', '-m',
        action='store_true',
        help='Gestionar aseguradoras beneficiarias'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'{config.APP_NAME} v{config.APP_VERSION}'
    )
    
    args = parser.parse_args()
    
    # Si no se especifica ningún argumento, mostrar ayuda
    if not any([args.interactive, args.from_json, args.stats, args.manage_payees]):
        parser.print_help()
        sys.exit(0)
    
    # Ejecutar según modo
    if args.interactive:
        interactive_mode()
    elif args.from_json:
        from_json_file(args.from_json)
    elif args.stats:
        stats = version_manager.get_statistics()
        print("\n📊 ESTADÍSTICAS DE DOCUMENTOS GENERADOS")
        print("=" * 50)
        for year, data in stats.items():
            print(f"Año {data['year']}: {data['total_documents']} documentos")
        print("=" * 50 + "\n")
    elif args.manage_payees:
        manage_payees_menu()


if __name__ == '__main__':
    main()
