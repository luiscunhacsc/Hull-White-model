import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def set_lab1_params():
    st.session_state.hw_a = 0.5
    st.session_state.hw_sigma = 0.005  # Will be rounded but preserved internally

def set_lab2_params():
    st.session_state.hw_sigma = 0.04
    st.session_state.hw_a = 0.1

def set_lab3_params():
    st.session_state.hw_years = 30
    st.session_state.hw_num_paths = 100


def reset_parameters():
    st.session_state["hw_a"] = 0.15
    st.session_state["hw_sigma"] = 0.01
    st.session_state["hw_r0"] = 0.02
    st.session_state["hw_num_paths"] = 20
    st.session_state["hw_years"] = 10
    st.session_state["hw_steps"] = 200

def simulate_hull_white(r0, a, sigma, T, steps, num_paths):
    dt = T/steps
    rates = np.zeros((steps+1, num_paths))
    rates[0] = r0
    
    for t in range(1, steps+1):
        dW = np.random.normal(0, np.sqrt(dt), num_paths)
        drift = a * (0.02 - rates[t-1]) * dt
        rates[t] = rates[t-1] + drift + sigma * dW
    
    return rates

st.set_page_config(layout="wide")
st.title("📈 Hull-White Interest Rate Model Explorer")
st.markdown(r"""
Understand how mean reversion and volatility shape interest rate paths through interactive exploration.
""")

