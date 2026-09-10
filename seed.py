import sys
import os

from database import init_db, seed_demo_students, clear_all_students, get_db

if __name__ == "__main__":
    if "--clear" in sys.argv:
        clear_all_students()
        print("All registered student profiles removed.")
    else:
        init_db(force_reset=True, seed_demo=True)
        print("Database seeded with sample campus student profiles.")
