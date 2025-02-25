import streamlit as st
from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv
load_dotenv()

# Set up Streamlit page configuration
st.set_page_config(page_title="Project Planning Assistant", layout="wide")
st.title("Project Planning Assistant")

# Input field for topic
topic = st.text_input("Enter your project topic:", "Build Todo App in reactjs")

# Create button to trigger the analysis
if st.button("Generate Plan"):
    with st.spinner("Generating project plan... This may take a few minutes."):
        llm_model = LLM(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        epicAgent = Agent(
            name="epicAgent",
            role="epicAgent",
            llm=llm_model,
            goal=f"Create a list of user stories from the {topic}",
            backstory="You are an expert in wrtiting user stories. These user stories is to be used to create a project plan. You are skilled in subdividing the requirements into smaller user stories. You are also skilled in allocating time to each user story.",
            allow_delegation=False,
            verbose=True,
        )

        projectPlanAgent = Agent(
            name="projectPlanAgent",
            role="projectPlanAgent",
            llm=llm_model,
            goal=f"Create a project plan for the {topic}",
            backstory="You are an expert in creating project plans. You are skilled in allocating time to each user story. You are also skilled in allocating resources to each user story.",
            verbose=True,
        )  

        UserStories = Task(
            description = f"1. create list of user stories from the {topic}",
            expected_output = "A list of user stories.",
            agent = epicAgent
        )

        projectPlan = Task(
            description = "1. create project plan from the user stories.",
            expected_output = "A project plan with a time and resource allocation.",
            agent = projectPlanAgent
        )

        crew = Crew(
            agents=[epicAgent, projectPlanAgent],
            tasks=[UserStories, projectPlan],
            verbose=True
        )

        # Execute the crew and display results
        result = crew.kickoff()
        
        # Display results in separate sections
        st.header("Generated Plan")
        
        # Convert the result to a more readable format
        try:
            # Assuming the result contains both user stories and project plan
            st.subheader("User Stories")
            user_stories = result.split("Project Plan")[0]
            st.text_area("", user_stories, height=300)
            
            st.subheader("Project Plan")
            project_plan = "Project Plan" + result.split("Project Plan")[1]
            st.text_area("", project_plan, height=300)
        except:
            # Fallback if the splitting doesn't work
            st.text_area("", result, height=600)

# Add some helpful information at the bottom
st.markdown("---")
st.markdown("### How to use:")
st.markdown("""
1. Enter your project topic in the text field
2. Click 'Generate Plan' to create user stories and project plan
3. Wait for the AI agents to generate the plan
""")
