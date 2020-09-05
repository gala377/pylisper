from subprocess import run 


def main():
    for dir in ['pylisper', 'tests']:
        print(f"Running for {dir}")
        run(['black', dir])
        run(['isort', dir])
        run(['autoflake', '-i', '-r', '--ignore-init-module-imports', dir])
        run(['flake8', dir])
