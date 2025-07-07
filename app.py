import streamlit as st
import matplotlib.pyplot as plt
import random

# UI: Title and religion choice
st.title("🌍 Global Religion Simulation")
religion = st.selectbox("Choose a religion to simulate:", ["Islam", "Christianity", "Judaism", "Buddhism", "Hinduism", "Atheism"])
adherence = st.slider("Religious adherence (%):", min_value=0, max_value=100, value=80)
N = st.slider("Population Size:", min_value=100, max_value=10000, value=1000)
steps = st.slider("Simulation Steps:", min_value=10, max_value=200, value=100)

# Agent class
class HumanAgent:
    def __init__(self, religion, adherence):
        self.religion = religion
        self.adherence = adherence / 100
        self.aggression = max(0.1, 1.0 - self.adherence)
        self.education = 0.3 + 0.5 * self.adherence
        self.happiness = 0.5 + 0.4 * self.adherence
        self.alive = True

    def interact(self, other):
        if not other.alive or not self.alive:
            return
        if self.aggression > 0.8 and random.random() < 0.02:
            other.alive = False
            self.happiness -= 0.05
        else:
            self.happiness += 0.03
            self.education += 0.01

# Run simulation
if st.button("Run Simulation"):
    agents = [HumanAgent(religion, adherence) for _ in range(N)]

    alive_over_time = []
    avg_edu = []
    avg_happy = []

    for _ in range(steps):
        for a in agents:
            if a.alive:
                other = random.choice(agents)
                a.interact(other)

        alive = sum(1 for a in agents if a.alive)
        edu = sum(a.education for a in agents if a.alive) / alive if alive > 0 else 0
        happy = sum(a.happiness for a in agents if a.alive) / alive if alive > 0 else 0

        alive_over_time.append(alive)
        avg_edu.append(edu)
        avg_happy.append(happy)

    # Plot results
    st.subheader("📊 Results")
    fig, ax = plt.subplots()
    ax.plot(alive_over_time, label="Alive", color='blue')
    ax.plot(avg_edu, label="Avg Education", color='skyblue')
    ax.plot(avg_happy, label="Avg Happiness", color='red')
    ax.legend()
    st.pyplot(fig)