pkill -f uwsgi -9
rm -rf uwsgi.log
uwsgi --ini app.ini