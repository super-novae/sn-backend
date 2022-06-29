from api import db, fake


def truncate_db_tables():
    meta = db.metadata
    for table in meta.sorted_tables[::-1]:
        db.session.execute(table.delete())
    db.session.commit()
