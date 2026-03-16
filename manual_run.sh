echo "Running the login, fetching signals, and placing orders in manual mode..."
echo " Select the task you want to run:"
echo "1. Fetch token"
echo "2. Fetch signals"
echo "3. Place orders"
echo "4. Run the bot"
echo "5. Exit"

# save uv path to a variable
UV_PATH="/home/ubuntu/.local/bin/uv"


read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "Fetching token..."
        $UV_PATH src/login.py
        ;;
    2)
        echo "Fetching signals..."
        $UV_PATH src/order_placer.py --fetch
        ;;
    3)
        echo "Placing orders..."
        $UV_PATH src/order_placer.py --place
        ;;
    4)
        echo "Running the bot..."
        $UV_PATH src/main.py
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please enter a number between 1 and 5."
        ;;
esac