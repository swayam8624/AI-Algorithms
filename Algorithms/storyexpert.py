import re
class ExpertSystem:
    def __init__(self):
        self.knowledge_base = []  # Stores the known facts
        self.rules = []  # Stores the rules (inferred facts based on conditions)

    # Add facts to the knowledge base
    def add_fact(self, fact):
        self.knowledge_base.append(fact)

    # Add rules to infer facts based on conditions
    def add_rule(self, conditions, result):
        self.rules.append((conditions, result))

    # Infer new facts based on existing rules and facts
    def infer(self):
        inferred_facts = []
        for conditions, result in self.rules:
            if all(condition in self.knowledge_base for condition in conditions):
                if result not in self.knowledge_base:
                    inferred_facts.append(result)
                    self.add_fact(result)
        return inferred_facts

    # Allow user to ask questions
    def ask(self, question):
        question = question.lower().strip()

        # Handle 'Who killed' type questions
        who_killed_match = re.match(r"who (killed|murdered|slew) (.+)\?", question)
        if who_killed_match:
            action = who_killed_match.group(1)
            object_of_action = who_killed_match.group(2)

            # Search facts for a match
            for fact in self.knowledge_base:
                fact = fact.lower()
                match = re.match(f"(.+) {action} {object_of_action}\.", fact)
                if match:
                    subject = match.group(1)
                    return f"{subject.capitalize()} {action} {object_of_action.capitalize()}."
            return f"I don't know who {action} {object_of_action}."

        # Handle 'What happened to' type questions
        what_happened_match = re.match(r"what happened to (.+)\?", question)
        if what_happened_match:
            object_of_action = what_happened_match.group(1)  # e.g., 'Banquo'

            # Search facts for any related action involving the object
            for fact in self.knowledge_base:
                if object_of_action in fact.lower():
                    return fact.capitalize()
            return f"I don't know what happened to {object_of_action}."

        # General fallback for unsupported questions
        return "I don't understand the question."

    # Load facts and rules from a text file
    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        is_rule_section = False
        for line in lines:
            line = line.strip()

            # Ignore empty lines and comments
            if not line or line.startswith('#'):
                continue

            if line.startswith("# Rules"):
                is_rule_section = True
                continue

            if is_rule_section:
                # Parse rules in the format: conditions -> result
                if "->" in line:
                    conditions_str, result = line.split("->")
                    conditions = [cond.strip() for cond in conditions_str.split(',')]
                    self.add_rule(conditions, result.strip())
            else:
                # Add facts from the fact section
                self.add_fact(line)

        # After loading, infer new facts from the rules
        self.infer()


# Interactive session where the user asks questions
def ask_question(expert_system):
    while True:
        question = input("Ask a question about the story (or type 'exit' to stop): ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            answer = expert_system.ask(question)
            print(answer)


# Initialize the expert system
story_expert_system = ExpertSystem()

# Load facts and rules from the text file
story_expert_system.load_from_file('story_facts_rules.txt')

# Run the interactive question-answering session
ask_question(story_expert_system)
