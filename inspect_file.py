file_path = r"whatsapp_misinfo\india\misinfo_anonymized.txt"

# Show first 5 lines of the file
with open(file_path, "r", encoding="utf-8") as f:
    for i in range(5):
        line = f.readline()
        print(f"Line {i+1}: {line}")
