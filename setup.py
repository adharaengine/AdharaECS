from setuptools import setup, find_packages
setup(
    name = "AdharaECS",
    version = "0.01",
    description = "A simple Entity Component System",
    author = "James Lee Vann",
    py_modules = ['adhara_ecs'],
    install_requires = ['adhara_db']
)
