from setuptools import setup

setup(
    name='gmlutil-ml-models',
    version='2.0.4',    
    description='General Machine Learning Utility Package for ML Model Training & Testing',
    url='https://github.com/Phillip1982/gmlutil_ml_models',
    author='Phillip Kim',
    author_email='phillip.kim@ejgallo.com',
    license='BSD 2-clause', ## Change this
    packages=['gmlutil_ml_models'],
    install_requires=[ # package>=0.2,<0.3
		'numpy==1.26.4',
		'pandas>2.1.0,<=2.2.2',
        'imbalanced-learn>=0.8.0',
        'kmodes>=0.11.0',
        'packaging>=21.3',
        'plotly>=5.5.0',
        'scikit-learn>=1.3.2', # 0.24.0,
        'scipy>=1.5.4',
        'seaborn>=0.11.2',
        'xgboost>=1.7.3'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
		'Operating System :: MacOS',
		'Operating System :: Microsoft :: Windows :: Windows XP',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
)
