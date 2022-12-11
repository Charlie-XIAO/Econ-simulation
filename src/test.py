from main import agent as _agent
import main.market as _market

def supply_demand_market_simulation():
    # Initialize the agents in the market
    agents = []
    for _ in range(20): agents.append(_agent.Farmer(120, 300, 0, 0, 15))
    for _ in range(20): agents.append(_agent.WoodCutter(120, 0, 0, 0, 15))
    for _ in range(20): agents.append(_agent.Miner(120, 0, 0, 0, 22.5))
    for _ in range(20): agents.append(_agent.Refiner(120, 0, 300, 0, 15))
    for _ in range(20): agents.append(_agent.BlackSmith(120, 0, 0, 150, 0))
    # Determine an initial price of the comodities
    prices = {
        "food": 2.00,
        "wood": 1.70,
        "ore": 2.00,
        "metal": 7.40,
        "tool": 18.00,
    }
    # Initialize the market
    market = _market.SupplyDemandMarket(agents, prices)
    print("Market successfully initialized:", market)
    # Simulating some exchange days
    market.simulate(20, verbose=True)
    # Plot the price adjustment history
    market.plot_price_history(save=True)

def walrasian_market_simulation():
    # Initialize the agents in the market
    agents = []
    for _ in range(20): agents.append(_agent.Farmer(120, 300, 0, 0, 15))
    for _ in range(20): agents.append(_agent.WoodCutter(120, 0, 0, 0, 15))
    for _ in range(20): agents.append(_agent.Miner(120, 0, 0, 0, 22.5))
    for _ in range(20): agents.append(_agent.Refiner(120, 0, 300, 0, 15))
    for _ in range(20): agents.append(_agent.BlackSmith(120, 0, 0, 150, 0))
    # Determine an initial price of the comodities
    prices = {
        "food": 2.00,
        "wood": 1.70,
        "ore": 2.00,
        "metal": 7.40,
        "tool": 18.00,
    }
    # Initialize the market
    market = _market.WalrasianMarket(agents, prices)
    print("Market successfully initialized:", market)
    # Simulating some exchange days
    market.simulate(20, verbose=True)
    # Plot the price adjustment history
    market.plot_price_history(save=True)

if __name__ == "__main__":
    walrasian_market_simulation()