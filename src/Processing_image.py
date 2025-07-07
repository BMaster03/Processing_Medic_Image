import os
import numpy as np
from PIL import Image
import SimpleITK as sitk
import nibabel as nib
import cv2

class ImagePreprocessor:
    def __init__(self, image_data_root, intensity, size, output_mode="16bit", resizer="pil", output_format=".tiff"):
        self.image_data_root = image_data_root
        self.intensity       = intensity.lower()
        self.size            = size
        self.output_mode     = output_mode.lower()
        self.resizer         = resizer.lower()
        self.output_format   = output_format.lower()

        dataset_name = os.path.basename(os.path.normpath(image_data_root))
        
        self.output_root = os.path.join(
            os.path.dirname(image_data_root),
            f"{dataset_name}_pre"
        )

        self.data_range = {
            "minmax01": 1,
            "minmax11": 2,
            "zscore": "zscore",
            "raw": 4095
            
        }.get(self.intensity)

        if self.data_range is None:
            raise ValueError(f"Tipo de intensidad inválido: {self.intensity}")

        if self.output_mode not in ["8bit", "16bit"]:
            raise ValueError("output_mode debe ser '8bit' o '16bit'")

        if self.resizer not in ["pil", "opencv"]:
            raise ValueError("resizer debe ser 'pil' u 'opencv'")

        self.nii_formats = [".nii", ".hdr", ".img"]
        self.dcm_formats = [".dcm", ".dicom"]
        self.tiff_formats = [".tif", ".tiff", ".btf"]

    def normalize_intensity(self, array):

        if self.intensity == "minmax01":
            return (array - np.min(array)) / (np.max(array) - np.min(array))
        
        elif self.intensity == "minmax11":
            return 2 * ((array - np.min(array)) / (np.max(array) - np.min(array))) - 1
        
        elif self.intensity == "zscore":
            std = np.std(array)
            if std == 0:
                return array * 0
            return (array - np.mean(array)) / std
        
        elif self.intensity == "raw":
            return array

    def scale_array(self, norm_array):

        if self.output_mode == "8bit":
            scaled = np.clip(norm_array, 0, 1) * 255
            return scaled.astype(np.uint8)
        
        elif self.output_mode == "16bit":
            if self.intensity != "raw":
                scaled = np.clip(norm_array, 0, 1) * 4095
            else:
                scaled = np.clip(norm_array, 0, 4095)

            return scaled.astype(np.uint16)

    def resize_array(self, array):

        if self.resizer == "pil":
            img = Image.fromarray(array)
            img = img.resize(self.size, Image.BILINEAR)
            return np.array(img)
        else:
            return cv2.resize(array, dsize=self.size, interpolation=cv2.INTER_LINEAR)

    def save_array(self, array, output_path):

        if self.output_format in self.nii_formats:
            nifti_img = nib.Nifti1Image(array, affine=np.eye(4))
            nib.save(nifti_img, output_path)

        elif self.output_format in self.dcm_formats:
            sitk_out = sitk.GetImageFromArray(array)
            sitk.WriteImage(sitk_out, output_path)
            
        elif self.output_format in self.tiff_formats:
            img = Image.fromarray(array)
            img.save(output_path, format="TIFF")

        else:
            raise ValueError(f"Formato no soportado: {self.output_format}")

    def process_image(self, input_path, output_path_no_ext):
        try:
            print(f"\nProcesando imagen: {input_path}")
            sitk_img = sitk.ReadImage(input_path)
            array    = sitk.GetArrayFromImage(sitk_img)

            if array.ndim == 3:
                array = array[0]

            norm_array    = self.normalize_intensity(array)
            scaled_array  = self.scale_array(norm_array)
            resized_array = self.resize_array(scaled_array)

            output_path = output_path_no_ext + self.output_format

            self.save_array(resized_array, output_path)

            return True

        except Exception as e:
            print(f"Error procesando {input_path}: {e}")
            return False

    def run(self):
        processed_count = 0
        print("\n=========================================")
        print(f"Iniciando preprocesamiento en: {self.image_data_root}")
        print(f"Modo intensidad: {self.intensity}")
        print(f"Rango dinámico: {self.data_range}")
        print(f"Bits: {self.output_mode}")
        print(f"Resizer: {self.resizer}")
        print(f"Formato salida: {self.output_format}")
        print("=========================================\n")

        if not os.path.exists(self.image_data_root):
            print(f"Ruta no existe: {self.image_data_root}")
            return

        for root, _, files in os.walk(self.image_data_root):

            relative_path = os.path.relpath(root, self.image_data_root)
            output_dir    = os.path.join(self.output_root, relative_path)
            os.makedirs(output_dir, exist_ok=True)

            print(f"\nExplorando carpeta: {root}")

            if not files:
                print("  (Vacío)")
                continue

            valid_files = [f for f in files if f.lower().endswith(
                ('.tif', '.tiff', '.dicom', '.dcm', '.nii', '.hdr', '.img', '.btf')
            )]

            if not valid_files:
                print("  No hay archivos válidos.")
                continue

            for filename in sorted(valid_files):
                input_path = os.path.join(root, filename)
                output_path_no_ext = os.path.join(output_dir, os.path.splitext(filename)[0])

                if self.process_image(input_path, output_path_no_ext):
                    processed_count += 1
                else:
                    print(f"Falló procesando: {input_path}")

        print("\n=========================================")
        print(f"Total imágenes procesadas: {processed_count}")
        print(f"Guardadas en: {self.output_root}")
        print("=========================================")
