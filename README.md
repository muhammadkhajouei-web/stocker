

# Stocker Laptop Data ETL & Valuation Pipeline 🚀

An end-to-end, metadata-driven Python data pipeline designed to ingest, clean, normalize, and structurally extract hardware configurations from raw ecommerce laptop listings. 

Beyond extraction, the system classifies machines into domain-specific tiers and scores them through a custom mathematical valuation matrix, calculating a normalized **Value-for-Money** score within each respective category.



🏗️ Architecture & Folder Structure



The project decouples core extraction logic from runtime string patterns by utilizing a JSON rule-engine approach. This allows updates to hardware regex definitions without modifying functional Python scripts.

```markdown
```text
stocker/
│
├── input_data/               # Raw unstructured scraped source files (.csv, .xlsx)
├── clean_data/               # Validated datasets, intermediates, and final reporting sheets
│
└── cleaning_prg/             # Main application codebase
    ├── main.py               # Central orchestrator driving ingestion, parsing, and load
    │
    ├── rules/                # Declarative Rule-Engine Layer (Metadata Constraints)
    │   ├── brand_rules.json  # Multi-lingual variations mapped to canonical brands
    │   ├── cpu_rules.json    # Generation extraction rules, families, and architectural classes
    │   ├── gpu_rules.json    # Precedence-ordered GPU maps separating Dedicated vs Integrated
    │   └── monitor_rules.json# Positional patterns for dimensions, resolutions, panels, and Hz
    │
    ├── parsers/              # Regex Parsing Core (Pure Execution Modules)
    │   ├── brand.py          # Resolves official manufacturer names via lookup arrays
    │   ├── cpu.py            # Extracts chip models, suffixes, and structural generations
    │   ├── gpu.py            # Matches sequential criteria patterns and isolates memory spaces
    │   ├── ram.py            # Captures memory capacity boundaries, defaulting to GB units
    │   ├── ssd.py            # Sanitizes storage capacities, stripping ram-leaks like DDR prefixes
    │   ├── monitor.py        # Compiles resolution tags, sizes, and pixel geometry (PPI)
    │   └── price.py          # Standardizes numerical rates based on currency denominations
    │
    └── utils/                # Systemic Utility Core
        └── normalize.py      # Pure stream-sanitizer (glyph conversions, digit corrections)

```

---

## 🔄 The Data Pipeline Flow

```
[Raw Scraped CSV/XLSX] 
        │
        ▼
[utils/normalize.py] ──────► Sanitizes text, translates Persian digits, unifies characters
        │
        ▼
[parsers/* + rules/*.json] ─► Regex execution engines parse structural attributes top-down
        │
        ▼
[scores.py] ───────────────► Scores distinct components on an analytical 1 to 5 scale
        │
        ▼
[valuator.py] ─────────────► Categorizes laptops & applies multi-variable weighted score bounds
        │
        ▼
[Final Normalized Output] ──► Exports pristine, production-ready dataset

```

### 1. Ingestion & Stream Sanitization (`utils/`)

Raw crawled texts often contain varied multi-lingual schemas, hidden glyphs, or control indicators. `normalize.py` transforms incoming records through pure functions by:

* Mapping Persian/Arabic localized characters and textual numbers (`اول` ➔ `1`) into standard English digits.
* Erasing noisy product metadata tags (`®`, `™`, `©`).
* Converting unicode arithmetic dimensions (`×`, `✕`) to standard characters (`x`) and dropping numeric formatting comma characters (`۲,۴۹۶` ➔ `2496`).

### 2. Prioritized Metadata Extraction (`parsers/`)

Rather than relying on brittle conditional scripts, parsing flows systematically based on ordering. For instance, in `gpu_rules.json`, dedicated frameworks sit explicitly above integrated structures.

* If a string reads `Intel 8GB RTX 3050 4GB`, the top-down pattern matches `RTX` first, flags it as **Dedicated**, locks **Nvidia** as the brand, and anchors the extraction boundary exclusively around the `4GB` neighboring the card identifier, entirely ignoring the shared `8GB` memory block.

### 3. Component Scoring (`scores.py`)

Hardware metrics are individually isolated and rated on a standardized **1 to 5** performance tier.

* **CPUs:** Apple Silicon models scale predictably based on chip modifiers (`M3 Pro` ➔ `5`, `M1` ➔ `2`). x86 chips utilize customized generational evaluation strategies based on architectures and suffix types.
* **RAM/SSD:** Capacity integers map directly to distinct performance thresholds (e.g., SSDs $\ge$ 1TB score a `5`; RAM $\ge$ 32GB scores a `5`).
* **Monitors:** Scales dimension categories combined with canonical resolution identifiers (`4K`/`2K`/`FHD`).

### 4. Categorization & Relative Valuation Metrics (`valuator.py`)

Laptops do not compete globally; a lightweight office device operates on different requirements than a heavy-duty workstation.

#### Phase A: Structural Classification

Each asset is dynamically routed into one of three primary markets based on its physical component specs:

1. **Gaming & High-Performance (`گیمینگ و حرفه‌ای`)**
2. **Design & Creative Graphics (`طراحی و گرافیک`)**
3. **Administrative & Corporate Student (`اداری و دانشجویی`)**

#### Phase B: Category-Weighted Raw Config Scores

The pipeline applies distinct architectural weights ($W$) dynamically based on the target category:

| Category | CPU Weight | GPU Weight | RAM Weight | SSD Weight |
| --- | --- | --- | --- | --- |
| **Gaming & Pro** | 30% | 50% | 12% | 8% |
| **Design & Creative** | 35% | 25% | 25% | 15% |
| **Administrative / Student** | 35% | 10% | 30% | 25% |

$$\text{Raw Config Score} = \frac{\sum (\text{Component Score} \times W_{\text{component}})}{\sum W}$$

#### Phase C: Local Category Normalization

To guarantee accurate market positioning, the raw metrics are min-max normalized strictly **within each category group** onto a readable **1 to 100** interval:

$$\text{Config Score} = 1 + 99 \times \left( \frac{\text{Current Raw Score} - \text{Min Raw Score}_{\text{category}}}{\text{Max Raw Score}_{\text{category}} - \text{Min Raw Score}_{\text{category}}} \right)$$

#### Phase D: Value-for-Money Computation

The final algorithmic score correlates the structural hardware capacity against the market listing price:

$$\text{Value Score}_{\text{raw}} = \frac{\text{Config Score}}{\text{Price}}$$

This value configuration undergoes a second round of min-max normalization within each category group to generate an actionable **Value-for-Money Score (1–100)**, explicitly highlighting high-spec anomalies listed below market rates.

---

## 🛠️ Usage and Execution

### Prerequisites

* Python 3.10+
* Pandas
* NumPy
* OpenPyXL (for spreadsheet parsing and logging outputs)

### Running the Pipeline

Execute the main parsing thread to clean raw ingestion data frames:

```bash
python cleaning_prg/main.py

```

### Tracking Incomplete Records

To check for missing parameters or incomplete parsing boundaries, run the reporting utility:

```bash
python cleaning_prg/reporter.py

```

This scans your output and logs the precise Excel cell indexes that returned empty records, allowing you to quickly patch your configuration JSON rules.

---

## 💡 Engineering Highlights

* **Pure Functional Separation:** `utils/normalize.py` maintains absolute isolation. It does not carry system state or database dependencies, ensuring swift runtime execution.
* **Order-of-Operations Architecture:** Resolves complex text-matching overlaps (like tracking dual-branded or integrated/dedicated shared specs) directly inside prioritized JSON rules, eliminating deeply nested code trees in your parsing engines.

