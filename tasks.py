import time
from invoke import task

pipenv_install = "pipenv install --dev"

@task
def unit_test(ctx, install=False):
    pipenv_run_test = "pipenv run pytest -m unit"
    if install:
        ctx.run(pipenv_install)
    ctx.run(pipenv_run_test)


@task
def build_image(ctx, tags="digdir/fulltext-search:latest", staging=False):
    if staging:
        ctx.run(pipenv_install)
    gen_requirements = "pipenv lock -r >requirements.txt"
    ctx.run(gen_requirements)
    tag = ""
    for t in tags.split(","):
        tag = tag + ' -t ' + t

    print("building image with tag " + tag)
    build_cmd = "docker build . " + tag
    ctx.run(build_cmd)


@task
def start_docker(ctx):
    print("starting docker network..")
    start_compose = "docker-compose -f tests/docker-compose.contract.yml up -d"
    ctx.run(start_compose)
    time.sleep(6)


@task
def stop_docker(ctx):
    print("stopping docker network..")
    down_and_clean = "docker-compose -f tests/docker-compose.contract.yml down --remove-orphans -v"
    ctx.run(down_and_clean)


@task
def contract_test(ctx, compose=False, build=False):
    print("______CONTRACT TESTS_______")
    if build:
        build_image(ctx)
    if compose:
        start_docker(ctx)
    pipenv_run_test = "pipenv run pytest -m contract"
    ctx.run(pipenv_run_test)
    if compose:
        stop_docker(ctx)
