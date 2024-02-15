# COMP0022-Movie-Database-CW

## Introduction
This is a coursework project for the COMP0022 module. 
The project provides:
- A dashboard to allow information about movies to be displayed, searched, and  filtered based on different criteria such as genre, release year, ratings, cast and actors, and statistics.
- The ability to analyse how audiences have responded to films that have been  released, and to help predict the market for films that might be produced in the future based on the different ratings of viewers and their varying preferences.

### Project Requirements
1. Visual browsing via a dashboard of film information by title, date, genres, tags, ratings, and any other criteria for which information is available. It should be possible to select what to display and the data should be presented in a usable and visually engaging fashion. You can also make use of additional data and images, such as provided by a site like RoWen Tomatoes or IMBD.
2. Searching for information on a specific film or films in the dataset, including the kind of content, date, director, lead actors and other criteria.
3. Reporting on which are the most popular genres of movies and which are the most polarising genres of movie (mostly rated either high or low by viewers but not in between). Again, making use of additional rating data such as provided by Rotten Tomatoes is allowed.
4. Analysis of viewers’ reaction to a film in relation to their rating history (e.g., did viewers who tend to give low ratings give another film a low rating too), and also by genres (e.g. do viewers who tend to rate sci-fi films highly also rate another genre highly)?
5. Predicting the likely viewer ratings for a soon-to-be-released film based on the tags or ratings for the film provided by a preview panel of viewers drawn from the population of viewers in the database.
6. Analysing the personality traits of viewers who give a film a high or low rating. Using the personality/ratings dataset from GroupLens, examine whether there is a correlation between personality traits (e.g. extrovert) and ratings for the films in the Personality 2018 dataset from Grouplens.org. Using the genres data from the small dataset, is there a correlation between personality traits and preferences for particular genres of film (e.g. horror)?

## Tech Stack

The project is built using the following technologies:

- **Backend API**: [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. FastAPI allows for easy setup of RESTful APIs with automatic interactive API documentation and is known for its high performance.

- **Frontend**: [Next.js](https://nextjs.org/) - An open-source React front-end development web framework that enables functionality such as server-side rendering and generating static websites for React-based web applications. It provides an excellent developer experience with features like fast refresh and built-in CSS support.

- **Database**: [PostgreSQL](https://www.postgresql.org/) - A powerful, open-source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads.

- **Load Balancer/Reverse Proxy**: [Traefik](https://traefik.io/traefik/) - A modern HTTP reverse proxy and load balancer made to deploy microservices with ease. It simplifies networking complexity and configurations with automatic service discovery and dynamic configuration capabilities.

- **Caching Layer**: [Redis](https://redis.io/) - An open-source (BSD licensed), in-memory data structure store, used as a database, cache, and message broker. Redis supports data structures such as strings, hashes, lists, sets, and much more.

- **Containerisation**: [Docker](https://www.docker.com/) - Docker is a set of platform-as-a-service (PaaS) products that use OS-level virtualisation to deliver software in packages called containers. Docker containers can be easily deployed to any machine without facing the typical issues of environment-specific configurations and dependencies.

This combination of technologies provides a robust, scalable, and high-performance foundation for building and deploying our web application efficiently.

## Project Structure Overview

This project is organised into distinct directories and utilises Docker for containerisation, ensuring smooth deployment and development processes. Here's a breakdown of the project's structure:

### Directories

- **`/backend`**: This directory is a Git submodule linking to a separate repository that houses the FastAPI application code. It encompasses all the server-side logic, API endpoints, and dependencies.

- **`/frontend`**: Another Git submodule pointing to its own repository, this directory contains the Next.js application. It includes the client-side interface, styling, and functionality, utilising Next.js for server-side rendering, static site generation, and other performance-enhancing features.

- **`/db`**:
  - **`/scripts`**: Contains SQL initialisation scripts essential for setting up the PostgreSQL database schema and initial datasets. These scripts automate the database preparation process, ensuring a ready-to-use database environment for the application.
  - **Migration Scripts (Planned)**: Anticipated to include migration scripts for managing database schema evolution and updates as the project develops.

### Root Directory Contents

- **`.env`**: Hosts environment variables critical for configuring the entire application stack, including database connections, external API keys, and other configuration details necessary for local development and production environments. This file is not committed and you should create your own `.env` file based on the `.env.example` file.

- **`docker-compose.yml`**: Defines and configures the application's services, networks, and volumes, facilitating the orchestration of the multi-container Docker application. This includes the setup for the backend, frontend, database, and all other services like Redis or Traefik.

- **Git Configuration and Documentation**: The root also contains Git-related files (e.g., `.gitignore`, `.gitmodules`) and project documentation, including this README.md.


## Getting Started

This section outlines the steps to get the project up and running on your local machine for development and testing purposes.

### Requirements

- **Docker**: Ensure you have Docker installed on your machine. If not, you can download and install Docker Desktop from the official website: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Git**: You will need Git to clone the repository and its submodules. If you don't have Git installed, you can download and install it from the official website: [Git](https://git-scm.com/downloads)

### Installation

1. **Clone the repository** with submodules:

   ```bash
   git clone --recurse-submodules https://github.com/SilentHacks/COMP0022-Movie-Database-CW.git
    ```
   
2. **Navigate to the project directory**:
   ```bash
   cd COMP0022-Movie-Database-CW
   ```
   
3. **Set up environment variables**:
   - Create a `.env` file in the root directory based on the `.env.example` file.
   - Update the environment variables in the `.env` file to match your local environment.

4. **Start the application** using Docker Compose:
   ```bash
   docker-compose up --build
   ```
   This command will build and start the application stack, including the backend, frontend, database, and other services.

### Usage

Once the application stack is up and running, you can access the following services:

- **Backend API**: Accessible at `http://localhost:8000/docs` for the interactive API documentation.
- **Frontend**: Accessible at `http://localhost:3000` for the Next.js application.
- **Database**: Accessible at `http://localhost:5432` for the PostgreSQL database.
- **Stop the application**: Run `docker-compose down` to stop and remove the containers.

