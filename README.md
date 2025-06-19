# pcb-sipiemc-chatbot

## Project Description

The primary objective of this project is to develop an AI-powered chatbot system tailored specifically for PCB designers, focusing on Signal Integrity (SI), Power Integrity (PI), and Electromagnetic Compatibility (EMC). Leveraging advanced Natural Language Processing (NLP) techniques and integration with existing Electronic Design Automation (EDA) software environments, the chatbot provides comprehensive support to developers throughout the design process.

### Key Objectives
- Define a functional framework for the chatbot system using **RASA NLU** and neural network methodologies.
- Implement entity extraction, intent recognition, and keyword mapping to enhance chatbot functionality.
- Facilitate seamless interaction between developers and the chatbot, enabling efficient access to domain-specific knowledge and guidance.

This project demonstrates the feasibility and efficacy of AI-powered chatbot systems in enhancing the PCB design workflow.

---

## Video of Result
[docs/Result.webm](docs/Result.webm)

---

## Installation

### Prerequisites
- Python 3 installed  
- For Ubuntu/Debian systems, install the `venv` module:
  ```bash
  sudo apt-get install python3-venv
  ```

### Setup Virtual Environment
```bash
python3 -m venv chatbot
source chatbot/bin/activate  # On Windows: chatbot\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Project

1. Start the RASA server with API enabled and CORS allowed:
   ```bash
   rasa run -m models --enable-api --cors "*"
   ```
2. Run the RASA actions server:
   ```bash
   rasa run actions --cors "*"
   ```
3. Run the LTspice API script:
   ```bash
   python LTspice_API.py
   ```

---

## Debugging and Training

- To train the RASA model:
  ```bash
  rasa train
  ```
- To test the RASA chatbot in shell mode:
  ```bash
  rasa shell
  ```

---

## Sample Queries to Test Chatbot

- Hi
- What factors should be considered when selecting a Decoupling Capacitor?
- Can you list the different types of Decoupling Capacitors?
- What is the formula for the effective impedance of a decoupling capacitor?
- Show me impedance curves of aluminum electrolytic capacitors and polymer capacitors

---

## Documentation

For detailed documentation, please refer to the report:  
[docs/Final_Report___Subgroup_ChatBot.pdf](docs/Final_Report___Subgroup_ChatBot.pdf)

---
