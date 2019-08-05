service supervisor start
service nginx start
service mysql start

cd /root/project/YongDan
git fetch 
git merge origin/master

cd project
python3 manage.py migrate --settings=project.settings_prod
python3 manage.py collectstatic --settings=project.settings_prod


supervisorctl restart project
service nginx restart
