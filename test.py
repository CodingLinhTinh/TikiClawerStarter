# Mở tệp để ghi dữ liệu vào
file_path = "example.txt"

# Write, Read, Append
with open(file_path, "w", encoding="utf-8") as file:
    lines = [
        "Line 1\n",
        "Line 2\n",
        "Line 3\n"
    ]
    
    file.writelines(lines)

print("File created successfully.")
