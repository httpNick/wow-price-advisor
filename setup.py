from setuptools import setup, find_packages

setup(
    name='wow_price_advisor',
    version='0.1',
    py_modules=["main"],
    packages=find_packages(),
    install_requires=[
        'openai>=1.46.1',
        'pandas>=2.2.3',
        'requests>=2.32.3',
        'scipy>=1.14.1',
        'numpy>=2.1.2',
        'beautifulsoup4>=4.12.3',
        'python-dotenv>=1.0.0',
    ],
    entry_points={
      'console_scripts': [
          'wowpriceadvise=wow_price_advisor.cli:main',
      ],
    },
)