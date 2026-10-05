"""Create reminder delivery tracking without changing existing library data."""

from backend.database import ROOT, run_sql


def main():
    run_sql(f'@"{ROOT / "database" / "reminders_upgrade.sql"}"')
    print("Reminder delivery tracking is ready. No messages were sent.")


if __name__ == "__main__":
    main()
