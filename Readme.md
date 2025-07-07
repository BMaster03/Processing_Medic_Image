# 🧠 Medical Image Preprocessing Tool

This project implements a **flexible and modular image preprocessing pipeline** for medical images.  
It allows you to:


```Bash
+ Normalize intensities  
+ Resize images  
+ Convert bit depth  
+ Export to multiple formats (TIFF, NIfTI, DICOM, etc.)
```

Developed on **Linux (Ubuntu 22.04)** and tested with **Python 3.12.4**.

---

## 📁 Dataset Structure

The tool preserves the **original folder hierarchy** of your dataset and generates a parallel output directory with a `_pre` suffix.

Example:

```Bash
/data/MyDataset
└── Patient01
        └──train/
            └── image00.tiff
        └──test/
            └── image71.tiff
        └──valid/
            └── image99.tiff

```

After processing:

```Bash
/data/MyDataset_pre
└── Patient01
        └──train/
            └── image00.tiff
        └──test/
            └── image71.tiff
        └──val/
            └── image99.tiff

└── image1.tiff
```

---

## 🛠️ Requirements

### Python Version

Developed and tested on:

Python 3.12.4


---

## 🐍 Python & Modules

### Install the modules manually

pip install numpy pillow SimpleITK nibabel opencv-python


Or create the environment from the provided `environment.yml` file.

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```Bash
$ git clone https://github.com/BMaster03/Processing_Medic_Image.git
$ cd Processing_Medic_Image/

```
---

### 2️⃣ Create a Conda Environment (Recommended)

```Bash
$ conda env create -f environment.yml
$ conda activate MRI-Synthesis
```

---

## ⚙️ Features

- **Intensity Normalization**:
  - Min-Max [0,1]
  - Min-Max [-1,1]
  - Z-Score
  - Raw values

- **Resizing**:
  - PIL or OpenCV interpolation

- **Bit Depth Conversion**:
  - 8-bit
  - 16-bit

- **Export Formats**:
  - `.tiff`
  - `.nii`
  - `.dcm`
  - and more

---

## 🧮 Processing Pipeline

The tool applies the following steps sequentially:

1. Intensity Normalization
2. Bit Depth Conversion
3. Resizing
4. Export in the selected format

All steps log progress and details to the console.

---

## 🧭 Command-Line Arguments

| Argument           | Description                                                           |
|--------------------|-----------------------------------------------------------------------|
| `--data_path`      | Base directory containing input images                               |
| `--intensity`      | Normalization method (`minmax01`, `minmax11`, `zscore`, `raw`)       |
| `--size`           | Output size in pixels (`width height`)                               |
| `--output_mode`    | Bit depth (`8bit`, `16bit`)                                          |
| `--resizer`        | Resizing library (`pil`, `opencv`)                                   |
| `--output_format`  | Output format (`.tiff`, `.nii`, `.dcm`, etc.)                        |

---


## License

Distributed under the **MIT License**.


## Contact

For questions or suggestions:

- **Author:** Bryan R. García Guerrero
- **Email:** bryan.rgg03@gmail.com