#!/bin/bash
echo "=========================================="
echo "       DDOS ATTACK TOOL TERMUX"
echo "=========================================="
echo "Note: Hanya untuk tujuan edukasi!"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python tidak terinstall! Installing..."
    pkg install python -y
fi

# Run the tool
python main.py
