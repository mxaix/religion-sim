import streamlit as st
import random
import pandas as pd

# Agent class
class HumanAgent:
    def __init__(self, religion):
        self.religion = religion
        self.aggression = random.uniform(0, 1)
        self.education = random.uniform(0.3, 0.7)
        self.happiness = 1.0
        self.alive = True

    def interact(self, other):
        if not (self.alive and other.alive) or self is other:
            return
        if self.aggression > 0.7 and random.random() < self.aggression:
            other.alive = False
            self.happiness -= 0.2
        else:
            self.happiness += 0.02
            self.education += 0.01

    def step(self):
        if not self.alive:
            return
        self.education = min(self.education + 0.01, 1.0)
        self.happiness = max(self.happiness - 0.01, 0.0)

def run_simulation(N, religion, steps):
    agents = [HumanAgent(religion) for _ in range(N)]
    records = []
    for _ in range(steps):
        alive_agents = [a for a in agents if a.alive]
        for agent in alive_agents:
            partner = random.choice(alive_agents)
            agent.interact(partner)
            agent.step()

        alive = sum(a.alive for a in agents)
        avg_edu = sum(a.education for a in agents if a.alive) / (alive or 1)
        avg_happy = sum(a.happiness for a in agents if a.alive) / (alive or 1)

        records.append({"Alive": alive, "Avg Education": avg_edu, "Avg Happiness": avg_happy})

    return pd.DataFrame(records)

# Streamlit UI
st.set_page_config(page_title="Global Religion Sim", layout="centered")
st.title("🌍 Global Religion Simulation")

religion = st.selectbox("Choose a religion for all agents:", [
    "Islam", "Christianity", "Judaism", "Buddhism", "Hinduism", "Atheism"
])
population = st.slider("Population size:", min_value=100, max_value=5000, value=1000, step=100)
steps = st.slider("Number of simulation steps:", min_value=10, max_value=200, value=100, step=10)

if st.button("Run Simulation"):
    with st.spinner("Running..."):
        df = run_simulation(population, religion, steps)
    st.subheader("📈 Results")
    st.line_chart(df)
    st.success("Simulation complete!")