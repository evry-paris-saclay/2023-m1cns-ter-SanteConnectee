# 2023-m2cns-rd-SanteConnectee

This project is part of the TER of M1CNS-SA, progressing during the second semester of the 2023/2024 academic year. For an introduction to the project's theme and its report, please refer to the docs folder.

The purpose of the script here is to establish a Chroma knowledge base via Chroma and utilize API calls to a large language model for automated diagnosis of annotated health data. During the diagnostic process, retrieval-augmented generation methods are employed using the generated Chroma knowledge base.
createCollection is a script to create a knowledge base, it requires a pdf file as input and give a chromaDB base as output.
diagnosis is a script to launch a diagnosis using a model(for example : gpt4.0 or claude3) choosed and knowledge base that you created.
StartPrompts, diagnosisGuidance, formatPrompts are the parts of prompts prewritten.
