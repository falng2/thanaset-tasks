import importlib.util
from pathlib import Path

from sqlalchemy import inspect

from app.db.models import Base
from app.db.session import engine


def load_migration_module():
    migration_path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "db"
        / "migrations"
        / "001_init.py"
    )
    spec = importlib.util.spec_from_file_location("migration_001_init", migration_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_T_01_database_schema_and_migration():
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)

    assert inspector.has_table("slots")
    assert inspector.has_table("bookings")
    assert inspector.has_table("audit_logs")

    slots_columns = {column["name"] for column in inspector.get_columns("slots")}
    assert {"slot_date", "start_time", "package_code", "capacity", "remaining", "created_at"}.issubset(slots_columns)

    booking_columns = {column["name"] for column in inspector.get_columns("bookings")}
    assert {"hn", "slot_id", "booking_date", "queue_no", "status", "created_at"}.issubset(booking_columns)
    assert "national_id" not in booking_columns

    audit_log_columns = {column["name"] for column in inspector.get_columns("audit_logs")}
    assert {"actor_id", "action", "hn", "accessed_at"}.issubset(audit_log_columns)

    migration_module = load_migration_module()
    migration_module.upgrade(engine)
    migration_module.downgrade(engine)
    migration_module.upgrade(engine)
