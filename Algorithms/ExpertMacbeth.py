# Knowledge base (facts and rules in FOL)
facts = {
    "King(Duncan)": True,
    "Ambitious(Macbeth)": True,
    "Prophecy(Witches, Macbeth)": True,
    "Killed(Macbeth, Duncan)": False,
    "King(Macbeth)": False,
    "SeeksRevenge(Macduff, Macbeth)": False,
    "Dies(Macbeth)": False,
}


# Rules that drive the inference
def apply_rules(facts):
    # Rule 1: If Macbeth is ambitious and receives a prophecy, he seeks power
    if facts["Ambitious(Macbeth)"] and facts["Prophecy(Witches, Macbeth)"]:
        print("Macbeth seeks power.")

    # Rule 2: If Macbeth kills Duncan, he becomes king
    if facts["Killed(Macbeth, Duncan)"]:
        facts["King(Macbeth)"] = True
        print("Macbeth becomes king.")

    # Rule 3: If Macbeth becomes king, Macduff seeks revenge
    if facts["King(Macbeth)"]:
        facts["SeeksRevenge(Macduff, Macbeth)"] = True
        print("Macduff seeks revenge against Macbeth.")

    # Rule 4: If someone is ambitious and kills someone, they will die
    if facts["Ambitious(Macbeth)"] and facts["Killed(Macbeth, Duncan)"]:
        facts["Dies(Macbeth)"] = True
        print("Macbeth will die.")

    return facts


# Scenario: Macbeth kills Duncan
facts["Killed(Macbeth, Duncan)"] = True

# Apply the rules to infer new facts
new_facts = apply_rules(facts)

# Output the final facts
print("\nFinal Facts:")
for fact, truth in new_facts.items():
    print(f"{fact}: {truth}")
