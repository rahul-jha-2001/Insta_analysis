CreatorInsight is your comprehensive tool for managing and analyzing creator data. This application provides a centralized platform to track, analyze, and manage information about content creators across various platforms.

Our application consists of five main components:

Creator Dictionary:

Overview: Browse our extensive database of creators. This page displays a table with creator names and key statistics, giving you a quick overview of our tracked creators.
Key Features: Search and filter creators, view summary statistics, and quickly access essential information.
Creator Detail:

In-Depth Analysis: Dive deep into individual creator profiles. Select a specific creator to view detailed information, including performance metrics, content analysis, and historical data.
Key Features: View detailed performance metrics, analyze content trends, and access historical data for comprehensive insights.
Creator to Scan:

Management: View and manage the list of creators scheduled for data collection and analysis. This page helps you keep track of which creators are in the pipeline for updates.
Key Features: Add or remove creators from the scan list, view scan status, and manage the data collection schedule.
Workflow:

Process Monitoring: Monitor and control the status of ongoing data collection and analysis processes. This page provides real-time updates on various workflows and allows you to manage these processes efficiently.
Key Features: View workflow status, manage ongoing processes, and ensure efficient data collection and analysis.
Main Page (You are here):

Central Hub: Your central hub for navigating the application and accessing key information at a glance.
Key Features: Overview of the application, quick access to main components, and navigation menu for easy exploration.


Sure! Here's a step-by-step guide on how to run the program on your system:

---

### How to Run the Program

To run the program on your system, follow these steps:

1. **Clone the Repository**:
   First, you need to pull the code from the repository. Open your terminal and execute the following command:
   ```bash
   git clone [repository-url]
   ```
   Replace `[repository-url]` with the actual URL of the repository.

2. **Navigate to the Project Directory**:
   Change your directory to the project directory:
   ```bash
   cd [project-directory]
   ```
   Replace `[project-directory]` with the actual name of the project directory.

3. **Run Docker Compose**:
   The project uses Docker to containerize the application. To run the program, you need to execute the Docker Compose file. Run the following command in your terminal:
   ```bash
   docker-compose up
   ```

4. **Access the Application**:
   Once the Docker containers are up and running, you can access the application in your web browser. By default, the application should be available at:
   ```
   http://localhost:8501
   ```

### Summary of Commands

```bash
git clone [repository-url]
cd [project-directory]
docker-compose up
```

### Notes

- Ensure Docker and Docker Compose are installed on your system before running these commands.
- If there are any environment variables or configurations needed, make sure to set them up as specified in the project documentation.

By following these steps, you'll be able to run the CreatorInsight application on your system and start exploring its features.

---
