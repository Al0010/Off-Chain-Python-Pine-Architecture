# Off-Chain Python Pine Script Architecture

## Introduction  

I believe this is currently the best way to bridge Python with TradingView's Pine Script programming language. I have tested this architecture for several years to solve various challenges such as strategy optimization, building indicators with advanced metrics, integrating machine learning models, and much more. Here you will find an example that you can improve or use as a starting point for your personal project. In this repository, I encapsulate the best practices and architecture I consider optimal when building a hybrid Python - Pine Script project. 

## System Architecture (2-Layer Design)

This project adopts a modular architecture to bridge Python with Pine Script live chart execution:
1. **Layer 1 - Python Backend (`src/backtest.py`):** Ingests historical CSV data, calculates indicators, runs a **Grid Search** optimization engine, and generates a compact string **payload** containing the optimal risk parameters.
2. **Layer 2 - TradingView Frontend (`pine_script/strategy.pine`):** A custom Pine Script v6 indicator that parses the payload dynamically, executes a trend-following SMA breakout strategy with ATR Trailing Stops, and plots the results directly on the chart.

## Asynchronous Calculation vs. Synchronous Rendering
- **Role Decoupling:** The heavy computational core does not reside on TradingView; instead, it runs in the background on external environments (Python servers, cloud instances, or local machines).
- **Unidirectional or Bidirectional Data Flow:** Processed data is "passed" to the graphical layer via a compact configuration payload.
- **Pine as a Visual "Thin Client":** In this model, Pine Script acts as a lightweight and efficient renderer, interpreting the received data streams and displaying them in real-time right over the chart candles.

## Practical Example
To demonstrate this architecture in action, we need a practical case study. 
Personally, I hate spending time manually configuring strategy parameters, so we will automate this process. We will task Python with finding the best parameter combination for our strategy. I chose a very simple, straightforward strategy to keep things clean:

- Buy & Sell Strategy
- Long only 
- Single order 
- Entry when close crosses over SMA 
- Exit 1: Take Profit %
- Exit 2: Trailing Stop (ATR True Range-based)

To solve this, we use a technique called Grid Search optimization. Grid Search, combined with a custom backtesting engine built in Python, tests hundreds of combinations and generates our payload. Finally, we pass that payload into our Pine script to visualize the optimized results on the chart.

## Quick Start 
1. Download CSV data from TradingView.
2. Upload your CSV data inside the `data` folder.
3. Update the CSV filename inside `src/backtest.py`.
4. Run the code and extract the payload string.
5. Paste the payload inside TradingView and review the results!

## Step-by-Step Installation & Setup Guide

Follow these steps directly from your terminal (macOS, Linux, or Windows) to set up and run the project from scratch.

### 1. Clone the Repository from GitHub
Open your terminal and clone the project repository using your GitHub link:
```bash
git clone https://github.com/Al0010/Off-Chain-Python-Pine-Architecture.git
```

### 2. Navigate into the Project Folder
Move inside the newly downloaded project directory:
```bash
cd Off-Chain-Python-Pine-Architecture
```

### 3. Create a Virtual Environment (`venv`)
Isolate the project dependencies by creating a Python virtual environment:
* **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  ```
* **On Windows:**
  ```bash
  python -m venv venv
  ```

### 4. Activate the Virtual Environment
Activate the environment so that all subsequent commands run inside it:
* **On macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
* **On Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate.bat
  ```
* **On Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
> **Note:** Once active, you will see `(venv)` appear at the beginning of your terminal prompt line.

### 5. Install Required Dependencies
Install the required packages (`pandas`, `numpy`, etc.) specified in the requirements file:
```bash
pip install -r requirements.txt
```
*(Alternatively, you can install them manually via: `pip install pandas numpy`)*.

### 6. Run the Python Backtest
Now that your environment is ready and libraries are installed, run the optimization and backtest script from the root folder:
```bash
python src/backtest.py
```
*(If you are on macOS/Linux and encounter issues, try `python3 src/backtest.py`)*.

---

## Usage on TradingView

Upon successful execution, the terminal will output a configuration string (payload) formatted like this:
```text
3.5,2.0,200,14
```

