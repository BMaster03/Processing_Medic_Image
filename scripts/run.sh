#!/bin/bash

python3 main.py --data_path "/ruta/a/tu/dataset" \
                --intensity "minmax11" \
                --size 512 512 \
                --output_mode "16bit" \
                --resizer "pil" \
                --output_format ".tiff"


       