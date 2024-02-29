import requests

s = requests.Session()

url = ""
directoryServices = []


# http://127.0.0.1:8000
def send_api_request(url, params=None, headers=None, method="GET", data=None):
    try:
        if method == "GET":
            response = s.get(url, params=params, headers=headers)
        elif method == "POST":
            response = s.post(url, data=data, headers=headers)
        elif method == "DELETE":
            response = s.delete(url, headers=headers)

        response.raise_for_status()

        return (
            response.json()
            if response.headers.get("content-type") == "application/json"
            else response.text
        )
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


directoryResponse = send_api_request(
    "https://newssites.pythonanywhere.com/api/directory/", method="GET"
)
directoryServices = directoryResponse


def get_user_input(prompt):
    return input(prompt).strip()


def checkUrlExists():
    if url == "":
        print("Please enter a URL while logging in. Stopping requested operation.")
        return False
    return True


while True:
    user_command = get_user_input("Enter a command (or 'exit' to quit): ")
    user_command_list = user_command.split(" ")

    if user_command_list[0].lower() == "exit":
        break

    if user_command_list[0].lower() == "login":
        url = user_command_list[1]
        print(url)
        username = get_user_input("Username: ")
        password = get_user_input("Password: ")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"username": username, "password": password}
        response = send_api_request(
            f"{url}/api/login", method="POST", data=data, headers=headers
        )
        if response is not None:
            print(response)
        else:
            url = ""

    if user_command_list[0].lower() == "logout":
        if checkUrlExists() == False:
            continue
        response = send_api_request(f"{url}/api/logout", method="POST")
        if response:
            url = ""
            print(response)

    if user_command_list[0].lower() == "post":
        if checkUrlExists() == False:
            continue
        headline = get_user_input("Headline: ")
        category = get_user_input("Category: ")
        region = get_user_input("Region: ")
        details = get_user_input("Details: ")
        data = {
            "headline": headline,
            "category": category,
            "region": region,
            "details": details,
        }
        response = send_api_request(f"{url}/api/stories", method="POST", data=data)
        if response:
            print(response)

    if user_command_list[0].lower() == "news":
        serviceId = False  # Change this so that it works with the directory
        params = {"story_cat": "*", "story_region": "*", "story_date": "*"}
        for param in user_command_list[1:]:
            if param.startswith("-id="):
                serviceId = param.split("=")[1]
            elif param.startswith("-cat="):
                params["story_cat"] = param.split("=")[1]
            elif param.startswith("-reg="):
                params["story_region"] = param.split("=")[1]
            elif param.startswith("-date="):
                params["story_date"] = param.split("=")[1]

        if serviceId:
            found = False
            # Get the URL from directoryServices
            for service in directoryServices:
                if service["agency_code"] == serviceId.upper():
                    found = True
                    response = send_api_request(
                        f"{service['url']}/api/stories", params=params, method="GET"
                    )
                    if response:
                        print(f'\nStories for {service["agency_name"]}\n')
                        for story in response["stories"]:
                            print(
                                f'Key: {story["key"]}\nHeadline: {story["headline"]}\nCategory: {story["story_cat"]}\nRegion: {story["story_region"]}\nAuthor: {story["author"]}\nDate: {story["story_date"]}\nDetails: {story["story_details"]}\n\n'
                            )
            if not found:
                print(f"Service with ID {serviceId} not found.")
        else:
            for service in directoryServices:
                response = send_api_request(
                    f"{service['url']}/api/stories", params=params, method="GET"
                )
                print(f'\nStories for {service["agency_name"]}\n')
                if response:
                    for story in response["stories"]:
                        print(
                            f'Key: {story["key"]}\nHeadline: {story["headline"]}\nCategory: {story["story_cat"]}\nRegion: {story["story_region"]}\nAuthor: {story["author"]}\nDate: {story["story_date"]}\nDetails: {story["story_details"]}\n\n'
                        )

    if user_command_list[0].lower() == "list":
        response = send_api_request(
            "https://newssites.pythonanywhere.com/api/directory/", method="GET"
        )
        if response:
            directoryServices = response
            for service in response:
                print(
                    f"Agency Name: {service['agency_name']}\nUrl: {service['url']}\nCode: {service['agency_code']}\n\n"
                )

    if user_command_list[0].lower() == "delete":
        if checkUrlExists() == False:
            continue
        storyKey = user_command_list[1]
        response = send_api_request(f"{url}/api/stories/{storyKey}", method="DELETE")
        if response:
            print(response)