1. Open **TradingView** and create a new **Pine Script v6** strategy.
2. Paste the strategy code provided in `pine_script/strategy.pine`.
3. Open the script settings and paste the payload string generated by Python into the **Payload** input field.
4. Enjoy the dynamic charts featuring trade duration gradients and smart moving averages!

## Advantages of Pine Script: Maximum Execution Speed
1. **Domain-Specific Language (DSL):** Pine Script is born and optimized exclusively for one single task: processing historical financial series and technical indicators. It does not carry the complexity or overhead of a general-purpose language.
2. **Native Execution on TradingView's Engine:** Pine code runs directly on TradingView's high-performance server infrastructure (built in low-level compiled languages like C++).
3. **Native Vectorized Bar Architecture:** Pine's entire logic is designed to flow sequentially or vectorially across chart bars without external interpreter overhead or package import requirements.

## Advantages of Python: Infinite Computational Power
1. **Specific Frameworks in C and C++:** Fundamental calculation libraries like NumPy, Pandas, SciPy, or TensorFlow have their interfaces written in Python, but their core engine is written in C or C++. When you run a complex calculation, Python acts merely as the "conductor," while heavy lifting is handled by low-level compiled code running close to pure hardware speeds.
2. **Vectorization:** In Python, thanks to NumPy, you can utilize vectorization: operations are passed directly to contiguous memory blocks, leveraging modern processor SIMD (Single Instruction, Multiple Data) instructions to process multiple data points simultaneously in a single clock cycle.
3. **Massive GPU Acceleration:** Intensive computing and machine learning frameworks like PyTorch or TensorFlow allow you to shift heavy workloads (such as neural network training or massive matrix multiplications) entirely from the CPU to the GPU. GPUs feature thousands of small cores built for lightning-fast parallel execution.
4. **An Unrivaled Scientific Ecosystem:** Python boasts decades of collaborative development by scientific and financial communities. There is an optimized library for almost every computing need:
   - Data analysis and matrices: NumPy, Pandas
   - Scientific computing and statistics: SciPy, Statsmodels
   - Artificial Intelligence and Deep Learning: PyTorch, Scikit-learn, TensorFlow
   - Quantitative finance: Zipline, Backtrader, QuantLib

## Why Combine Them?
Uniting Python and Pine Script into a single hybrid architecture unlocks massive advantages that radically transform your approach to quantitative trading and technical analysis. Leveraging the best of both worlds eliminates the compromises typical of using a single platform.

Here is why I personally consider this architecture a right approach to combine Py and Pine languages:
1. **Breaking Computational Limits & Extending Intelligence:**
   - *Uncapped computing power:* You can offload heavy tasks to Python, such as portfolio genetic optimization, Monte Carlo simulations across millions of iterations, or training machine learning/deep learning models.
   - *Alternative data integration:* Python allows you to pull unlimited data sources (sentiment analysis from Twitter/X, crypto on-chain data, macroeconomic reports) and fuse them with historical prices—something impossible to achieve natively with Pine Script alone.
2. **Real-Time Execution and Visualization:**
   - *The ultimate interface:* TradingView and Pine Script offer the world's best charting engine for interactive market data visualization.
   - *Zero visual latency:* Once Python processes complex signals or calculates critical parameters in the background, it passes them to Pine Script, which instantly renders them over the candles. This gives the trader a clean, responsive dashboard that is easy to monitor at a glance.
3. **Professional Flexibility and Scalability:**
   - *Separation of Concerns:* Advanced backtesting logic, mathematical risk management, and statistical research reside in Python's robust, modular environment. Signal execution, real-time alerts, and visual clarity are left to TradingView.
   - *Overcoming technical roadblocks:* Avoid timeout errors, array limits, and memory constraints encountered when trying to run excessively complex calculations directly within chart scripts.

## 📂 Project Structure

```text
Off-Chain-Python-Pine-Architecture/
│
├── data/
│   └── OANDA_XAUUSD, 15.csv      # Historical dataset (15m timeframe)
│
├── pine_script/
│   └── strategy.pine             # Pine Script v6 strategy with string parser
│
├── src/
│   └── backtest.py               # Python Grid Search & payload generator
│
├── .gitignore
├── LICENSE
├── README.md 
└── requirements.txt
