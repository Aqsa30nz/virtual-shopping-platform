# 🛍️ Virtual Shopping Platform

An AI-powered virtual shopping platform that helps users **discover, compare, and visualize products** before making a purchase.

The platform combines a product catalog with **AI-assisted product comparison** and **AI-assisted furniture visualization**, giving users additional context when evaluating products online.

---

## ✨ Features

### 🛒 Product Discovery

* Browse products from the catalog
* View product details and specifications
* Explore products across available categories
* Select products for comparison or visualization

### 🤖 AI-Powered Product Comparison

The platform uses AI to analyze available product information and generate a structured comparison.

Users can evaluate products based on:

* Product specifications
* Key differences
* Advantages and disadvantages
* Relative strengths
* Suitability for different requirements

### 🛋️ AI-Assisted Furniture Visualization

Users can upload a room image and visualize selected furniture within the environment.

The visualization workflow combines **image processing, computer vision, and AI-based image generation** to produce a visual representation of the selected furniture in the room.

### 📊 Structured Product Data

Product information is maintained using structured data, allowing the application to consistently retrieve product details for browsing, comparison, and visualization.

---

## 🔄 User Flow

```text
                    ┌──────────────────┐
                    │   Open Platform  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Browse Products  │
                    └────────┬─────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
          ┌───────────────┐     ┌─────────────────┐
          │ Select Product│     │ Compare Products│
          └───────┬───────┘     └────────┬────────┘
                  │                      │
                  │                      ▼
                  │              ┌────────────────┐
                  │              │ AI Comparison  │
                  │              └────────────────┘
                  │
                  ▼
          ┌──────────────────┐
          │ Upload Room Image│
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ AI Visualization │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Visualized Result│
          └──────────────────┘
```

---

## 🏗️ Architecture

The application consists of four main components: **frontend, backend, AI functionality, and product data/assets**.

```text
┌──────────────────────────────────────────────┐
│                  FRONTEND                    │
│             Next.js / TypeScript             │
│                                              │
│       Product UI • Catalog • User Flow       │
└──────────────────────┬───────────────────────┘
                       │
                       │ HTTP / REST API
                       ▼
┌──────────────────────────────────────────────┐
│                  BACKEND                     │
│                   FastAPI                    │
│                                              │
│       API Layer • Image Processing           │
└───────────────┬──────────────────┬───────────┘
                │                  │
                ▼                  ▼
       ┌─────────────────┐  ┌─────────────────┐
       │       AI        │  │      DATA       │
       │                 │  │                 │
       │  Comparison     │  │ Product Catalog │
       │  Visualization  │  │ Product Assets  │
       └─────────────────┘  └─────────────────┘
```

---

## 🧰 Tech Stack

| Layer                 | Technology              |
| --------------------- | ----------------------- |
| Frontend              | Next.js                 |
| Frontend Language     | TypeScript              |
| Styling               | Tailwind CSS            |
| Backend               | FastAPI                 |
| Backend Language      | Python                  |
| Computer Vision       | OpenCV                  |
| AI / Image Generation | Replicate API           |
| Data                  | Structured Product Data |

---

## 📁 Project Structure

```text
virtual-shopping-platform/
│
├── ai/
│   └── comparison.py
│
├── backend/
│   ├── main.py
│   └── image_analysis.py
│
├── frontend/
│   ├── app/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   └── tsconfig.json
│
└── .gitignore
```

### `ai/`

Contains the AI-assisted product comparison functionality.

* `comparison.py` — product comparison logic

### `backend/`

Contains the FastAPI application and image-processing functionality.

* `main.py` — FastAPI application and API layer
* `image_analysis.py` — image analysis and furniture placement processing

### `frontend/`

Contains the Next.js application and user-facing interface.

* `app/` — application pages and UI
* `public/` — static assets
* `package.json` — frontend dependencies and scripts
* `next.config.ts` — Next.js configuration
* `tsconfig.json` — TypeScript configuration

---

## 🧠 AI & Computer Vision

The furniture visualization workflow combines computer vision, image processing, and AI-based image generation.

