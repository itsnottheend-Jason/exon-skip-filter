text
# Exon-Skip Filter

A containerized Python CLI tool for filtering exon skip events from genomic data. Works identically across Windows, Linux, and Mac.

## Quick Start

### Prerequisites
- Docker Desktop installed
- Git

### 1. Clone & Setup
```bash
git clone https://github.com/itsnottheend-Jason/exon-skip-filter
cd exon-skip-filter
mkdir data output logs
2. Test with Sample Data
bash
# Copy sample data
cp sample-data/* data/

# Build & run
docker build -t exon-skip-filter .
docker run --rm -v ./data:/app/data -v ./output:/app/output -v ./logs:/app/logs exon-skip-filter --input data/events.txt --output output/output.json
3. Check Results
bash
cat logs/exon_filter.log      # Processing logs with timestamps
cat output/output.json        # Filtered exon skip results
Platform-Specific Commands
Windows (PowerShell)
powershell
cd exon-skip-filter
docker run --rm -v '.\data:/app/data' -v '.\output:/app/output' -v '.\logs:/app/logs' exon-skip-filter --input data/events.txt --output output/output.json
Windows (CMD)
text
cd /d exon-skip-filter
docker run --rm -v ".\data:/app/data" -v ".\output:/app/output" -v ".\logs:/app/logs" exon-skip-filter --input data/events.txt --output output/output.json
Linux/Mac
bash
cd exon-skip-filter
docker run --rm -v ./data:/app/data -v ./output:/app/output -v ./logs:/app/logs exon-skip-filter --input data/events.txt --output output/output.json
Local Python Usage
bash
cd exon-skip-filter
pip install -r requirements.txt
python src/cli.py --input data/events.txt --output output/output.json
CLI Arguments
--input, -i (required) - Path to events.txt

--output, -o - Output JSON (default: output/output.json)

Project Structure
text
exon-skip-filter/
├── Dockerfile              # Production-ready Python 3.12
├── requirements.txt        # PyYAML, pandas, numpy
├── src/
│   ├── cli.py             # CLI entrypoint
│   ├── pipeline.py        # Core pipeline logic
│   ├── parser.py          # Parser for large inputs
│   ├── filters.py         # Extensible filters
│   ├── enrichment.py      # Gene name enrichment
│   └── logging_config.py  # Dual console/file logging
├── sample-data/           # Test events.txt
├── data/                  # Mount your input here
├── output/                # Results appear here
└── logs/                  # Processing logs here
Output Files
output/output.json - Filtered exon skip events

logs/exon_filter.log - Detailed processing log:

text
2026-03-19 16:30:00 [INFO] cli: Processing data/events.txt
2026-03-19 16:30:01 [INFO] Exon_filter.parser: Found 23 events
2026-03-19 16:30:02 [INFO] __main__: Pipeline completed successfully
Troubleshooting
"Input file not found" - Check data/events.txt exists

Windows path issues - Use '.\data' (PowerShell) or ".\data" (CMD)

No logs - Verify ./logs folder mounted and logging configured

Features
Zero dependency issues - Dockerized environment

Cross-platform - Windows/Linux/Mac identical results

Persistent data - Input/output/logs on filesystem

Production logging - Live console + file logging

Clean modular structure - Separate parser, filters, pipeline

Lightweight - Python 3.12-slim (~200MB image)