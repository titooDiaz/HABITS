<p align="center">
  <img width="150px" src="https://i.ibb.co/bXvzjXm/LOGO-h1.png" alt="Logo del proyecto" />
</p>

# Gestión de Rutinas Diarias con Flask 🕒  

¡Bienvenido! Esta aplicación está diseñada para ayudarte a gestionar tus rutinas diarias de manera efectiva y convertirte en una persona más disciplinada, enfocada en alcanzar tus metas y contribuir al mundo.  

**¿Por qué esta aplicación?**  
La disciplina es la clave del éxito personal y profesional. Con esta herramienta, podrás organizar tu día a día, monitorear tu progreso y cultivar hábitos positivos de forma sostenible.  

## Características ✨  
- **Gestión de Rutinas**: Agrega, edita y elimina tareas diarias.  
- **Seguimiento de Progreso**: Revisa tu desempeño semanal o mensual.  
- **Personalización**: Ajusta tus metas y horarios según tus necesidades.  
- **Código Abierto**: Modifica y adapta la aplicación a tus preferencias personales.  

## Tecnologías Utilizadas 🛠️  
- **Flask**: Framework para el backend.  
- **HTML/CSS/JavaScript**: Para la interfaz de usuario.  
- **SQLite**: Base de datos ligera y fácil de usar.  
- **Tailwind CSS**: Para el diseño responsivo.  

## Instalación 🚀  

### Requisitos  
- Python 3.9 o superior  
- pip (gestor de paquetes de Python)  

### Pasos  
1. Clona este repositorio:  
   ```bash  
   git clone https://github.com/titooDiaz/HABITS.git
   cd HABITS
   ```  
2. Crea un entorno virtual:  
   ```bash  
   python3 -m venv venv  
   source venv/bin/activate  # En Windows: venv\Scripts\activate  
   ```  
3. Instala las dependencias:  
   ```bash  
   pip install -r requirements.txt  
   ```  
4. Configura el archivo `.env` (si usas variables de entorno).  
5. Ejecuta la aplicación:
   modo desarrollador:
   ```bash  
   python main.py
   ```  
   modo produccion:
   modo desarrollador
   ```bash  
   gunicorn -w 4 -b 0.0.0.0:8000 main:app
   ``` 
6. Accede a la aplicación en tu navegador: [http://localhost:8000](http://localhost:8000)  

## Cómo Contribuir 🤝  
¡Esta aplicación es para todos! Si deseas mejorarla, sigue estos pasos:  
1. Haz un fork del proyecto.  
2. Crea una rama para tu función o corrección:  
   ```bash  
   git checkout -b mi-nueva-funcionalidad  
   ```  
3. Realiza tus cambios y súbelos:  
   ```bash  
   git commit -m "Añadida nueva funcionalidad"  
   git push origin mi-nueva-funcionalidad  
   ```  
4. Crea un Pull Request desde GitHub.  

## Licencia 📄  
Este proyecto está bajo la Licencia MIT. Puedes consultar el archivo [LICENSE](LICENSE) para más detalles.  

## Agradecimientos 💖  
Gracias por utilizar esta aplicación. Espero que te ayude tanto como a mí en el camino hacia una vida más disciplinada y significativa.  
