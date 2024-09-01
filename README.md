# Data_App


The main goal of this data application is to begin with a set of structured data in CSV format and use both structured and unstructured techniques to extract valuable insights. This process involves not only analyzing the existing data but also generating synthetic data to enhance the dataset. By leveraging advanced data engineering methods, the application aims to facilitate knowledge mining, enabling deeper understanding and discovery from the data.



## Dependencies and Tech Stack

### Folder Structure:

```bash
root_directory/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_processing.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── db_models.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── neo4j_connection.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── graph_utils.py
│   │   └── aws_utils.py
│   ├── templates/
│   │   └── example_template.html
│   └── static/
│       └── styles.css
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_data_quality.py
│   └── test_integration.py
│
├── notebooks/
│   ├── data_analysis.ipynb
│   ├── graph_analysis.ipynb
│   └── model_training.ipynb
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
└── pyproject.toml

```


### 1. **LangChain Ecosystem**:
   - **`langchain`**: A framework for developing applications that use large language models (LLMs). It enables creating chains of processes for text handling, API interaction, and other language-based workflows.
   - **`langgraph`**: A tool that complements LangChain for creating and manipulating graphs for stateful apps with LLMs.
   - **`langchain_community`**: Extensions and community contributions to LangChain, providing additional modules and tools to enhance functionality.
   - **`langchain_groq`**: Optimization of LangChain for specific hardware, such as Groq, a type of AI accelerator.
   - **`langchain_experimental`**: New and experimental features of LangChain, which are still in the testing phase and may not be fully mature.
   - **`langsmith`**: For obserbaility of the LLM interactions as monitoring service

### 2. **Data Manipulation and Analysis**:
   - **`pandas`**: A fundamental library in Python for data manipulation and analysis. It provides efficient and easy-to-use data structures like DataFrames.
   - **`numpy`**: A library for scientific computing in Python, offering support for multidimensional arrays and high-level mathematical functions.

### 3. **Web Frameworks**:
   - **`streamlit`**: A framework for quickly creating interactive web applications in Python. Popular for building dashboards and data visualization applications.
   - **`fastapi`**: A modern, high-performance web framework for building APIs in Python. It is asynchronous and supports automatic API documentation generation.
   - **`uvicorn`**: A fast and lightweight ASGI server for Python, commonly used to run FastAPI applications.

### 4. **Graph and Database**:
   - **`neo4j`**: A highly optimized graph database used for modeling and storing data with complex relationships. It allows for advanced queries using Cypher, its query language.
   - **`yfiles-jupyter-graphs`**: A library for visualizing and analyzing graphs in Jupyter environments, facilitating the representation of data as graphs and networks.

### 5. **Configuration and Testing**:
   - **`toml`**: A simple and human-readable configuration file format, often used for storing project and application configurations.
   - **`pytest`**: A testing framework in Python for writing simple and scalable tests. It is extensible and supports plugins for various functionalities.

### 6. **Data Quality**:
   - **`great_expectations`**: A tool for validating, documenting, and ensuring data quality. It allows defining expectations about the data and running tests to verify its integrity and consistency.

### 7. **AWS Integration**:
   - **`boto3`**: Amazon Web Services (AWS) SDK for Python, which enables programmatic interaction with AWS services.
   - **`awswrangler`**: An extension of Pandas to facilitate direct access and manipulation of data from AWS, providing a more efficient way to work with services like S3, Athena, and Redshift.

### 8. **Containerization and Continuous Integration**:
   - **`Docker`**: A platform to develop, ship, and run applications inside lightweight containers. It enables consistent environments across multiple stages of development and deployment.
   - **`GitHub Actions`**: A CI/CD tool that allows you to automate, customize, and execute your software development workflows right in your GitHub repository. It's used for running tests, building applications, and deploying to various environments.

