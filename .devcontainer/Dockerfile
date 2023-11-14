FROM quay.io/astronomer/astro-runtime:9.2.0


# install soda into a virtual environment
RUN python -m venv soda_venv && source soda_venv/bin/activate && \
    pip install --no-cache-dir soda-core-bigquery==3.0.45 &&\
    pip install --no-cache-dir soda-core-duckdb==3.0.45 &&\
    pip install --no-cache-dir soda-core-scientific==3.0.45 && deactivate