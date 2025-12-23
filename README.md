# Food Ordering Microservices System

This project implements a microservices architecture for a Food Ordering System using Flask.

## Architecture

*   **Frontend**: Flask app serving HTML/CSS (Port 5001)
*   **API Gateway**: Central entry point routing requests (Port 5000)
*   **Login Service**: Handles user authentication (Port 5002)
*   **Hotel Service**: Manages hotel/restaurant listings and menus (Port 5003)
*   **Order Service**: Manages order creation and lifecycle (Port 5004)
*   **Payment Service**: Mocks payment processing (Port 5005)

## Prerequisites

*   Python 3.x
*   Pip

## Installation

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the System

You can run all services simultaneously using the helper script:

```bash
python run_services.py
```

Or run each service individually in separate terminals:

```bash
python api_gateway/app.py
python frontend/app.py
python login_service/app.py
python hotel_service/app.py
python order_service/app.py
python payment_service/app.py
```

## Usage

1.  Open `http://localhost:5001` in your browser.
2.  Login with:
    *   Username: `user`
    *   Password: `password`
3.  Browse Hotels.
4.  Select a Hotel to view its menu.
5.  Select items and Place Order.

## Design Notes

*   **Communication**: Use of API Gateway ensures no direct communication between services (except via Gateway).
*   **Frontend**: Rich aesthetics using dark mode and responsive card layout.
*   **Code**: Kept concise with minimal boilerplate.
