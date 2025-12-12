# Retail Analytics & Price Optimization Platform

A High-Fidelity Multi-Page Web Application for Retail Intelligence, Pricing Simulation, and Inventory Management.

## 🚀 Features

*   **📊 Sales Analytics Dashboard**: Interactive visualization of revenue trends, brand performance, and seasonal impact.
*   **💰 Price Optimization Engine**: ML-powered simulation to predict demand and revenue curves at different price points.
*   **📦 Inventory Management**: Real-time stock monitoring with visual alerts for low-stock and overstocked items.
*   **🔄 Returns Intelligence**: Predictive analysis of return risks and breakdown of return reasons (Size, Quality, etc.).
*   **📉 Synthetic Data Generator**: Built-in engine to generate realistic retail transaction data matching industry schemas.

## 🛠️ Tech Stack

*   **Frontend**: Dash (React-based), Dash Bootstrap Components
*   **Backend**: Python, Flask (underlying Dash)
*   **Machine Learning**: Scikit-Learn (Random Forest Regressors/Classifiers)
*   **Data Processing**: Pandas, NumPy
*   **Visualization**: Plotly Interactive Charts

## 🏗️ Architecture

The application is structured as a **Multi-Page App (MPA)**:

*   `app/app.py`: Main entry point and layout container.
*   `app/pages/`: Individual page modules.
    *   `home.py`: Landing page with KPIs.
    *   `analytics.py`: Sales deep-dives.
    *   `price_optimizer.py`: The core ML pricing tool.
    *   `returns.py`, `inventory.py`, `dataset.py`: Dedicated functional modules.
*   `app/model.py`: Manages training and inference for Demand and Return models.
*   `app/data_generation.py`: Creates the synthetic dataset.

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Hareesh1/Price-Optimization-Web-Application.git
    cd Price-Optimization-Web-Application
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Generate Data**
    (Optional: data is usually generated automatically, but you can force a refresh)
    ```bash
    python app/data_generation.py
    ```

4.  **Run the Application**
    ```bash
    python -m app.app
    ```
    Access the dashboard at `http://127.0.0.1:8050/`.

## ☁️ Deployment

### AWS App Runner (Recommended)

This project includes a production-ready `Dockerfile`.

1.  **Build** the Docker image:
    ```bash
    docker build -t retail-app .
    ```
2.  **Run** container locally (test):
    ```bash
    docker run -p 8080:8080 retail-app
    ```
3.  **Deploy** to AWS App Runner using the provided `Dockerfile`.

*See `aws_deployment_guide.md` in the artifacts for full cloud deployment instructions.*

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License

MIT License.
