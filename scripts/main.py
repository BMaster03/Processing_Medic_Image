from src.Processing_image import ImagePreprocessor
from src.options import get_preprocessing_args

def main():
    
    args = get_preprocessing_args()

    processor = ImagePreprocessor(
        image_data_root=args.data_path,
        intensity=args.intensity,
        size=tuple(args.size),
        output_mode=args.output_mode,
        resizer=args.resizer,
        output_format=args.output_format
    )

    processor.run()

if __name__ == "__main__":
    main()
