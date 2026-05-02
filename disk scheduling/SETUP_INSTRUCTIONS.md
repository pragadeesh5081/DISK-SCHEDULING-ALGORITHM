# Single Command Setup Instructions

## Quick Setup (Single Command)

```bash
# 1. Install Python 3.7+ from https://python.org/downloads/
# 2. Copy this project folder to your laptop
# 3. Open terminal/command prompt in project folder
# 4. Run this single command:

pip install streamlit matplotlib numpy pandas && streamlit run app.py

# 5. Open browser to: http://localhost:8501
```

## Alternative (Step by Step)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Verify Installation

```bash
python -c "import streamlit, matplotlib, numpy, pandas; print('All packages installed successfully')"
```

## Requirements Summary
- Python 3.7+
- streamlit>=1.28.0
- matplotlib>=3.7.0  
- numpy>=1.24.0
- pandas>=2.0.0
