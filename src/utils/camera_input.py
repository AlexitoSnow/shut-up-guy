# Manejo de entrada del usuario
# Gestiona la entrada del teclado y mouse,
# incluyendo mapeo de teclas y estados de input
import cv2
import mediapipe as mp
import math
import threading

class CameraInput:
    @staticmethod
    def list_available_cameras():
        """Lista todas las cámaras disponibles en el sistema"""
        available_cameras = []
        for i in range(3):  # Verificar hasta 3 cámaras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras

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
            self.thumb_extended = True
            self.direction = 0
            self.hand_detected = False

            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    self.hand_detected = True
                    # Puntos clave de los dedos
                    thumb_tip = hand_landmarks.landmark[4]   # Punta del pulgar
                    index_tip = hand_landmarks.landmark[8]   # Punta del índice
                    index_mcp = hand_landmarks.landmark[5]   # Base del índice

                    # Verificar si el índice está extendido (comparando con su articulación)
                    self.index_extended = index_tip.y < index_mcp.y

                    # Verificar si el pulgar está extendido (usando la distancia desde la base)
                    thumb_extension = math.hypot(
                        thumb_tip.x - index_mcp.x,
                        thumb_tip.y - index_mcp.y
                    )

                    self.thumb_extended = thumb_extension > 0.1  # Ajustar el umbral según sea necesario

                    # Si el índice está extendido, determinar dirección
                    if self.index_extended:
                        center_x = frame.shape[1] // 2
                        index_screen_x = index_tip.x * frame.shape[1]

                        if index_screen_x < center_x - 40:
                            self.direction = 1  # Izquierda
                        elif index_screen_x > center_x + 40:
                            self.direction = -1   # Derecha
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
