from subprocess import run 


def main():
    run(['black', 'pylisper'])
    run(['isort', 'pylisper'])
    run(['autoflake', '-i', '-r', '--ignore-init-module-imports', 'pylisper'])
    run(['flake8', 'pylisper'])
