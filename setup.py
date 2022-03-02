from setuptools import setup

setup(
    name="gin",
    version="0.1.0",
    py_modules=['gin'],
    install_requires=[
        'Click',
        'click_completion',
        'requests',
        'gitpython'
    ],
    entry_points='''
        [console_scripts]
        gin=gin.commands:cli
    '''
)
