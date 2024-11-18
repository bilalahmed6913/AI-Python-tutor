import streamlit as st
import sqlite3
from test2 import python_ide
from content2 import display_module, display_test, project_content, get_file_content, get_progress
from authentication2 import signup  # Keep the signup function




# Initialize the database
def init_db():
    with sqlite3.connect('testing.db', check_same_thread=False) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS testing
                     (id TEXT PRIMARY KEY, password TEXT, module_progress INTEGER)''')
        conn.commit()




# Initialize session state for module_progress
def initialize_session_state():
    if 'module_progress' not in st.session_state:
        st.session_state['module_progress'] = 0




def login():
    # Create input fields for user credentials
    user_id = st.text_input("User ID", placeholder="Enter your user ID")
    password = st.text_input("Password", type='password', placeholder="Enter your password")




    if st.button("Login"):
        with sqlite3.connect('testing.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM testing WHERE id = ? AND password = ?", (user_id, password))
            user = c.fetchone()
            if user:
                # If user found, set the session state and redirect to home
                st.session_state['user_id'] = user_id
                st.session_state['module_progress'] = user[2]  # Set module_progress from the database
                st.session_state['page'] = "home"  # Change to home page
                st.rerun()  # Rerun to reflect changes
            else:
                st.error("Invalid User ID or Password. Please try again.")




def signup():
    # Create input fields for user credentials
    user_id = st.text_input("User ID", placeholder="Choose your user ID")
    password = st.text_input("Password", type='password', placeholder="Create your password")




    if st.button("Sign Up"):
        with sqlite3.connect('testing.db') as conn:
            c = conn.cursor()
            # Check if the user already exists
            c.execute("SELECT * FROM testing WHERE id = ?", (user_id,))
            if c.fetchone():
                st.error("User ID already exists. Please choose another.")
            else:
                # Insert new user into the database
                c.execute("INSERT INTO testing (id, password, module_progress) VALUES (?, ?, ?)", (user_id, password, 0))
                conn.commit()
                st.success("Account created successfully! You can now log in.")




# Main function to handle page routing
def main():
    initialize_session_state()  # Ensure session state is initialized


    if 'page' not in st.session_state:
        st.session_state['page'] = "login"


    print(f"Current page: {st.session_state['page']}")


    if st.session_state['page'] == "login":
        login()
        if st.button("Don't have an account? Sign Up"):
            st.session_state['page'] = "signup"
            st.rerun()
    elif st.session_state['page'] == "signup":
        signup()
        if st.button("Already have an account? Login"):
            st.session_state['page'] = "login"
            st.rerun()
    else:  # If the user is logged in and the page is not login/signup
        # Move buttons to sidebar
        st.sidebar.title("Navigation")


        if st.sidebar.button("Home"):
            st.session_state['page'] = "home"
            st.rerun()


        if st.sidebar.button("Python IDE"):
            st.session_state['page'] = "python_ide"
            st.rerun()


        if st.sidebar.button("Modules"):
            st.session_state['page'] = "modules"
            st.rerun()


        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()


        # Logic for displaying content based on selected page
        if st.session_state['page'] == "home":
            user_id = st.session_state.get('user_id')


            if user_id:
                progress = get_progress(user_id)


                # Display the progress in the top-right corner
                st.success(f"Modules completed: {progress - 1}")


            st.title("Welcome to Your AI-Powered Python Tutor! 🚀")


            # CSS for boxes (with text color added)
            st.markdown(
                """
                <style>
                .box {
                    background-color: #d3d3d3;
                    border: 1px solid #ccc;
                    padding: 20px;
                    margin-bottom: 10px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    color: black; /* Ensures the text inside is black */
                }
                </style>
                """, unsafe_allow_html=True
            )


            # Display the content in boxes
            st.markdown(
                """
                <style>
                .box {
                    background-color: #d3d3d3;
                    border: 1px solid #ccc;
                    padding: 20px;
                    margin-bottom: 10px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    color: black; /* Ensures the text inside is solid black */
                }
                .box h4 {
                    font-weight: bold; /* Makes the heading bold */
                    color: black; /* Ensures the heading is solid black */
                }
                </style>
                """, unsafe_allow_html=True
            )


            st.markdown("""<div class="box"><h4>Ready to take your Python skills to the next level?</h4><p>Whether you're just starting or looking to sharpen your coding expertise, AI Python Tutor is here to guide you 24/7 with personalized lessons tailored just for you.</p></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="box"><h4>Imagine having a mentor...</h4><p>Imagine having a mentor who never gets tired of your questions, explains concepts with infinite patience, and celebrates every bit of progress you make. With AI Tutor for Python, that’s exactly what you’ll get—a dedicated coding companion designed to make learning Python fun, exciting, and achievable at your own pace.</p></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="box"><h4>AI Python Tutor: Your Perfect Coding Companion</h4><p>AI Python Tutor is designed to be that perfect companion on your coding journey.</p></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="box"><h4>Committed to Your Success</h4><p>By your side at every step, AI tutor is dedicated to helping you unlock your full potential, providing guidance with an unwavering commitment to your growth and success.</p></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="box"><h4>Boundless Encouragement and Support</h4><p>Experience personalized learning with the machine-driven equivalent of boundless encouragement and support.</p></div>""", unsafe_allow_html=True)


        elif st.session_state['page'] == "python_ide":
            st.write(python_ide())


        elif st.session_state['page'] == "modules":
            module_selected = st.sidebar.radio("Select a module", options=[
                "Introduction",
                "Module-1 : Introduction to python", "Module-1 test",
                "Module-2 : Python variables", "Module-2 test",
                "Module-3 : Python Data Types", "Module-3 test",
                "Module-4 : Operators-1", "Module-4 test",
                "Module-5 : Data Structures", "Module-5 test",
                "Module-6 : Operators-2", "Module-6 test",
                "Module-7 : Logical Operators", "Module-7 test",
                "Module-8 : Conditional Statements", "Module-8 test",
                "Module-9 : Loops", "Module-9 test", "Project-1",
                "Module-10 : Sets", "Module-10 test",
                "Module-11 : Dictionary", "Module-11 test",
                "Module-12 : String Functions", "Module-12 test",
                "Module-13 : Functions", "Module-13 test",
                "Module-14 : Lambda Functions", "Module-14 test",
                "Module-15 : File Handling", "Module-15 test",
                "Module-16 : Exception Handling", "Module-16 test",
                "Module-17 : OOPs-1", "Module-17 test",
                "Module-18 : OOPs-2", "Module-18 test",
                "Module-19 : OOPs-3", "Module-19 test", "Project-2"
            ])


            if module_selected == "Introduction":
                st.video(r"https://youtu.be/SaGTAj3n_aU?si=MwJr4NJ3ZJahatRG")
                content = get_file_content("Modules/introduction")
                st.markdown(content, unsafe_allow_html=True)


            # Module 1
            elif module_selected == "Module-1 : Introduction to python":
                display_module(1, "Using the print function, write a sentence about your hobbies.", "Just the print function and nothing else")
            elif module_selected == "Module-1 test":
                display_test(1, "You are a student and need to introduce yourself. Use the Python print function to print your introduction.")


            # Module 2
            elif module_selected == "Module-2 : Python variables":
                display_module(2, "Create a few Python variables to store your name, age, and favorite hobby. Then, print them.", "Focus on creating variables and printing them.")
            elif module_selected == "Module-2 test":
                display_test(2, "Write a Python program to store and display your name, age, and favorite hobby.")


            # Module 3
            elif module_selected == "Module-3 : Python Data Types":
                display_module(3, "Learn about different data types. Create a list of your top 3 favorite foods and print it.", "Focus on understanding data types.")
            elif module_selected == "Module-3 test":
                display_test(3, "Write a Python program that creates a list of your top 3 favorite foods and prints them.")


            # Module 4
            elif module_selected == "Module-4 : Operators-1":
                display_module(4, "Explore basic operators in Python. Write a simple calculator using addition and subtraction.", "Focus on using `+` and `-` operators.")
            elif module_selected == "Module-4 test":
                display_test(4, "Write a Python program that adds and subtracts two numbers input by the user.")


            # Module 5
            elif module_selected == "Module-5 : Data Structures":
                display_module(5, "Learn about data structures like lists and tuples. Create a list of five numbers and print the sum.", "Use Python's `sum()` function.")
            elif module_selected == "Module-5 test":
                display_test(5, "Write a Python program to create a list of five numbers and print their sum.")


            # Module 6
            elif module_selected == "Module-6 : Operators-2":
                display_module(6, "Deep dive into operators like multiplication and division. Write a Python program that multiplies two numbers.", "Use the `*` and `/` operators.")
            elif module_selected == "Module-6 test":
                display_test(6, "Write a Python program to multiply two numbers and print the result.")


            # Module 7
            elif module_selected == "Module-7 : Logical Operators":
                display_module(7, "Understand logical operators (and, or, not). Write a Python program to check if a number is positive and even.", "Use logical operators in conditions.")
            elif module_selected == "Module-7 test":
                display_test(7, "Write a Python program to check if a number is both positive and even.")


            # Module 8
            elif module_selected == "Module-8 : Conditional Statements":
                display_module(8, "Learn about conditional statements (`if`, `else`). Write a program to check if a number is odd or even.", "Use `if` and `else` statements.")
            elif module_selected == "Module-8 test":
                display_test(8, "Write a Python program to check if a number is odd or even using conditional statements.")


            # Module 9
            elif module_selected == "Module-9 : Loops":
                display_module(9, "Explore loops in Python. Write a program that prints numbers 1 to 10 using a loop.", "Use a `for` loop or `while` loop.")
            elif module_selected == "Module-9 test":
                display_test(9, "Write a Python program that prints numbers 1 to 10 using a loop.")


            # Project 1
            elif module_selected == "Project-1":
                project_content(1, "Combine what you've learned to create a simple interactive program that takes user input and performs basic arithmetic operations.")
           
            # Module 10
            elif module_selected == "Module-10 : Sets":
                display_module(10, "Learn about sets. Create two sets of numbers and print their union and intersection.", "Use set operations in Python.")
            elif module_selected == "Module-10 test":
                display_test(10, "Write a Python program to create two sets and find their union and intersection.")


            # Module 11
            elif module_selected == "Module-11 : Dictionary":
                display_module(11, "Explore dictionaries in Python. Create a dictionary to store the names and ages of three people.", "Use Python's dictionary data type.")
            elif module_selected == "Module-11 test":
                display_test(11, "Write a Python program to create a dictionary with names and ages, then print the dictionary.")


            # Module 12
            elif module_selected == "Module-12 : String Functions":
                display_module(12, "Learn string functions. Write a Python program to take a string input and print it in uppercase.", "Use string methods like `upper()`.")
            elif module_selected == "Module-12 test":
                display_test(12, "Write a Python program to convert a string to uppercase and print it.")


            # Module 13
            elif module_selected == "Module-13 : Functions":
                display_module(13, "Understand how to create functions in Python. Write a function that returns the square of a number.", "Define a Python function.")
            elif module_selected == "Module-13 test":
                display_test(13, "Write a Python function to return the square of a number and test it.")


            # Module 14
            elif module_selected == "Module-14 : Lambda Functions":
                display_module(14, "Learn about lambda functions. Write a lambda function that multiplies two numbers.", "Use Python's lambda syntax.")
            elif module_selected == "Module-14 test":
                display_test(14, "Write a lambda function to multiply two numbers and print the result.")


            # Module 15
            elif module_selected == "Module-15 : File Handling":
                display_module(15, "Learn about file handling. Write a Python program to open and read a file.", "Use `open()` to handle files.")
            elif module_selected == "Module-15 test":
                display_test(15, "Write a Python program to open a file and print its content.")


            # Module 16
            elif module_selected == "Module-16 : Exception Handling":
                display_module(16, "Understand exception handling. Write a Python program to handle division by zero errors.", "Use `try` and `except` blocks.")
            elif module_selected == "Module-16 test":
                display_test(16, "Write a Python program to catch and handle division by zero errors.")


            # Module 17
            elif module_selected == "Module-17 : OOPs-1":
                display_module(17, "Learn object-oriented programming. Define a class to represent a student with attributes and methods.", "Create a class with `__init__()`.")
            elif module_selected == "Module-17 test":
                display_test(17, "Write a Python class to represent a student and print their details.")


            # Module 18
            elif module_selected == "Module-18 : OOPs-2":
                display_module(18, "Explore inheritance in Python. Create a parent class and a child class that inherits from it.", "Use class inheritance.")
            elif module_selected == "Module-18 test":
                display_test(18, "Write a Python program to demonstrate inheritance between classes.")


            # Module 19
            elif module_selected == "Module-19 : OOPs-3":
                display_module(19, "Learn about method overriding in Python. Override a method in the child class from Module 18.", "Use method overriding in inheritance.")
            elif module_selected == "Module-19 test":
                display_test(19, "Write a Python program to override a method in a child class.")


            # Project 2
            elif module_selected == "Project-2":
                project_content(2, "Develop a Python program that incorporates OOP principles, error handling, and file operations. Your program should manage a simple inventory system.")




if __name__ == "__main__":
    init_db()
    main()

















