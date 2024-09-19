from setuptools import setup, find_packages


setup(
  include_package_data=True,
  name='swarm_rqa_test',
  version='0.1.0',
  description='SWARM_RQA_TEST',
  packages = find_packages(),
  install_requires = [
    'imbalanced-learn==0.12.3',
    'joblib==1.4.2',
    'matplotlib==3.9.1',
    'pandas==2.2.2',
    'pyyaml==6.0.1',
    'scikit-learn==1.4.0',
    'scipy==1.13.1',
    'tqdm==4.66',
    'xgboost==2.1.0',
    'yacs==0.1.8',
    'pywavelets==1.6.0'
  ],
  package_data={
    'my_package': ['configs/*']
  },
  
)