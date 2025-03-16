#!/bin/bash
echo "Uruchamianie kontenerów..."

# Usunięcie starych kontenerów (opcjonalne)
docker-compose down

# Budowanie i uruchamianie kontenerów
docker-compose up -d --build

echo "Oczekiwanie na uruchomienie baz danych..."
sleep 30

echo "Uruchamianie testów z main.py..."
source .venv/Scripts/activate
python main.py


echo "Testy zakończone!"
read -p "Naciśnij dowolny klawisz, aby zamknąć..."
