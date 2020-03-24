import time
from invoke import task


@task
def unit_test(ctx):
    pipenv_cmd = "pipenv install"
    pipenv_run_test = "pipenv run pytest -m unit"
    ctx.run(pipenv_cmd)
    ctx.run(pipenv_run_test)


@task
def build_image(ctx):
    print("building image as digdir/fulltext-search:latest")
    gen_requirements = "pipenv lock -r >requirements.txt"
    ctx.run(gen_requirements)
    build_cmd = "docker build . -t digdir/fulltext-search:latest --rm "
    ctx.run(build_cmd)


@task(pre=[build_image])
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


@task(pre=[start_docker], post=[stop_docker])
def contract_test(ctx):
    print("______CONTRACT TESTS_______")
    pipenv_cmd = "pipenv install"
    pipenv_run_test = "pipenv run pytest -m contract"
    ctx.run(pipenv_cmd)
    ctx.run(pipenv_run_test)

@task
def no_setup_contract_test(ctx):
    ctx.run("pytest -m contract")
