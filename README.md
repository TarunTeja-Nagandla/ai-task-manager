# 🤖 AI-Powered Task Manager

An intelligent, natural language task management web application powered by **LangChain**, **LangGraph**, **Streamlit**, and **SQLAlchemy 2.0**. This application enables users to manage their to-do lists conversationally using natural language prompts while persisting data in a local **SQLite** database.

---

## 🏗️ Architecture Overview

The system follows a modular 3-tier architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit UI                           │
│                        (app.py)                             │
└──────────────────────────────┬──────────────────────────────┘
                               │ User Input / Query
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  LangChain / LangGraph Agent                │
│                        (agent.py)                           │
│  - System Prompt & Date Context                             │
│  - Memory Checkpointer (InMemorySaver)                      │
└──────────────────────────────┬──────────────────────────────┘
                               │ Tool Invocations
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       Agent Tools                           │
│                        (tools.py)                           │
│  - create_tasks | list_tasks | update_tasks | delete_tasks │
└──────────────────────────────┬──────────────────────────────┘
                               │ SQLAlchemy 2.0 ORM
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     SQLite Database                         │
│                    (database.py / tasks.db)                 │
└─────────────────────────────────────────────────────────────┘
```

1. **User Interface (`app.py`)**: Built with Streamlit, providing a clean chat interface, session history state, and sidebar controls.
2. **AI Agent Layer (`agent.py`)**: Powered by `ChatGroq` (`gpt-oss-120b`) and `create_agent` from LangChain/LangGraph. Integrates dynamic date context, custom markdown output formatting, proactive task completion detection, and `InMemorySaver` checkpointer memory.
3. **Tool Execution Layer (`tools.py`)**: Implements `@tool` standard interfaces for CRUD actions on the database.
4. **Database & Persistence (`database.py`)**: Implements SQLAlchemy 2.0 Declarative Mapping for the `Task` ORM model stored in `tasks.db`.

---

## 🛠️ Key Technologies Used

| Technology | Role & Usage |
| :--- | :--- |
| **[Python 3.10+](https://www.python.org/)** | Primary programming language |
| **[Streamlit](https://streamlit.io/)** | Interactive Web UI and chat frontend framework |
| **[LangChain](https://www.langchain.com/)** | LLM tooling framework (`@tool` integration) |
| **[LangGraph](https://langchain-ai.github.io/langgraph/)** | Agent state graph management & checkpointer memory (`create_agent`, `InMemorySaver`) |
| **[LangChain Groq](https://pypi.org/project/langchain-groq/)** | LLM connection wrapper (`ChatGroq` using `gpt-oss-120b`) |
| **[SQLAlchemy 2.0](https://www.sqlalchemy.org/)** | Modern ORM database toolkit and object mapper |
| **[SQLite](https://www.sqlite.org/)** | Embedded relational database backend (`tasks.db`) |
| **[python-dotenv](https://pypi.org/project/python-dotenv/)** | Environment variable management for API keys and endpoints |
| **[Docker](https://www.docker.com/) & Docker Compose** | Containerized packaging, deployment, and persistent volume management |

---

## 📁 Project Structure

```
AI_Task_Manager/
├── app.py              # Streamlit entry point & web interface
├── agent.py            # AI Agent initialization, system prompt & query execution logic
├── tools.py            # LangChain tools mapping natural language actions to database operations
├── database.py         # SQLAlchemy engine configuration, Task ORM model, and DB initializer
├── requirements.txt    # Project Python dependencies
├── Dockerfile          # Container image definition for the Streamlit application
├── docker-compose.yaml # Multi-container / volume orchestration configuration
├── .dockerignore       # Files excluded from the Docker build context
├── .env                # Environment configuration (API keys)
└── tasks.db            # SQLite database storing tasks and metadata
```

### File Breakdown

- **app.py**: Configures the Streamlit page layout, manages `st.session_state` chat messages, handles user query submission, and features a chat history reset sidebar button.
- **agent.py**: Defines the system prompt with strict guidelines for markdown table formatting, date calculation, status mapping, and automatic completion detection.
- **tools.py**: Exposes four main agent tools:
  - `create_tasks`: Create a task with title, description, priority (`low`, `medium`, `high`), and optional due date.
  - `list_tasks`: Retrieve tasks filtered by `status` and `priority`.
  - `update_tasks`: Update task title, description, status (`pending`, `in_progress`, `done`), priority, or due date by `task_id`.
  - `delete_tasks`: Permanently delete a task by `task_id`.
- **database.py**: Sets up the SQLAlchemy connection (configurable via `DATABASE_URL`, defaulting to `sqlite:///tasks.db`), defines the `Task` ORM class targeting the `todos` table, and provides `init_db()`.
- **requirements.txt**: Lists all required Python packages.
- **Dockerfile**: Builds a `python:3.11-slim` container image, installs dependencies, creates `/app/data`, configures a Streamlit health check, and launches the app on port `8501`.
- **docker-compose.yaml**: Runs the `ai-task-manager` service on port `8501`, loads environment variables from `.env`, sets `DATABASE_URL=sqlite:///data/tasks.db`, and mounts the persistent `tasks_data` volume to `/app/data`.
- **.dockerignore**: Excludes `.env`, local virtual environments, git files, and local `.db` files from the Docker build context.

