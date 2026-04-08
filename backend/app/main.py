from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.predict import router as predict_router


app = FastAPI(
    title="Ionic SL API",
    version="0.1.0",
    description="Dual-phase ionic conductivity prediction service for solid and liquid lithium battery electrolytes.",
)
@app.get("/")
def root():
    return {"status": "Ionic SL API is running", "docs": "/docs"}
from fastapi.responses import HTMLResponse

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>⚡ Ionic Conductivity Predictor</h2>

            <form onsubmit="event.preventDefault(); sendData();">
                <input id="formula" placeholder="Enter formula (e.g. LiPF6 in EC/EMC)" style="padding:10px; width:300px;">
                <br><br>
                <button type="submit" style="padding:10px 20px;">Predict</button>
            </form>

            <h3 id="result"></h3>

            <script>
                async function sendData() {
                    const formula = document.getElementById("formula").value;

                    const response = await fetch("/predict", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ formula: formula })
                    });

                    const data = await response.json();

                    document.getElementById("result").innerText =
                        "Log Sigma: " + data.log_sigma + " | " + data.category;
                }
            </script>
        </body>
    </html>
    """
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(predict_router)
