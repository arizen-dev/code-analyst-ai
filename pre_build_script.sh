#!/bin/bash

# This script runs before the main application starts.
# It prepares the environment for Chainlit.

# 1. Create the .files directory that Chainlit needs for caching.
mkdir -p /app/.files

# 2. Give full read, write, and execute permissions to all users for this directory.
# This ensures the application user has the necessary access.
chmod -R 777 /app/.files