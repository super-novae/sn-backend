from api.extensions import db
from api.extensions import logger
from flask import abort
from sys import exc_info


def save(entity):
    error = False

    try:
        db.session.add(entity)
        db.session.commit()

    except Exception:
        error = True
        logger.warning(exc_info())
        db.session.rollback()
        abort(500)

    finally:
        db.session.close()

    return entity, error


def modify(entity):
    error = False

    try:
        db.session.commit()

    except Exception:
        error = True
        logger.warning(exc_info())
        db.session.rollback()
        abort(500)

    finally:
        db.session.close()

    return entity, error


def delete(entity):
    error = False

    try:
        db.session.delete(entity)
        db.session.commit()

    except Exception:
        error = True
        logger.warning(exc_info())
        db.session.rollback()
        abort(500)

    finally:
        db.session.close()

    return entity, error
