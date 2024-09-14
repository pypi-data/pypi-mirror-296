import sys
import io
import logging
import asyncio
from threading import Thread
from chaski.streamer import ChaskiStreamer


class AsyncInterceptOutput(io.StringIO):
    def __init__(self, streamer):
        super().__init__()
        self.original_stdout = sys.stdout  # Guardamos el stdout original
        self.original_stderr = sys.stderr  # Guardamos el stderr original
        sys.stdout = self  # Redirigimos stdout
        sys.stderr = self  # Redirigimos stderr
        # Redirigimos también el logging a este buffer
        self.logging_handler = logging.StreamHandler(self)
        logging.getLogger().addHandler(self.logging_handler)

        self.streamer = streamer
        self.loop = asyncio.new_event_loop()  # Creamos un nuevo bucle de eventos
        self.loop_thread = Thread(target=self.start_background_loop, args=(self.loop,), daemon=True)
        self.loop_thread.start()

    def start_background_loop(self, loop):
        """Iniciar el bucle de eventos en un hilo en segundo plano"""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def write(self, data):
        super().write(data)  # Guardar la salida en el buffer de forma estándar
        # Ejemplo de operación adicional: escribir en stdout original
        self.original_stdout.write(f"[Intercepted async]: {data}")

        # Delegamos la tarea al bucle de eventos en segundo plano
        self.loop.call_soon_threadsafe(asyncio.create_task, self.streamer.push('logs', data))

    def restore(self):
        # Restaurar stdout, stderr y remover el handler de logging
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        logging.getLogger().removeHandler(self.logging_handler)
        self.loop.stop()  # Detener el bucle de eventos en segundo plano


# Configurar logging
logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------------------------
async def main():
    streamer = ChaskiStreamer(run=False)

    asyncio.create_task(streamer.run())
    asyncio.create_task(streamer.connect('127.0.0.1', 51114))

    # Crear interceptor que captura stdout, stderr y logging
    interceptor = AsyncInterceptOutput(streamer)

    # # Generar algunos logs
    # print("Este es un mensaje interceptado desde print.")
    # logging.info("Este es un mensaje interceptado desde logging.")

    # await asyncio.sleep(1)  # Simulación de tiempo para procesamiento de logs

# Ejecutar la función asíncrona
asyncio.run(main())
