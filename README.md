# Translation from EN-SP and SP-EN with a Helsinki-NLP/opus-mt-en-es model

Project developed in Poetry-FastAPI-Python as the objective of the pre-professional practices carried out in www.jrtec.io

## About this project

This project consists of creating APIS through the FastAPI framework that allow a translation from English to Spanish and from Spanish to English given an input text and resulting in an output text. In addition, the APIS will have authentication, therefore, only authorized users can make use of them.

The project currently does not work with a database model nor is it containerized.

## Chosen Models

- Helsinki-NLP/opus-mt-en-es

## Clone de project

```sh
git clone https://github.com/AlexanderG1999/Translator-En-Es.git
```

## Activate virtual environment

```sh
poetry shell
```

## Install all dependencies

```sh
poetry install
```

## Project operation
<i><h3 align="left">Create environment variables</h3></i>
In the path where the <b>__init__.py</b> file is located, it is necessary to create an .env file that will store the respective passwords for each user who is authorized to use the APIS. In addition, a secret key is stored that allows the creation of a session token.

<i>Note: The user's password must be hashed with bdcrypt. You can use this page to encrypt: https://bcrypt-generator.com/</i>

image.png

Then, it is necessary to create a <b>.gitignore</b> file where the <b>.env</b> file will be placed as an exception.
To access the environment variables, through the python os and dotenv modules, it is done as follows.

```sh
# Load environment variables
dotenv.load_dotenv()

# Access the content of an environment variable
os.getenv("PASSWOR_USER1")
```

## Run the server
You must be located in the path where the <b>__init__.py</b> is located and run this command.

```sh
uvicorn __init__:app --reload
```

If all is well, you can access the following link: http://127.0.0.1:8000/
image.png

If you want to test the APIS, enter the following link: http://127.0.0.1:8000/docs
image.png

## Authorization and use of APIS
To make use of the APIS it is necessary to authenticate using the username and password registered in the project.

image.png
image.png

To use the APIS after being authenticated.
- Select the translation to perform.
- It is placed in the "try it out" option.
- Enter the text to be translated and click on execute.
- The results are shown at the bottom.

image.png
image.png

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the terms of the **[MIT license](LICENSE)**