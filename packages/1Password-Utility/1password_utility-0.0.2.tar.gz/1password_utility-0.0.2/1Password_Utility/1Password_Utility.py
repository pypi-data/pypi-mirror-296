import subprocess
import re

def get_credentials_from_1password(item_uuid):
    """Retrieves username and password from a 1Password item using the CLI.

    Args:
        item_uuid: The UUID of the 1Password item.

    Returns:
        A tuple containing the username and password, or (None, None) if not found.
    """

    try:
        result = subprocess.run(
            ["op", "item", "get", item_uuid, "--reveal"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Use regular expressions to extract username and password
        username_match = re.search(r"username:\s+(.*)", result.stdout)
        password_match = re.search(r"password:\s+(.*)", result.stdout)

        if username_match and password_match:
            username = username_match.group(1)
            password = password_match.group(1)
            return username, password
        else:
            print("Failed to parse credentials from output.")
            return None, None

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving credentials: {e}")
        return None, None
