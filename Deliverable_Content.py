import json
# Takes in Prompts and generates content for the Deliverable
formatting_instructions = """
            "tables": {
                        "TableName": {
                            "columns": {
                                "Column Name": "Column Type"
                            }
                    """
class Deliverable_Content:
    def __init__(self, client):
        self.client = client
        # self.problem_requirements = None
        # self.deliverable_plan = None
        # self.technical_plan = None
        # self.data_plan = None

    def generate_problem_requirements(self, business_problem, tech_stack, time_constraint, resource_constraints):
        prompt = f"generate a clear and concise business plan as a json where the fields are executive-summary, problem-definition, and problem-requirements and technical-solution based on the business problem: {business_problem}, tech stack: {tech_stack}, time constraint: {time_constraint}, resource constraints: {resource_constraints}" 
        print("Prompt for problem requirements generation:\n", prompt)
        return json.loads(self.client.get_response(prompt))
    
    def generate_technical_plan(self, problem_requirements):
        prompt = f"Based on the following problem requirements, generate a detailed technical plan as a json with the fields: technical-approach, architecture-overview, and technology-stack. Problem requirements: {problem_requirements}"
        print("Prompt for technical plan generation:\n", prompt)
        return json.loads(self.client.get_response(prompt))
    
    def generate_deliverable_plan(self, technical_plan):
        prompt = f"Based on the following technical plan, generate a detailed deliverable plan as a json with the fields: deliverable-overview, key-milestones, and success-criteria. Technical plan: {technical_plan}"
        print("Prompt for deliverable plan generation:\n", prompt)
        return json.loads(self.client.get_response(prompt))
    
    def generate_data_plan(self, technical_plan):
        prompt = f"Based on the following technical plan, generate a detailed data plan as a json with the fields: data-requirements, data-schema, data-sources, and data-governance. Technical plan: {technical_plan}"
        print("Prompt for data plan generation:\n", prompt)
        return json.loads(self.client.get_response(prompt))
    
    def generate_full_problem_requirements(self, business_problem, tech_stack, time_constraint, resource_constraints):
        prompt = "generate a clear and concise business plan as a json where the fields are executive-summary, problem-definition, problem-requirements, technical-solution, data architecture in the format:" + formatting_instructions + f"(with table names and column schemas) and delivery plan based on the business problem: {business_problem}, tech stack: {tech_stack}, time constraint: {time_constraint}, resource constraints: {resource_constraints}" 
        print("Prompt for problem requirements generation:\n", prompt)
        return json.loads(self.client.get_response(prompt))
    