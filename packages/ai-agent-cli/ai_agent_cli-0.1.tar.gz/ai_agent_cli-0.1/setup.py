from setuptools import setup, find_packages

setup(
    name='ai_agent_cli',
    version='0.1',
    description='AI agent for automatic backend server creation',
    author='Anand Ranjan',
    author_email='annadranjan789@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'argparse',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'create-backend=ai_agent_cli.cli:main',
        ],
    },
)

