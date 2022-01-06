start:
	docker-compose up -d
	watchman-make -p 'app/**/*.py' -s 1 --run 'touch uwsgi-reload'
stop:
	docker-compose down