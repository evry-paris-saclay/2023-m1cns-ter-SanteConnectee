# 2023-m2cns-rd-SanteConnectee

This project is part of the TER of M1CNS-SA, progressing during the second semester of the 2023/2024 academic year. 

This project aims to propose a solution based on connected health applications to address the challenges faced by personalized and precision medicine in implementation, particularly concerning the issues of delayed diagnosis and misdiagnosis, especially for delayed diagnosis. The resolution of this problem holds significant potential implications for public health and healthcare system efficiency, as misdiagnosis is a important contributor to iatrogenic harm, while delayed diagnosis poses a high risk of amplifying the health consequences of diseases substantially. The proposed solution has the potential to mitigate unnecessary adverse medical outcomes and protect lives by facilitating timely medical intervention for patients with significant diseases and reducing the occurrence of misdiagnoses. Moreover, the enhancement of accuracy and timeliness in medical diagnostics will significantly contribute to the more efficient operation of the healthcare system, thereby reducing the burden on healthcare professionals. In this project, the design of the solution involves continuous health monitoring in daily life using wearable devices and rapid responses to potential health issues.

Index Terms: Health monitoring, wearable devices, personalized and precision medicine, large language model

<b> Encadrant : Massinissa HAMIDI (massinissa.hamidi@univ-evry.fr) </b>

# Files in this repository

In folder docs you'll find my report and poster for this project, for more information and details, please read the report.

In folder src you'll find scripts written during this project, their function is to establish a Chroma knowledge base via Chroma and utilize API calls to a large language model for automated diagnosis of annotated health data. During the diagnostic process, retrieval-augmented generation methods are employed using the generated Chroma knowledge base. 

createCollection.py is the script to create a knowledge base, it requires a pdf file as input and give a chromaDB base as output.

diagnosis.py is the script to launch a diagnosis using a model(for example : gpt 4.0 or claude 3) choosed and knowledge base that you created.

StartPrompts.txt, diagnosisGuidance.txt, formatPrompts.txt are the parts of prompts prewritten.

API-Key.env is the configuration file for the key of the API to be called.

<b> Considering copyright issues, the original literatures used to build the knowledge base in this project and the knowledge base constructed based on them are not provided here </b>

# to start with scripts provided

<ul>
   <li> The first thing to do is to write your own API-KEY in API-Key.env, here, API services of OpenAI and CLAUDE will be called, so replace "put_your_key_here" in API-Key.env after the corresponding key name with your ownn API key.
   <li> Secondly, you can build your own knowledg base using createCollection.py, the script defaults to using a PDF file named 'knowledge. pdf' in the same directory as input. Please merge the literature to be used for building the knowledge base into one PDF file and change it to this name. Then just run the script by simply:
     `` python  createCollection.py``
     If successful, the script will create a database file for the knowledge base in the same directory after it finishes.
     As mentionned, the documents of original literatures used in my work are not provided here, you can find them on internet or choose any other literatures. The literatures that I used are :
   <ul>
     <li> Tomas B Garcia. 12-lead ECG.
     <li> Jane Huff. ECG Workout Exercises in Arrhythmia Interpretation.
  </ul>
  <li> Now you can try make a diagnosis, for that, create a txt file in the same directory and input the information to be diagnosed. This part of the information should be obtained from the health data of patients collected through annotations by another dedicated model in the proposed solution of this project for testing. It can also be manually entered or randomly generated using LLM. NB: This information should be presented in natural language and should be cut as accurately as possible, avoid using overly concise abbreviations. featurePrompts.txt is an example of such information. 

    By simply: 
    `` python  diagnosis.py``
    run the script, the script will ask to choose the LLM that will be used, then ask the name of input file name, just tape it.
</ul>
