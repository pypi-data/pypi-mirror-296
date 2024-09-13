import click
import subprocess


@click.command()
def test1():
    subprocess.run(["ls"])

@click.command()
def start():
    """Start your vm"""
    subprocess.run(["gcloud", "compute", "instances", "start", "da-bootcamp"])


@click.command()
def stop():
    """Stop your vm"""
    subprocess.run(["gcloud", "compute", "instances", "stop", "da-bootcamp"])


@click.command()
def connect():
    """Connect to your vm"""
    subprocess.run(
        [
            "code",
            "--folder-uri",
            # eg. code --folder-uri vscode-remote://ssh-remote+brunolajoie@35.240.107.210/home/brunolajoie/
            "vscode-remote://ssh-remote+iza@34.32.47.149/home/vianaxabreu",
        ]
    )
