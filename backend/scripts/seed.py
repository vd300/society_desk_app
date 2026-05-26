from decimal import Decimal

from sqlalchemy import select

from app.core.database import SessionLocal, init_db
from app.core.security import hash_password
from app.models import Building, Flat, Resident, Society, User
from app.models.enums import UserRole

PASSWORD = "password123"


def get_or_create_user(db, name: str, email: str, role: UserRole) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user:
        return user
    user = User(name=name, email=email, password_hash=hash_password(PASSWORD), role=role)
    db.add(user)
    db.flush()
    return user


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        society = db.scalar(select(Society).where(Society.name == "Green Heights"))
        if not society:
            society = Society(name="Green Heights", address="MG Road, Pune")
            db.add(society)
            db.flush()

        buildings: list[Building] = []
        for name in ["A Wing", "B Wing"]:
            building = db.scalar(
                select(Building).where(Building.society_id == society.id, Building.name == name)
            )
            if not building:
                building = Building(society_id=society.id, name=name)
                db.add(building)
                db.flush()
            buildings.append(building)

        flats: list[Flat] = []
        for building in buildings:
            wing = building.name[0]
            for number in range(101, 106):
                flat_number = f"{wing}-{number}"
                flat = db.scalar(
                    select(Flat).where(
                        Flat.building_id == building.id,
                        Flat.flat_number == flat_number,
                    )
                )
                if not flat:
                    flat = Flat(
                        society_id=society.id,
                        building_id=building.id,
                        flat_number=flat_number,
                        floor_number=1,
                        maintenance_amount=Decimal("3000.00"),
                    )
                    db.add(flat)
                    db.flush()
                flats.append(flat)

        get_or_create_user(db, "Admin User", "admin@societydesk.com", UserRole.ADMIN)
        get_or_create_user(db, "Security User", "security@societydesk.com", UserRole.SECURITY)
        resident_users = [
            get_or_create_user(db, f"Resident {index}", f"resident{index}@societydesk.com", UserRole.RESIDENT)
            for index in range(1, 4)
        ]

        for index, user in enumerate(resident_users):
            existing = db.scalar(select(Resident).where(Resident.user_id == user.id))
            if existing:
                continue
            db.add(
                Resident(
                    user_id=user.id,
                    society_id=society.id,
                    flat_id=flats[index].id,
                    phone=f"900000000{index + 1}",
                    is_owner=index == 0,
                )
            )

        db.commit()
        print("Seed data ready.")
        print("Password for all seed users: password123")
    finally:
        db.close()


if __name__ == "__main__":
    main()
