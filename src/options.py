import argparse

def get_preprocessing_args():
    """
    Configura y devuelve los argumentos de línea de comandos para el preprocesamiento de imágenes médicas.
    """

    intensity_choices = ['minmax01', 'zscore', 'raw', 'minmax11']
    output_modes = ['8bit', '16bit']
    resizer_choices = ['pil', 'opencv']
    format_choices = ['.dcm', '.dicom', '.nii', '.hdr', '.img', '.tif', '.tiff', '.btf']

    parser = argparse.ArgumentParser(description="Preprocesamiento de imágenes médicas")

    parser.add_argument('--data_path',          type=str, required=True, help="Ruta base donde están las carpetas con imágenes.")
    parser.add_argument('--intensity',          type=str, required=True, choices=intensity_choices, help="Tipo de normalización [minmax01, zscore, raw, minmax11].")
    parser.add_argument('--size',               type=int,nargs=2,required=True,help="Tamaño final de las imágenes, formato: ancho alto (ej: 512 512).")
    parser.add_argument('--output_mode',        type=str,default="16bit",choices=output_modes,help="Profundidad de bits de salida.")
    parser.add_argument('--resizer',            type=str,default="pil",choices=resizer_choices,help="Librería de redimensionamiento: pil u opencv.")
    parser.add_argument('--output_format',      type=str, required=True,choices=format_choices,help="Formato de archivo de salida.")

    return parser.parse_args()
