# E-Commerce API

This project provides a Flask-based API for managing an e-commerce platform. The API includes endpoints for handling carts, products, users, and order history.

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Yashpatel1522/ecommerce-api.git
    cd ecommerce-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. Set up the database (SQLite is used by default):

    ```bash
    python app.py
    ```

    This will create the database and run the Flask development server.

2. Open a web browser or use Postman to interact with the API at `http://127.0.0.1:5000`.

## Postman Collection

To import the API collection into Postman:

1. Open Postman.
2. Click on the "Import" button in the top-left corner.
3. Choose the "Upload Files" tab.
4. Navigate to the `collections` folder in your project directory and select the `e-commerce-api.postman_collection.json` file.
5. Click "Open" to import the collection.

This will load the API endpoints into Postman for easy testing and interaction.

### Postman Collection File

The Postman collection JSON file is located in the `collections` folder:
## Contributing

We welcome contributions to the E-Commerce API project! To ensure a smooth and efficient process, please follow the guidelines below.

### Getting Started

1. **Fork the Repository**

   Start by forking the repository to your own GitHub account. This allows you to freely experiment and make changes without affecting the main repository.

2. **Clone Your Fork**

   Clone your forked repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/ecommerce-api.git
   cd ecommerce-api

