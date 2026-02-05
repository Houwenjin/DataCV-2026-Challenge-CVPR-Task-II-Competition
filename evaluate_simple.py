#!/usr/bin/env python3
"""
Simplified MCQ evaluation script
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
import random


def load_mcq_data(json_path: str) -> List[Dict]:
    """Load MCQ data from JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading MCQ data: {e}")
        sys.exit(1)


def find_image_path(image_name: str, image_dirs: List[str]) -> Optional[str]:
    """Find the full path to an image given its name and search directories."""
    for img_dir in image_dirs:
        img_path = Path(img_dir) / image_name
        if img_path.exists():
            return str(img_path)
    return None


def parse_response(response: str) -> str:
    """
    Parse response using lenient pattern matching.
    Returns an option (A/B/C/D), defaults to D if no match found.
    """
    if not response or not isinstance(response, str):
        return "D"

    response = response.strip()

    # LENIENT: Multiple pattern matching
    lenient_option = None
    patterns = [
        r'answer\s*[:\-]\s*\[([ABCD])\]',             # Answer: [A] (anywhere in text)
        r'\[([ABCD])\]',                               # [A] (anywhere in text)
        r'answer\s*[:\-]\s*([ABCD])\b',                # Answer: A (with word boundary)
        r'\b([ABCD])\b',                               # A (single letter with word boundaries)
        r'answer\s*[:\-]\s*\[([ABCD])\]\b',            # Answer: [A] (with word boundary)
        r'answer\s*is\s*\[([ABCD])\]',                 # Answer is [A]
        r'answer\s*is\s*([ABCD])',                     # Answer is A
        r'the\s*answer\s*is\s*\[([ABCD])\]',           # The answer is [A]
        r'the\s*answer\s*is\s*([ABCD])',               # The answer is A
        r'choice\s*[:\-]\s*\[([ABCD])\]',              # Choice: [A]
        r'option\s*[:\-]\s*\[([ABCD])\]'               # Option: [A]
    ]

    for pattern in patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            lenient_option = match.group(1).upper()
            break

    # Handle uncertainty patterns
    if lenient_option is None:
        if re.search(r'not\s+sure|unsure|uncertain|don\'?t\s+know', response, re.IGNORECASE):
            lenient_option = "D"
        else:
            lenient_option = "D"  # Default fallback

    return lenient_option


def option_to_number(option: str) -> int:
    """
    Convert option letter (A/B/C/D) to number (0/1/2/3).
    """
    mapping = {"A": 0, "B": 1, "C": 2, "D": 3}
    return mapping.get(option.upper(), 3)  # Default to 3 (D) if invalid


def extract_index_from_image_name(image_name: str) -> Optional[int]:
    """
    Extract index from image name (e.g., "0.jpg" -> 0, "123.png" -> 123).
    Assumes format: number.extension
    """
    # Extract the number before the first dot
    match = re.match(r'^(\d+)\.', image_name)
    if match:
        return int(match.group(1))
    return None


def save_results_txt(results: List[Dict], output_path: str) -> None:
    """
    Save results to TXT file with two columns: index and answer (both as numbers).
    Format (no header): index answer (space-separated, one per line)
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            # Write data rows (no header)
            for result in results:
                index = result.get("index", -1)
                answer_num = result.get("answer_num", 3)  # Default to 3 (D)
                f.write(f"{index} {answer_num}\n")
    except Exception as e:
        print(f"Error saving results to {output_path}: {e}")
        raise




def evaluate_mcq(
    mcq_data: List[Dict],
    image_dirs: List[str],
    output_path: str,
    use_random: bool = False,
) -> List[Dict]:
    """
    Evaluate MCQ questions using model inference and generate competition results.

    Args:
        mcq_data: List of MCQ question dictionaries
        image_dirs: List of directories to search for images
        output_path: Path to save results TXT file

    Returns:
        List of result dictionaries
    """
    # Model instantiation - modify this section to instantiate your model
    # If use_random is True, model is not used.
    model = None if use_random else ...

    results = []

    for i, question in enumerate(mcq_data):
        image_name = question.get("image_name", "")
        if not image_name:
            continue

        # Extract index from image name (e.g., "0.jpg" -> 0)
        index = extract_index_from_image_name(image_name)
        if index is None:
            continue

        # Find image
        image_path = find_image_path(image_name, image_dirs)
        if not image_path:
            continue

        # Get prompt: combine Question and option
        question_text = question.get("Question", "")
        option_text = question.get("option", "")
        # You can modify the prompt as you want
        prompt = f"{question_text}\n{option_text}".strip()  

        try:
            if use_random:
                # Random baseline: uniformly sample from A/B/C/D
                lenient_option = random.choice(["A", "B", "C", "D"])
            else:
                # Call model for inference - modify this section to call your model
                # raw_response = model.chat(image_path=image_path, prompt=prompt)
                raw_response = ""  # Placeholder, replace with actual model call

                if not raw_response or raw_response.startswith("ERROR"):
                    raw_response = "ERROR: Model inference failed"

                # Parse response with matching logic
                lenient_option = parse_response(raw_response)

            # Convert option to number (A->0, B->1, C->2, D->3)
            answer_num = option_to_number(lenient_option)

            result = {
                "index": index,
                "lenient_option": lenient_option,
                "answer_num": answer_num
            }

            results.append(result)

        except Exception:
            # On error, default to D (3)
            result = {
                "index": index,
                "lenient_option": "D",
                "answer_num": 3
            }
            results.append(result)

    # Sort results by index to ensure correct order
    results.sort(key=lambda x: x.get("index", -1))

    # Save results to TXT file
    save_results_txt(results, output_path)

    return results


def main():
    parser = argparse.ArgumentParser(description="Evaluate MCQ for competition - generates TXT file with index and answer columns")
    parser.add_argument("--mcq-data", required=True, help="Path to MCQ JSON file")
    parser.add_argument("--image-dirs", nargs="+", required=True, help="Directories to search for images")
    parser.add_argument("--output", required=True, help="Path to save results TXT file (format: index answer)")
    parser.add_argument("--random", action="store_true", help="Use random predictions instead of a model")

    args = parser.parse_args()

    # Load MCQ data
    mcq_data = load_mcq_data(args.mcq_data)

    # Evaluate and generate results
    evaluate_mcq(
        mcq_data=mcq_data,
        image_dirs=args.image_dirs,
        output_path=args.output,
        use_random=args.random,
    )

    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
