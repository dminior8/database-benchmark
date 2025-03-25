#!/bin/bash
echo "Starting containers..."

# Remove old containers (optional)
docker-compose down
# Build and start containers
docker-compose up -d --build

echo "Waiting for databases to start..."
sleep 20

echo "Installing dependencies..."
source .venv/Scripts/activate
pip install -r requirements.txt

echo "Running tests from main.py..."
# Wait until Cassandra is ready
until docker exec -it cassandra-test cqlsh -e "SELECT now() FROM system.local"; do
  echo "Cassandra is not up yet. Waiting..."
  sleep 5
done

# Load data
docker exec -i cassandra-test cqlsh -e "SOURCE '/docker-entrypoint-initdb.d/init.cql';"
echo "CassandraDB is running!"

python main.py

echo "Tests completed!"
read -p "Press any key to close..."