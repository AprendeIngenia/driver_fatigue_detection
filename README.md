# Deteccion de somnolencia:
Hola, chicos en este repositorio encontrarán la programación para que puedan crear su sistema de deteccion de somnolencia en tiempo real.

## Conceptos introductorios:
- Este repositorio contiene el código fuente en Python para ejecutar y utilizar nuestro sistema de etiquetado automatico con el fin de entrenar modelos de detección de objetos.
- Para iniciar recomendamos ver algunos conceptos introductorios con el fin de entender un poco mejor todo el funcionamiento, por eso te dejamos la explicacion en este [video.](https://youtu.be/PQ71QvvFbA8?si=r77MhBOwhD5UDZx3)
- Los modelos lo puedes encontrar [aqui.]([https://github.com/IDEA-Research/GroundingDINO](https://github.com/google-ai-edge/mediapipe))

## Características

- **Procesamiento en tiempo real:** Utiliza Mediapipe para detectar puntos clave faciales y de las manos.
- **Interfaz gráfica:** Desarrollada con Flet para mostrar los resultados de la detección.
- **Dockerizable:** Facilita la ejecución en servidores remotos.
- **API robusta:** Utiliza FastAPI para ofrecer un backend modular y extensible.

![YoloV8](https://github.com/user-attachments/assets/607fac48-6132-4b36-981b-530491ada198)

## Requisitos:
Para utilizar este código, asegúrese de cumplir con los siguientes requisitos previos:

- Sistema operativo compatible: Windows, Linux o macOS
- Versión de Python: 3.10 o superior
- Version CUDA: 11.7
- Paquetes adicionales: NumPy, OpenCV, Flet, etc. Consulte el archivo [requirements.txt](https://github.com/AprendeIngenia/driver_fatigue_detection/blob/012943fa6e02abbf65fde26573ce52e710f0a5a8/requirements.txt) para ver la lista completa de dependencias.
- Docker (opcional para despliegue en contenedor)

## Instalación

#### 1. Clonar el repositorio

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu_usuario/drowsiness-detection.git
cd drowsiness-detection
```

#### 2. Crear y activar entorno virtual
```bash
python -m venv venv
```

Activar venv en Windows
```bash
./venv/Scripts/activate
```

Activar venv en Linux
```bash
source venv/bin/acitvate
```

#### 3. Instalar dependencias 
```bash
pip install -r requirements.txt
```

#### 4. Ejecutar el servidor
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

#### 5. Ejecutar interfaz grafica
```bash
flet main.py
```

## Dockerizacion
#### 1. Construir la imagen Docker
```bash
docker build -t drowsiness-server .
```

#### 2. Ejecutar el contenedor:
```bash
docker run -d -p 8000:8000 --name drowsiness-server drowsiness-server
```
Ó
```bash
docker start drowsiness-server
```


#### 3. Ejecutar interfaz grafica
```bash
flet main.py
``` 

#### 4. Detener el contenedor
```bash
docker stop drowsiness-server
``` 

#### 5. Revisar estado del contenedor
```bash
docker ps -a
```

## Contacto
¡Gracias por usar el Drowsiness Detection System! Si tienes alguna duda o sugerencia, no dudes en abrir un issue o contactarme.

Si tiene preguntas o consultas relacionadas con este proyecto, no dude en contactarnos en nuestro canal de Youtube [Aprende e Ingenia](https://www.youtube.com/@AprendeIngenia/videos). Le responderemos tan pronto como nos sea posible.
Gracias por visitar nuestro repositorio y esperamos que disfrute trabajando con nuestro codigo. :smile:

## Recuerda que puedes contribuir a que siga desarrollando:
Simplemente suscribiendote a mi canal de YouTube:
- [Canal YouTube](https://www.youtube.com/channel/UCzwHEOCbsZLjfELperJ6VeQ/videos)

### Siguiendome en mis redes sociales: 
- [Instagram](https://www.instagram.com/santiagsanchezr/)
- [Twitter](https://twitter.com/SantiagSanchezR)
