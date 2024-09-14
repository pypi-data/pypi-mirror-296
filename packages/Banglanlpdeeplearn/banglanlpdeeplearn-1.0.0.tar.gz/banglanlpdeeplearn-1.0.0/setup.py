from setuptools import setup, find_packages

setup(
    name='Banglanlpdeeplearn',
    version='1.0.0',
    description='A package for Bangla text sentiment analysis using deep learning models.',
    author='Alamgir kabir',
    author_email='alomgirkabir720@gmail.com',
    url='https://github.com/yourusername/bangla_text_sentiment',  # Replace with your GitHub repository URL
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0',
        'scikit-learn',
        'pandas',
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
