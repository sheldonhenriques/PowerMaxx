# PowerMaxx

**PowerMaxx** is a real-time, power-aware compute optimization platform that dynamically allocates compute resources—such as ASIC miners and GPUs—to maximize revenue per watt. By leveraging live market data, blockchain statistics, and predictive AI models, PowerMaxx ensures optimal hardware utilization within defined power constraints.

---

## 🚀 Features

- **Real-Time Optimization**: Continuously analyzes market and blockchain data to adjust compute resource allocation.
- **Predictive Modeling**: Employs LSTM models to forecast Bitcoin hashrate trends.
- **Dynamic Resource Allocation**: Solves bounded knapsack problems to determine the most profitable mix of hardware under power limits.
- **No API Keys Required**: Utilizes public RPC endpoints for data retrieval, eliminating the need for API keys.
- **User-Friendly Interface**: Provides a modern, responsive web interface for monitoring and control.

---

## 🧐 How It Works

1. **Data Ingestion**: Fetches live data on token prices, energy costs, and blockchain metrics using public RPC endpoints.
2. **Forecasting**: Applies LSTM models to predict near-future hashrate and market conditions.
3. **Optimization**: Calculates revenue-per-watt for available hardware and solves a bounded knapsack problem to maximize profitability within the power budget.
4. **Execution**: Outputs optimal hardware allocation strategies and provides actionable insights through the web interface.

---

## 📁 Project Structure

```plaintext
PowerMaxx/
├── app.py                      # Main Flask application
├── templates/
│   └── index.html              # Web interface template
├── lstm_7day_model.weights.h5  # Pretrained LSTM model weights
├── price_scaler.pkl            # Scaler for price normalization
├── 7day_data.csv               # Historical data for model training
├── EnergyModel.ipynb           # Jupyter notebook for energy modeling
├── Hash_Price_Prediction.ipynb # Jupyter notebook for price prediction
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## ⚙️ Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/sheldonhenriques/PowerMaxx.git
   cd PowerMaxx
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:

   ```bash
   python app.py
   ```

4. **Access the Web Interface**:

   Open your browser and navigate to `http://localhost:5000`

---

## 📈 Usage

- **Real-Time Monitoring**: View current hardware allocations and performance metrics through the web interface.
- **Predictive Insights**: Analyze forecasts for hashrate and market trends to inform decision-making.
- **Dynamic Allocation**: Adjust hardware configurations on-the-fly to respond to changing market conditions.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**

2. **Create a New Branch**:

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**:

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to Your Fork**:

   ```bash
   git push origin feature/YourFeature
   ```

5. **Submit a Pull Request**

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📨 Contact

For questions or support, please contact [sheldonhenriques](https://github.com/sheldonhenriques).

