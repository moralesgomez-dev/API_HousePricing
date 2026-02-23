# 🚀 Deploy Guide — House Pricing API on Render (Docker)

---

## 1. Fix your local project structure

Make sure your project looks exactly like this before anything else:

```
API_HousePricing/
├── app/
│   ├── __init__.py
│   ├── main.py          ← use the fixed version provided
│   ├── model.py
│   ├── schemas.py
│   └── preprocess.py
├── outputs/
│   ├── best_model.pkl
│   └── preprocess_pipeline.pkl
├── training/            ← optional, can be excluded via .gitignore
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

> ⚠️ The `outputs/` folder with your `.pkl` files **must be committed to GitHub** since Render will use them at runtime. They are NOT in `.gitignore`.

---

## 2. Push to GitHub

```bash
# Inside your project root
git init
git add .
git commit -m "Initial commit - House Pricing API"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/API_HousePricing.git
git branch -M main
git push -u origin main
```

---

## 3. Create a Web Service on Render

1. Go to [https://render.com](https://render.com) and sign in (or create a free account).
2. Click **"New +"** → **"Web Service"**.
3. Connect your GitHub account and select your `API_HousePricing` repository.
4. Fill in the settings:

| Field | Value |
|---|---|
| **Name** | `house-pricing-api` (or anything you like) |
| **Region** | Closest to you |
| **Branch** | `main` |
| **Runtime** | **Docker** |
| **Dockerfile Path** | `./Dockerfile` |
| **Instance Type** | Free (for testing) |

5. Click **"Create Web Service"**.

---

## 4. Wait for the build

Render will:
1. Pull your repo
2. Build the Docker image
3. Start the container with `uvicorn`

This takes **2–5 minutes** on first deploy. You can follow the logs in real time on the Render dashboard.

---

## 5. Verify your deployment

Once it shows **"Live"**, test your endpoints:

```bash
# Health check
curl https://YOUR-APP-NAME.onrender.com/health

# Prediction
curl -X POST "https://YOUR-APP-NAME.onrender.com/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "OverallQual": 7,
    "GrLivArea": 1500,
    "GarageCars": 2,
    "GarageArea": 480,
    "TotalBsmtSF": 900
  }'
```

Or visit the interactive docs: `https://YOUR-APP-NAME.onrender.com/docs`

---

## 6. Update your README

Replace the placeholder URLs in your `README.md`:

```
https://tu-api.onrender.com  →  https://YOUR-APP-NAME.onrender.com
```

---

## ⚠️ Common issues

**Build fails — module not found**
- Make sure `requirements.txt` versions match what you used to train the model (especially `scikit-learn`).
- If unsure, run `pip freeze` in your local venv and copy the exact versions.

**Prediction fails — pickle error / version mismatch**
- Your `.pkl` files must be loaded with the **same scikit-learn version** used to create them.
- Check your local version: `python -c "import sklearn; print(sklearn.__version__)"` and update `requirements.txt` accordingly.

**Free tier spins down after inactivity**
- Render's free tier sleeps after 15 min of inactivity. The first request after sleep takes ~30 seconds. This is normal.

---

## ✅ Summary checklist

- [ ] Fixed `main.py` (lifespan pattern) in place
- [ ] `outputs/best_model.pkl` and `outputs/preprocess_pipeline.pkl` present
- [ ] `Dockerfile` and `requirements.txt` in root
- [ ] Repo pushed to GitHub
- [ ] Web Service created on Render with Docker runtime
- [ ] Deploy successful and `/health` returns OK
- [ ] README updated with live URL
