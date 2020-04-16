import os
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
def start_docker(ctx, image="digdir/fulltext-search:latest"):
    print("starting docker network..")
    host_dir = os.getcwd()
    start_compose = "TEST_IMAGE={0} MOCK_DIR={1} docker-compose -f  tests/docker-compose.contract.yml up -d".format(image,host_dir)
    ctx.run(start_compose)

@task
def start_docker_attach(ctx, image="digdir/fulltext-search:latest"):
    print("starting docker network..")
    host_dir = os.getcwd()
    start_compose = "TEST_IMAGE={0} MOCK_DIR={1} docker-compose -f  tests/docker-compose.contract.yml up".format(image,host_dir)
    ctx.run(start_compose)

@task
def start_docker_local(ctx, image="digdir/fulltext-search:latest"):
    print("starting docker network..")
    host_dir = os.getcwd()
    start_compose = "TEST_IMAGE={0} MOCK_DIR={1} docker-compose up".format(image,host_dir)
    ctx.run(start_compose)


@task
def stop_docker(ctx,clean=False,all=False):
    print("stopping docker network..")
    kill = "docker-compose -f tests/docker-compose.contract.yml kill"
    docker_clean = "docker system prune"
    ctx.run(kill)
    if clean:
        if all:
            ctx.run(f"{docker_clean} -a")
        else:
            ctx.run(docker_clean)



@task
def contract_test(ctx, image="digdir/fulltext-search:latest", compose=False, build=False):
    print("______CONTRACT TESTS_______")
    if build:
        build_image(ctx, image)
    if compose:
        start_docker(ctx, image)
    pipenv_run_test = "pipenv run pytest -m contract"
    ctx.run(pipenv_run_test)
