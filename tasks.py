from invoke import task

@task(default=True)
def server(ctx):
    """Run the Flask app."""
    ctx.run("python web.py", pty=True)
