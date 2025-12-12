import click
from jobbot.core import run_bot

@click.command()
@click.option('--role', prompt='Job role', help='Example: python developer')
@click.option('--location', prompt='Location (or "all")', help='Example: bangalore')
@click.option('--salary', prompt='Salary range (LPA)', help='Example: 3-6')
@click.option('--experience', prompt='Experience (years)', help='Example: 0-2')
@click.option('--jobtype', prompt='Remote / Hybrid / Onsite / All')
@click.option('--alert', prompt='Alert method (email / whatsapp / both)')
def cli(role, location, salary, experience, jobtype, alert):
    """Universal JobBot - Find jobs for ANY role"""

    print("\n🔍 Running JobBot...\n")

    run_bot(
        job_role=role,
        location=location,
        salary_range=salary,
        exp_range=experience,
        job_type=jobtype,
        alert_method=alert
    )

    print("\n✅ Done!\n")

if __name__ == "__main__":
    cli()
