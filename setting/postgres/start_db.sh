docker pull postgres
sudo docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=ssd_project -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres
pg_restore -h 127.0.0.1  -p 5432 -U postgres -1 admissionBD_backup 
