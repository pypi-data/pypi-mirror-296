# Ensure get_localzone is imported properly
from tzlocal import get_localzone

# Define the hello function
def hello():
    print("This is the function from Chronoflow/datetime module.")
    print(f"You are working from {ltz_here()}")

# Define the ltz_here function
def ltz_here():
    return get_localzone()