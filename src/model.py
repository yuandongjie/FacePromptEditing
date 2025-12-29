from diffusers import StableDiffusionPipeline
import torch


def load_model():
    model_path = r"D:\SoftwareWorkSpace\PyCharm\FacePromptEditing\models\v1-5-pruned-emaonly-fp16.safetensors"

    # 从单个 safetensors 文件加载
    pipe = StableDiffusionPipeline.from_single_file(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        safety_checker=None
    )

    if torch.cuda.is_available():
        pipe.to("cuda")
    return pipe
