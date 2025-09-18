# Heroku-optimized Dockerfile for AI Security Lab
FROM jupyter/scipy-notebook:python-3.9

# Switch to root for installations
USER root

# Install essential packages only (keep it lightweight)
RUN pip install --no-cache-dir \
    torch==2.0.0 \
    torchvision==0.15.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Copy lab materials
COPY lab_notebook.ipynb /home/jovyan/work/
COPY utils.py /home/jovyan/work/
COPY README.md /home/jovyan/work/

# Set permissions
RUN chown -R jovyan:users /home/jovyan/work/

# Switch back to jovyan
USER jovyan

# Set working directory
WORKDIR /home/jovyan/work

# Use Heroku's PORT environment variable
ENV PORT=8888
EXPOSE $PORT

# Heroku-compatible startup
CMD jupyter lab --ip=0.0.0.0 --port=$PORT --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*'