---

## 📊 Database Schema (`todos` table)

The SQLite database table `todos` is modeled via SQLAlchemy in `database.py`:

| Column Name | Type | Description | Default / Constraints |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | Unique primary key | Auto-increment |
| `title` | `String(200)` | Task title | Required |
| `description` | `String(500)` | Additional details/notes | Empty string `""` |
| `status` | `String(20)` | Task status (`pending`, `in_progress`, `done`) | `"pending"` |
| `priority` | `String(20)` | Priority level (`low`, `medium`, `high`) | `"medium"` |
| `due_date` | `Date` | Target completion date (`YYYY-MM-DD`) | `Nullable` |
| `created_at` | `DateTime` | Timestamp of task creation | `func.now()` |

---

## 🚀 Setup & Installation Instructions

Follow these steps to set up and run the application locally:

### 1. Prerequisites

Ensure you have Python 3.10 or higher installed on your machine:
```bash
python --version
```

### 2. Clone / Open Project Directory

Navigate to the project root directory:
```bash
cd AI_Task_Manager
```

### 3. Create & Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install all required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create or edit the `.env` file in the root directory and specify your LLM configuration:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **Note:** Obtain your API key from the [Groq Console](https://console.groq.com/). Avoid spaces around `=` or quotes if you plan to pass `.env` to Docker / Docker Compose.

---

## 🏃 Running the Application

### Option 1: Run Locally with Python

To start the Streamlit web application server locally, run:

```bash
streamlit run app.py
```

Once executed, Streamlit will launch the web interface in your default browser at:
- **Local URL**: `http://localhost:8501`

### Option 2: Run with Docker Compose (Recommended for Containers)

Ensure [Docker](https://docs.docker.com/get-docker/) and Docker Compose are installed, and that your `.env` file is created in the project root.

1. **Build and start the container:**
   ```bash
   docker compose up --build
   ```
   *(Add `-d` to run in detached/background mode: `docker compose up -d --build`)*

2. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`.

3. **Stop the container:**
   ```bash
   docker compose down
   ```
   > **Note:** Your SQLite database is persisted in the `tasks_data` Docker volume (`/app/data/tasks.db`). To also remove the stored database volume, run `docker compose down -v`.

### Option 3: Run with Standalone Docker

If you prefer using the `Dockerfile` directly without Docker Compose:

```bash
# Build the image
docker build -t ai-task-manager .

# Run the container
docker run -d -p 8501:8501 --env-file .env --name ai-task-manager ai-task-manager
```

---

## 💬 Usage Examples

Once the server is running, you can interact with the assistant using natural language prompts:

### 1. Creating Tasks
- *"Add a task to buy groceries tomorrow with high priority"*
- *"Create a task named 'Prepare Presentation' with description 'Slides for team sync' due on 2026-08-15"*

### 2. Listing & Filtering Tasks
- *"Show all my pending tasks"*
- *"List high priority tasks"*
- *"What tasks do I have?"*

### 3. Updating Tasks
- *"Mark task 1 as done"*
- *"Change priority of task 2 to low"*
- *"Update task 3 status to in progress"*

### 4. Smart Proactive Completion
- *"I bought the groceries"* *(automatically updates matching pending task status to `done`)*

### 5. Deleting Tasks
- *"Delete task 3"*

---

## 📜 Available Commands Summary

| Command | Purpose |
| :--- | :--- |
| `pip install -r requirements.txt` | Install project dependencies |
| `streamlit run app.py` | Launch the Streamlit development web server |
| `python -c "from database import init_db; init_db()"` | Manually initialize the SQLite database table |
| `docker compose up --build` | Build and start the containerized app with persistent volume |
| `docker compose down` | Stop and remove the Docker Compose container |
| `docker build -t ai-task-manager .` | Build the standalone Docker image |

---

## 📄 License

This project is open source and available under the standard MIT License.
