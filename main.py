import transaction
if __name__=="__main__":
    print("\n*************** Welcome to Portfolio Analyzer Window **************")

    while True:
        print("\n******* Enter Your Choice *******")
        print("1️⃣  Add Transaction")
        print("2️⃣  View Portfolio")
        print("0️⃣  Exit")

        choice = input("👉 Enter your choice: ").strip()

        if choice == '1':
            transaction.add_transaction()
        elif choice == '2':
            print("\n📊 Portfolio feature coming soon...")  # Placeholder
        elif choice == '0':
            confirm_exit = input("\n❓ Are you sure you want to exit? (yes/no): ").strip().lower()
            if confirm_exit in ('yes', 'y'):
                print("\n👋 Thank you for using Portfolio Analyzer. Goodbye!")
                break
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, or 0.")

