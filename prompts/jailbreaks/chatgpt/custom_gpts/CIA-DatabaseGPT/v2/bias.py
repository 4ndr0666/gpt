#!/usr/bin/env python3
import os
import sys
import yaml
import re

def compute_bias_score(text):
    """
    Compute a simple bias score based on the ratio of
    adjectives/adverbs to total words.
    """
    words = text.split()
    matches = re.findall(r"\b\w+(ly|ous|ive|ful|ic)\b", text, flags=re.IGNORECASE)
    return round(len(matches) / max(len(words), 1), 3)

def main():
    if len(sys.argv) != 2:
        print("Usage: bias.py <directory_of_yaml_summaries>", file=sys.stderr)
        sys.exit(1)

    dir_path = sys.argv[1]
    for filename in os.listdir(dir_path):
        if not filename.endswith(".yaml"):
            continue
        path = os.path.join(dir_path, filename)
        try:
            doc = yaml.safe_load(open(path, encoding="utf-8"))
        except Exception as e:
            print(f"Error loading YAML {path}: {e}", file=sys.stderr)
            continue

        # Concatenate abstract and bullet facts for bias analysis
        text = doc.get("abstract", "")
        for bullet in doc.get("bullets", []):
            text += " " + bullet.get("fact", "")

        score = compute_bias_score(text)
        doc["bias_score"] = score
        if score > 0.3:
            # Add tag for bias warning
            tags = doc.get("tags", [])
            if "bias-warning" not in tags:
                tags.append("bias-warning")
            doc["tags"] = tags

        # Write updated document back
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(doc, f, allow_unicode=True)

if __name__ == "__main__":
    main()
