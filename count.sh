find . -maxdepth 1 -type f -name "*.py" ! -name "test.py" -exec wc -l {} + | sort -n
