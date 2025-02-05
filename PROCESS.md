# My Process

## AI Usage

I leaned on two main AI tools throughout this project:

1. **ChatGPT**: This was a huge help in brainstorming, refining my approach, and troubleshooting issues. Since I haven’t built a Python project from scratch in a while, I used it to get up to speed quickly on best practices and it also helped me think through the data model and API design, acting as a sounding board for my ideas.

2. **GitHub Copilot**: This sped up development significantly by handling boilerplate code and generating test cases. I’ve been using Copilot for a while now, and it’s great for reducing repetitive tasks. While it's not magic, it definitely helps with getting things up and running faster.

## General Approach

### Setting Up the Project
I chose FastAPI as the web framework because it’s lightweight and has great built-in support for OpenAPI docs. Postgres was my database of choice due to its reliability and strong support.

To keep things manageable, I set up Docker and Docker Compose early on. This ensures that everything runs in a consistent environment and makes it easy for someone else to spin up the project quickly.

### Defining the Data Model and API Endpoints
I started with a rough schema based on the requirements and iterated a number of times as I went. The goal was to keep data normalized and efficient while allowing for flexible queries.

For API design, I prioritized small, composable endpoints that could be combined for more complex queries, making the system more flexible and easier to extend, to avoid over-fetching data, and to keep the API responses fast.

### Testing and Validating the API
I wrote a suite of API tests to validate the core functionality, though I’m not really satisfied with them. If this were a long-term project, I’d go back and:

- Improve test data management to make sure edge cases (like multiple shipping addresses per order) are covered.
- Add more integration tests to simulate real-world API usage.
