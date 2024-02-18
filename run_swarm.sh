export $(cat .env) > /dev/null 2>&1;

# Run the swarm
docker stack deploy -c docker-compose.prod.yml comp0022