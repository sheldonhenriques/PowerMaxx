from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import requests

app = Flask(__name__)

# API configuration
PRICE_API_URL = "https://mara-hackathon-api.onrender.com/prices"
SITES_API_URL = "https://mara-hackathon-api.onrender.com/sites"
MACHINES_API_URL = "https://mara-hackathon-api.onrender.com/machines"
API_KEY = "a03f730b-bfc6-440f-b458-ceb53c37d2f8"

def get_mixed_allocation(market_data, hardware_specs, power_cap=1_000_000):
    best_mix = None
    best_total_revenue = 0
    best_timestamp = None

    device_options = {
        **{f"{k}_compute": v for k, v in hardware_specs["inference"].items()},
        **{f"{k}_miners": v for k, v in hardware_specs["miners"].items()}
    }

    for market in market_data:
        token_price = market["token_price"]
        hash_price = market["hash_price"]
        timestamp = market["timestamp"]

        device_revenue_info = []

        # Step 1: Calculate revenue-per-watt
        for name, device in device_options.items():
            if name.endswith("_compute"):
                revenue = device["tokens"] * token_price
            elif name.endswith("_miners"):
                revenue = device["hashrate"] * hash_price
            else:
                continue

            revenue_per_watt = revenue / device["power"]
            device_revenue_info.append({
                "name": name,
                "revenue": revenue,
                "power": device["power"],
                "revenue_per_watt": revenue_per_watt
            })

        # Step 2: Greedy allocation
        device_revenue_info.sort(key=lambda x: x["revenue_per_watt"], reverse=True)

        allocation = {}
        total_revenue = 0
        remaining_power = power_cap

        for device in device_revenue_info:
            max_units = remaining_power // device["power"]
            if max_units == 0:
                continue

            allocation[device["name"]] = int(max_units)
            power_used = int(max_units) * device["power"]
            revenue_earned = int(max_units) * device["revenue"]

            remaining_power -= power_used
            total_revenue += revenue_earned

        if total_revenue > best_total_revenue:
            best_total_revenue = total_revenue
            best_mix = allocation
            best_timestamp = timestamp

    # Handle case where no allocation was found
    if best_mix is None:
        return {
            "best_mix": {},
            "expected_total_revenue": 0,
            "unallocated_power": power_cap,
            "market_timestamp": None
        }

    return {
        "best_mix": best_mix,
        "expected_total_revenue": round(best_total_revenue, 2),
        "unallocated_power": power_cap - sum(
            hardware_specs["inference"].get(k.split("_")[0], {}).get("power", 0) * v
            if k.endswith("_compute")
            else hardware_specs["miners"].get(k.split("_")[0], {}).get("power", 0) * v
            for k, v in best_mix.items()
        ),
        "market_timestamp": best_timestamp
    }

def get_best_allocation(market_data, hardware_specs, power_cap=1_000_000):
    """Wrapper function for get_mixed_allocation for backward compatibility"""
    return get_mixed_allocation(market_data, hardware_specs, power_cap)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test-allocation')
def test_allocation():
    """Test endpoint for the allocation algorithm using real market data"""
    try:
        # Fetch real market data from the prices API
        headers = {
            'X-Api-Key': API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(PRICE_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        prices_data = response.json()
        
        # Use the first price object as market_data
        if prices_data and len(prices_data) > 0:
            first_price = prices_data[0]
            market_data = [{
                "hash_price": first_price.get("hash_price", 0),
                "token_price": first_price.get("token_price", 0),
                "energy_price": first_price.get("energy_price", 0),
                "timestamp": first_price.get("timestamp", datetime.now().isoformat())
            }]
        else:
            # Fallback to test data if no real data is available
            market_data = [
                {
                    "hash_price": 1.6452360741024257,
                    "token_price": 1.0051279914607045,
                    "energy_price": 1.4124149430780548,
                    "timestamp": "2025-06-21T19:50:00"
                }
            ]
        
        hardware_specs = {
            "miners": {
                "air": {
                    "hashrate": 1000,
                    "power": 3333
                },
                "hydro": {
                    "hashrate": 10000,
                    "power": 5000
                },
                "immersion": {
                    "hashrate": 5000,
                    "power": 10000
                }
            },
            "inference": {
                "gpu": {
                    "tokens": 1000,
                    "power": 3333
                },
                "asic": {
                    "tokens": 5000,
                    "power": 10000
                }
            }
        }

        result = get_best_allocation(market_data, hardware_specs)
        
        # Add the market data used to the response for debugging
        result["market_data_used"] = market_data
        
        return jsonify(result)
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Failed to fetch market data: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/prices')
def get_prices():
    """Fetch real-time prices from the external API"""
    try:
        headers = {
            'X-Api-Key': API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(PRICE_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        prices = response.json()
        return jsonify({
            'prices': prices,
            'status': 'success',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            'prices': [],
            'status': 'error',
            'message': f'Failed to fetch prices: {str(e)}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/api/sites')
def get_sites():
    """Fetch site data from the external API"""
    try:
        headers = {
            'X-Api-Key': API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(SITES_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        site = response.json()
        return jsonify({
            'site': site,
            'status': 'success',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            'site': None,
            'status': 'error',
            'message': f'Failed to fetch site: {str(e)}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/api/machines')
def get_machines():
    """Fetch machines data from the external API"""
    try:
        headers = {
            'X-Api-Key': API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(MACHINES_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        machines = response.json()
        return jsonify({
            'machines': machines,
            'status': 'success',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            'machines': None,
            'status': 'error',
            'message': f'Failed to fetch machines: {str(e)}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/api/update-machines-with-allocation')
def update_machines_with_allocation():
    """Get optimal allocation and update machines with the best mix"""
    try:
        # First, get the optimal allocation
        allocation_response = test_allocation()
        if allocation_response.status_code != 200:
            return jsonify({
                "error": "Failed to get optimal allocation",
                "status": "error"
            }), 500
        
        allocation_data = allocation_response.get_json()
        best_mix = allocation_data.get("best_mix", {})
        
        if not best_mix:
            return jsonify({
                "error": "No optimal allocation found",
                "status": "error"
            }), 400
        
        # Update machines with the best mix
        headers = {
            'X-Api-Key': API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.put(MACHINES_API_URL, 
                              headers=headers, 
                              json=best_mix, 
                              timeout=10)
        response.raise_for_status()
        
        machines_data = response.json()
        
        return jsonify({
            "status": "success",
            "message": "Machines updated successfully with optimal allocation",
            "allocation": allocation_data,
            "machines_updated": machines_data,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Failed to update machines: {str(e)}",
            "status": "error"
        }), 500
    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/update-machines', methods=['POST'])
def update_machines():
    """Update machines with provided data"""
    try:
        machine_data = request.get_json()
        
        if not machine_data:
            return jsonify({
                "error": "No machine data provided",
                "status": "error"
            }), 400
        
        headers = {
            'X-Api-Key': API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.put(MACHINES_API_URL, 
                              headers=headers, 
                              json=machine_data, 
                              timeout=10)
        response.raise_for_status()
        
        machines_data = response.json()
        
        return jsonify({
            "status": "success",
            "message": "Machines updated successfully",
            "data": machines_data,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Failed to update machines: {str(e)}",
            "status": "error"
        }), 500
    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 