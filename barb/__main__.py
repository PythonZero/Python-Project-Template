from barb import ConfigValues

ConfigValues.load("config/prod.yaml")
ConfigValues.load("config/prod.json")

print(ConfigValues.xyz)
print(ConfigValues.Name)
print(ConfigValues.Role)


cyz = ConfigValues.CYZ
