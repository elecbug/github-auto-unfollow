import requests

# Function to get GitHub username and access token from file
def get_info():
    # Enter the GitHub user name and access token
    try:
        with open("NAME_AND_TOKEN", 'r') as file:
            lines = file.readlines()
            username = lines[0].strip()
            token = lines[1].strip()

            headers = {
                "Authorization": f"token {token}"
            }

            return username, headers
    except Exception as e:
        raise Exception(f"Error reading NAME_AND_TOKEN file: {e}")

# Function to get all items from paginated GitHub API endpoints
def get_all_items(url, headers):
    items = []
    page = 1
    while True:
        response = requests.get(f"{url}&page={page}", headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break
        data = response.json()
        if not data:
            break
        items.extend(data)
        page += 1
    return items

# Function to get all following and followers of the user
def get_all_about_follow(username, headers):
    # Get following list
    following_url = f"https://api.github.com/users/{username}/following?per_page=100"
    following = get_all_items(following_url, headers)

    # Get followers list
    followers_url = f"https://api.github.com/users/{username}/followers?per_page=100"
    followers = get_all_items(followers_url, headers)

    return following, followers

# Function to check if a user is an organization
def is_organization(login, headers):
    url = f"https://api.github.com/users/{login}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to check user type {login}: {response.status_code}, {response.text}")
        return False  # Assume it's not an organization if we can't get the user info

    data = response.json()
    return data.get("type") == "Organization"

# Function to read the whitelist from a file
def get_whitelist():
    try:
        with open("WHITELIST", 'r') as file:
            whitelist = [line.strip() for line in file if line.strip()]
            return whitelist
    except Exception as e:
        print(f"Error reading whitelist: {e}")
        print("Proceeding with an empty whitelist")
        return []

# Function to filter out users who are not following back, excluding whitelisted users and organizations
def get_excluded_list(not_following_back, not_following_back_whitelist, headers):
    # Exclude whitelisted users
    not_following_back = [
        user
        for user in not_following_back
        if user not in not_following_back_whitelist
    ]

    # Exclude organizations from the list
    not_following_back = [
        user
        for user in not_following_back
        if not is_organization(user, headers)
    ]

    return not_following_back

# Function to unfollow a user
def unfollow_user(username_to_unfollow, headers):
    url = f"https://api.github.com/user/following/{username_to_unfollow}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Unfollowed: {username_to_unfollow}")
        return True
    else:
        print(f"Failed to unfollow {username_to_unfollow}: {response.status_code}, {response.text}")
        return False

def main():
    # Get username and headers for authentication
    username, headers = get_info()

    # Get all following and followers of the user
    following, followers = get_all_about_follow(username, headers)

    print(f"Followers: {len(followers)}, Following: {len(following)}")

    # Create a set of follower usernames for quick lookup
    follower_usernames = {user['login'] for user in followers}
    following_usernames = {user['login'] for user in following}

    # Find users who are following but not followed back
    not_following_back = [user for user in following_usernames if user not in follower_usernames]

    # Specific users to whitelist (e.g., important accounts)
    not_following_back_whitelist = get_whitelist()

    # Filter out whitelisted users and organizations from the not following back list
    checked_list = get_excluded_list(not_following_back, not_following_back_whitelist, headers)

    # Print results
    print("Users not following me back:", checked_list)

    # Prompt user for confirmation before unfollowing each user
    for user in checked_list:
        confirm = input(f"{user} Unfollow? (y(es)/n(o)/q(uit)): ").strip().lower()

        if confirm == 'y':
            unfollow_user(user, headers)
        elif confirm == 'q':
            print("Quitted")
            break
        else:
            print(f"Skipped: {user}")

if __name__ == "__main__":
    main()