from setuptools import setup, find_packages

setup(
    name="testy-test-python-framework",  
    version="0.1.0",  
    description="A Jest-like Python testing framework",  
    author="Vagif Aghayev",
    author_email="vagifaghayev270298@gmail.com",  
    url="https://github.com/GaoFan98/testy",
    packages=find_packages(),  
    include_package_data=True,  
    entry_points={  
        "console_scripts": [
            "testy=testy.cli:run_cli",  
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
