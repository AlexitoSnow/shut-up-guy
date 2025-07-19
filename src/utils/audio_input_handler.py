import speech_recognition as sr
import threading
import time

class AudioInputHandler:
    def __init__(self):
        print("Iniciando AudioInputHandler...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(3)
        self.voice_thread = None
        self.running = False
        self.shoot_detected = False

        # Lista de dispositivos de audio disponibles
        print("\nDispositivos de audio disponibles:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Micrófono {index}: {name}")

        # Calibrar el reconocedor de voz con el ruido ambiente
        print("\nCalibrando micrófono...")
        try:
            with self.microphone as source:
                print("Ajustando para ruido ambiente...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("¡Calibración completada!")
        except Exception as e:
            print(f"Error durante la calibración: {e}")

    def _listen_for_command(self):
        """Proceso en segundo plano para escuchar comandos de voz"""
        print("Iniciando escucha de comandos de voz...")
        while self.running:
            try:
                print("Esperando comando...")
                with self.microphone as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=1.5)

                try:
                    # Intentar reconocer el comando
                    text = self.recognizer.recognize_google(audio, language="es-ES").lower()
                    print(f"Audio detectado: '{text}'")

                    # Verificar si el comando es "shoot" o similares
                    trigger_words = ["shoot", "dispara", "fuego", "disparo", "pum", "bang"]
                    if any(word in text for word in trigger_words):
                        print("¡Comando de disparo detectado!")
                        self.shoot_detected = True

                except sr.UnknownValueError:
                    print(".", end="", flush=True)  # Indicador de que está escuchando
                except sr.RequestError as e:
                    print(f"\nError con el servicio de reconocimiento: {e}")
                    time.sleep(1)  # Esperar antes de reintentar

            except Exception as e:
                print(f"\nError en el reconocimiento de voz: {e}")
                time.sleep(1)  # Esperar antes de reintentar

    def start(self):
        """Inicia el proceso de escucha de comandos de voz"""
        if not self.running:
            self.running = True
            print("Iniciando thread de audio...")
            self.voice_thread = threading.Thread(target=self._listen_for_command, daemon=True)
            self.voice_thread.start()
            print("Thread de audio iniciado")

    def stop(self):
        """Detiene el proceso de escucha"""
        print("Deteniendo AudioInputHandler...")
        self.running = False

    def was_shoot_commanded(self):
        """Verifica si se detectó un comando de disparo"""
        if self.shoot_detected:
            self.shoot_detected = False
            return True
        return False

