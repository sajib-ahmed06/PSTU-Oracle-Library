"""Apply the data-preserving circulation upgrade, without running setup/reset."""

from backend.database import ROOT, run_sql


def main():
    print(
        run_sql(
            f'@"{ROOT / "database" / "circulation_upgrade.sql"}"\n@"{ROOT / "database" / "circulation_audit_upgrade.sql"}"\n@"{ROOT / "database" / "reservations_upgrade.sql"}"\n@"{ROOT / "database" / "reservations_audit_upgrade.sql"}"\n@"{ROOT / "database" / "student_activation_upgrade.sql"}"'
        )
    )
    errors = run_sql("SELECT name||':'||line||':'||text FROM user_errors ORDER BY name,sequence;")
    if errors:
        raise RuntimeError(errors)
    print("Circulation upgrade completed; existing data preserved.")


if __name__ == "__main__":
    main()
