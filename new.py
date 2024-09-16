import bcrypt
import json
import os

USERS_FILE = "users.json"
BLOGS_FILE = "blogs.json"


def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def register_user(users):
    username = input("Enter a new username: ")
    if username in users:
        print("Username already exists. Please try a different one.")
        return
    
    password = input("Enter a new password: ").encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    users[username] = hashed_password.decode('utf-8')
    save_data(USERS_FILE, users)
    print("User registered successfully!")


def authenticate_user(users):
    username = input("Enter your username: ")
    if username not in users:
        print("Username not found. Please register first.")
        return None
    
    password = input("Enter your password: ").encode('utf-8')
    hashed_password = users[username].encode('utf-8')
    print(hashed_password)

    if bcrypt.checkpw(password, hashed_password):
        print("Login successful!")
        return username
    else:
        print("Incorrect password. Please try again.")
        return None


def create_blog_post(username, blogs):
    title = input("Enter the title of the blog post: ")
    content = input("Enter the content of the blog post: ")

    if username not in blogs:
        blogs[username] = []

    blogs[username].append({"title": title, "content": content})
    save_data(BLOGS_FILE, blogs)
    print("Blog post created successfully!")


def delete_blog_post(username, blogs):
    if username not in blogs or not blogs[username]:
        print("No blog posts found.")
        return
    
    for idx, post in enumerate(blogs[username], start=1):
        print(f"{idx}. {post['title']}")

    choice = int(input("Enter the number of the blog post to delete: ")) - 1

    if 0 <= choice < len(blogs[username]):
        del blogs[username][choice]
        save_data(BLOGS_FILE, blogs)
        print("Blog post deleted successfully!")
    else:
        print("Invalid choice. Please try again.")


def modify_blog_post(username, blogs):
    if username not in blogs or not blogs[username]:
        print("No blog posts found.")
        return

    for idx, post in enumerate(blogs[username], start=1):
        print(f"{idx}. {post['title']}")

    choice = int(input("Enter the number of the blog post to modify: ")) - 1

    if 0 <= choice < len(blogs[username]):
        new_title = input("Enter the new title: ")
        new_content = input("Enter the new content: ")

        blogs[username][choice] = {"title": new_title, "content": new_content}
        save_data(BLOGS_FILE, blogs)
        print("Blog post modified successfully!")
    else:
        print("Invalid choice. Please try again.")


def main():
    
    users = load_data(USERS_FILE)
    blogs = load_data(BLOGS_FILE)

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_user(users)
        elif choice == '2':
            username = authenticate_user(users)
            if username:
                while True:
                    print("\n1. Create Blog Post")
                    print("2. Delete Blog Post")
                    print("3. Modify Blog Post")
                    print("4. Logout")

                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        create_blog_post(username, blogs)
                    elif user_choice == '2':
                        delete_blog_post(username, blogs)
                    elif user_choice == '3':
                        modify_blog_post(username, blogs)
                    elif user_choice == '4':
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
