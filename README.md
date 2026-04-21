# 🧮 Calculator Hub

A comprehensive web-based calculator application built with FastAPI, featuring multiple calculation tools in one beautiful interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔢 Mathematical Calculator
- Basic operations: addition, subtraction, multiplication, division
- Advanced functions: power, square root, logarithm
- Trigonometric functions: sine, cosine, tangent (degrees/radians)
- Factorial and percentage calculations

### 💰 Financial Calculator
- **Discount Calculator** - Calculate discounted prices and savings
- **Loan Calculator** - Monthly payments with amortization
- **ROI Calculator** - Return on Investment analysis
- **VAT Calculator** - Value Added Tax calculations (inclusive/exclusive)
- **Compound Interest** - Investment growth projections

### ❤️ Health Calculator
- **BMI Calculator** - Body Mass Index with health categories
- **BMR Calculator** - Basal Metabolic Rate (Mifflin-St Jeor equation)
- **Water Intake** - Daily hydration recommendations
- **TDEE Calculator** - Total Daily Energy Expenditure with calorie goals

### 🔄 Unit Converter
- Length (meter, kilometer, mile, yard, foot, inch, etc.)
- Weight (kilogram, gram, pound, ounce, stone, ton, etc.)
- Temperature (Celsius, Fahrenheit, Kelvin)
- Speed (m/s, km/h, mph, knot, ft/s)
- Data Storage (byte, KB, MB, GB, TB, PB, bits)

### 📜 Additional Features
- Calculation history with SQLite storage
- Beautiful dark theme with smooth animations
- Responsive design for all devices
- RESTful API with automatic documentation
- Exportable calculation history

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Running

#### Option 1: Simple Run (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

#### Option 2: Install as Package
```bash
# Install in development mode
pip install -e .

# Run using command
calculator-hub

# Or run directly
python run.py
```

#### Option 3: Docker
```bash
# Using Docker Compose
docker-compose up

# Or using Docker directly
docker build -t calculator-hub .
docker run -p 8000:8000 calculator-hub
```

### Access the Application
- **Web Interface**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## 📁 Project Structure

```
calculator-hub/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py      # API module init
│   │   ├── routes.py        # Calculator API endpoints
│   │   ├── history_routes.py # History management endpoints
│   │   └── database.py      # SQLite database operations
│   ├── calculators/
│   │   ├── __init__.py      # Calculators module init
│   │   ├── math_ops.py      # Mathematical operations
│   │   ├── finance_ops.py   # Financial calculations
│   │   ├── health_ops.py    # Health calculations
│   │   └── converter_ops.py # Unit conversion logic
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css   # Application styles
│   │   └── js/
│   │       └── app.js       # Frontend JavaScript
│   └── templates/
│       └── index.html       # Main HTML template
├── run.py                   # Simple launch script
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup script
├── README.md                # This file
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
├── Dockerfile              # Docker image configuration
└── docker-compose.yml      # Docker Compose configuration
```

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.8+)
- **Frontend**: Vanilla JavaScript, CSS3, HTML5
- **Database**: SQLite (file-based, no setup required)
- **Styling**: Custom CSS with CSS Variables
- **API**: RESTful with OpenAPI/Swagger documentation

## 📖 API Usage

### Example: Calculate BMI

```bash
curl -X POST "http://127.0.0.1:8000/api/health/bmi" \
  -H "Content-Type: application/json" \
  -d '{"weight_kg": 70, "height_cm": 175}'
```

### Example: Convert Units

```bash
curl -X POST "http://127.0.0.1:8000/api/converter/convert" \
  -H "Content-Type: application/json" \
  -d '{"value": 100, "category": "length", "from_unit": "meter", "to_unit": "foot"}'
```

### Example: Get Calculation History

```bash
curl "http://127.0.0.1:8000/api/history"
```

See full API documentation at http://127.0.0.1:8000/docs

## ⚙️ Configuration

The application runs with sensible defaults:

| Setting | Default | Description |
|---------|---------|-------------|
| Host | 0.0.0.0 | Server binding address |
| Port | 8000 | Server port |
| Database | calculators.db | SQLite database file |
| Reload | True | Auto-reload on code changes |

To customize, edit `app/main.py` and modify the `uvicorn.run()` parameters.

## 🧪 Testing

```bash
# Test the API endpoints manually via the web interface
# or use the Swagger UI at /docs

# Check health status
curl http://127.0.0.1:8000/health
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Icons and design inspired by modern web applications
- Calculation formulas based on standard mathematical and scientific references

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

Made with ❤️ using FastAPI
