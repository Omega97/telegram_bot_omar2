from architect import Architect


architect = Architect()
# architect.add_user(1, "user1")
users = architect.get_user_info()

for k in users:
    print(k, users[k])
