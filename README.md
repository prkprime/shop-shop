## Shopping Application with smart suggestions

This website analyzes the products that already in user's cart and gives the suggestions for the products based on the rules created by FP-Growth algorithm on the previous ~4lakh transactions

Cloud link of database required is already there in the config.py file so that u don't have to create your own database for this.
(Don't keep such database or any other credentials lying in public repositories)

### Steps to run the app

clone the repo and go to root directory of project
```bash
git clone https://github.com/prkprime/shop-shop
cd shop-shop
```

create virtual environment, activate it and install all requirements
```bash
python3 -m venv venv/
source venv/bin/activate
pip3 install -r requirements.txt
```

Run the app in development mode
```
python3 -m primecart
```
