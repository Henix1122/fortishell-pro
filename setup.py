from setuptools import setup, find_packages

setup(
    name="fortishell-pro",
    version="1.0.0",
    description="Advanced modular cybersecurity toolkit (CLI + GUI)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="FortiShell Pro Team",
    author_email="michaelboadiasareot@gmail.com, michaelboadiasareot@outlook.com",
    url="https://github.com/Henix1122/fortishell-pro",
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    install_requires=[
        "rich>=13.0.0",
        "requests>=2.25.0",
        "urllib3>=1.26.0",
        "Pillow>=8.0.0",
        "cryptography>=3.4.0",
        "dnspython>=2.0.0",
        "python-whois>=0.7.3",
        "validators>=0.20.0",
        "watchdog>=2.1.0",
        "psutil>=5.8.0",
        "zxcvbn>=4.4.28",
        "loguru>=0.5.3",
        "jsonschema>=3.2.0"
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black",
            "mypy"
        ],
        "gui": [
            "PyQt5>=5.15.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "fortishell=main:main",
            "fortishell-gui=gui.launcher:launch_gui"
        ]
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "assets/*", "config/*"]
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Natural Language :: English"
    ],
    keywords="cybersecurity cli gui modular toolkit",
    project_urls={
        "Documentation": "https://github.com/Henix1122/fortishell-pro/wiki",
        "Source": "https://github.com/Henix1122/fortishell-pro",
        "Tracker": "https://github.com/Henix1122/fortishell-pro/issues"
    },
    zip_safe=False,
)
