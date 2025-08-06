#!/bin/bash

# Apache startup script for Investment Portfolio

echo "Starting Apache HTTP Server..."

# Test configuration
echo "Testing Apache configuration..."
httpd -t

if [ $? -ne 0 ]; then
    echo "ERROR: Apache configuration test failed!"
    exit 1
fi

echo "Apache configuration is valid."

# Start Apache in foreground
echo "Starting Apache..."
exec httpd -D FOREGROUND 