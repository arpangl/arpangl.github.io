# GPE Judge

目前預設為**純前端模式**：題庫與測資由靜態檔提供，批改在瀏覽器端執行（WASM）。

## 純前端模式（推薦）

### 1. 產生前端題庫索引

在 `judge/` 目錄執行：

```bash
python3 build_frontend_manifest.py
```

會產生 `problems_manifest.json`（前端用來讀取題目與測資清單）。

> 每次新增/修改 `problems/` 內題目或測資後，都要重跑一次。

### 2. 啟動靜態伺服器

```bash
python3 -m http.server 5269
```

開啟：

```text
http://127.0.0.1:5269/
```

### 3. 純前端模式語言支援

- ✅ Python 3.9（Pyodide / WASM）
- ✅ C++14（browsercc Clang/LLD + WASI / WASM）

> C++ 第一次執行會下載大型工具鏈（約百 MB 級別），首次等待時間會比 Python 長很多。

---

## 舊版後端模式（仍可用）

若你要使用原本 `judge.py` / `server.py` 伺服器批改流程，仍可照舊執行：

```bash
python3 server.py --host 127.0.0.1 --port 5269
```

或 CLI：

```bash
python3 judge.py --list
python3 judge.py --info 10416
python3 judge.py 10416 my_solution.py
python3 judge.py 10416 my_solution.cpp
```

---

## 目錄重點

```text
judge/
├── build_frontend_manifest.py  # 產生純前端索引
├── problems_manifest.json      # 純前端題庫索引（生成檔）
├── problems/                   # 題目與測資
├── index.html                  # 前端入口
├── styles.css
├── app.js
├── judge-worker.js             # 瀏覽器端批改 worker
├── judge.py                    # CLI judge（後端模式）
└── server.py                   # Web API（後端模式）
```
