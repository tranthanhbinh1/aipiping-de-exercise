import json


data = json.loads(open("test_data/linkedin_example.json").read())
print(type(data))   

print(data.keys())

print(data["person"]["lastName"])
print(data["person"]["firstName"])


person = data["person"]
print(person["lastName"])
print(person["firstName"])
print(person["emails"])
print(person["photoUrl"])