```text
┌───────────────┐
│  Room Image   │
└───────┬───────┘
        │
        ▼
┌──────────────────┐
│   Image Upload   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Image Analysis  │
│     / OpenCV     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Selected Product │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ AI Visualization     │
│   / Replicate API    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────┐
│ Visualized Room  │
└──────────────────┘
```

The computer-vision layer performs image-processing and product-placement operations, while the AI service assists with generating the visualization.

---

## 🔍 AI Product Comparison

The product comparison functionality is implemented in the `ai/` module.

```text
Product Information
        │
        ▼
┌────────────────────┐
│ Comparison Module  │
│  ai/comparison.py  │
└─────────┬──────────┘
          │
          ▼
   AI-Assisted Analysis
          │
          ▼
   Structured Comparison
```

The comparison workflow turns product information into a structured analysis, helping users understand differences without manually inspecting multiple product listings.

---

## 🚀 Getting Started

### Prerequisites

Make sure the following are installed:

* **Node.js**
* **npm**
* **Python 3.12+**
* **Git**

An API token for the AI service is required for AI-powered functionality.

### 1. Clone the Repository

```bash
git clone https://github.com/Aqsa30nz/virtual-shopping-platform.git
cd virtual-shopping-platform
```

### 2. Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

### 3. Backend Setup

Open another terminal and navigate to the backend:

```bash
cd backend
```

#### Create a Virtual Environment

**Windows:**

```powershell
py -3.12 -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Install Dependencies

Install the packages required by the backend and AI components according to the project's dependency configuration.

#### Start the FastAPI Server

```bash
python -m uvicorn main:app --reload --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

---

## 🔐 Environment Variables

AI functionality requires the appropriate API credentials.

Create a local `.env` file or configure the environment variable:

```env
REPLICATE_API_TOKEN=your_api_token_here
```

Keep API credentials in your local environment.

**Never commit API keys, tokens, or other sensitive credentials to GitHub.**

---

## ▶️ Running the Application

Start the backend:

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

Then, in a separate terminal, start the frontend:

```bash
cd frontend
npm run dev
```

Open the application:

```text
http://localhost:3000
```

---

## 📡 Backend API

The backend is built using **FastAPI** and exposes HTTP endpoints used by the frontend and image-processing workflows.

FastAPI automatically provides interactive API documentation at:

```text
http://localhost:8000/docs
```

The Swagger interface can be used to inspect and test the available endpoints during development.

---

## 🎯 Current MVP

The current MVP demonstrates an AI-assisted shopping workflow consisting of:

* Product catalog
* Product discovery
* Product selection
* AI-assisted product comparison
* Room image upload
* Furniture visualization
* Computer-vision-based image processing
* AI-assisted visualization
* Structured product data
* Separate frontend and backend components

The project is currently under active development.

---

## 🔮 Future Improvements

* Personalized product recommendations
* Preference-based product ranking
* Additional product categories
* Improved furniture segmentation
* More accurate spatial understanding
* Better perspective and scale estimation
* Multi-product visualization
* Improved visualization quality
* Real-time product price and availability
* User accounts
* Saved products and comparisons
* Shopping cart functionality
* Conversational shopping assistant
* User-defined comparison criteria

---

## 💡 Project Goal

The goal of Virtual Shopping Platform is to explore how **AI, computer vision, and modern web technologies** can improve the online shopping experience.

Traditional e-commerce primarily presents users with product listings and specifications. This project explores a more interactive approach:

```text
        DISCOVER
           │
           ▼
         COMPARE
           │
           ▼
       VISUALIZE
           │
           ▼
     Make an Informed
        Decision
```

By combining structured product information, AI-assisted comparison, and furniture visualization, the platform aims to provide users with more useful context before making a purchasing decision.

---

## 🚧 Project Status

**Status: Active MVP / Personal Project**

The project is currently being developed and tested locally.

Deployment has **not yet been implemented** and may be considered in a future iteration.

---

## 👩‍💻 Author

**Aqsa Naaz**

GitHub: [@Aqsa30nz](https://github.com/Aqsa30nz)

---

## 📄 License

This project is intended for **educational, experimental, and personal development purposes**.
