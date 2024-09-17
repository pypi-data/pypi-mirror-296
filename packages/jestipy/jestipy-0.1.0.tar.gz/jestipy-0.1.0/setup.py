from setuptools import setup, find_packages

setup(
    name="jestipy",  
    version="0.1.0",  
    description="A Jest-like testing framework for Python",  
    author="Vagif Aghayev",
    author_email="vagifaghayev270298@gmail.com",  
    url="https://github.com/GaoFan98/jestipy",
    packages=find_packages(),  
    include_package_data=True,  
    entry_points={  
        "console_scripts": [
            "jestipy=jestipy.cli:run_cli",  
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
    install_requires=[  
    ],
)
