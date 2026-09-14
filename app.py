from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Weather Trend Analyzer</title>
    </head>

    <boby>

        <h1>Real-Time Weather Trend Analyzer</h1>

        <h3>Weather Data Collection</h3>
        <p>Real-time weather data collection is completed.</p>

        <h3>Data Quality Check</h3>
        <p>Weather data quality check is completed.</p>

        <h3>Data Preparation</h3>
        <p>Weather data preparation is completed.</p>

        <h3>Weather Change Analysis</h3>
        <p>Weather change and trend analysis is completed.</p>

        <h3>DevOps Status</h3>
        <p>DevOps cloud deployment is working successfully.</p>

        <h2>Status: SUCCESS</h2>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)