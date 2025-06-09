# HomeSync AI

![HomeSync AI Logo Placeholder](https://via.placeholder.com/150/007bff/FFFFFF?text=HomeSync+AI)

Welcome to **HomeSync AI**, an innovative application designed to streamline household management by leveraging advanced AI capabilities, specifically Google's Gemini Pro Vision model. This project aims to digitize grocery receipts, analyze spending habits, and provide smart recommendations for household purchases.

---

## Table of Contents

1.  [About the Project](#about-the-project)
2.  [Features](#features)
3.  [Technology Stack](#technology-stack)
4.  [Project Structure](#project-structure)
5.  [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Backend Setup (`src/`)](#backend-setup-src)
    - [Frontend Setup (`interface/`)](#frontend-setup-interface)
6.  [Running the Application](#running-the-application)
7.  [Usage](#usage)
8.  [Database Schema](#database-schema)
9.  [Contributing](#contributing)
10. [License](#license)

---

## About the Project

HomeSync AI is a personal assistant that helps you keep track of your grocery spending and manage your household inventory. By simply scanning your receipts, the application extracts product information, categorizes your purchases, and stores them in a robust database. This data is then used to provide insights into your spending patterns and intelligently recommend when to repurchase items based on your past habits.

## Features

- **Receipt Digitization:** Upload or capture images of your grocery receipts.
- **AI-Powered Data Extraction:** Utilizes Google's **Gemini Pro Vision** to accurately extract product names, quantities, unit prices, total prices, and purchase dates from receipts.
- **Spending Analytics:** Track your expenditure by specific categories (e.g., "cereals", "soft drinks") over custom time periods (daily, weekly, monthly, annually).
- **Smart Purchase Recommendations:** (Future Development) Suggests when to buy specific items again based on your historical purchasing frequency.
- **Voice Command Integration:** (Simulated via text input) Interact with the AI to query spending or request recommendations.
- **Persistent Data Storage:** All extracted data is stored in a PostgreSQL database.

---

## Technology Stack

### Backend (`src/`)

- **Python:** The core language for the backend logic.
- **FastAPI:** A modern, fast (high-performance) web framework for building APIs.
- **Google Gemini Pro Vision API:** For advanced image analysis and text generation from receipts.
- **SQLAlchemy:** Python SQL Toolkit and Object Relational Mapper (ORM) for database interactions.
- **PostgreSQL:** A powerful, open-source relational database system for data storage.
- **`python-dotenv`:** For managing environment variables securely.

### Frontend (`interface/`)

- **React Native (with Expo):** For building cross-platform mobile applications (iOS and Android).
- **`expo-image-picker`:** To handle camera and photo library interactions.
- **Axios:** A promise-based HTTP client for making API requests to the backend.
- **`react-native-dotenv`:** For handling environment variables in the React Native application.

---

## Project Structure

```
HomeSyncAI/
├── .env                           # Centralized environment variables for the entire project
├── cfg/                           # Shared configuration and constants (Python)
│   ├── _config.py
│   └── init.py
├── src/                           # Backend (Python - FastAPI)
│   ├── venv/                      # Python virtual environment
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Backend configuration
│   ├── database/                  # Database models and CRUD operations
│   │   ├── models.py              # SQLAlchemy models (Ticket, Item)
│   │   ├── crud.py                # Database interaction functions
│   │   └── connection.py          # Database connection setup
│   ├── services/                  # Business logic and external API integrations
│   │   ├── gemini_service.py      # Gemini API integration
│   │   └── analytics_service.py   # (Future) Analytics logic
│   ├── api/                       # API routes (endpoints) and Pydantic schemas
│   │   ├── routes.py              # FastAPI endpoints
│   │   └── schemas.py             # Data models for API requests/responses
│   ├── requirements.txt           # Python dependencies
│   └── init.py                # Makes 'src' a Python package
└── interface/                     # Frontend (React Native - Expo)
├── node_modules/              # Node.js dependencies
├── App.js                     # Main application component (UI & logic)
├── app.json                   # Expo project configuration
├── package.json               # Node.js dependencies and scripts
├── babel.config.js            # Babel configuration for react-native-dotenv
└── .env                       # (No longer used, .env is in root)

```

---

## Setup and Installation

### Prerequisites

- **Python 3.9+**
- **Node.js 14+** and **npm** or **yarn**
- **Expo CLI:** `npm install -g expo-cli`
- **Docker Desktop (recommended for PostgreSQL):** [Install Docker](https://www.docker.com/products/docker-desktop/)
- A **Google Cloud Project** with the **Gemini API enabled** and an **API Key**.

### Backend Setup (`src/`)

1.  **Navigate to the project root:**
    ```bash
    cd HomeSyncAI/
    ```
2.  **Create a Python virtual environment for the backend:**
    ```bash
    python -m venv src/venv
    ```
3.  **Activate the virtual environment:**
    - **macOS/Linux:**
      ```bash
      source src/venv/bin/activate
      ```
    - **Windows:**
      ```bash
      src\venv\Scripts\activate
      ```
4.  **Install backend dependencies:**

    ```bash
    pip install -r src/requirements.txt
    ```

    (Ensure `requirements.txt` contains: `fastapi`, `uvicorn`, `google-generativeai`, `psycopg2-binary`, `sqlalchemy`, `python-dotenv`, `pydantic`).

5.  **Set up PostgreSQL (using Docker):**
    ```bash
    docker run --name homesync-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
    ```
    - **Important:** Replace `mysecretpassword` with a strong password.
6.  **Create the database:**
    ```bash
    docker exec -it homesync-postgres psql -U postgres
    ```
    Inside `psql` console, run:
    ```sql
    CREATE DATABASE homesync_db;
    \q
    ```
7.  **Create your `.env` file at the `HomeSyncAI/` root directory:**

    ```dotenv
    # HomeSyncAI/.env
    DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/homesync_db"
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

    # Frontend related variables (for backend to know its own IP/Port if needed)
    FRONTEND_BACKEND_IP="YOUR_LOCAL_MACHINE_IP" # e.g., 192.168.1.XX or 10.0.2.2 for Android emulator
    FRONTEND_BACKEND_PORT="8000"
    FRONTEND_API_VERSION="v1"
    ```

    - **Replace `YOUR_GEMINI_API_KEY`** with your actual API key.
    - **Replace `YOUR_LOCAL_MACHINE_IP`** with your computer's IP address. For Android emulators, `10.0.2.2` often works. For physical devices, your computer's local Wi-Fi IP is needed.

### Frontend Setup (`interface/`)

1.  **Navigate to the frontend directory:**
    ```bash
    cd HomeSyncAI/interface/
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```
3.  **Configure `react-native-dotenv` in `babel.config.js`:**
    Ensure `interface/babel.config.js` contains the `module:react-native-dotenv` plugin with `path: '../.env'`:
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
              path: "../.env", // <-- Reads .env from the parent directory
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

1.  **Start the Backend (from `HomeSyncAI/` root):**
    Ensure your virtual environment is active.

    ```bash
    cd HomeSyncAI/
    source src/venv/bin/activate # or src\venv\Scripts\activate on Windows
    uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    ```

    This will start the FastAPI server, usually accessible at `http://0.0.0.0:8000`. It will also create your database tables on startup.

2.  **Start the Frontend (from `HomeSyncAI/interface/`):**

    ```bash
    cd HomeSyncAI/interface/
    npx expo start
    ```

    This will open the Expo Dev Tools in your browser and display a QR code in the terminal.

3.  **Open on Device/Emulator:**

    - Scan the QR code with the **Expo Go** app on your physical device (ensure both are on the same Wi-Fi network).
    - Or, use an emulator: press `a` for Android, `i` for iOS (if you have Xcode installed).

4.  **Verify Backend URL in Frontend:**
    In `interface/App.js`, the `BACKEND_URL` is constructed dynamically from your `.env` variables. Ensure `FRONTEND_BACKEND_IP` in `HomeSyncAI/.env` matches the IP address where your backend is running and is accessible from your device/emulator. Check the console logs for the exact URL being used by the frontend.

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

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (You might want to create a LICENSE file in your root directory if you plan to share this project).
