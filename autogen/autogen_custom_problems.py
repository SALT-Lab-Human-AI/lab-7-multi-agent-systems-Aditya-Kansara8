"""
AutoGen Custom Problems Demo - Exercise 4

This demo implements multiple custom problem-solving scenarios using AutoGen:
1. Plan a 3-day conference agenda
2. Design a marketing strategy for a product
3. Create a research paper outline
4. Plan a software architecture

Each scenario uses a multi-agent workflow with specialized agents.
"""

from datetime import datetime
from config import Config
import json

# Try to import OpenAI client
try:
    from openai import OpenAI
except ImportError:
    print("ERROR: OpenAI client is not installed!")
    print("Please run: pip install -r ../requirements.txt")
    exit(1)


class CustomProblemWorkflow:
    """Flexible workflow for custom problem-solving scenarios"""

    # Scenario configurations
    SCENARIOS = {
        "conference": {
            "name": "3-Day Conference Agenda Planning",
            "phases": [
                {
                    "name": "Research & Requirements",
                    "agent": "Conference Researcher",
                    "prompt": "You are a conference planning expert. Research and identify key requirements for a 3-day conference including: target audience, main themes, session types, networking opportunities, and logistical needs. Provide a comprehensive overview in 150 words."
                },
                {
                    "name": "Agenda Structure",
                    "agent": "Agenda Designer",
                    "prompt": "You are an agenda design specialist. Based on the research, create a structured 3-day conference agenda structure including: daily themes, session timing, breaks, keynote slots, and parallel tracks. Provide a day-by-day framework in 150 words."
                },
                {
                    "name": "Content Planning",
                    "agent": "Content Strategist",
                    "prompt": "You are a content strategist. Based on the agenda structure, plan specific session topics, speaker recommendations, workshop ideas, and interactive activities for each day. Make it engaging and valuable in 150 words."
                },
                {
                    "name": "Final Review",
                    "agent": "Conference Reviewer",
                    "prompt": "You are a conference quality reviewer. Review the complete conference plan and provide 3 key recommendations for success, potential improvements, and critical success factors. Be concise in 150 words."
                }
            ]
        },
        "marketing": {
            "name": "Marketing Strategy Design",
            "phases": [
                {
                    "name": "Market Analysis",
                    "agent": "Market Analyst",
                    "prompt": "You are a market analyst. Analyze the target market for the product including: customer segments, competitive landscape, market trends, and opportunities. Provide insights in 150 words."
                },
                {
                    "name": "Strategy Development",
                    "agent": "Marketing Strategist",
                    "prompt": "You are a marketing strategist. Based on the market analysis, develop a comprehensive marketing strategy including: positioning, key messages, target channels, and campaign approach. Be strategic in 150 words."
                },
                {
                    "name": "Tactical Planning",
                    "agent": "Marketing Tactician",
                    "prompt": "You are a marketing tactician. Based on the strategy, create specific tactical plans including: content types, social media approach, advertising channels, and promotional activities. Be actionable in 150 words."
                },
                {
                    "name": "Success Metrics",
                    "agent": "Marketing Analyst",
                    "prompt": "You are a marketing analyst. Define success metrics and KPIs for the marketing strategy including: measurement methods, target goals, and evaluation criteria. Be specific in 150 words."
                }
            ]
        },
        "research": {
            "name": "Research Paper Outline",
            "phases": [
                {
                    "name": "Topic Research",
                    "agent": "Research Specialist",
                    "prompt": "You are a research specialist. Research and identify the research topic scope, key questions, existing literature gaps, and significance of the research area. Provide a comprehensive overview in 150 words."
                },
                {
                    "name": "Outline Structure",
                    "agent": "Academic Writer",
                    "prompt": "You are an academic writer. Based on the research, create a structured research paper outline including: abstract, introduction, literature review, methodology, results, discussion, and conclusion sections. Provide a detailed framework in 150 words."
                },
                {
                    "name": "Content Planning",
                    "agent": "Content Planner",
                    "prompt": "You are a content planner. Based on the outline, plan specific content for each section including: key points, data requirements, analysis methods, and expected contributions. Be detailed in 150 words."
                },
                {
                    "name": "Review & Refinement",
                    "agent": "Academic Reviewer",
                    "prompt": "You are an academic reviewer. Review the research paper outline and provide 3 key recommendations for improvement, potential gaps, and academic rigor enhancements. Be constructive in 150 words."
                }
            ]
        },
        "architecture": {
            "name": "Software Architecture Planning",
            "phases": [
                {
                    "name": "Requirements Analysis",
                    "agent": "Systems Analyst",
                    "prompt": "You are a systems analyst. Analyze the software requirements including: functional requirements, non-functional requirements, scalability needs, and technical constraints. Provide a comprehensive analysis in 150 words."
                },
                {
                    "name": "Architecture Design",
                    "agent": "Software Architect",
                    "prompt": "You are a software architect. Based on the requirements, design the software architecture including: system components, technology stack, architectural patterns, and system interactions. Provide a high-level design in 150 words."
                },
                {
                    "name": "Technical Planning",
                    "agent": "Technical Lead",
                    "prompt": "You are a technical lead. Based on the architecture, plan technical implementation details including: database design, API structure, security measures, and deployment strategy. Be technical in 150 words."
                },
                {
                    "name": "Architecture Review",
                    "agent": "Architecture Reviewer",
                    "prompt": "You are an architecture reviewer. Review the software architecture plan and provide 3 key recommendations for improvement, potential risks, and best practices. Be critical in 150 words."
                }
            ]
        }
    }

    def __init__(self, scenario_type="conference", topic=""):
        """
        Initialize the workflow
        
        Args:
            scenario_type: One of "conference", "marketing", "research", "architecture"
            topic: Specific topic or product name for the scenario
        """
        if not Config.validate_setup():
            print("ERROR: Configuration validation failed!")
            exit(1)

        if scenario_type not in self.SCENARIOS:
            print(f"ERROR: Unknown scenario type '{scenario_type}'")
            print(f"Available scenarios: {', '.join(self.SCENARIOS.keys())}")
            exit(1)

        self.client = OpenAI(api_key=Config.API_KEY, base_url=Config.API_BASE)
        self.outputs = {}
        self.model = Config.OPENAI_MODEL
        self.scenario = self.SCENARIOS[scenario_type]
        self.scenario_type = scenario_type
        self.topic = topic

    def run(self):
        """Execute the complete workflow"""
        print("\n" + "="*80)
        print(f"AUTOGEN {self.scenario['name'].upper()} WORKFLOW")
        print("="*80)
        if self.topic:
            print(f"Topic: {self.topic}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Model: {self.model}\n")

        # Execute each phase
        for i, phase in enumerate(self.scenario['phases'], 1):
            self.execute_phase(i, phase)

        # Summary
        self.print_summary()

    def execute_phase(self, phase_num, phase_config):
        """Execute a single phase of the workflow"""
        print("\n" + "="*80)
        print(f"PHASE {phase_num}: {phase_config['name'].upper()}")
        print("="*80)
        print(f"[{phase_config['agent']} is working...]")

        # Build the user message
        user_message = phase_config['prompt']
        
        # Add context from previous phases
        if phase_num > 1:
            context = "\n\nPrevious Phase Results:\n"
            for prev_phase in self.scenario['phases'][:phase_num-1]:
                phase_key = prev_phase['name'].lower().replace(' ', '_')
                if phase_key in self.outputs:
                    context += f"\n{prev_phase['name']}:\n{self.outputs[phase_key]}\n"
            user_message = context + "\n" + user_message

        # Add topic if provided
        if self.topic:
            user_message = f"Topic/Product: {self.topic}\n\n" + user_message

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=Config.AGENT_TEMPERATURE,
            max_tokens=Config.AGENT_MAX_TOKENS,
            messages=[
                {"role": "system", "content": f"You are {phase_config['agent']}. {phase_config['prompt']}"},
                {"role": "user", "content": user_message}
            ]
        )

        phase_key = phase_config['name'].lower().replace(' ', '_')
        self.outputs[phase_key] = response.choices[0].message.content
        
        print(f"\n[{phase_config['agent']} Output]")
        print(self.outputs[phase_key])

    def print_summary(self):
        """Print final summary"""
        print("\n" + "="*80)
        print("FINAL SUMMARY")
        print("="*80)

        print(f"""
This workflow demonstrated a {len(self.scenario['phases'])}-agent collaboration for {self.scenario['name']}:
""")
        for i, phase in enumerate(self.scenario['phases'], 1):
            print(f"{i}. {phase['agent']} - {phase['name']}")

        print("""
Each agent received context from the previous agent's output,
demonstrating the sequential workflow pattern of AutoGen.
""")

        # Print full results
        print("\n" + "="*80)
        print("FULL RESULTS - ALL PHASES")
        print("="*80)
        
        for i, phase in enumerate(self.scenario['phases'], 1):
            phase_key = phase['name'].lower().replace(' ', '_')
            print("\n" + "-"*80)
            print(f"PHASE {i}: {phase['name'].upper()} (Full Output)")
            print("-"*80)
            print(self.outputs[phase_key])

        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"Exercise_4_{self.scenario_type}_{timestamp}.txt"
        with open(output_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write(f"AUTOGEN {self.scenario['name'].upper()} - FULL RESULTS\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: {self.model}\n")
            if self.topic:
                f.write(f"Topic: {self.topic}\n")
            f.write("\n")
            
            for i, phase in enumerate(self.scenario['phases'], 1):
                phase_key = phase['name'].lower().replace(' ', '_')
                f.write("\n" + "-"*80 + "\n")
                f.write(f"PHASE {i}: {phase['name'].upper()}\n")
                f.write("-"*80 + "\n")
                f.write(self.outputs[phase_key] + "\n")
        
        print(f"\n💾 Full results saved to: {output_file}")

        print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)


