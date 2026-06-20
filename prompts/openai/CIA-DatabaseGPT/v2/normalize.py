#!/usr/bin/env python3
import sys
import json

def normalize(record):
    """
    Normalize a raw JSON record to the core schema.
    Required keys: id, title, url, published, description
    """
    return {
        "id": record.get("@id") or record.get("id"),
        "title": record.get("name") or record.get("title"),
        "url": record.get("url", ""),
        "published": record.get("datePublished", ""),
        "description": record.get("description", "")
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: normalize.py <input.json>", file=sys.stderr)
        sys.exit(1)

    infile = sys.argv[1]
    try:
        data = json.load(open(infile, encoding="utf-8"))
    except Exception as e:
        print(f"Error parsing JSON from {infile}: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine if JSON is an array or object with @graph
    records = data if isinstance(data, list) else data.get("@graph", [])
    for record in records:
        norm = normalize(record)
        # Only output records with both id and url
        if norm["id"] and norm["url"]:
            print(json.dumps(norm, ensure_ascii=False))

if __name__ == "__main__":
    main()