with st.sidebar:
    st.header("⚙️ Parameters")
    st.button("↺ Reset Defaults", on_click=reset_parameters)
    
    st.subheader("Model Parameters")
    a = st.slider(
        r"Mean Reversion ($a$)",
        0.0, 1.0, 0.15, key="hw_a",
        help=r"Speed of reversion to long-term mean: $\theta - a(r_t - \theta)dt$"
    )
    sigma = st.slider(
        r"Volatility ($\sigma$)",
        0.0, 0.05, 0.01, key="hw_sigma", step=0.01,
        help=r"Instantaneous volatility of rate changes: $\sigma dW_t$"
    )
    r0 = st.slider(
        r"Initial Rate ($r_0$)",
        0.0, 0.1, 0.02, key="hw_r0",
        help="Starting short rate"
    )
    
    st.subheader("Simulation Settings")
    num_paths = st.slider("Number of Paths", 1, 100, 20, key="hw_num_paths")
    years = st.slider("Time Horizon (Years)", 1, 30, 10, key="hw_years")
    steps = st.slider("Time Steps", 50, 500, 200, key="hw_steps")

    st.markdown("---")
    st.markdown(
    """
    **⚠️ Disclaimer**  
    *Educational purposes only. No accuracy guarantees. Do not use this tool for actual interest rate modeling without professional verification.*  
    
    <small>
    The author does not engage in professional interest rate modeling and does not endorse 
    using these models without proper validation. All information provided is for educational 
    purposes only and should not be construed as financial or investment advice. Fixed income 
    derivatives involve significant risks and may not be suitable for all investors. Always 
    consult a qualified financial professional before making any investment decisions.
    </small>
    """,
    unsafe_allow_html=True
    )
    
    st.markdown("""
    <div style="margin-top: 20px;">
        <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.en" target="_blank">
            <img src="https://licensebuttons.net/l/by-nc/4.0/88x31.png" alt="CC BY-NC 4.0">
        </a>
        <br>
        <span style="font-size: 0.8em;">By Luís Simões da Cunha</span>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎮 Interactive Tool", 
    "📚 Theory Behind Model", 
    "📖 Step-by-Step Guide", 
    "🛠️ Practical Labs",
    "🧠 Interest Rate Basics"
])

with tab1:
    st.subheader("Live Model Demonstration")
    
    rates = simulate_hull_white(r0, a, sigma, years, steps, num_paths)
    time = np.linspace(0, years, steps+1)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(time, rates, alpha=0.6, linewidth=1)
        ax1.axhline(0.02, color='red', linestyle='--', 
                   label=r'Long-term Mean ($\theta = 2\%$)')
        ax1.set_title(f"{num_paths} Simulated Rate Paths")
        ax1.set_xlabel("Years ($t$)")
        ax1.set_ylabel("Interest Rate ($r_t$)")
        ax1.legend()
        st.pyplot(fig1)
    
    with col2:
        st.metric(r"Current Short Rate ($r_0$)", f"{r0:.2%}")
        st.metric(r"Long-term Mean ($\theta$)", "2.00%")
        
        st.markdown(r"**Path Statistics**")
        terminal_rates = rates[-1]
        st.latex(rf"\mathbb{{E}}[r_T] = {np.mean(terminal_rates):.2%}")
        st.latex(rf"\max(r_T) = {np.max(terminal_rates):.2%}")
        st.latex(rf"\min(r_T) = {np.min(terminal_rates):.2%}")
        
        fig2, ax2 = plt.subplots()
        ax2.hist(terminal_rates, bins=10, edgecolor='black')
        ax2.set_title(r"Terminal Rate Distribution ($r_T$)")
        ax2.set_xlabel("Rate")
        ax2.set_ylabel("Frequency")
        st.pyplot(fig2)

with tab2:
    st.markdown(r"""
    ## Core Concept: Mean-Reverting Rates
    
    The Hull-White model describes short-term interest rate dynamics through the 
    stochastic differential equation:
    
    $$
    dr_t = \underbrace{a(\theta - r_t)dt}_{\text{Mean reversion}} + 
    \underbrace{\sigma dW_t}_{\text{Random shock}}
    $$
    
    Where:
    - $a$ = Speed of mean reversion (your slider!)
    - $\sigma$ = Volatility of rate changes (your slider!)
    - $\theta$ = Long-term mean rate (fixed at 2%)
    - $W_t$ = Wiener process (Brownian motion)
    """)
    
    with st.expander("🧠 Why Mean Reversion Matters", expanded=True):
        st.markdown(r"""
        **Economic Interpretation:**  
        The term $a(\theta - r_t)$ acts like a spring pulling rates toward equilibrium:
        - When $r_t > \theta$: Negative drift brings rates down  
        - When $r_t < \theta$: Positive drift lifts rates up  
        
        Strength determined by $a$:
        $$
        \text{Half-life} = \frac{\ln 2}{a} \approx \frac{0.693}{a}
        $$
        """)
    
    with st.expander(r"📐 Model Solution (Advanced Mathematics)"):
        st.markdown(r"""
        **Closed-Form Solution:**  
        The future rate $r_t$ can be expressed as:
        
        $$
        r_t = e^{-at}r_0 + \theta(1 - e^{-at}) + 
        \sigma\int_0^t e^{-a(t-s)}dW_s
        $$
        
        This solution guarantees:
        1. Rates remain positive when $\theta > 0$  
        2. Variance grows with time horizon  
        3. Explicit dependence on initial conditions
        """)

with tab3:
    st.markdown(r"""
    ## Learning Path: 4 Key Steps
    
    1. **Baseline Scenario**  
       Click → Reset Defaults. Observe:
       - Rates fluctuate around $\theta = 2\%$  
       - Moderate oscillations ($\sigma = 0.01$)
    
    2. **Strong Mean Reversion ($a > 0.3$)**  
       Notice:
       - Tighter clustering around $\theta$  
       - Faster recovery after shocks (short half-life)
    
    3. **High Volatility ($\sigma = 0.05$)**  
       See:
       - Wider distribution of $r_t$  
       - Increased extreme values (fat tails)
    
    4. **No Reversion ($a = 0$)**  
       Watch rates drift freely:
       $$
       dr_t = \sigma dW_t \quad \text{(Arithmetic Brownian Motion)}
       $$
    """)

with tab4:
    st.header("🔬 Practical Labs")
    
    lab = st.radio("Choose Lab:", [
        "Lab 1: Central Bank Policy", 
        "Lab 2: Market Crisis Simulation",
        "Lab 3: Rate Forecasting"
    ])
    
    if lab == "Lab 1: Central Bank Policy":
        st.markdown(r"""
        **Scenario:** Strong monetary policy control  
        - Set $a = 0.5$, $\sigma = 0.005$  
        - Observe tight clustering around $\theta$
        """)
        if st.button("⚡ Set Lab 1 Parameters", 
                    on_click=set_lab1_params,  # Use on_click parameter
                    key="lab1_button"):
            st.warning("""
            **Note:** While the volatility slider shows 0.01 due to step size limits, 
            the actual simulation uses σ = 0.005. Check the parameter values in the sidebar
            after clicking to verify the precise values being used.
            """)
            
    elif lab == "Lab 2: Market Crisis Simulation":
        st.markdown(r"""
        **Scenario:** Financial crisis conditions  
        - Set $\sigma = 0.04$, $a = 0.1$  
        - Notice extreme rate swings and slow recovery
        """)
        st.button("⚡ Set Lab 2 Parameters", 
                 on_click=set_lab2_params,
                 key="lab2_button")
            
    else:
        st.markdown(r"""
        **Scenario:** Long-term forecasting  
        - Set $T=30$ years, paths=100  
        - Verify terminal distribution approaches:
        $$
        r_\infty \sim \mathcal{N}\left(\theta, \frac{\sigma^2}{2a}\right)
        $$
        """)
        st.button("⚡ Set Lab 3 Parameters", 
                 on_click=set_lab3_params,
                 key="lab3_button")
        
with tab5:
    st.markdown(r"""
    ## Understanding Interest Rates Through Modeling
    
    **What are interest rates?**  
    The "price" of borrowing money. Like any price, they change daily based on:
    - Economic growth 📈
    - Inflation pressures 🎈  
    - Central bank policies 🏦
    - Market expectations 🤔
    
    **Why model them?**  
    Because rates impact EVERYTHING in finance:
    - Your mortgage payments 🏠
    - Government bond yields 🇺🇸
    - Corporate loan costs 🏢  
    - Retirement savings growth 💰
    
    **The Big Challenge:**  
    Rates behave like a restless wanderer:
    - Sometimes runs far from "normal" levels 🏃♂️  
    - But eventually pulled back by economic gravity ⚖️  
    - With random pushes from market shocks 💥
    
    ### How Our Model Helps
    
    **The Hull-White Model Simulates 3 Key Forces:**
    1. **Mean Reversion**  
       _The economic "rubber band"_  
       ```python
       drift = a * (θ - current_rate)  # Spring force to normal
       ```
    2. **Random Shocks**  
       _Daily market surprises_  
       ```python
       dW = np.random.normal()  # Random push from news/events
       ```
    3. **Volatility**  
       _Size of rate jumps_  
       ```python
       shock_size = σ * dW  # How big are the pushes?
       ```
    
    **See Theory in Action:**  
    Play with these live in the simulator:
    - `a (Mean Reversion)`: Higher = faster return to normal  
      _Try 0.8 vs 0.1 - watch how quickly rates stabilize_
    - `σ (Volatility)`: Higher = wilder rate swings  
      _Set to 0.05 - see crisis-like turbulence_
    - `θ (Long-term Rate)`: The economic anchor  
      _Fixed at 2% here - central bank's dream target_
    
    **Real-World Insights You'll Gain:**
    - Why 2008 crisis rates bounced back 🎢  
    - How Fed policies gradually take effect ⏳  
    - Why 30-year mortgages have rate buffers 🛡️  
    - What "rate normalization" really means 🔄
    
    ### Learning Cheat Sheet
    
    | Concept          | Real-Life Parallel          | Model Control       |
    |------------------|-----------------------------|---------------------|
    | Mean Reversion   | Economic gravity            | `a` slider          |
    | Volatility       | Market panic/euphoria       | `σ` slider          |
    | Long-term Rate   | Central bank target         | Fixed θ=2%          |
    | Random Shocks    | Unexpected news             | Built-in randomness |
    
    **Key Takeaway:**  
    While unpredictable day-to-day, rates have inherent stability through mean reversion.  
    This model helps separate short-term noise from long-term trends - crucial for:
    - Investors 🧑💼  
    - Policy makers 👔  
    - Home buyers 🔑  
    - Retirement planners 🧓
    """)
    
    
    