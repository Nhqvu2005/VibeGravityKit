from setuptools import setup, find_packages

setup(
    name="VibeGravityKit",
    version="2.8.0",
    packages=["VibeGravityKit"],
    include_package_data=True,
    install_requires=[
        "requests",
        "beautifulsoup4",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "vibe=VibeGravityKit.cli:main",
            "vibegravity=VibeGravityKit.cli:main",
        ],
    },
    author="Vibe Coding Team",
    description="The AI-Native Software House in a Box",
)
