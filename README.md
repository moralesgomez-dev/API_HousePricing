# House Pricing API

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)
![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-20BEFF?logo=kaggle&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

REST API for predicting house prices using Machine Learning, built on the [Kaggle House Prices dataset](https://www.kaggle.com/c/house-prices-advanced-regression-techniques).

**Live API:** [https://api-housepricing.onrender.com](https://api-housepricing.onrender.com)

---

## Quick Demo

Test the API quickly:

👉 **[https://api-housepricing.onrender.com/docs](https://api-housepricing.onrender.com/docs)**

---

## Aim of this project

Predict the price of a house based on five key features from the **[Kaggle House Prices: Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)** dataset:

- **Overall Quality**
- **Living Area**
- **Garage Cars**
- **Garage Area**
- **Basement Area**

---

## Example of use

### cURL:
```bash
curl -X POST "https://api-housepricing.onrender.com/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "OverallQual": 7,
    "GrLivArea": 1500,
    "GarageCars": 2,
    "GarageArea": 480,
    "TotalBsmtSF": 900
  }'
```

### Response:
```json
{
  "predicted_price": 181234.56,
  "currency": "USD",
  "model_version": "v1.0"
}
```

---

## Local Install

### Requirements
- Python 3.11+

### Steps

```bash
# 1. Clone repository
git clone https://github.com/moralesgomez-dev/API_HousePricing.git
cd API_HousePricing

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start server
uvicorn app.main:app --reload
```

**API:** http://localhost:8000

**Docs:** http://localhost:8000/docs

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive docs |
| POST | `/v1/predict` | House price prediction |

---

## Testing

```bash
# Install pytest
pip install pytest httpx

# Run tests
pytest tests/test_api.py -v
```

**Expected result:** 10/10 tests passed ✅

---

## Project Structure

```
API_HousePricing/
│
├── app/                        # API source code
│   ├── __init__.py             # Module initialization
│   ├── main.py                 # FastAPI endpoints
│   ├── model.py                # Model loading and prediction
│   ├── schemas.py              # Data validation (Pydantic)
│   └── preprocess.py           # Preprocessing pipeline
│
├── outputs/                    # Trained models
│   ├── best_model.pkl          # Trained ML model
│   └── preprocess_pipeline.pkl # Preprocessing pipeline
│
├── DATA/                       # Training data (optional)
│   └── train.csv               # Kaggle dataset
│
├── tests/                      # Automated tests
│   └── test_api.py             # Tests with pytest
│
├── .gitignore                  # Files to ignore in Git
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── LICENSE                     # MIT License
```

---

## How to Contribute

1. Fork the project
2. Create your branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## Author

**AlejandroMoralesGomezDev**
- GitHub: [moralesgomez-dev](https://github.com/moralesgomez-dev)
- Kaggle: [moralesgomez](https://www.kaggle.com/moralesgomez)

---

## License

MIT License - see [LICENSE](LICENSE) for more details
