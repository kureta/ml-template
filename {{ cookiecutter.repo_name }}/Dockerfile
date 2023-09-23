# base cuda image
FROM {{ cookiecutter.registry_name }}/ml-base:0.1.0

# install system dependencies
# If you need to install system dependencies, uncomment the following lines
# and add your dependencies
# ===========================
# USER root
# RUN --mount=type=cache,target=/var/cache/apt \
#   mkdir -p /var/cache/apt/lists/partial && \
#   apt-get update && apt-get install -y --no-install-recommends \
#   libsndfile1=1.0.28-7ubuntu0.1 \
#   llvm=1:10.0-50~exp1 \
#   && \
#   rm -rf /var/lib/apt/lists/
# ===========================

# setup user
WORKDIR $HOME/app
USER $USER
# ===========================

# copy python dependencies
COPY --chown=$USER:$GROUP ./pyproject.toml ./pyproject.toml
# install dependencies
RUN --mount=type=cache,target=$HOME/.cache/pip,uid=$UID,gid=$GID \
  pip install -e .
# ===========================

# copy project files
COPY --chown=$USER:$GROUP . .

# expose jupyter lab port
EXPOSE 8888

# default command
CMD [ "bash" ] 
