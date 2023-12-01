# Stock Take Home Project

**Python 3.8 or higher is recommended**
**PostgreSQL 12 or higher is recommended**

## Instructions to run Locally

Initialize dev environment and install libraries

```shell
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt
```

Create .env file based in the .env.default with updated values and load them
```shell
cp .env.default .env
```

Take a look to previous file to ensure you have all required configurations.

Prepare your database and user to make connection and update the .env file previously mentioned.

Don't forget about the keys if you want to enable OTP.

Then execute migrations and create database (Ensure to do previous step)
```shell
python3 main.py db init
python3 main.py db migrate --message "Initial"
python3 main.py db upgrade
```

If you want to start from sample user without OTP, run:
```shell
python3 main.py seed_user
```

Add the configuration variables to Alpha Vantage and run:
```shell
python3 main.py symbols_alpha
```

If you want to run tests, please type the following command
```shell
python3 main.py test
```

Finally run the project as follow:
```shell
python3 main.py run
```

Run linter/Formatter
```shell
python3 -m black .
```

This project uses coode best practices, you may find them in `pyproject.toml`.

## Instructions with Docker

To run locally do the following:
(Ensure to have the .env file updated)

```shell
#Build
docker build -t angyay0/stock-take-home .

#run
docker run --env-file=.env  -d -p 81:5001 angyay0/stock-take-home
```

## K8s 
This project contains the image building, k8s files is left.

## About CI/CD
This project includes deployment validations, workflow and more tooling using Github actions, you can fin them inside `.github/workflow/` for the current pipeline.

The project is configured with environment secrets.