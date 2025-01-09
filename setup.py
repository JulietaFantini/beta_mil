from setuptools import setup, find_packages

setup(
    name="Generador de Imágenes con IA",
    version="0.1.0",
    description="Una aplicación de Streamlit para generar descripciones detalladas para IA generadoras de imágenes.",
    author="Julieta Fantini",
    author_email="tu-email@dominio.com",  # Cambiar por tu email
    packages=find_packages(),
    install_requires=[
        "streamlit==1.15.2",
        "altair==4.2.0",
        "pandas",
        "numpy",
        "requests",
        "watchdog",
    ],
    entry_points={
        "console_scripts": [
            "run-app=app:main",
        ],
    },
)
