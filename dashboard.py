"""
Simple web dashboard to visualize price history.
Uses Flask and Chart.js for graphing.
"""

import os
import json
from flask import Flask, render_template_string, jsonify
import tracker

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ticket Price Tracker</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns"></script>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            margin: 0;
            padding: 20px;
        }
        h1 { color: #00d9ff; margin-bottom: 10px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .chart-container {
            background: #16213e;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: #16213e;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        .stat-value { font-size: 2em; color: #00d9ff; font-weight: bold; }
        .stat-label { color: #888; font-size: 0.9em; }
        .url-info {
            background: #16213e;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            word-break: break-all;
            font-size: 0.9em;
            color: #888;
        }
        .no-data {
            text-align: center;
            padding: 50px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Ticket Price Tracker</h1>

        {% if url %}
        <div class="url-info">Tracking: {{ url }}</div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">${{ "%.2f"|format(current_price) }}</div>
                <div class="stat-label">Current Price</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${{ "%.2f"|format(lowest_price) }}</div>
                <div class="stat-label">Lowest Price</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${{ "%.2f"|format(highest_price) }}</div>
                <div class="stat-label">Highest Price</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ data_points }}</div>
                <div class="stat-label">Data Points</div>
            </div>
        </div>

        <div class="chart-container">
            <canvas id="priceChart"></canvas>
        </div>

        <script>
            const ctx = document.getElementById('priceChart').getContext('2d');
            const priceData = {{ price_data|safe }};

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: priceData.map(d => d.timestamp),
                    datasets: [{
                        label: 'Price ($)',
                        data: priceData.map(d => d.price),
                        borderColor: '#00d9ff',
                        backgroundColor: 'rgba(0, 217, 255, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        title: {
                            display: true,
                            text: 'Price History',
                            color: '#eee',
                            font: { size: 16 }
                        }
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: { unit: 'day' },
                            ticks: { color: '#888' },
                            grid: { color: '#333' }
                        },
                        y: {
                            ticks: {
                                color: '#888',
                                callback: function(value) { return '$' + value; }
                            },
                            grid: { color: '#333' }
                        }
                    }
                }
            });
        </script>

        {% else %}
        <div class="no-data">
            <h2>No price data yet</h2>
            <p>The tracker will start collecting data once it runs.</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route('/')
def dashboard():
    """Main dashboard page with price graph."""
    urls = tracker.get_all_urls()

    if not urls:
        return render_template_string(DASHBOARD_HTML, url=None)

    # Get the first tracked URL (you could extend this to show multiple)
    url = urls[0]
    history = tracker.get_price_history(url)

    if not history:
        return render_template_string(DASHBOARD_HTML, url=None)

    prices = [h['price'] for h in history]

    return render_template_string(
        DASHBOARD_HTML,
        url=url,
        current_price=prices[-1],
        lowest_price=min(prices),
        highest_price=max(prices),
        data_points=len(prices),
        price_data=json.dumps(history)
    )


@app.route('/api/prices')
def api_prices():
    """JSON API endpoint for price data."""
    urls = tracker.get_all_urls()
    data = {}
    for url in urls:
        data[url] = tracker.get_price_history(url)
    return jsonify(data)


def run_dashboard():
    """Run the dashboard server."""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    run_dashboard()
