<div align="center">
    <h1>DApp API with FastAPI</h1>
    <h3>㊢ Fully customizable DApp API with FastAPI which includes cloud database (MongoDB), user registration, JWT authtentication, e-Mail verification, and Web3 user digital wallet verification integrations.</h3>
</div>

<br>

<div align="center">
	| 
    <a href="https://woosal.net">blog</a> | 
    <a href="https://gist.github.com/woosal1337">gist</a> | 
    <a href="https://github.com/woosal1337/dotfiles">dotfiles</a> |  
    <a href="https://www.reddit.com/user/woosal1337">reddit</a> | 
    <a href="https://keybase.io/woosal">keybase</a> | 
    <a href="https://t.me/woosal1337">telegram</a> |
    <a href="https://twitter.com/woosal1337">twitter</a> | 
    <a href="https://www.instagram.com/woosal1337/">instagram</a> |
    <a href="https://open.spotify.com/user/3pd70lv4jpyjbjxjfgysx3pzl">spotify</a> |
    <a href="https://discordapp.com/users/901937888688758785">discord</a> |
    <a href="mailto:me@woosal.net">mail</a> |
</div>

# Contents
- [1. Introduction](#introduction)
- [2. Features](#Features)
- [3. Setup](#Setup)
- [4. Usage](#Usage)
- [5. License](#License)

# Introduction
This project has been done to serve as a blueprint / template for the Web3 DApp API 
development. By simply cloning and creating a free MongoDB accounts, you can easily
start modifying and integrating the database to your applications.

# Features
- [x] User registration through digital wallet
- [x] User login through digital wallet
- [x] User profile update
- [x] User profile delete
- [x] User profile get
- [x] User profiles get all
- [x] User profile get by digital wallet address (public key)
- [x] User profile get by email
- [x] JWT authentication / verification
- [x] Signature (Signing) registration
- [x] Custom BaseModels by [pydantic](https://pydantic-docs.helpmanual.io/)
- [x] JWT only admin/registered user access check
- [x] `get`/`set` e-mail accounts in the database
- [x] Custom `pymongo` database class wrapper
- [x] Full `logging` support with built-in `logging` and saving the logs to custom files
- [x] `pymongo` exception handlers
- [x] Custom `FastAPI` middleware
- [x] Function docs and parameters explanation and use cases
- [x] `x` days (custom time) JWT token expiration checks
- [x] All `SECRET`s are stored in the `.env` file for security and accessibility
- [x] Ready to deploy and use on [Heroku](https://heroku.com) and [Vercel]
  (https://vercel.com) with `Procfile` and `requirements.txt`
- [ ] All endpoints and functions tests ([fastapi/issues/5675](https://github.com/tiangolo/fastapi/issues/5675))

# Setup
```zsh
# Clone the repository
$ git clone https://github.com/woosal1337/dapp-api-with-fastapi.git
$ cd dapp-api-with-fastapi/

$ python3 -m venv venv # or conda create -n "dapp-api-with-fastapi" python=3.10
$ source venv/bin/activate # or conda activate "dapp-api-with-fastapi"
$ pip install -r requirements.txt
```

# Usage

### 1. Create a free MongoDB account and database then copy the connection link to .env file
- [MongoDB](https://www.mongodb.com/)
- [Tutorial](https://www.mongodb.com/basics/create-database)

```zsh
$ source venv/bin/activate # or conda activate "dapp-api-with-fastapi"
$ uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000} --reload
```

# Deploy
- [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
```zsh
$ heroku login
$ heroku create
$ git push heroku main
$ heroku open
```

# License
- [MIT](LICENSE)