def main():
    """Main function to run the custom problem workflow"""
    import sys

    # Default scenario
    scenario = "conference"
    topic = ""

    # Parse command line arguments
    if len(sys.argv) > 1:
        scenario = sys.argv[1].lower()
    if len(sys.argv) > 2:
        topic = " ".join(sys.argv[2:])

    # Interactive mode if no arguments
    if len(sys.argv) == 1:
        print("\n" + "="*80)
        print("AUTOGEN CUSTOM PROBLEMS - EXERCISE 4")
        print("="*80)
        print("\nAvailable Scenarios:")
        print("1. conference - Plan a 3-day conference agenda")
        print("2. marketing  - Design a marketing strategy for a product")
        print("3. research   - Create a research paper outline")
        print("4. architecture - Plan a software architecture")
        print()
        
        choice = input("Select scenario (1-4) or name: ").strip().lower()
        
        if choice == "1" or choice == "conference":
            scenario = "conference"
            topic = input("Enter conference topic (e.g., 'AI & Machine Learning'): ").strip()
        elif choice == "2" or choice == "marketing":
            scenario = "marketing"
            topic = input("Enter product name (e.g., 'Smart Home Assistant'): ").strip()
        elif choice == "3" or choice == "research":
            scenario = "research"
            topic = input("Enter research topic (e.g., 'Climate Change Impact'): ").strip()
        elif choice == "4" or choice == "architecture":
            scenario = "architecture"
            topic = input("Enter software project (e.g., 'E-commerce Platform'): ").strip()
        else:
            print(f"Invalid choice. Using default: conference")
            scenario = "conference"

    try:
        workflow = CustomProblemWorkflow(scenario_type=scenario, topic=topic)
        workflow.run()
        print("\n✅ Workflow completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during workflow execution: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Verify OPENAI_API_KEY is set in parent directory .env (../.env)")
        print("2. Check your API key has sufficient credits")
        print("3. Verify internet connection")
        print("4. Ensure config.py can access shared_config from parent directory")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

