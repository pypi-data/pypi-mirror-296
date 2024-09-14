from distutils.core import setup

setup(name='amz_extractor',
      version='1.0.1',
      description='提取亚马逊详情页和评论信息',
      author='lonely',
      packages=['amz_extractor'],
      package_dir={'amz_extractor': 'amz_extractor'},
      install_requires=['dateparser>=1.1.4', 'pyquery>=1.4.3']
      )
