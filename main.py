from database import create_tables, add_meal, show_meals
from prediction import predict_food
from rescue import add_surplus_food, show_surplus, reserve_food
from report import waste_report, menu_wise_report


def main():
    print("main function started")

    create_tables()

    while True:

        print("\n")
        print("======================================")
        print("          🧠 MESSMIND")
        print(" Smart Food Waste Management System")
        print("======================================")

        print("\n1. Add Meal Record")
        print("2. View Meal Records")
        print("3. Predict Food Requirement")
        print("4. Add Surplus Food")
        print("5. View Available Surplus Food")
        print("6. Reserve Surplus Food")
        print("7. Food Waste Report")
        print("8. Menu-wise Waste Report")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_meal()

        elif choice == "2":
            show_meals()

        elif choice == "3":
            predict_food()

        elif choice == "4":
            add_surplus_food()

        elif choice == "5":
            show_surplus()

        elif choice == "6":
            reserve_food()

        elif choice == "7":
            waste_report()

        elif choice == "8":
            menu_wise_report()

        elif choice == "9":

            print("\nThank you for using MESSMIND!")

            break

        else:
            print("\n❌ Invalid choice.")


if __name__ == "__main__":
    main()