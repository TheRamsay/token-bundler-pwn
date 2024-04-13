pip3.9 install -r requirements.txt
python3.9 ./token_bundler/manage.py makemigrations --noinput
python3.9 ./token_bundler/manage.py migrate --noinput