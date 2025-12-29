# FacePromptEditing

## 1. 项目简介

本项目复现了 **Prompt-to-Prompt (P2P) 人脸属性编辑算法**，实现对单张人脸图像的多种属性修改，包括：

- 年龄（Age）：例如“年轻 -> 年老”  
- 表情（Expression）：例如“中性 -> 微笑”  
- 遮挡（Occlusion）：例如“佩戴口罩”  
- 风格（Style）：例如“动漫风格”  

核心思想是**在保持身份特征的前提下，通过编辑 Prompt 对图像进行微调**，并生成对比图和实验指标文件。

---

## 2. 项目文件夹结构

```text
FacePromptEditing/
├─ src/
│  ├─ main.py                # 主程序入口
│  ├─ generate.py            # 属性编辑核心函数
│  ├─ sample.py              # prompt_to_prompt_edit 函数
│  └─ model.py               # 模型加载函数
├─ models/
│  └─ v1-5-pruned-emaonly-fp16.safetensors  # Stable Diffusion v1.5 模型
├─ results/
│  └─ base_face.png          # 待编辑的基准人脸图
├─ requirements.txt          # Python 依赖列表
└─ README.md                 # 项目说明

```

---

## 3. 环境配置与运行
### 3.1 系统与依赖
- **操作系统**：Windows 11 x64处理器
- **CPU**：Ultra9
- **内存**：32G
- **硬盘存储**：1T
- **Python**: 3.10.10

### 3.2 安装依赖
推荐使用 `requirements.txt` 安装，pip install -r requirements.txt，内容如下：
```
torch
diffusers
transformers
accelerate
safetensors
pillow
```

### 3.3 模型准备
下载 Stable Diffusion v1.5 safetensors 模型，并放置在：
models/v1-5-pruned-emaonly-fp16.safetensors (已下载好)


### 3.4 数据准备
将待编辑的基准人脸图像放在：
results/base_face.png


### 3.5 运行

python src/main.py --seed 42
--seed 参数可固定随机种子，保证结果可复现。


### 3.6 关于 CPU 与 GPU 的选择

本项目在 Windows 11 + Ultra9 CPU 环境下即可运行，无需 GPU，原因如下：

1. **图片数量少**  
   - 本项目仅对一张基准人脸进行多属性编辑（age, expression, occlusion, style 共 4 张编辑图）。  
   - 总体生成量小，CPU 即可在合理时间内完成（每张图可能几十秒）。

2. **模型精度与输出要求**  
   - 项目主要用于演示 Prompt-to-Prompt 编辑效果，并生成对比图与 JSON 指标。  
   - 对速度要求不高，也不涉及大批量训练或高分辨率图像生成，CPU 已足够满足需求。

3. **GPU 可选**  
   - 若环境中有 GPU，可加快生成速度，但并非必须。  
   - CPU 运行结果与 GPU 一致，仅速度较慢。

**总结**：对于本项目，CPU 完全能够完成实验任务，保证结果可复现，同时无需额外 GPU 配置。

---

## 4. 期望输出
运行完成后，results/ 目录下将生成：

原始图像：generated_original.png

编辑图像 (每个属性一张)：

generated_edited_age.png

generated_edited_expression.png

generated_edited_occlusion.png

generated_edited_style.png

对比图 (原图 + 编辑图并排)：

generated_compare_age.png

generated_compare_expression.png

generated_compare_occlusion.png

generated_compare_style.png

实验指标 JSON (metrics.json)：
```
{
  "results": [
    {
      "attribute": "age",
      "base_prompt": "...",
      "edit_prompt": "young -> old",
      "negative_prompt": "...",
      "original_image": "results/generated_original.png",
      "edited_image": "results/generated_edited_age.png",
      "compare_image": "results/generated_compare_age.png"
    },
    {
      "attribute": "expression",
      "edit_prompt": "neutral -> smiling",
      "edited_image": "results/generated_edited_expression.png",
      "compare_image": "results/generated_compare_expression.png"
    },
    {
      "attribute": "occlusion",
      "edit_prompt": "wearing a mask",
      "edited_image": "results/generated_edited_occlusion.png",
      "compare_image": "results/generated_compare_occlusion.png"
    },
    {
      "attribute": "style",
      "edit_prompt": "anime",
      "edited_image": "results/generated_edited_style.png",
      "compare_image": "results/generated_compare_style.png"
    }
  ]
}
```
JSON 记录 Base Prompt、Negative Prompt、每个属性的编辑信息和生成图片路径，可用于复现和分析。

---
# 5. 注意事项
身份保持：Prompt-only 编辑无法完全保证身份不变，可能存在漂移。

生成速度：在 CPU 环境下生成速度较慢（每张图片可能3~6分钟）。

效果依赖：编辑效果依赖于 Base Prompt 和属性 Prompt 的描述精确度。
