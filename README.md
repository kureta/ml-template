# Notes to self

- To be able to build the docker image you have to have the following in your `/etc/docker/daemon.json` file:

  ```json
  {
    "runtimes": {
      "nvidia": {
        "path": "nvidia-container-runtime",
        "runtimeArgs": []
      }
    },
    "features": {
      "buildkit": true
    }
  }
  ```

  First entry is for the `nvidia` runtime, second is to enable the `buildkit` features.
  Then run this command to make buildkit the default builder.

  ```
  docker buildx install
  ```

  I am stil trying to wrap my head around docker, so feel free to correct me or suggest something simpler.

- Look at the `Makefile` to see available commands.
- Do not forget to add any commands you use into the `Makefile`.
- Image versions are tracked in the `.env` file
- Python package version is tracked in the `pyproject.toml` file

## TODO

Adding pre-commit and nbstripout. There is some uglyness. I had to create an external venv just to run these during development.
It is unclear how development will be carried out. I plan on using `make jupyter` and pycharm remote docker interpreter.
A development image/setting is necessary mostly for linting and things like that (pre-commit hooks and nbstripout filter/smudge).
I can also setup a fullfledged astronvim installation but seems unnecessary. Even so, commiting to git from within docker seems wrong.

Until (if ever) I find a better/cleaner way, it goes like this:

- run `make init` to create a development venv and install pre-commit and nbstripout
- source this venv on host machine, not inside docker
- this venv does not have any project dependencies, only for pre-commit, nbstripout, and dvc
- the actual project environment is fully inside docker

Decided to use dvc only for data versioning

## Important!

minio s3 instance inside the mlfow stack does not have the required bucket at start.

```
mc config host add myminio http://s3:9000 admin 314159265
mc mb myminio/mlflow
```

make this into an entrypoint or something that will run at start and create the bucket if it doesn't already exist.

# Some list of items to do

- [ ] add `pre-commit` configuration for:
  - [ ] `.py`
  - [ ] `.ipynb`
  - [ ] `Dockerfile`
  - [ ] `docker-compose.yml`
  - [ ] `Makefile`
  - [ ] `pyproject.toml`
- [ ] add nbstripout to remove output from notebooks
- [ ] configure `dvc` for data versioning
- [ ] configure `mlflow` for experiment tracking
- [ ] configure automated testing
- [ ] use `loguru` for logging
- [ ] look at `pydantic 2` and `hypothesis` integration
- [ ] add `pytorch-lightning`
- [ ] add `optuna`
- [ ] add base `jupyterlab` configuration
