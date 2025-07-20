# Manejo de entrada del usuario
# Gestiona la entrada del teclado y mouse,
# incluyendo mapeo de teclas y estados de input
# src/utils/input_handler.py
import cv2
import mediapipe as mp
import math
import threading

class CameraInputHandler:
    @staticmethod
    def list_available_cameras():
        """Lista todas las cámaras disponibles en el sistema"""
        available_cameras = []
        for i in range(10):  # Verificar hasta 10 cámaras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras
    
    @staticmethod
    def print_available_cameras():
        """Imprime las cámaras disponibles en el sistema"""
        cameras = CameraInputHandler.list_available_cameras()
        print("\nCámaras disponibles:")
        for cam_index in cameras:
            print(f"  Cámara {cam_index}")
        if not cameras:
            print("  No se encontraron cámaras disponibles")
        return cameras

    def __init__(self, camera_index=0, threshold=30):
        print(f"Inicializando CameraInputHandler con cámara {camera_index}")
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        
        # Verificar si la cámara se abrió correctamente
        if not self.cap.isOpened():
            print(f"Error: No se pudo abrir la cámara {camera_index}")
            # Intentar con la cámara por defecto
            print("Intentando con la cámara por defecto (índice 0)...")
            self.camera_index = 0
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: No se pudo abrir ninguna cámara")
        else:
            print(f"Cámara {camera_index} abierta correctamente")
            
        self.running = False
        self.thread = None

        # Estados de los dedos
        self.index_extended = False
        self.thumb_extended = False
        self.direction = 0
        self.hand_detected = False

        # Para evitar disparos accidentales
        self.last_thumb_state = True
        self.thumb_state_count = 0

    def start(self):
        if not self.running:
            self.running = True
            # Iniciar el hilo de la cámara
            self.thread = threading.Thread(target=self._process_camera, daemon=True)
            self.thread.start()

    def _process_camera(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_results = self.hands.process(img_rgb)

            # Resetear estados
            self.index_extended = False
            self.thumb_extended = True  # Por defecto consideramos el pulgar extendido (no dispara)
            self.direction = 0
            self.hand_detected = False

            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    self.hand_detected = True
                    # Puntos clave de los dedos
                    thumb_tip = hand_landmarks.landmark[4]   # Punta del pulgar
                    thumb_ip = hand_landmarks.landmark[3]    # Primera articulación del pulgar
                    thumb_mcp = hand_landmarks.landmark[2]   # Base del pulgar
                    index_tip = hand_landmarks.landmark[8]   # Punta del índice
                    index_pip = hand_landmarks.landmark[6]   # Segunda articulación del índice

                    # Verificar si el índice está extendido (comparando con su articulación)
                    self.index_extended = index_tip.y < index_pip.y

                    # Verificar si el pulgar está extendido (usando la distancia desde la base)
                    thumb_extension = math.hypot(
                        thumb_tip.x - thumb_mcp.x,
                        thumb_tip.y - thumb_mcp.y
                    )

                    # Detección más estable del pulgar
                    current_thumb_extended = thumb_extension > 0.1

                    # Solo cambiar el estado si se mantiene por algunos frames
                    if current_thumb_extended == self.last_thumb_state:
                        self.thumb_state_count += 1
                        if self.thumb_state_count > 3:  # requiere 3 frames consecutivos
                            self.thumb_extended = current_thumb_extended
                    else:
                        self.thumb_state_count = 0
                        self.last_thumb_state = current_thumb_extended

                    # Si el índice está extendido, determinar dirección
                    if self.index_extended:
                        center_x = frame.shape[1] // 2
                        index_screen_x = index_tip.x * frame.shape[1]

                        if index_screen_x < center_x - 40:
                            self.direction = 1  # Izquierda
                        elif index_screen_x > center_x + 40:
                            self.direction = -1   # Derecha

                    # Debug info
                    print(f"""Estado de la mano:
Mano detectada: {self.hand_detected}
Índice extendido: {self.index_extended}
Pulgar extendido: {self.thumb_extended}
Dirección: {self.direction}
Extensión del pulgar: {thumb_extension:.3f}
""")
                    break

    def get_direction(self):
        # Solo retorna dirección si hay una mano y el índice está extendido
        return self.direction if self.hand_detected and self.index_extended else 0

    def is_index_extended(self):
        # Solo retorna verdadero si hay una mano
        return self.hand_detected and self.index_extended

    def is_thumb_extended(self):
        # Solo retorna el estado del pulgar si hay una mano, de lo contrario siempre true
        return True if not self.hand_detected else self.thumb_extended

    def stop(self):
        print(f"Deteniendo CameraInputHandler (cámara {self.camera_index})")
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)  # Esperar hasta 1 segundo
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("Cámara liberada correctamente")
