import json
import re
import sys

def parse_text_to_json(text: str) -> dict:
    entries = text.strip().split('\n\n')
    result = {}

    for entry in entries:
        lines = entry.strip().splitlines()
        label = None
        text_value = None
        choices = []

        for line in lines:
            if line.startswith("label"):
                match = re.search(r'"(.*?)"', line)
                if match: label = match.group(1)
            elif line.startswith("text"):
                match = re.search(r'"(.*?)"', line)
                if match: text_value = match.group(1)
            elif line.startswith("choices"):
                choice_matches = re.findall(r'\("([^"]+)"\s*:\s*"([^"]+)"\)', line)
                for next_label, choice_text in choice_matches:
                    choices.append({ "text": choice_text, "next": next_label })

        if label:
            result[label] = {
                "text": text_value,
                "choices": choices
            }

    return result

def main():
    with open("raw.txt", "r") as f:
        text = f.read()

    json_text = parse_text_to_json(text)

    with open("test.json", "w") as f:
         json.dump(json_text, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
