astro_obj = {"earth": 1, "mars": 2, "jupiter": 3}
print(astro_obj)
print(astro_obj["earth"])
astro_obj["sun"] = 's'
print(astro_obj)
del astro_obj["earth"]
print(astro_obj)
print("jupiter" in astro_obj)
print("earth" in astro_obj)
print("earth" not in astro_obj)
print(len(astro_obj))