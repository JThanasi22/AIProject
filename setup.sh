#!/bin/bash

echo "=========================================="
echo "Setup i Asistentit të Kodit Penal"
echo "=========================================="
echo ""

echo "1. Krijimi i mjedisit virtual..."
python3 -m venv venv

echo "2. Aktivizimi i mjedisit virtual..."
source venv/bin/activate

echo "3. Instalimi i varësive..."
pip install --upgrade pip
pip install -r requirements.txt

echo "4. Krijimi i strukturës së dosjeve..."
mkdir -p data templates static/css static/js

echo ""
echo "=========================================="
echo "Setup i përfunduar!"
echo "=========================================="
echo ""
echo "Hapat e ardhshëm:"
echo "1. Vendosni tekstin e Kodit Penal në data/criminal_code_raw.txt"
echo "2. Ekzekutoni: python download_code.py"
echo "3. Ekzekutoni: python create_index.py"
echo "4. Ekzekutoni: python app.py"
echo ""
echo "Për aktivizim të mjedisit virtual në të ardhmen:"
echo "source venv/bin/activate"
