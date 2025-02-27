   #!/bin/bash

   # Vérifier le style de code avec flake8
   python3 -m flake8
   flake8 --format=html --htmldir=flake8_report