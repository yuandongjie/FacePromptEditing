# src/main.py
import argparse
from model import load_model
from generate import edit_face

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42, help="固定随机种子保证可复现")
    args = parser.parse_args()

    # 定义 4 类属性及对应编辑 prompt
    attribute_prompts = {
        "age": "young -> old",
        "expression": "neutral -> smiling",
        "occlusion": "wearing a mask",
        "style": "anime"
    }

    model = load_model()
    base_image_path = "results/base_face.png"
    edit_face(model, base_image_path, attribute_prompts, seed=args.seed)
