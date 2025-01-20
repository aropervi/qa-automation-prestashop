import os

# Ruta al proyecto local (se ajusta automáticamente a la ubicación del script)
project_path = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(project_path, "summary.txt")

# Extensiones relevantes (modifica según tus necesidades)
extensions = [".py", ".yaml", ".json", ".md", ".sh"]

with open(output_file, "w", encoding="utf-8") as summary:
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                summary.write(f"\n--- {file_path} ---\n")
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    summary.write(f.read())
