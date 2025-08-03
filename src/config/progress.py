import json
import os
from os.path import dirname, abspath, join

class Progress:
    def __init__(self):
        # Crear ruta absoluta para el archivo de progreso
        current_dir = dirname(abspath(__file__))
        project_root = dirname(dirname(current_dir))
        data_dir = join(project_root, 'data')
        self.progress_file = join(data_dir, 'progress.json')

        # Asegurar que el directorio existe
        os.makedirs(data_dir, exist_ok=True)

        self.load_progress()

    def load_progress(self):
        try:
            with open(self.progress_file, 'r') as file:
                progress = json.load(file)
                self.levels = progress.get('levels', [])
        except FileNotFoundError:
            self.levels = []

    def save_progress(self):
        progress = {
            'levels': self.levels
        }
        with open(self.progress_file, 'w') as file:
            json.dump(progress, file, indent=4)

    def add_level(self, level):
        """
        Actualiza o añade la información de un nivel.
        Si el nivel existe, actualiza o agrega la dificultad correspondiente.
        Si el nivel no existe, lo crea con la dificultad proporcionada.
        """
        # Buscar si el nivel existe
        existing_level = next((l for l in self.levels if l['number'] == level['number']), None)
        if existing_level:
            # Actualizar las dificultades del nivel existente
            for difficulty, score in level.items():
                if difficulty != 'number':
                    existing_level[difficulty] = score
        else:
            # Agregar nuevo nivel
            self.levels.append(level)

        # Ordenar niveles por número
        self.levels.sort(key=lambda x: x['number'])
        self.save_progress()

    def level_exists(self, level_number):
        """
        Verifica si un nivel con el número dado ya existe.
        """
        return any(level['number'] == level_number for level in self.levels)

    def reset_progress(self):
        self.levels = []
        self.save_progress()