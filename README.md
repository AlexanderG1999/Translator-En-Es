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

<img width="513" alt="image1" src="https://user-images.githubusercontent.com/95202925/226965036-4ee02bd8-63e6-4074-915c-c6c5e53f1a09.png">


<i>Note: The user's password must be hashed with bdcrypt. You can use this page to encrypt: https://bcrypt-generator.com/</i>

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

<img width="960" alt="image5" src="https://user-images.githubusercontent.com/95202925/226964059-c5b7ccb5-3ea4-4ec3-ab71-781827886ce6.png">

If you want to test the APIS, enter the following link: http://127.0.0.1:8000/docs

<img width="959" alt="image4" src="https://user-images.githubusercontent.com/95202925/226963766-9d035c07-2caf-45d6-987f-5eb4db966786.png">

## Authorization and use of APIS
To make use of the APIS it is necessary to authenticate using the username and password registered in the project.

<img width="488" alt="image2" src="https://user-images.githubusercontent.com/95202925/226963041-ac280036-6034-49f3-9343-ed219d1f3d4c.png">

<img width="488" alt="image3" src="https://user-images.githubusercontent.com/95202925/226963561-3ea64c04-b198-4df3-a7c2-2167bf5a2848.png">

To use the APIS after being authenticated.
- Select the translation to perform.
- It is placed in the "try it out" option.
- Enter the text to be translated and click on execute.
- The results are shown at the bottom.


<img width="926" alt="image6" src="https://user-images.githubusercontent.com/95202925/226964231-ec73cbb0-2836-4ec7-951c-b31587125041.png">

<img width="917" alt="image7" src="https://user-images.githubusercontent.com/95202925/226964330-f917879e-f9af-4be6-af98-702fee6337a1.png">

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the terms of the **[MIT license](LICENSE)**