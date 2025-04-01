# langchain_postgres doesn't allows include the psycopg3-binary package
pip uninstall -y psycopg
pip install "psycopg[binary]"
