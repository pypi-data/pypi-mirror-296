# driver_initializer.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from dotenv import load_dotenv
import os
import csv
import json


def init_driver(url):
    """
    Initialize the WebDriver with specified options and navigate to the given URL.

    Args:
        url (str): The URL to navigate to.

    Returns:
        WebDriver: The initialized WebDriver instance.
    """
    opt = Options()
    opt.add_argument("--search-engine-choice-country")
    opt.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(options=opt)
    driver.maximize_window()
    try:
        driver.get(url)
    except Exception as e:
        print("Error navigating to URL:", e)
        driver.quit()
    time.sleep(2)
    return driver


def read_login_env(username_id, password_id):
    """
    Reads environment variables for username and password IDs.

    Args:
        username_id (str): The environment variable for the username for example: "LOGIN_NAME".
        password_id (str): The environment variable for the password for example: "PASSWORD".
    """
    load_dotenv()
    return os.getenv(username_id), os.getenv(password_id)


def read_csv(path):
    """
    Reads a CSV file and returns the data as a list of dictionaries.

    Args:
        path (str): The path to the CSV file.
        data (list): The list to append the data to. Defaults to an empty list.

    Returns:
        list: The data from the CSV file as a list of dictionaries.

    """
    data = []
    try:
        with open(path, "rb") as csvfile:
            content = csvfile.read().decode("utf-8-sig")  # Remove BOM if present
            csvreader = csv.DictReader(content.splitlines(), delimiter=";")

            # Iterate through each row in the CSV
            for row in csvreader:
                # Append each row (as a dictionary) to the data list
                data.append(row)

    except FileNotFoundError:
        # Print the current working directory
        print("Current working directory:", os.getcwd())
        print(f"File not found at path: {os.getcwd()}{path}")
        print("File not found.")
    except Exception as e:
        print("Error reading CSV file.")
        print(e)

    return data


def save_csv(path, data):
    """
    Saves the data to a CSV file at the specified path.

    Args:
        path (str): The path to the CSV file.
        data (list): The data to be saved as a list of dictionaries.

    Returns:
        bool: True if the data was saved successfully, False otherwise.

    """
    # Save the updated data back to the CSV file
    try:
        with open(path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                key for key in data[0].keys()
            ]  # Get the fieldnames from the first row
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
            print("Data saved successfully.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")


def read_json(path):
    """
    Reads a JSON file and returns the data as a list of dictionaries.

    Args:
        path (str): The path to the JSON file.
        data (list): The list to append the data to. Defaults to an empty list.

    Returns:
        list: The data from the JSON file as a list of dictionaries.

    """
    data = []
    try:
        with open(path, "r", encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
    except FileNotFoundError:
        print(f"File not found at path: {path}")
    except Exception as e:
        print("Error reading JSON file.")
        print(e)

    return data


def save_json(path, data):
    """
    Saves the data to a JSON file at the specified path.

    Args:
        path (str): The path to the JSON file.
        data (list): The data to be saved as a list of dictionaries.

    Returns:
        bool: True if the data was saved successfully, False otherwise.

    """
    # Save the updated data back to the JSON file
    try:
        with open(path, "w", encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)
            print("Data saved successfully.")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
        return False
    
    return True


def clear_console():
        # For Windows
    if os.name == "nt":
        os.system("cls")
    # For Mac and Linux (os.name is 'posix')
    else:
        os.system("clear")