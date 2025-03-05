# Hull-White Interest Rate Model Explorer

An interactive simulation tool built with Streamlit that demonstrates the Hull-White interest rate model. Adjust key parameters, visualize simulated interest rate paths, and explore theoretical insights—all in one place.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [The Hull-White Model](#the-hull-white-model)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Author](#author)

## Overview

The **Hull-White Interest Rate Model Explorer** is designed for educational purposes to help users understand how mean reversion and volatility impact interest rates. The tool simulates multiple interest rate paths using the Hull-White model, providing an intuitive interface with interactive controls and detailed theoretical background.

## Features

- **Interactive Simulation:**  
  Adjust parameters like mean reversion speed (*a*), volatility (σ), initial rate, number of paths, time horizon, and time steps using the intuitive sidebar.
  
- **Dynamic Visualizations:**  
  - **Line Chart:** See multiple simulated interest rate paths over time.
  - **Histogram:** View the terminal rate distribution.
  
- **Educational Tabs:**  
  The app is divided into multiple tabs including:
  - **Interactive Tool:** Live demonstration of the simulation.
  - **Theory Behind Model:** Explanation of the mean-reversion concept and the model's mathematics.
  - **Step-by-Step Guide:** Walkthrough of the simulation process.
  - **Practical Labs:** Pre-configured scenarios such as central bank policy and market crisis simulation.
  - **Interest Rate Basics:** An introduction to the real-life impact of interest rates.

- **Practical Labs:**  
  Experiment with different scenarios by clicking preset buttons to adjust parameters for central bank policy, crisis simulations, or long-term forecasting.

## Installation

### Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/hull-white-model-explorer.git
   cd hull-white-model-explorer
   ```

2. **Install the required packages:**

   ```bash
   pip install streamlit numpy matplotlib
   ```

## Usage

To run the interactive simulation, execute the following command in your terminal:

```bash
streamlit run Hull-White.py
```

This command will launch the Streamlit app in your default web browser. Use the sidebar controls to adjust simulation parameters and navigate through the different tabs to learn more about the model and its applications.

## The Hull-White Model

The Hull-White model is a short rate model widely used in finance for modeling interest rate dynamics. It is governed by the stochastic differential equation:

$$
dr_t = a(\theta - r_t)dt + \sigma dW_t
$$

Where:
- **\(a\)**: Speed of mean reversion (adjustable via the slider).
- **\(\sigma\)**: Volatility of the rate changes (adjustable via the slider).
- **\(\theta\)**: Long-term mean rate, fixed at 2% in this simulation.
- **\(W_t\)**: A Wiener process representing random market shocks.

The model captures how interest rates tend to revert toward a long-term mean while being influenced by random fluctuations.

## Disclaimer

> **Educational Purposes Only:**  
> This tool is intended solely for educational and research purposes. The simulation is provided without any guarantee of accuracy or suitability for professional financial modeling. Do not use this tool as a basis for real financial or investment decisions. Always consult a qualified financial professional before making any investment decisions.

## License

This project is licensed under the [CC BY-NC 4.0 License](https://creativecommons.org/licenses/by-nc/4.0/).

## Author

By Luís Simões da Cunha
