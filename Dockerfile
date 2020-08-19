FROM jupyter/base-notebook

LABEL version=".1"
LABEL description="Jupyter notebook with support for interactive widgets"

# Set the working directory
WORKDIR /home/jovyan/
COPY . /home/jovyan/

RUN conda install --quiet --yes -c conda-forge\
    'numpy' \
    'scipy' \
    'pandas' \
    'matplotlib' \
    'jupyter' \
    'bqplot' \
    'voila' && \
    jupyter serverextension enable voila --sys-prefix && \
    rm -rf work

# Expose default HTTP port
EXPOSE 8866

# we have to use the root user so that we can use task storage volume on ECS
# See: https://github.com/aws/containers-roadmap/issues/938
USER root

# start voila dahboard
CMD ["voila", "coviz/notebooks/Dashboard.ipynb", "--VoilaConfiguration.theme='dark'", "--MappingKernelManager.cull_interval=60", "--MappingKernelManager.cull_idle_timeout=300", "--no-browser"]

# EXPOSE 8888
# start jupyter notebook
# CMD jupyter notebook --no-browser --port 8888 --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.disable_check_xsrf=True --allow-root

# docker command
# docker run -p 8866:8866 -v "$PWD":/home/jovyan qr:v2
