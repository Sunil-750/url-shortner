**Words from Sunil**

**1. What did you ask the AI to do, and what did you write or decide yourself?**
- Its essential to understand the current task before explaining Claude. My strategy was here to make a SRS document which clarify the actual functional and non functional requirement. Though it might not have all the necessary information But covers the basic working of the URL shortner.
 - Based on the SRS document I asked to code the requirement. First it was mixing the utils code to main code. Which was the additional hidden requirement for code modularity.


**2. Where did you override, correct, or throw away the AI’s output — and why?**
- Actually I tried using without SRS document because it was not having clear idea of the task, like skope, complexity of the system etc.. So I had to make a centralised requirement document which can be refered by Claude any time and stick to requirements. 

**3. The two or three biggest trade-offs you made, and the alternatives you considered.**
- **In-memory storage vs Persistent database**: We chose in-memory storage for simplicity and fast implementation. This satisfies the MVP requirement but loses all data on application restart. The alternative would be to add a database (PostgreSQL, MongoDB) for persistence.
- **Sequential Base62 generation vs Random 6-character codes**: First I thought of generating it with random number, but thinking of any collision at large scale, I thought it to generate it a number sequentially and convert it into Base62 format.

**4. What's missing, or what you'd do with another day?**
- **Data persistence**: Add a SQLite or PostgreSQL database to survive application restarts, enabling the service to be production-ready.
- **Custom code support**: Allow users to specify custom aliases (e.g., `/shorten` with `custom_code` parameter) with validation to prevent collisions.
- **Expiration mechanism**: Add TTL (time-to-live) for short codes so they automatically expire after a set period.
- **Admin endpoints**: Create endpoints to list all active codes, delete specific codes, or view redirect statistics.


**5. Additional SKILLS.md** :
- This is a Skill md file which is like Behavioral guidelines to reduce common LLM coding mistakes. Everytime I start any task I give clear instructions Claude to use the SKILLS before generating the solution.

