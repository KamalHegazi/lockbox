#!/bin/sh

# Make the lockbox.py script executable
chmod 777 lockbox.py

# Create the directory for lockbox
mkdir -p /usr/share/lockbox

# Copy the lockbox.py script to the new directory
cp lockbox.py /usr/share/lockbox/lockbox.py

# Create the shell script to execute lockbox.py
echo '#!/bin/sh\nexec python3 /usr/share/lockbox/lockbox.py "$@"' > /usr/bin/lockbox

# Make the new scripts executable
chmod +x /usr/bin/lockbox
chmod +x /usr/share/lockbox/lockbox.py

echo "[ ! ] Done."
