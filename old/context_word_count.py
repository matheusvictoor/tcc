# import json
import re
from pathlib import Path

INPUT_FILE = Path("data.jsonl")
# OUTPUT_FILE = Path("data_atualizado.jsonl")

def word_count(content):
    context_text = content
    context_text = re.sub(r'\[.*?\]\(.*?\)', '', context_text)
    context_text = re.sub(r'^[#*>-]+\s?', '', context_text, flags=re.MULTILINE)
    context_text = re.sub(r'\s+', ' ', context_text).strip()
    context_text = re.findall(r'\b\w+(?:[-/.,]\w+)*\b', context_text)

    # print(context_text)

    word_count = len(context_text)
    return word_count

# def main():
#     with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
#           open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
#         # rows = fin.readlines()
#         # row = rows[7]
#         # adr = json.loads(row)
#         # content = adr.get("content", "")
#         # wc = word_count(content)
#         # print(f"Repo: {adr['repositoryUrl']}, Path: {adr['path']}, Context Words: {wc}")

#         count = 0
#         for line in fin:
#             adr = json.loads(line)
#             content = adr.get("content", "")
#             wc = word_count(content)

#             adr["wordCount"] = wc
#             fout.write(json.dumps(adr, ensure_ascii=False) + "\n")
#             # print(f"Repo: {adr['repositoryUrl']}, Path: {adr['path']}, Context Words: {wc}")
#             count += 1
#             print(f"wc ->{wc}")

#             # if count == 5: break
#         print(f"Total ADRs processadas: {count}")

# if __name__ == "__main__":
#     main()