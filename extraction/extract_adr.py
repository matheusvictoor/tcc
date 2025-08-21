import os
import requests
import json
import time
from pathlib import Path
import base64
from tqdm import tqdm
from context_word_count import word_count

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

with open("GITHUB_TOKEN", "r") as f:
    GITHUB_TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

REPO_DIR = Path("ADR-Study-Dataset/repositories")
OUTPUT_FILE = Path("data.jsonl")
ERRO_FILE = Path("erro_dataset.jsonl")

def get_adr_content(repositorie, adr_path):
    url = f"https://api.github.com/repos/{repositorie}/contents/{adr_path}"
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response:
            encoding = response.json().get("encoding", "base64")

            if encoding == "base64":
                content = response.json().get("content", "")
                return content.encode("ascii")
        return None
    except Exception as e:
        print(f"Erro na requisicao ao github: {e}")
     
def main():
    count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file, open(ERRO_FILE, "w", encoding="utf-8") as erro_file:
        for file in tqdm(list(REPO_DIR.glob("*.json"))):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            repo_url = data.get("repositoryUrl")
            if not repo_url:
                continue
            
            repo = repo_url.replace("https://github.com/", "").replace(".git", "")
            for adr in data.get("adrFiles", []):
                count += 1
                path = f"{adr['adrDirectory']}/{adr['path']}"
                content_b64 = get_adr_content(repo, path)
                time.sleep(2)

                if content_b64:
                    try:
                        content = base64.b64decode(content_b64).decode("utf-8", errors="ignore")
                        title_line = content.strip().splitlines()[0] if content.strip() else ""
                        title = title_line.lstrip("#").strip() if title_line.startswith("#") else "(sem título)"
                        wc = word_count(content)

                        record = {
                            "repositoryUrl": repo_url,
                            "path": path,
                            "template": adr.get("template"),
                            "status": adr.get("status"),
                            "firstCommit": adr.get("firstCommit"),
                            "lastCommit": adr.get("lastCommit"),
                            "numberOfCommits": adr.get("numberOfCommits"),
                            "title": title,
                            "wordCount": wc,
                            "content": content
                        }

                        out_file.write(json.dumps(record, ensure_ascii=False) + "\n")
                        print(f"Ok [{count}] Processando ADR: {repo_url}/{path}")
                    except Exception as e:
                        erro_file.write(json.dumps({
                            "repositoryUrl": repo_url,
                            "path": path,
                            "error": str(e) }) + "\n")
                        print(f"X [{count}] Erro o processar ADR em {repo_url}/{path}: {e}")
                else:
                    erro_file.write(json.dumps({
                        "repositoryUrl": repo_url,
                        "path": path,
                        "error": "Falha na requisicao ou conteudo invalido"
                    }) +  "\n")
                    print(f"X [{count}] Falha ao buscar {repo_url}/{path}: Conteudo nao encontrado!")

if __name__ == "__main__":
    main()

