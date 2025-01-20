import os
from pathlib import Path

class FileUtils:
    """Utilidades básicas para manejo de archivos en pruebas"""
    
    @staticmethod
    def get_test_file_path(filename):
        """
        Retorna la ruta absoluta de un archivo en el directorio test_files.
        
        Args:
            filename: Nombre del archivo (ej: "mi_archivo.txt")
            
        Returns:
            str: Ruta absoluta al archivo
        """
        # Obtiene la ruta raíz del proyecto
        project_root = Path(__file__).parent.parent
        
        # Construye la ruta al directorio test_files
        test_files_dir = os.path.join(project_root, "test_files")
        
        # Crea el directorio si no existe
        os.makedirs(test_files_dir, exist_ok=True)
        
        # Retorna la ruta completa al archivo
        return os.path.join(test_files_dir, filename)

    @staticmethod
    def validate_file_exists(file_path):
        """
        Valida que el archivo existe y es accesible.
        
        Args:
            file_path: Ruta al archivo a validar
            
        Returns:
            bool: True si el archivo existe y es accesible
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
        
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"No hay permisos de lectura para: {file_path}")
            
        return True