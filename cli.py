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

logger = get_logger(__name__)


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
        '--version', '-v',
        action='version',
        version=f'{config.APP_NAME} v{config.APP_VERSION}'
    )
    
    args = parser.parse_args()
    
    # Si no se especifica ningún argumento, mostrar ayuda
    if not any([args.interactive, args.from_json, args.stats]):
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


if __name__ == '__main__':
    main()
