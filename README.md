# Exon-Skip Filter

A containerized Python CLI tool for filtering exon skip events from genomic data.  
Designed for scalable genomic preprocessing pipelines where exon-skipping events
must be filtered efficiently and reproducibly across environments.
Runs identically across **Windows, Linux, and macOS**.

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop
- Git

---

### 1. Clone & Setup

```bash
git clone https://github.com/itsnottheend-Jason/exon-skip-filter
cd exon-skip-filter

mkdir data output logs
```

---

### 2. Test with Sample Data

```bash
# Copy sample data
cp sample-data/* data/
```

**Using real data:**
Replace `data/events.txt` with your genomic events file.

---

### 3. Run with Python (CLI)

```bash
python src/cli.py \
  --input data/events.txt \
  --output output/output.json
```

#### Arguments

| Argument | Required | Description |
|----------|--------|------------|
| `--input`, `-i` | ✅ | Path to `events.txt` |
| `--output`, `-o` | ❌ | Output JSON (default: `output/output.json`) |
| `--logs`, `-o` | ❌ | Output logs (default: `logs/exon-skip-filter.log`) |

---

### 4. Run with Docker

```bash
docker build -t exon-skip-filter .

docker run --rm \
  -v ./data:/app/data \
  -v ./output:/app/output \
  -v ./logs:/app/logs \
  exon-skip-filter \
  --input data/events.txt \
  --output output/output.json
```

---

### 5. Check Results

```bash
cat logs/exon_filter.log
cat output/output.json
```

---

## 🖥 Platform-Specific Commands

### Windows (PowerShell)

```powershell
docker run --rm -v '.\data:/app/data' -v '.\output:/app/output' -v '.\logs:/app/logs' exon-skip-filter --input data/events.txt --output output/output.json
```

### Windows (CMD)

```cmd
docker run --rm -v ".\data:/app/data" -v ".\output:/app/output" -v ".\logs:/app/logs" exon-skip-filter --input data/events.txt --output output/output.json
```

### Linux / macOS

```bash
docker run --rm -v ./data:/app/data -v ./output:/app/output -v ./logs:/app/logs exon-skip-filter --input data/events.txt --output output/output.json
```

---

## Project Structure

```text
exon-skip-filter/
├── Dockerfile
├── requirements.txt
├── src/
│   ├── parser.py
│   ├── filters.py
│   ├── enrichment.py
│   ├── pipeline.py
│   ├── logging_config.py
│   └── cli.py
├── data/
├── output/
└── logs/
```

---

## Output Files

After execution:

- `output/output.json` → Filtered exon skip events
- `logs/exon_filter.log` → Detailed processing logs

Example log:

```text
2026-03-19 20:01:56,042 [INFO] pipeline: === Starting exon skip pipeline version 1.0.0 ===
2026-03-19 20:01:56,043 [INFO] pipeline: Input: data/events.txt
2026-03-19 20:01:56,047 [INFO] pipeline: Total events to process: 73
2026-03-19 20:01:56,470 [INFO] enrichment: GENE-NAME added: TASOR2
2026-03-19 20:01:56,470 [INFO] enrichment: using cached GENE-NAME to save API calls
2026-03-19 20:01:56,471 [INFO] enrichment: using cached GENE-NAME to save API calls
2026-03-19 20:01:56,471 [INFO] enrichment: using cached GENE-NAME to save API calls
2026-03-19 20:01:56,643 [INFO] enrichment: GENE-NAME added: FBH1
2026-03-19 20:01:56,873 [INFO] enrichment: GENE-NAME added: PRKCQ-AS1
2026-03-19 20:01:57,044 [INFO] enrichment: GENE-NAME added: UPF2
2026-03-19 20:01:57,217 [INFO] enrichment: GENE-NAME added: PRPF18
2026-03-19 20:01:57,386 [INFO] enrichment: GENE-NAME added: RPP38
2026-03-19 20:01:57,611 [INFO] enrichment: GENE-NAME added: STAM
2026-03-19 20:01:57,794 [INFO] enrichment: GENE-NAME added: ARL5B
2026-03-19 20:01:57,973 [INFO] enrichment: GENE-NAME added: PLXDC2
2026-03-19 20:01:58,170 [INFO] enrichment: GENE-NAME added: ANKRD16
2026-03-19 20:01:58,336 [INFO] enrichment: GENE-NAME added: IL15RA
2026-03-19 20:01:58,503 [INFO] enrichment: GENE-NAME added: FRMD4A
2026-03-19 20:01:58,686 [INFO] enrichment: GENE-NAME added: FAM107B
2026-03-19 20:01:58,861 [INFO] enrichment: GENE-NAME added: RSU1
2026-03-19 20:01:58,875 [INFO] pipeline: Pipeline complete!
2026-03-19 20:01:58,875 [INFO] pipeline: Processed: 73 → Output: 17 events
2026-03-19 20:01:58,875 [INFO] pipeline: Cache stats: 14 unique genes found
2026-03-19 20:01:58,876 [INFO] pipeline: Result: output/output.json
```

---

## ⚠️ Troubleshooting

- **"Input file not found"**  
  → Ensure `data/events.txt` exists

- **Windows path issues**  
  → Use:
  - PowerShell: `.\data`
  - CMD: `.\\data`

- **No logs generated**  
  → Check:
  - `./logs` is mounted
  - Logging outputs to `logs/exon-skip-filter.log`

---

## Features

- Dockerized → zero dependency issues
- Cross-platform consistency
- Persistent data (mounted volumes)
- Structured logging (module-level)
- Clean exit codes and error handling
- Lightweight (~200MB, Python 3.12-slim)

---