import os

def explore_helper(folder_path):
    result = {}
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            result[item] = item_path
        elif os.path.isdir(item_path):
            result[item] = explore_helper(item_path)
    return result

print(explore_helper("/home/_3hy/Documents/home-server/static"))

