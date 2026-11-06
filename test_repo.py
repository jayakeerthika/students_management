from database import init_db
from repository import StudentRepository

init_db()
repo = StudentRepository()

new_id = repo.add("Asha", "asha@example.com", 20, "CS")
print("Added with id:", new_id)

print("All:", repo.get_all())
print("By id:", repo.get_by_id(new_id))
print("Missing:", repo.get_by_id(999))

print("Updated:", repo.update(new_id, "Asha K", "asha@example.com", 21, "IT"))
print("After update:", repo.get_by_id(new_id))

print("Deleted:", repo.delete(new_id))
print("After delete:", repo.get_by_id(new_id))