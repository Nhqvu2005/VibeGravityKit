from setuptools import setup, find_packages

setup(
    name="VibeGravityKit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "click",  # For CLI
    ],
    entry_points={
        "console_scripts": [
            "vibe=vibe_cli:main",
        ],
    },
    author="Vibe Coding Team",
    description="The AI-Native Software House in a Box",
)
