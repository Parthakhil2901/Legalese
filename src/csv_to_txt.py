import pandas as pd
import os
import re

input_file = "data/legal_docs/ipc_sections.csv"
output_folder = "data/legal_docs/ipc"

os.makedirs(output_folder, exist_ok=True)

df = pd.read_csv(input_file)

# Print column names once (to debug)
print("Columns:", df.columns)

for index, row in df.iterrows():

    # Safely access columns by name
    section = str(row["Section"]) if "Section" in df.columns else str(index)
    description = str(row["Description"]) if "Description" in df.columns else str(row[1])

    # Clean section number (remove special characters)
    section_clean = re.sub(r"[^0-9A-Za-z]", "_", section)

    filename = f"{output_folder}/section_{section_clean}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Section {section}\n\n{description}")

print("Conversion complete")