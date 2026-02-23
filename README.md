# House Pricing API

API REST for predicting house prices using Machine Learning.

**API** [https://api-housepricing.onrender.com](https://api-housepricing.onrender.com)

---

## Quick DEMO

Test my API quickly:

👉 **[https://api-housepricing.onrender.com/docs](https://api-housepricing.onrender.com/docs)**

---

## Aim of this project:

Predict the price of a house based on five key features:
- **Overall Quality** 
- **Living Area** 
- **Garage Cars** 
- **Garage Area** 
- **Basement Area**

---

## Example os use

### cURL:
```bash
curl -X POST "https://tu-api.onrender.com/v1/predict" \
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

## Local install

### Requeriments
- Python 3.11+

### Steps

```bash
# 1. Clone Repository
git clone https://github.com/tu-usuario/API_HousePricing.git
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

**API location** http://localhost:8000

**Doc** http://localhost:8000/docs

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/docs` | Doc |
| POST | `/v1/predict` | House Price Prediction |

---

## Testing

```bash
# Install pytest
pip install pytest httpx

# Execute test
pytest test_api_simple.py -v
```

**Expected Result:** 10/10 tests passed ✅

---

## Project Structure

```
API_HousePricing/
│
├── app/                       # API source code
│   ├── __init__.py            # Module initialization
│   ├── main.py                # FastAPI endpoints
│   ├── model.py               # Model loading and prediction
│   ├── schemas.py             # Data validation (Pydantic)
│   └── preprocess.py          # Preprocessing pipeline
│
├── outputs/                   # Trained models
│   ├── best_model.pkl         # Trained ML model
│   └── preprocess_pipeline.pkl# Preprocessing pipeline
│
├── DATA/                      # Training data (optional)
│   └── train.csv              # Kaggle dataset
│
├── tests/                     # Automated tests
│   └── test_api.py            # Tests with pytest
│
├── .gitignore                 # Files to ignore in Git
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── LICENSE                    # MIT License

```

---

## How to contribute:

1. Fork the projec
2. Upgrade it(`git checkout -b feature/upgrade`)
3. Commit (`git commit -am 'upgrade'`)
4. Push (`git push origin feature/upgrade`)
5. Open a Pull Request

---

## Autor

**AlejandroMoralesGomezDev**
- GitHub: [moralesgomez-dev](https://github.com/moralesgomez-dev)
- Kaggle: [moralesgomez](https://www.kaggle.com/moralesgomez)

---

## License

MIT License - see [LICENSE](LICENSE) for mor details

---

