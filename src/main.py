import os
import sys
import time
from db_manager import DBManager
import capture_faces
import train_model
import recognize_faces

def login():
    print("="*40)
    print("   SMART-GATE SYSTEM LOGIN   ")
    print("="*40)
    username = input("Username: ")
    password = input("Password: ")
    
    # Simple hardcoded login for prototype
    if username == "admin" and password == "ipl2026":
        return True
    else:
        print("Invalid credentials.")
        return False

def main_menu():
    if not login():
        return

    db = DBManager()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*40)
        print("   SMART-GATE: BIOMETRIC ACCESS SYSTEM   ")
        print("="*40)
        print("1. Register New User (Capture Faces)")
        print("2. Train Recognition Model")
        print("3. Start Access Control (Real-time)")
        print("4. View Access Logs")
        print("5. Manage Users (Edit/Delete)")
        print("6. Delete All Logs")
        print("7. Exit")
        print("-" * 40)
        
        choice = input("Select an option: ")
        
        if choice == '1':
            db.close()
            capture_faces.capture_faces()
            db = DBManager()
        elif choice == '2':
            train_model.train_model()
            input("\nPress Enter to continue...")
        elif choice == '3':
            db.close()
            recognize_faces.recognize_faces()
            db = DBManager()
        elif choice == '4':
            logs = db.get_all_logs()
            print("\nID | Name       | Timestamp           | Status      | Conf")
            print("-" * 65)
            for log in logs:
                name = log[1] if log[1] else "Intruder"
                print(f"{log[0]:<2} | {name:<10} | {log[2]} | {log[3]:<10} | {log[4] if log[4] else 'N/A'}")
            input("\nPress Enter to continue...")
        elif choice == '5':
            users = db.get_users()
            print("\nID | Name       | Created At")
            print("-" * 40)
            for u in users:
                print(f"{u[0]:<2} | {u[1]:<10} | {u[2]}")
            
            sub_choice = input("\n(U)pdate name, (D)elete user, or (B)ack? ").lower()
            if sub_choice == 'u':
                uid = input("Enter User ID to update: ")
                new_name = input("Enter new name: ")
                db.update_user(uid, new_name)
                print("User updated.")
            elif sub_choice == 'd':
                uid = input("Enter User ID to delete: ")
                confirm = input(f"Are you sure you want to delete ID {uid}? (y/n): ")
                if confirm.lower() == 'y':
                    db.delete_user(uid)
                    print("User deleted.")
            input("\nPress Enter to continue...")
        elif choice == '6':
            confirm = input("Are you sure you want to delete all logs? (y/n): ")
            if confirm.lower() == 'y':
                db.cursor.execute("DELETE FROM access_logs")
                db.conn.commit()
                print("Logs deleted.")
            input("\nPress Enter to continue...")
        elif choice == '7':
            print("Exiting Smart-Gate. Goodbye!")
            break
        else:
            print("Invalid option.")
            time.sleep(1)
            
    db.close()

if __name__ == "__main__":
    main_menu()
