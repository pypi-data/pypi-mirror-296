from setuptools import setup, find_packages

setup(
    name='asistan_ai',  # Paketinin ismi
    version='1.1.0',  # Paketinin versiyonu
    packages=find_packages(),
    install_requires=['requests'],  # Bağımlılıklarını buraya ekle
    description='A Python client for Asistan AI model',
    author='Keremcem Kaysi',  # Adını ekleyebilirsin
    author_email='kader.61ts@icloud.com',  # İletişim bilgilerini ekleyebilirsin
    url='https://github.com/Keremcm/Asistan-AI',  # Projeyle ilgili GitHub ya da web sitesi linki
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python versiyonunu belirtebilirsin
)
