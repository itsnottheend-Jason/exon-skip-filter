## Exon-Skip Filter
A containerized Python CLI tool for filtering exon skip events from genomic data. Works identically across Windows, Linux, and Mac.

## Quick Start
# Prerequisites
Docker Desktop installed
Git

1. Clone & Setup
git clone https://github.com/itsnottheend-Jason/exon-skip-filter
cd exon-skip-filter
mkdir data output logs

2. Test with Sample Data (manual work)
# Copy sample data
cp sample-data/* data/
# Real Data
Replace data/events.txt with real genomic events file

# CLI Usage (python)
cd exon-skip-filter
python src/cli.py --input data/events.txt --output output/output.json

# Arguments:
--input, -i (required) - Path to events.txt
--output, -o - Output JSON (default: output/output.json)

# Docker Build & run (for Different OS/platform, see 'Platform-Specific Commands')
docker build -t exon-skip-filter .
docker run --rm -v ./data:/app/data -v ./output:/app/output -v ./logs:/app/logs exon-skip-filter --input data/events.txt --output output/output.json

3. Check Results
cat logs/exon_filter.log      # Processing logs with timestamps
cat output/output.json        # Filtered exon skip results



## Platform-Specific Commands
# Windows (PowerShell)
cd exon-skip-filter
docker build -t exon-skip-filter .
docker run --rm -v '.\data:/app/data' -v '.\output:/app/output' -v '.\logs:/app/logs' exon-skip-filter --input data/events.txt --output output/output.json
# Windows (CMD)
cd /d exon-skip-filter
docker build -t exon-skip-filter .
docker run --rm -v ".\data:/app/data" -v ".\output:/app/output" -v ".\logs:/app/logs" exon-skip-filter --input data/events.txt --output output/output.json

# Linux/Mac
cd exon-skip-filter
docker build -t exon-skip-filter .
docker run --rm -v ./data:/app/data -v ./output:/app/output -v ./logs:/app/logs exon-skip-filter --input data/events.txt --output output/output.json




## Project Structure
exon-skip-filter/
├── Dockerfile              # Production-ready Python 3.12
├── requirements.txt        # PyYAML, pandas, numpy
├── src/
│   ├── parser.py           # parser, iter for large inputs
│   └── filters.py          # filters, extendable
│   └── enrichment.py       # for gene name
│   └── pipeline.py         # Core pipeline logic
│   └── logging_config.py   # configration of logger for both file and runtime display
│   └── cli.py              # CLI entrypoint (--input, --output)
├── data/                   # Mount your input here
├── output/                 # Results appear here  
└── logs/                   # Processing logs here


## Output Files
After run:

output/output.json - Filtered exon skip events
logs/exon_filter.log - Detailed processing log:

2026-03-19 16:30:00 [INFO] cli: Processing data/events.txt
2026-03-19 16:30:01 [INFO] Exon_filter.parser: Found 23 events
2026-03-19 16:30:02 [INFO] __main__: Pipeline completed successfully


# Troubleshooting
"Input file not found" - Check data/events.txt exists

Windows path issues - Use '.\data' (PowerShell) or ".\\data" (CMD)

No logs - Verify ./logs folder mounted and logging configured to logs/exon_filter.log

## Features
Zero dependency issues - Dockerized environment

Cross-platform - Windows/Linux/Mac identical results

Persistent data - Input/output/logs on filesystem

Production logging - Module-level logs (cli, Exon_filter.parser)

Clean exit codes - Proper error handling

Lightweight - Python 3.12-slim (~200MB image)