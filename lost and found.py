from datetime import date

# ── Data Store ───────────────────────────────────────────────────────────────
items = [
    {
        "id": 1,
        "name": "AirPods Pro",
        "type": "lost",
        "category": "Electronics",
        "location": "Library 2F",
        "date": "Apr 1",
        "desc": "White AirPods Pro with scratch",
        "reporter": "Aryan",
        "email": "aryan@campus.edu",
    },
    {
        "id": 2,
        "name": "Spiral Notebook",
        "type": "found",
        "category": "Stationery",
        "location": "Block A",
        "date": "Mar 28",
        "desc": "Green notebook Kabir name",
        "reporter": "Ananya",
        "email": "ananya@campus.edu",
    },
]

next_id = len(items) + 1
CATEGORIES = ["Electronics", "Bags", "Documents", "Stationery", "Other"]
inbox = {}


# ── Safe Input Helper ─────────────────────────────────────────────────────────
def safe_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\n  Input interrupted. Returning to menu.\n")
        return None


# ── Messaging System ─────────────────────────────────────────────────────────
def send_message(to_name, from_name, subject, body):
    if to_name not in inbox:
        inbox[to_name] = []

    inbox[to_name].append(
        {
            "from": from_name,
            "subject": subject,
            "body": body,
            "date": date.today().strftime("%b %d"),
        }
    )


def view_inbox(username):
    msgs = inbox.get(username, [])
    if not msgs:
        print("\n  Your inbox is empty.\n")
        return

    print(f"\n  Inbox for {username} ({len(msgs)} messages):\n")
    for msg in msgs:
        print("------------------------------")
        print(f"From   : {msg['from']}")
        print(f"Date   : {msg['date']}")
        print(f"Subject: {msg['subject']}")
        print(f"Message: {msg['body']}")
        print("------------------------------")


# ── SMART MATCHING ───────────────────────────────────────────────────────────
def check_and_notify(new_item):
    match_type = "found" if new_item["type"] == "lost" else "lost"
    new_text = (new_item["name"] + " " + new_item["desc"]).lower()
    new_words = set(new_text.split())

    for item in items:
        if item["id"] == new_item["id"]:
            continue
        if item["type"] != match_type:
            continue
        old_text = (item["name"] + " " + item["desc"]).lower()
        old_words = set(old_text.split())

        # MATCH CONDITION
        if item["category"] == new_item["category"] and (new_words & old_words):
            if new_item["type"] == "lost":
                loser = new_item
                finder = item
            else:
                loser = item
                finder = new_item

            # Message to loser
            send_message(
                loser["reporter"],
                "Portal",
                "Your item has been found!",
                f"Good news! '{loser['name']}' found by {finder['reporter']} at {finder['location']}",
            )

            # Message to finder
            send_message(
                finder["reporter"],
                "Portal",
                "Owner found!",
                f"Owner of '{finder['name']}' is {loser['reporter']}",
            )

            # Print live notification
            print("\n🔥A MATCH FOUND!")
            print(f"Item   : {loser['name']}")
            print(f"Owner  : {loser['reporter']}")
            print(f"Finder : {finder['reporter']}")
            print("📩 Message sent to both users!\n")


# ── REPORT ITEM ──────────────────────────────────────────────────────────────
def report_item():
    global next_id

    print("\n1. Lost\n2. Found")
    choice = safe_input("Choose: ")
    if choice is None:
        return

    if choice == "1":
        item_type = "lost"
    elif choice == "2":
        item_type = "found"
    else:
        print("Invalid choice.")
        return

    name = safe_input("Item name: ")
    if not name:
        return
    desc = safe_input("Description: ") or ""
    category = safe_input("Category: ") or "Other"
    location = safe_input("Location: ") or "Unknown"
    reporter = safe_input("Your name: ") or "Anonymous"
    email = safe_input("Email: ") or ""

    new_item = {
        "id": next_id,
        "name": name,
        "type": item_type,
        "category": category,
        "location": location,
        "date": date.today().strftime("%b %d"),
        "desc": desc,
        "reporter": reporter,
        "email": email,
    }

    items.append(new_item)
    next_id += 1

    print("\n  Item reported successfully!\n")
    check_and_notify(new_item)


# ── BROWSE ───────────────────────────────────────────────────────────────────
def browse():
    if not items:
        print("\n  No items to display.\n")
        return
    for item in items:
        print("\n------------------------------")
        print(f"{item['name']} | {item['type']}")
        print(f"{item['desc']}")
        print(f"Location: {item['location']} | Category: {item['category']}")
        print("------------------------------")


# ── MAIN MENU ────────────────────────────────────────────────────────────────
def main():
    while True:
        print("\n1. Browse Items")
        print("2. Report Item")
        print("3. Inbox")
        print("4. Exit")

        choice = safe_input("Choose: ")
        if choice is None:
            continue

        if choice == "1":
            browse()
        elif choice == "2":
            report_item()
        elif choice == "3":
            username = safe_input("Enter your name: ")
            if username:
                view_inbox(username)
        elif choice == "4":
            print("\n  Goodbye! Stay safe on campus.\n")
            break
        else:
            print("Invalid choice, try again.")


# ── ENTRY POINT ──────────────────────────────────────────────────────────────
if __name__ == "__main__":

    main()
