# 🧽 CSV Data Cleaner

A simple and powerful Shell + Python-based tool to clean messy CSV files.  
Removes null values, trims whitespace, and fixes date formats using pandas — all wrapped inside a user-friendly shell script and deployed on Streamlit

---

## 📌 Project Description

This project provides an automated pipeline to clean `.csv` files using a Bash shell script. It acts as a quick and efficient data preprocessor to prepare datasets for analysis or machine learning tasks.

## 🚀 Features
- Remove rows with missing/null values
- Trim leading/trailing whitespaces in strings
- Standardize date formats
- Command-line and Web UI support (via Streamlit)
- Shell script for easy execution

---

## 🛠️ Tools & Technologies Used

| Tool/Tech        | Purpose                                |
|------------------|----------------------------------------|
| Python (pandas)  | Data manipulation & cleaning           |
| Bash (clean.sh)  | Shell script for CLI-based execution   |
| Ubuntu (WSL)     | Development environment                |
| Git & GitHub     | Version control and collaboration      |
| VS Code          | Code editing                           |

---

## 📁 File Structure
├── clean_csv.py       # Python script to clean CSV

├── clean.sh           # Shell wrapper script

├── app.py             # Streamlit frontend

├── sample.csv         # Example CSV file

├── cleaned_sample.csv # Cleaned output

├── README.md          # Project documentation

---


## 🚀 How to Run the Project

### ⚙️ Prerequisites

- Python 3 installed
- `pandas` library (`pip install pandas` inside a virtual environment)
- Bash terminal (via WSL or Linux)

### 🔄 Setup Steps


#### Step 1: Clone or navigate to project folder
cd csv-data-cleaner

#### Step 2: (Optional) Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

#### Step 3: Install required libraries
pip install pandas

#### Step 4: Run the Shell script
./clean.sh input.csv output.csv

#### Step 5: Run the app locally:
streamlit run app.py
---

## ✅ Output Preview
After successful execution, your cleaned CSV will be saved as cleaned_sample.csv or whatever output filename you provided.

