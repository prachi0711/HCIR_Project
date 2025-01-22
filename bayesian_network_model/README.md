# Bayesian Network Model

## Objective:

The purpose of this model is to provide career recommendations by utilizing probabilistic reasoning. The system considers user preferences as input and outputs the most likely career option based on the Bayesian Network’s inference.

---

## 1. Components of the Network

The Bayesian Network in this project is composed of the following components:

- **User Preferences:** 
  - **Interest:** Represents the user's interest in a specific field (Science, Arts, or Technology).
  - **Skill:** Represents the user's skill level (Analytical, Creative, or Communicative).
  - **Background:** Represents the user's educational background (STEM, Humanities, or Commerce).
  - **Lifestyle:** Represents the user's preferred lifestyle (Flexible, Fixed Hours, or Traveling).
- **Career Choices:**
  - **Career:** Represents the possible career options (Data Scientist, Writer, or Manager).

Each of these nodes is a **LabelizedVariable** where the values are discrete, and each variable has three possible outcomes, represented as integers (0, 1, 2).

---

## 2. Relationships and Dependencies

In a Bayesian Network, relationships are defined by **directed edges (arcs)** between nodes, indicating dependency or influence between variables. In this network, the relationships and dependencies are as follows:

- **Interest → Career:** The user's interest in a particular field (Science, Arts, or Technology) directly influences the possible career options they may pursue.
- **Skill → Career:** The user's skill level (Analytical, Creative, or Communicative) also has a direct impact on career recommendations.
- **Background → Career:** The user's educational background (STEM, Humanities, or Commerce) is another factor influencing career choices.
- **Lifestyle → Career:** The user's preferred lifestyle (Flexible, Fixed Hours, or Traveling) affects the recommended career options.

These dependencies are encoded in the structure of the Bayesian Network, where **Career** is the child node of the other four variables (Interest, Skill, Background, and Lifestyle), implying that Career depends on these four variables.

---

## 3. Conditional Probability Table (CPT)

The Conditional Probability Table (CPT) defines the probability of each possible outcome for a node, given the values of its parent nodes. For each variable in the network (Interest, Skill, Background, Lifestyle), a prior probability distribution is defined. 

For example:
- The **CPT for Interest** might define the probability distribution of the user's interest in Science, Arts, or Technology, with values such as:
  - Interest = Science (0.4), Arts (0.3), Technology (0.3).
  
- The **CPT for Skill** defines the probability distribution for the user's skill type, e.g.:
  - Skill = Analytical (0.3), Creative (0.4), Communicative (0.3).

For the **Career** variable, the CPT defines the probabilities of each career option (Data Scientist, Writer, or Manager) based on different combinations of the values for **Interest**, **Skill**, **Background**, and **Lifestyle**. These probabilities are assigned manually, reflecting how likely each career is given different combinations of user preferences.

For example:
- If the user’s interest is in Science, their skill level is Analytical, and their background is in STEM, the probability of them being recommended as a **Data Scientist** might be very high (e.g., 0.9), with lower probabilities for Writer and Manager (e.g., 0.05 each).

--- 

## 4. Inference Process

The inference process in a Bayesian Network is the calculation of the posterior probabilities of certain variables, given evidence (observed values) for other variables. The process involves updating the probabilities of the **Career** node based on the user’s inputs (the evidence provided for Interest, Skill, Background, and Lifestyle).

### Steps of Inference:

1. **Set Evidence:** The user’s preferences for Interest, Skill, Background, and Lifestyle are input as evidence. These inputs set the values for the corresponding nodes in the network.

2. **Make Inference:** Once the evidence is set, the Bayesian Network calculates the posterior probability distribution for the **Career** node. This process uses the dependencies and CPTs defined in the network to propagate the evidence through the network and calculate the likelihood of each career option.

3. **Rank Career Options:** After inference, the system outputs the posterior probabilities for each career option (Data Scientist, Writer, Manager). These probabilities are used to rank the careers in order of likelihood, with the most probable career being the highest ranked.

The **LazyPropagation** algorithm in pyAgrum is used for efficient inference. It ensures that the network is updated and the posterior probabilities are computed accurately, given the observed evidence.
