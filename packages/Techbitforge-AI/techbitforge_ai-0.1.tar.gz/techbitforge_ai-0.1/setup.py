from setuptools import setup    


setup(
    name='Techbitforge_AI',
    version='0.1',
    packages=['API'],
    install_requires=[
        'groq',
        'requests',
        're',
        'typing',
        'shutil',
        'gradio_client',
        'random',
        'os'
    ],
)
