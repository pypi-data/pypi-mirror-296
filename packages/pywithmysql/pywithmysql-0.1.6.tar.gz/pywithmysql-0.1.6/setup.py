from setuptools import setup, find_packages
from setuptools.command.install import install
import os


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        self.create_config_file()

    def create_config_file(self):
        # Отримуємо поточну робочу директорію
        config_path = os.path.join(os.getcwd(), 'config')

        if not os.path.exists(config_path):
            print(f"Creating config file at {config_path}")
            with open(config_path, 'w') as f:
                f.write("DB_HOST=your_host\n")
                f.write("DB_PORT=your_port\n")
                f.write("DB_USER=your_user\n")
                f.write("DB_PASSWORD=your_password\n")
                f.write("DB_NAME=your_db_name\n")
        else:
            print(f"Config file already exists at {config_path}")


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pywithmysql',
    version='0.1.6',
    description='The library to work with MySQL databases for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hardusss/pywithmysql',
    author='DanikBlatota777',
    author_email='danylo29bro@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'python-dotenv'
    ],
    cmdclass={
        "install": PostInstallCommand
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
