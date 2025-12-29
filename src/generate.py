# src/generate.py
import json
from PIL import Image
from sample import prompt_to_prompt_edit

# ===== 1. 固定 base prompt（身份锚点）=====
BASE_PROMPT = (
    "a realistic portrait of a young Chinese female face, "
    "front view, "
    "symmetrical face, "
    "natural skin texture, "
    "photorealistic, "
    "high quality"
)

# ===== 2. 固定 negative prompt（抑制身份漂移）=====
NEGATIVE_PROMPT = (
    "male, man, boy, child, "
    "elderly man, "
    "different person, different face, "
    "cartoon, anime, "
    "low quality, distorted face"
)


def edit_face(model, base_image_path, attribute_prompts, seed=42):
    """
    对 base_face.png 执行 4 类属性编辑（Prompt-only）
    """

    # 仅用于展示对比，不作为生成约束
    original_img = Image.open(base_image_path).convert("RGB")

    # 保存原始图
    original_path = "results/generated_original.png"
    original_img.save(original_path)

    results = []

    for attribute, edit_prompt in attribute_prompts.items():

        # === 核心：base prompt + edit prompt ===
        edited_img = prompt_to_prompt_edit(
            pipe=model,
            base_prompt=BASE_PROMPT,
            edit_prompt=edit_prompt,
            negative_prompt=NEGATIVE_PROMPT,
            seed=seed
        )

        # 保存编辑图
        edited_path = f"results/generated_edited_{attribute}.png"
        edited_img.save(edited_path)

        # 保存并排对比图
        compare_img = Image.new(
            'RGB',
            (original_img.width * 2, original_img.height)
        )
        compare_img.paste(original_img, (0, 0))
        compare_img.paste(edited_img, (original_img.width, 0))

        compare_path = f"results/generated_compare_{attribute}.png"
        compare_img.save(compare_path)

        # 记录结果
        results.append({
            "attribute": attribute,
            "base_prompt": BASE_PROMPT,
            "edit_prompt": edit_prompt,
            "negative_prompt": NEGATIVE_PROMPT,
            "original_image": original_path,
            "edited_image": edited_path,
            "compare_image": compare_path
        })

    # ===== 3. metrics.json（真实、可复现）=====
    metrics = {
        "model": "Stable Diffusion v1.5",
        "editing_method": "Prompt-to-Prompt (prompt-only)",
        "seed": seed,
        "input_type": "cropped face image (for visualization only)",
        "base_prompt": BASE_PROMPT,
        "negative_prompt": NEGATIVE_PROMPT,
        "results": results,
        "limitations": [
            "No explicit identity constraint",
            "Prompt-only editing",
            "Identity preservation is not guaranteed"
        ]
    }

    with open("results/metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4, ensure_ascii=False)

    print("所有编辑完成，结果已保存到 results/ 目录")
