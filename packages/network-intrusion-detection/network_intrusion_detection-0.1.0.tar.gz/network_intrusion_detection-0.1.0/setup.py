from setuptools import setup, find_packages

setup(
    name='network_intrusion_detection',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tensorflow',  'numpy', 'pandas', 'scikit-learn',
      ],
    package_data={'network_intrusion_detection': ['cnn_lstm_unsw_finetuned.h5']},
    description='A Python package for CNN-LSTM model pre-trained on CICIDS2017 and finetuned on UNSW-NB15 for intrusion detection.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mamah Joy',
    author_email='joyceamymamah@gmail.com',
       classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

