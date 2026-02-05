# DataCV 2026 Challenge @ CVPR – Task II: Real-World Visual Illusions and Anomalies

This repository contains the evaluation framework and starter code for **Task II: Real-world visual illusions and anomalies understanding** of the DataCV 2026 Challenge @ CVPR 2026, as described on the official challenge page ([DataCV Challenge](https://sites.google.com/view/datacv-2026-cvpr/challenge?authuser=0)).

## Overview

Task II focuses on evaluating **vision-language models (VLMs)** under real-world visual illusions and perceptual anomalies, using **multiple-choice (A/B/C/D)** questions:
- Input: an image + a prompt that includes a question and options {A, B, C, or D}
- Goal: select the single correct option under diverse illusion/anomaly scenarios
- Constraint: **inference-only** – no model training or fine-tuning is allowed; participants may design any strategy

We organize the benchmark into 6 conceptual categories:
- **VA** (Visual Amomaly)
- **CI** (Color Illusion)
- **MI** (Motion Illusion)
- **GI** (Gestalt Illusion)
- **GSI** (Geometric and Spatial Illusion)
- **VI** (Visual Illusion)

## Dataset Structure

For **Task II - Validation**, the released archive has the following structure:

```text
├── val/                      # Validation data
│   ├── images/               # Validation images
│   │   ├── 0.jpg
│   │   ├── 1.webp
│   │   └── ...
│   └── val.json              # Validation questions and options (no ground-truth answers)
```

Images are named as `{index}.{extension}` (e.g., `0.jpg`, `1.webp`).

**Note**: The `val/` dataset is provided for participants to validate their methods before the official competition. During the test phase (official competition), a separate **test** archive will be released for final evaluation.

### Data Format

Each entry in `val.json` has the following structure:
```json
{
  "image_name": "0.jpg",
  "Question": "Question:\nHow many fingers are in the image?",
  "option": "Option: \nA. 5\nB. 6\nC. 4\nD. Not Sure\n"
}
```

## Getting Started

### 1. Setup Environment

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Model

Edit `evaluate_simple.py` and modify the following sections:

**Model Instantiation** (around line 140):
```python
# Model instantiation - modify this section to instantiate your model
model = ...  # Replace with your model initialization
```

**Model Inference** (around line 165):
```python
# Call model for inference - modify this section to call your model
# raw_response = model.chat(image_path=image_path, prompt=prompt)
raw_response = ""  # Replace with actual model call
```

### 3. Generate Predictions

Run the evaluation script:

```bash
python evaluate_simple.py \
  --mcq-data val/val.json \
  --image-dirs val/images \
  --output result.txt
```

**Note**: You can also test with random predictions:
```bash
python evaluate_simple.py \
  --mcq-data val/val.json \
  --image-dirs val/images \
  --output result.txt \
  --random
```

### 4. Output Format

The output file `result.txt` should contain one prediction per line:
```
0 1
1 2
2 0
3 3
...
```

Format: `{image_index} {answer}` where:
- `image_index`: Extracted from image filename (0, 1, 2, ...)
- `answer`: Integer in {0, 1, 2, 3}, converted from choice letters:
  - A → 0
  - B → 1
  - C → 2
  - D → 3

## Evaluation Metrics

The evaluation computes 7 metrics:

1. **VA_ACC**: Accuracy on Visual Anomaly subset
2. **CI_ACC**: Accuracy on Color Illusion subset
3. **MI_ACC**: Accuracy on Motion Illusion subset
4. **GI_ACC**: Accuracy on Gestalt Illusion subset
5. **GSI_ACC**: Accuracy on Geometric and Spatial Illusion subset
6. **VI_ACC**: Accuracy on Visual Illusion subset
7. **Overall_ACC**: Overall accuracy across all valid samples

## Submission

Please follow these steps to prepare your submission:

- **Step 1: Generate `result.txt`**
  - Write your predictions into a plain text file named `result.txt`, with **one `image_index` and one `answer` per line**.
  - Example:
    ```text
    0 1
    1 2
    ...
    100 0
    ```
  - Each `answer` must be an integer in `{0, 1, 2, 3}`, converted from the choice letter:
    - A → 0
    - B → 1
    - C → 2
    - D → 3

- **Step 2: Create `model.json`**
  - Write your model name and main inference-time parameters into `model.json`.
  - Example:
    ```json
    {
      "model": "gpt-4o",
      "parameters": {
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 2048,
        "frequency_penalty": 0.5
      }
    }
    ```

- **Step 3: Zip the files into `result.zip`**
  - Put `result.txt` and `model.json` in the **same directory**, then run:
    ```bash
    zip -r result.zip . -x "*DS_Store" -x "__MACOSX/*" -x ".*"
    ```
    This command creates a clean zip file and excludes macOS hidden files (e.g., `.DS_Store`, `__MACOSX`), which may otherwise break the grading script.

- **Step 4: Submit `result.zip`** to the competition website.

**Note: we will provide an example `result.zip` in the repository for reference.**

All winning teams are required to provide **complete, runnable code** for their solution after the competition ends, including:
- Model definition and loading
- Inference / decoding logic
- Any preprocessing and postprocessing code  
The organizing committee may request code and environment details for result verification and reproducibility.

## Files

- `evaluate_simple.py`: Main evaluation script for participants

## License

[MIT License]

## Citation
If you use this dataset, please cite:
```bibtex
@misc{hou2026seeingbelievingbenchmarkmultimodal,
      title={Seeing Is Believing? A Benchmark for Multimodal Large Language Models on Visual Illusions and Anomalies}, 
      author={Wenjin Hou and Wei Liu and Han Hu and Xiaoxiao Sun and Serena Yeung-Levy and Hehe Fan},
      year={2026},
      eprint={2602.01816},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2602.01816}
}
```
