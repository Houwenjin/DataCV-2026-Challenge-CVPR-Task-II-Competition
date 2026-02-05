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
  --output prediction.txt
```

**Note**: You can also test with random predictions:
```bash
python evaluate_simple.py \
  --mcq-data val/val.json \
  --image-dirs val/images \
  --output prediction.txt \
  --random
```

### 4. Output Format

The output file `prediction.txt` should contain one prediction per line:
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

### 1. Prepare Your Files
You need to include **two files** in your submission:
1.  **Prediction File**: A text file containing your results (e.g., `result.txt` or `prediction.txt`), following the format described in the **Output Format** section.
2.  **Model Metadata**: A JSON file named **`model.json`** containing your model details.

### 2. Create the Zip Archive
Compress both files into a single zip archive (e.g., named **`result.zip`**). Please follow the instructions below to ensure a clean submission.

####  For Windows Users
1. Select **both** your prediction file and `model.json`.
2. Right-click and select **"Send to"** > **"Compressed (zipped) folder"** (or "Compress to ZIP file").
3. Rename the resulting file to `result.zip`.

####  For macOS Users
**Important Warning:** Do NOT use the default right-click "Compress" feature. It creates hidden files (e.g., `__MACOSX`, `.DS_Store`) that will cause the grading script to **fail**.

Please use the terminal to create a clean zip file:
1. Open Terminal and navigate to the folder containing your files.
2. Run the following command (replace `result.txt` with your actual prediction filename):
   ```bash
   zip result.zip result.txt model.json -x "*.DS_Store" -x "__MACOSX/*" -x ".*"
   
### 3.Code Verification
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
