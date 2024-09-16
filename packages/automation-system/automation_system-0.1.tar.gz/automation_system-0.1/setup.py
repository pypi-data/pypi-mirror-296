from setuptools import setup, find_packages
import io

setup(
    name="automation-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'gspread',
        'oauth2client',
        'selenium',
        'webdriver_manager',
        'PyQt5',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'keyword_search=keyword_search:main',
            'seo=seo:main',
            'tao=tao:main',
            'percenty=percenty:main',
            'heyseller=heyseller:main',
            'gui=main:main'
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="An automation system for e-commerce product management",
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="http://github.com/yourusername/automation-system",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)