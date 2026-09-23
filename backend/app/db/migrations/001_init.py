from app.db.models import Base


def upgrade(engine):
    """Supports: CON-TECH-01, DOM-PDPA-01, IF-HIS-01."""
    Base.metadata.create_all(bind=engine)


def downgrade(engine):
    """Supports: CON-TECH-01, DOM-PDPA-01, IF-HIS-01."""
    Base.metadata.drop_all(bind=engine)
