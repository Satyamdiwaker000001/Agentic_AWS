from utils.generate import generate_response
from prompts.general_prompt import GENERAL_PROMPT


# ─── Professional knowledge base for instant, high-quality responses ───
KNOWLEDGE_BASE = {
    "e=mc": {
        "response": (
            "## Einstein's Mass-Energy Equivalence: E = mc²\n\n"
            "**E = mc²** is one of the most famous equations in physics, formulated by Albert Einstein in 1905 as part of his Special Theory of Relativity.\n\n"
            "### What It Means\n"
            "- **E** = Energy (measured in Joules)\n"
            "- **m** = Mass (measured in kilograms)\n"
            "- **c** = Speed of light in vacuum (≈ 3 × 10⁸ m/s)\n\n"
            "### Key Insight\n"
            "Mass and energy are **interchangeable**. A small amount of mass can be converted into an enormous amount of energy because *c²* is an extremely large number (~9 × 10¹⁶).\n\n"
            "### Real-World Applications\n"
            "1. **Nuclear Fission** — Splitting uranium atoms releases energy (nuclear power plants)\n"
            "2. **Nuclear Fusion** — Combining hydrogen nuclei in stars produces sunlight\n"
            "3. **PET Scans** — Medical imaging uses positron-electron annihilation\n"
            "4. **Particle Accelerators** — Converting kinetic energy into new particles at CERN\n\n"
            "### Example Calculation\n"
            "If 1 kg of matter is fully converted to energy:\n"
            "E = 1 × (3 × 10⁸)² = **9 × 10¹⁶ Joules** — enough to power a city for years."
        ),
        "keywords": ["e=mc", "emc2", "mass energy", "einstein equation", "mass-energy"]
    },
    "polarity": {
        "response": (
            "## Polarity in Chemistry & Physics\n\n"
            "**Polarity** refers to the uneven distribution of electrical charge in a molecule or bond.\n\n"
            "### Types of Polarity\n\n"
            "#### 1. Bond Polarity\n"
            "When two atoms with **different electronegativities** share electrons unequally:\n"
            "- **Polar bond**: Electrons pulled toward more electronegative atom (e.g., H-Cl)\n"
            "- **Non-polar bond**: Electrons shared equally (e.g., O=O, H-H)\n\n"
            "#### 2. Molecular Polarity\n"
            "Depends on both bond polarity AND molecular geometry:\n"
            "- **Water (H₂O)**: Polar — bent shape, dipole moments don't cancel\n"
            "- **CO₂**: Non-polar — linear shape, dipole moments cancel out\n\n"
            "### Why Polarity Matters\n"
            "- **Solubility**: \"Like dissolves like\" — polar solvents dissolve polar solutes\n"
            "- **Boiling points**: Polar molecules have higher boiling points due to stronger intermolecular forces\n"
            "- **Biological membranes**: Cell membranes use non-polar lipid bilayers to control what enters/exits cells"
        ),
        "keywords": ["polarity", "polar", "nonpolar", "electronegativity", "dipole"]
    },
    "ai": {
        "response": (
            "## Artificial Intelligence (AI)\n\n"
            "**Artificial Intelligence** is the simulation of human intelligence by computer systems. It encompasses learning, reasoning, problem-solving, perception, and language understanding.\n\n"
            "### Types of AI\n\n"
            "| Type | Description | Example |\n"
            "|------|-------------|--------|\n"
            "| **Narrow AI (ANI)** | Specialized in one task | Siri, Chess engines |\n"
            "| **General AI (AGI)** | Human-level reasoning across domains | Hypothetical |\n"
            "| **Super AI (ASI)** | Surpasses human intelligence | Theoretical |\n\n"
            "### Key Subfields\n"
            "1. **Machine Learning** — Systems that learn from data patterns\n"
            "2. **Deep Learning** — Neural networks with many layers (CNNs, Transformers)\n"
            "3. **Natural Language Processing (NLP)** — Understanding and generating human language\n"
            "4. **Computer Vision** — Interpreting images and video\n"
            "5. **Reinforcement Learning** — Learning through trial-and-error rewards\n\n"
            "### Current Applications\n"
            "- Healthcare diagnostics, autonomous vehicles, language translation, recommendation systems, fraud detection, and creative content generation."
        ),
        "keywords": ["artificial intelligence", "what is ai", "explain ai", "about ai", "types of ai"]
    },
    "machine learning": {
        "response": (
            "## Machine Learning (ML)\n\n"
            "**Machine Learning** is a subset of AI where systems learn patterns from data without being explicitly programmed.\n\n"
            "### Three Types of Learning\n\n"
            "#### 1. Supervised Learning\n"
            "- **Input**: Labeled data (features + correct answers)\n"
            "- **Goal**: Learn mapping from input → output\n"
            "- **Examples**: Spam detection, image classification, price prediction\n"
            "- **Algorithms**: Linear Regression, Decision Trees, Random Forest, SVM, Neural Networks\n\n"
            "#### 2. Unsupervised Learning\n"
            "- **Input**: Unlabeled data (only features)\n"
            "- **Goal**: Discover hidden patterns or groupings\n"
            "- **Examples**: Customer segmentation, anomaly detection\n"
            "- **Algorithms**: K-Means, DBSCAN, PCA, Autoencoders\n\n"
            "#### 3. Reinforcement Learning\n"
            "- **Input**: Environment with rewards/penalties\n"
            "- **Goal**: Learn optimal strategy through trial-and-error\n"
            "- **Examples**: Game AI (AlphaGo), robotics, trading bots\n"
            "- **Algorithms**: Q-Learning, PPO, DQN\n\n"
            "### ML Pipeline\n"
            "Data Collection → Preprocessing → Feature Engineering → Model Training → Evaluation → Deployment"
        ),
        "keywords": ["machine learning", "ml", "supervised", "unsupervised", "reinforcement learning"]
    },
    "newton": {
        "response": (
            "## Newton's Laws of Motion\n\n"
            "Sir Isaac Newton formulated three fundamental laws that describe the relationship between forces acting on an object and its motion.\n\n"
            "### First Law (Law of Inertia)\n"
            "An object at rest stays at rest, and an object in motion stays in motion at constant velocity, **unless acted upon by a net external force**.\n"
            "- Example: A ball on a table won't move unless pushed\n\n"
            "### Second Law (F = ma)\n"
            "The acceleration of an object is directly proportional to the net force and inversely proportional to its mass.\n"
            "- **F = ma** (Force = Mass × Acceleration)\n"
            "- Example: Pushing a heavier cart requires more force for the same acceleration\n\n"
            "### Third Law (Action-Reaction)\n"
            "For every action, there is an **equal and opposite reaction**.\n"
            "- Example: A rocket expels gas downward (action), propelling itself upward (reaction)\n"
            "- Swimming: You push water backward, water pushes you forward"
        ),
        "keywords": ["newton", "laws of motion", "newton's laws", "first law", "second law", "third law", "inertia"]
    },
    "python": {
        "response": (
            "## Python Programming Language\n\n"
            "**Python** is a high-level, interpreted, general-purpose programming language created by Guido van Rossum in 1991.\n\n"
            "### Key Features\n"
            "- **Simple Syntax**: Readable, uses indentation instead of braces\n"
            "- **Dynamically Typed**: No need to declare variable types\n"
            "- **Interpreted**: Runs line-by-line, no compilation needed\n"
            "- **Multi-paradigm**: Supports OOP, functional, and procedural styles\n\n"
            "### Popular Use Cases\n"
            "| Domain | Libraries/Frameworks |\n"
            "|--------|--------------------|\n"
            "| Web Development | Django, Flask, FastAPI |\n"
            "| Data Science | Pandas, NumPy, Matplotlib |\n"
            "| Machine Learning | TensorFlow, PyTorch, scikit-learn |\n"
            "| Automation | Selenium, BeautifulSoup |\n"
            "| API Development | FastAPI, Flask |\n\n"
            "### Why Python is Popular\n"
            "1. Beginner-friendly with gentle learning curve\n"
            "2. Massive ecosystem of 400,000+ packages on PyPI\n"
            "3. Strong community support and documentation\n"
            "4. Used by Google, Netflix, Instagram, and NASA"
        ),
        "keywords": ["python", "python language", "what is python", "python programming"]
    },
    "gravity": {
        "response": (
            "## Gravity — The Universal Force\n\n"
            "**Gravity** is a fundamental force of nature that attracts any two objects with mass toward each other.\n\n"
            "### Newton's Law of Universal Gravitation\n"
            "**F = G × (m₁ × m₂) / r²**\n\n"
            "Where:\n"
            "- F = Gravitational force between two objects\n"
            "- G = Gravitational constant (6.674 × 10⁻¹¹ N⋅m²/kg²)\n"
            "- m₁, m₂ = Masses of the two objects\n"
            "- r = Distance between their centers\n\n"
            "### Key Facts\n"
            "- **g on Earth** = 9.8 m/s² (acceleration due to gravity)\n"
            "- **g on Moon** = 1.62 m/s² (about 1/6 of Earth)\n"
            "- **g on Jupiter** = 24.79 m/s²\n\n"
            "### Einstein's General Relativity\n"
            "Einstein redefined gravity not as a force, but as a **curvature of spacetime** caused by mass and energy. Massive objects like the Sun curve spacetime, and planets follow these curved paths (geodesics)."
        ),
        "keywords": ["gravity", "gravitational", "gravitation", "g force"]
    },
}


def _find_knowledge_response(query_lower):
    """Search knowledge base for matching topics."""
    for topic, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword in query_lower:
                return data["response"]
    return None


def general_agent(state):
    message = state["message"]
    query_lower = message.lower()

    # 1. Check knowledge base for instant, professional responses
    knowledge_response = _find_knowledge_response(query_lower)
    if knowledge_response:
        return {"response": knowledge_response}

    # 2. Fallback to Qwen model for unknown queries
    prompt = GENERAL_PROMPT + "\n" + message
    answer = generate_response(prompt)

    return {"response": answer}