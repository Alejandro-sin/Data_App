#!/bin/bash

# Create GitHub workflows
mkdir -p .github/workflows
touch .github/workflows/ci-cd.yml

# Create root level files
touch .dockerignore
touch .gitignore
touch Dockerfile
touch README.md
touch requirements.txt
touch pyproject.toml

# Create app directory and subdirectories
mkdir -p app
    touch app/__init__.py
    touch app/main.py
    touch app/config.py

    mkdir -p app/routes
        touch app/routes/__init__.py
        touch app/routes/api.py

    mkdir -p app/services
        touch app/services/__init__.py
        touch app/services/data_processing.py

    mkdir -p app/models
        touch app/models/__init__.py
        touch app/models/db_models.py

    mkdir -p app/db
        touch app/db/__init__.py
        touch app/db/neo4j_connection.py

    mkdir -p app/utils
        touch app/utils/__init__.py
        touch app/utils/graph_utils.py
        touch app/utils/aws_utils.py

    mkdir -p app/templates
        touch app/templates/example_template.html

    mkdir -p app/static
        touch app/static/styles.css

# Create tests directory
mkdir -p tests
    touch tests/__init__.py
    touch tests/test_api.py
    touch tests/test_data_quality.py
    touch tests/test_integration.py

# Create notebooks directory
mkdir -p notebooks
    touch notebooks/data_analysis.ipynb
    touch notebooks/graph_analysis.ipynb
    touch notebooks/model_training.ipynb

echo "Project structure created successfully in the current directory."



# Creamos python ambiente
#python3 -m venv env 
#source env/bin/activate
#chmod +x setup_project.sh
