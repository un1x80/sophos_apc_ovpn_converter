#!/bin/bash

INFILE=$1
PASS=$2

# Check if input file has a .epc extension
if [[ "${INFILE##*.}" != "epc" ]]; then
    echo "Error: Please provide a .epc file"
    exit 1
fi

# Define output file with .apc extension
OUTFILE="${INFILE%.epc}.apc"

# Decrypt the file
if openssl enc -d -aes-256-cbc -in "$INFILE" -out "$OUTFILE" -pass pass:"$PASS"; then
    echo "Decryption successful: $OUTFILE"
else
    echo "Error: Decryption failed"
    exit 1
fi
