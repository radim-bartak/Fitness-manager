from app.models import db, Trainer, Class, Reservation
from sqlalchemy import func, case

def trainer_utilization_report():
    """
    Vytváří seznam trenérů s informacemi o jejich vytížení.

    :return: Seznam trenérů s informacemi o využití jejich lekcí
    """
    subquery = (
        db.session.query(
            Class.trainer_id.label("trainer_id"),
            func.count(Class.id).label("total_classes"),
            func.sum(Class.capacity).label("total_capacity"),
            func.count(Reservation.id).label("total_reservations")
        )
        .outerjoin(Reservation, Reservation.class_id == Class.id)
        .group_by(Class.trainer_id)
        .subquery()
    )

    report_data = (
        db.session.query(
            Trainer.id.label("trainer_id"),
            Trainer.name.label("trainer_name"),
            Trainer.specialization.label("specialization"),
            subquery.c.total_classes,
            (subquery.c.total_capacity - subquery.c.total_reservations).label("total_free_spots"),
            subquery.c.total_reservations,
            case(
                (subquery.c.total_capacity > 0, (subquery.c.total_reservations / subquery.c.total_capacity) * 100),
                else_=0
            ).label("average_utilization")
        )
        .outerjoin(subquery, Trainer.id == subquery.c.trainer_id)
        .all()
    )

    return [
        {
            "trainer_id": row.trainer_id,
            "trainer_name": row.trainer_name,
            "specialization": row.specialization,
            "total_classes": row.total_classes,
            "total_free_spots": row.total_free_spots,
            "total_reservations": row.total_reservations,
            "average_utilization": row.average_utilization
        }
        for row in report_data
    ]

