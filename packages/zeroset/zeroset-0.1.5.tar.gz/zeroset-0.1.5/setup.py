import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name="zeroset",
        version="0.1.5",
        author="Bomm Kim",
        author_email="springnode@gmail.com",
        description="Useful collection of features.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/springkim/zeroset",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=[
            'natsort>=8.0.0',
            'Pillow>=10.0.0',
            'opencv-python',
            'screeninfo>=0.8.0',
            'tabulate>=0.9.0',
            'pytz',
            'selenium>=4.0.0',
            'webdriver-manager>=4.0.0',
            'screeninfo',
            'gif',
            'chromedriver_autoinstaller',
            'image_similarity_measures',
            'pyfftw',
            'imagehash',
        ],
)
