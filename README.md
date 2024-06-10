# Code Developed during Databricks Summit in 2024 - LLM Hackathon

 

**Desciption:**

Welcome to the Commodity Trading Assistant repository, where our Language Model (LLM) empowers traders with immediate access to vital pricing information. Say goodbye to time-consuming data collection and hello to swift, accurate insights. Ask what you need - high, low, standard deviation, rolling averages - and get instant answers for your commodity so you can keep trading!

 

**Why did we choose this topic?**

For Commodity Traders operate in high volatility markets where split-second decisions can make a significant impact. They simply don't have the luxury of time to write lengthy code scripts. By integrating an LLM model to assist traders with real-time questions, we alleviate the burden of manual coding. Traders can quickly obtain insights without the need for extensive coding, allowing them to focus on critical decision-making during fast-moving market conditions.

 

**Which open-source LLM and any additional open-source datasets did we use? Explain why**

We chose the DBRX LLM model in conjunction with Databricks. The DBRX LLM model offers versatility in handling a wide range of natural language queries, making it suitable for our project's requirements also leveraging Databricks for data processing and analysis seamlessly integrates with the DBRX LLM model, creating a cohesive workflow.

- Databricks GenAI SDK: is a layer on top of the REST API. It handles low-level details, such as authentication and mapping model IDs to endpoint URLs, making it easier to interact with the models.
- AI-Generated Text: is used for generating quality comments using the assistance of Databricks’ recommendation.
- LLM context (database/tables metadata): generate database/tables context automatically based on the `information_schema` symatic database with Unity-Catalogs.

As a dataset, we have leaveraged the **Crude Oil Prices: West Texas Intermediate - Cushing, Oklahoma** containing WTI spot prices since 1986.

 

**How does the project provide relevant and insightful information to the end user?**

Our integration of the DBRX MML model enables users to interact with the system using natural language queries. This intuitive interface allows traders to ask specific questions about commodity pricing, trends, correlations, and more, without the need for specialized technical knowledge. Whether traders seek information on pricing trends, volatility analysis, or market sentiment, our system delivers precise and relevant insights customized to their needs.

 

 

Developers:

Tung Nguyen

Jonathan Barry

Fernando Crevoculski

 
