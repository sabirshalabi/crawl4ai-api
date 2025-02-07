#!/usr/bin/env bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright and its dependencies
playwright install
playwright install-deps
