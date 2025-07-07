import streamlit as st
import random
import matplotlib.pyplot as plt

RELIGION_TRAITS = {
    "Islam": {"agg_mod": 0.6, "edu_mod": 1.1, "happy_mod": 1.0},
    "Christianity": {"agg_mod": 0.7, "edu_mod": 1.0, "happy_mod": 1.0},
    "Judaism": {"agg_mod": 0.5, "edu_mod": 1.2, "happy_mod": 0.9},
    "Buddhism": {"agg_mod": 0.3, "edu_mod": 0.9, "happy_mod": 1.3},
    "Hinduism": {"agg_mod": 0.7, "edu_mod": 1.0, "happy_mod": 1.0},
    "Atheism": {"agg_mod": 0.8, "edu_mod": 1.3, "happy_mod": 0.8}
}

class HumanAgent:
    def __init__(self, adherence, traits):
        self.alive = True
        self.adherence = adherence
        self.traits = traits
        self.aggression = 0.5 * (1 - adherence) * traits["agg_mod"]
        self.happiness = min(1.0, max(0.0, (0.5 + 0.4 * adherence) * traits["happy_mod"]))
        self.education = 0.5 * traits["edu_mod"]

        self.aggression *= random.uniform(0.8, 1.2)
        self.happiness *= random.uniform(0.8, 1.2)
        self.education *= random.uniform(0.8, 1.2)

    def interact(self, other):
        if not self.alive or not other.alive:
            return

        if random.random() < self.aggression * 0.05:
            if random.random() < 0.5:
                other.alive = False
                self.happiness -= 0.1
            else:
                self.happiness -= 0.05
        else:
            self.happiness += 0.1 * self.adherence * self.traits["happy_mod"]
            self.education += 0.05 * self.adherence * self.traits["edu_mod"]

        self.happiness = min(1.0, max(0.0, self.happiness))
        self.education = min(1.0, max(0.0, self.education))

# Streamlit UI
st.title("🌍 Humanity Simulation Under Religious Systems")

religion = st.selectbox("Choose a Religion", list(RELIGION_TRAITS.keys()))
adherence = st.slider("Adherence Level", 0.0, 1.0, 0.8)
population_size = st.slider("Population Size", 100, 5000, 1000)
steps = st.slider("Simulation Steps", 50, 500, 200)

if st.button("Run Simulation"):
    traits = RELIGION_TRAITS[religion]
    agents = [HumanAgent(adherence, traits) for _ in range(population_size)]

    population_data = []
    happiness_data = []
    education_data = []

    for _ in range(steps):
        for agent in agents:
            other = random.choice(agents)
            agent.interact(other)

        alive_agents = [a for a in agents if a.alive]
        pop = len(alive_agents)
        avg_happy = sum(a.happiness for a in alive_agents) / pop if pop > 0 else 0
        avg_edu = sum(a.education for a in alive_agents) / pop if pop > 0 else 0

        population_data.append(pop)
        happiness_data.append(avg_happy)
        education_data.append(avg_edu)

    st.subheader("📈 Simulation Results")

    fig, ax = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
    ax[0].plot(population_data, label="Population")
    ax[0].set_ylabel("Alive Humans")
    ax[0].legend()

    ax[1].plot(happiness_data, label="Avg Happiness", color='green')
    ax[1].set_ylabel("Happiness")
    ax[1].legend()

    ax[2].plot(education_data, label="Avg Education", color='purple')
    ax[2].set_ylabel("Education")
    ax[2].set_xlabel("Time Step")
    ax[2].legend()

    st.pyplot(fig)