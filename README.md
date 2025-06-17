# HomeSync AI: Your Intelligent Household Management Assistant

![HomeSync AI Logo Placeholder](https://github.com/fermaat/HomeSync_AI/blob/main/data/files/logo.jpg?raw=true)

Welcome to **HomeSync AI**, an innovative application designed to transform household management through the power of advanced Artificial Intelligence. At its heart, HomeSync AI leverages Google's cutting-edge **Gemini Pro Vision** model, providing an intelligent, multi-modal approach to digitizing grocery receipts, analyzing spending habits, and offering smart, data-driven recommendations for household purchases.

---

## Table of Contents

1.  [About the Project](#about-the-project)
2.  [AI Core & Multi-Modality](#ai-core--multi-modality)
3.  [Features](#features)
4.  [Technology Stack](#technology-stack)
5.  [Project Structure](#project-structure)
6.  [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Dockerized Setup (Recommended)](#dockerized-setup-recommended)
    - [Backend Setup (`src/`) (Manual, if not using Docker)](#backend-setup-src-manual-if-not-using-docker)
    - [Frontend Setup (`interface/`)](#frontend-setup-interface)
7.  [Running the Application](#running-the-application)
8.  [Usage](#usage)
9.  [Database Schema](#database-schema)
10. [Contributing](#contributing)
11. [License](#license)

---

## About the Project

HomeSync AI isn't just another household management app; it's a personal AI assistant that intelligent automates the tedious task of tracking your grocery expenses and managing your home inventory. Our core innovation lies in the seamless integration of **visual intelligence** to process unstructured data (like receipt images) and **natural language understanding** to provide actionable insights. By simply scanning your grocery receipts, HomeSync AI precisely extracts product information, intelligently categorizes your purchases, and securely stores this invaluable data in a robust PostgreSQL database. This rich dataset then fuels sophisticated analytics, offering you a clear overview of your spending patterns and paving the way for intelligent recommendations on when to repurchase essential items, helping you optimize your budget and reduce waste.

---

## AI Core & Multi-Modality

The intelligence behind HomeSync AI is powered by **Google's Gemini Pro Vision model**, a foundational AI model renowned for its multi-modal capabilities. This enables our application to process and understand information from various types of input, going beyond just text.

### How Gemini's Multi-Modality is Leveraged:

1.  **Image Understanding (Receipt Digitization):**

    - **Visual Input:** The mobile application captures or selects an image of a physical grocery receipt.
    - **Gemini Pro Vision Analysis:** This image, as a visual data input, is sent directly to the Gemini Pro Vision API. Gemini's advanced computer vision capabilities analyze the image to identify text (OCR), recognize patterns, and understand the layout of the receipt.
    - **Intelligent Extraction:** Unlike simple OCR, Gemini understands the _context_ of the text within the image. It can accurately differentiate product names from prices, quantities from unit measurements, and even pinpoint the purchase date and store name, even with varying receipt formats, fonts, and potential creases or distortions. This is a key multi-modal strength – interpreting visual information to extract structured data.

2.  **Textual Comprehension & Generation (Voice/Text Commands):**
    - **Textual Input:** Users can interact with the AI via text commands (simulating voice input).
    - **Gemini's Language Capabilities:** Gemini processes these natural language queries (e.g., "How much did I spend on dairy products last month?", "What are my most frequently purchased items?").
    - **Contextual Reasoning & Response Generation:** By combining its understanding of the user's textual query with the structured data retrieved from the database (which was originally extracted from images), Gemini can formulate intelligent, human-like responses and actionable insights. This demonstrates its ability to bridge different data types – natural language input, structured database data, and its inherent understanding of categories and trends.

By harnessing Gemini's ability to seamlessly integrate visual and textual understanding, HomeSync AI moves beyond basic data entry, providing a truly intelligent and adaptive household management experience.

---

## Features

- **Intelligent Receipt Digitization:** Effortlessly capture or upload grocery receipts, with **Gemini Pro Vision** extracting detailed product information, prices, quantities, and dates, even from complex or varied layouts.
- **AI-Powered Spending Analytics:** Gain deep insights into your expenditure. HomeSync AI automatically categorizes purchases and allows you to track spending by category (e.g., "cereals", "soft drinks") over custom time periods (daily, weekly, monthly, annually), all powered by AI-extracted data.
- **Smart Purchase Recommendations:** (Future Development) Leverage historical purchasing data analyzed by AI to receive intelligent suggestions on when to repurchase specific items, helping to prevent stock-outs and reduce impulsive buys.
- **Conversational AI Interface:** Interact with your household assistant using natural language (via text input). Ask questions about your spending, get summaries, or inquire about inventory needs, with AI providing relevant and insightful responses.
- **Persistent Data Storage:** All AI-extracted and user-generated data is securely stored in a robust PostgreSQL database, forming the foundation for comprehensive analytics and future AI enhancements.
- **Containerized Development:** Easy setup and consistent environments for both backend and database using Docker and Docker Compose.

---

## Technology Stack

### Backend (`src/`)

- **Python:** The core language for the backend logic.
- **FastAPI:** A modern, fast (high-performance) web framework for building APIs.
- **Google Gemini Pro Vision API:** The powerhouse for multi-modal AI capabilities, including image analysis and text generation.
- **SQLAlchemy:** Python SQL Toolkit and Object Relational Mapper (ORM) for robust database interactions.
- **PostgreSQL:** A powerful, open-source relational database system for data storage (runs in Docker).
- **Docker & Docker Compose:** For containerized, reproducible backend and database environments.
- **`python-dotenv`:** For managing environment variables securely.

### Frontend (`interface/`)

- **React Native (with Expo):** For building cross-platform mobile applications (iOS and Android).
- **`expo-image-picker`:** To handle camera and photo library interactions for visual input.
- **Axios:** A promise-based HTTP client for making API requests to the backend.
- **`react-native-dotenv`:** For handling environment variables in the React Native application.

---

## Project Structure

```
HomeSyncAI/
├── .env                           # Centralized environment variables for the entire project
├── docker-compose.yml             # Docker Compose file for backend & PostgreSQL
├── cfg/                           # Shared configuration and constants (Python)
│   ├── _config.py
│   └── __init__.py
├── src/                           # Backend (Python - FastAPI)
│   ├── Dockerfile                 # Dockerfile for backend API
│   ├── main.py                    # FastAPI application entry point
│   ├── requirements.txt           # Python dependencies
│   ├── database/                  # Database models and CRUD operations
│   │   ├── models.py
│   │   ├── crud.py
│   │   └── connection.py
│   ├── services/                  # Business logic and external API integrations
│   │   ├── gemini_service.py
│   │   └── analytics_service.py   # (Future)
│   ├── api/                       # API routes (endpoints) and Pydantic schemas
│   │   ├── routes.py
│   │   └── schemas.py
│   └── __init__.py
└── interface/                     # Frontend (React Native - Expo)
    ├── node_modules/
    ├── App.js
    ├── app.json
    ├── package.json
    ├── babel.config.js
    └── .env
```

---

## Setup and Installation

### Prerequisites

- **Python 3.9+**
- **Node.js 14+** and **npm** or **yarn**
- **Expo CLI:** `npm install -g expo-cli`
- **Docker Desktop:** [Install Docker](https://www.docker.com/products/docker-desktop/)
- A **Google Cloud Project** with the **Gemini API enabled** and an **API Key**.

---

### Dockerized Setup (Recommended)

The easiest way to get started is using Docker Compose, which will spin up both the PostgreSQL database and the backend API.

1. **Clone the repository and navigate to the root:**

   ```bash
   git clone https://github.com/yourusername/HomeSyncAI.git
   cd HomeSyncAI/
   ```

2. **Create your `.env` file at the project root:**

   ```dotenv
   # HomeSyncAI/.env
   DATABASE_URL=postgresql://postgres:mysecretpassword@db:5432/homesync_db
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY

   # Frontend related variables
   FRONTEND_BACKEND_IP=YOUR_LOCAL_MACHINE_IP
   FRONTEND_BACKEND_PORT=8000
   FRONTEND_API_VERSION=v1
   ```

   - Replace `YOUR_GEMINI_API_KEY` and `YOUR_LOCAL_MACHINE_IP` as needed.

3. **Start the backend and database:**

   ```bash
   docker-compose up --build
   ```

   - This will build the backend image, start the FastAPI server, and launch a PostgreSQL container.
   - The backend will be available at `http://localhost:8000`.

4. **(Optional) Run database migrations or initialization scripts if needed.**
   - The backend will auto-create tables on startup.

---

### Backend Setup (`src/`) (Manual, if not using Docker)

1. **Create and activate a Python virtual environment:**

   ```bash
   python -m venv src/venv
   source src/venv/bin/activate
   ```

2. **Install backend dependencies:**

   ```bash
   pip install -r src/requirements.txt
   ```

3. **Set up PostgreSQL (using Docker, recommended):**

   ```bash
   docker run --name homesync-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
   ```

   - Or use your own PostgreSQL instance.

4. **Create the database:**

   ```bash
   docker exec -it homesync-postgres psql -U postgres
   ```

   Inside `psql`:

   ```sql
   CREATE DATABASE homesync_db;
   \q
   ```

5. **Configure your `.env` as above.**

6. **Start the backend:**
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

### Frontend Setup (`interface/`)

1. **Navigate to the frontend directory:**

   ```bash
   cd interface/
   ```

2. **Install Node.js dependencies:**

   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure `react-native-dotenv` in `babel.config.js`:**
   Ensure `babel.config.js` contains:
   ```javascript
   // interface/babel.config.js
   module.exports = function (api) {
     api.cache(true);
     return {
       presets: ["babel-preset-expo"],
       plugins: [
         [
           "module:react-native-dotenv",
           {
             moduleName: "@env",
             path: "../.env",
             safe: false,
             allowUndefined: true,
           },
         ],
       ],
     };
   };
   ```

---

## Running the Application

### Using Docker Compose (Recommended)

1. **Start everything:**

   ```bash
   docker-compose up --build
   ```

   - Backend: [http://localhost:8000](http://localhost:8000)
   - PostgreSQL: exposed on port 5432 (internal to Docker network as `db`)

2. **Start the Frontend:**
   ```bash
   cd interface/
   npx expo start
   ```
   - Scan the QR code with Expo Go or use an emulator.

### Manual (Non-Docker) Workflow

- Start PostgreSQL (see above).
- Activate Python venv and run backend with `uvicorn`.
- Start frontend as above.

---

## Usage

Once the application is running:

1.  **Process Ticket:**

    - Tap the "Take/Select Photo of Ticket" button to capture an image of a grocery receipt.
    - Tap "Send Ticket to AI (Gemini)" to send the image to the backend for processing.
    - The extracted data from Gemini (products, prices, etc.) will be displayed on the screen and stored in your PostgreSQL database.

2.  **Voice Command (Text Simulation):**
    - Type a command into the text input field (e.g., "How much did I spend on cereals this month?", "What do we need to buy?").
    - Tap "Send Command to AI" to get a response based on Gemini's interpretation and your stored data.

---

## Database Schema

### `tickets` table

- `id`: UUID (Primary Key)
- `fecha_compra`: DATE
- `supermercado`: VARCHAR (Nullable)
- `total_ticket`: NUMERIC(10, 2)
- `raw_gemini_data`: JSONB (Stores the raw JSON response from Gemini)

### `items` table

- `id`: UUID (Primary Key)
- `ticket_id`: UUID (Foreign Key to `tickets.id`)
- `nombre_producto`: VARCHAR
- `categoria`: VARCHAR (e.g., "Cereales", "Dairy", "Beverages")
- `precio_unitario`: NUMERIC(10, 2)
- `cantidad`: NUMERIC(10, 3)
- `precio_total_linea`: NUMERIC(10, 2)
- `fecha_item`: DATE (Same as `fecha_compra` from the ticket)

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'feat: Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

📬 Contact  
For questions, collaborations, or feedback, feel free to reach out:

📧 Email: fermaat.vl@gmail.com  
🧑‍💻 GitHub: [@fermaat](https://github.com/fermaat)  
🌐 [Website](https://fermaat.github.io)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
