# joker-remastered
## Get your daily jokes

# Requirements
* Python 3.10
* Redis 7.2.3
* PostgreSQL 12.17
* MongoDB 7.0.0

# Install
## Local setup

### Clone
```bash
git clone https://github.com/GoGei/joker-remastered.git
```

### Add hosts
* Ubuntu: /etc/hosts
* Windows: c:\Windows\System32\Drivers\etc\hosts
* MacOS: /private/etc/hosts
```bash
127.0.0.1           joker-remastered.local 
127.0.0.1       api.joker-remastered.local 
127.0.0.1     admin.joker-remastered.local 
```

### Create DB
```postgresql
create user joker_remastered with encrypted password 'joker_remastered' superuser createdb;
create database joker_remastered with owner joker_remastered;
```

### Copy settings
```bash
cp configs/example.py configs/settings.py
```

### Setup env
```bash
cd joker-remastered/
python3.10 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
```