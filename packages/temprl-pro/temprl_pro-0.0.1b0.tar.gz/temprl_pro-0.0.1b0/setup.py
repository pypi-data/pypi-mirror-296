# setup.py

from setuptools import setup, find_packages

readMe = """
# Temprl Pro 📦

Welcome to **Temprl Pro**! This package is designed to help you extract and process data efficiently using various strategies, including LLM-based extraction. Below you'll find detailed information on how to get started, install the package, and use its features.

## Features ✨

- **Data Extraction**: Extract data from various sources using different strategies.
- **API Integration**: Fetch data from APIs with ease.
- **Customizable**: Configure and customize extraction strategies to fit your needs.
- **Error Handling**: Robust error handling to ensure smooth operation.

## Installation 🛠️

To install the package, simply run:
```bash
pip install temprl_pro
```

## Documentation 📚

For detailed documentation and usage examples, please refer to [docs.temprl.pro](https://docs.temprl.pro)

"""

setup(
    name='temprl_pro',  # Replace with your package name
    version='0.0.1b',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'html2text',
    ],
    entry_points={
        'console_scripts': [
            'your_command=your_module:main_function',  # Replace with your command and function
        ],
    },
    long_description=readMe,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Sri Santh M',
    author_email='srisanth234567@gmail.com',
    url='https://github.com/Pr0fe5s0r',
)
