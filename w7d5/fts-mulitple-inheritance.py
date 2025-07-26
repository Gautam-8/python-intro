# Financial Trading System with Multiple Inheritance
# Create a sophisticated trading platform with multiple inheritance for different trading capabilities:

# Base Classes:

# TradingAccount: Basic account management
# RiskManagement: Risk assessment methods
# AnalyticsEngine: Market analysis capabilities
# NotificationSystem: Alert and reporting functionality
# Derived Classes:

# StockTrader(TradingAccount, RiskManagement, AnalyticsEngine): Stock trading with risk management
# CryptoTrader(TradingAccount, RiskManagement, NotificationSystem): Cryptocurrency trading with alerts
# ProfessionalTrader(StockTrader, CryptoTrader): Full-featured trader with all capabilities
# Requirements:

# Implement method resolution order correctly
# Override methods appropriately in each class
# Handle conflicts in multiple inheritance
# Implement portfolio tracking and performance metrics

class TradingAccount:
    def __init__(self, account_id, account_holder, balance=0.0):
        self.account_id = account_id
        self.account_holder = account_holder
        self.balance = balance
        self.portfolio = {}

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            raise ValueError("Invalid withdrawal amount")
        self.balance -= amount
        return f"Withdrew ${amount}, new balance is ${self.balance}"

    def get_balance(self):
        return self.balance

    def update_portfolio(self, asset, quantity):
        self.portfolio[asset] = self.portfolio.get(asset, 0) + quantity
        if self.portfolio[asset] == 0:
            del self.portfolio[asset]

    def get_portfolio(self):
        return dict(self.portfolio)

    def get_portfolio_value(self, price_lookup):
        # price_lookup: dict mapping asset to price
        return sum(self.portfolio.get(asset, 0) * price_lookup.get(asset, 0) for asset in self.portfolio)

class RiskManagement:
    def assess_portfolio_risk(self):
        # Dummy risk assessment based on portfolio size
        if hasattr(self, 'portfolio'):
            size = sum(abs(qty) for qty in getattr(self, 'portfolio', {}).values())
            if size > 100:
                return "High"
            elif size > 10:
                return "Medium"
        return "Low"

    def calculate_position_size(self, asset, price):
        # Use 10% of balance for each position as a simple rule
        if hasattr(self, 'balance'):
            position_value = self.balance * 0.1
            return int(position_value // price)
        return 0

class AnalyticsEngine:
    def analyze_market_trend(self, asset):
        # Dummy implementation
        return {"trend": "upward", "confidence": 0.85}

    def performance_metrics(self, price_lookup):
        # Calculate total value and return
        if hasattr(self, 'get_portfolio_value'):
            value = self.get_portfolio_value(price_lookup)
            return {"total_value": value}
        return {"total_value": 0}

class NotificationSystem:
    def __init__(self):
        self.notifications = []

    def set_price_alert(self, asset, price, condition):
        self.notifications.append({"asset": asset, "price": price, "condition": condition})
        return True

    def get_pending_notifications(self):
        return list(self.notifications)

class StockTrader(TradingAccount, RiskManagement, AnalyticsEngine):
    def __init__(self, account_id, account_holder, balance=0.0):
        TradingAccount.__init__(self, account_id, account_holder, balance)

    def execute_trade(self, asset, quantity, price):
        cost = quantity * price
        if cost > self.balance:
            raise ValueError("Insufficient funds")
        self.withdraw(cost)
        self.update_portfolio(asset, quantity)
        return f"Executed trade for {quantity} shares of {asset} at ${price}"

    def performance_metrics(self, price_lookup):
        # Override to add stock-specific metrics
        metrics = super().performance_metrics(price_lookup)
        metrics["type"] = "stock"
        return metrics

class CryptoTrader(TradingAccount, RiskManagement, NotificationSystem):
    def __init__(self, account_id, account_holder, balance=0.0):
        TradingAccount.__init__(self, account_id, account_holder, balance)
        NotificationSystem.__init__(self)

    def trade_crypto(self, asset, quantity, price):
        cost = quantity * price
        if cost > self.balance:
            raise ValueError("Insufficient funds")
        self.withdraw(cost)
        self.update_portfolio(asset, quantity)
        return f"Executed trade for {quantity} units of {asset} at ${price}"

    def performance_metrics(self, price_lookup):
        metrics = {"total_value": self.get_portfolio_value(price_lookup), "type": "crypto"}
        return metrics

class ProfessionalTrader(StockTrader, CryptoTrader):
    def __init__(self, account_id, account_holder, balance=0.0):
        StockTrader.__init__(self, account_id, account_holder, balance)
        NotificationSystem.__init__(self)  # Needed for NotificationSystem part

    def execute_diversified_strategy(self, strategy, price_lookup):
        # strategy: dict with keys 'stocks', 'crypto', 'allocation'
        stocks = strategy.get("stocks", [])
        cryptos = strategy.get("crypto", [])
        allocation = strategy.get("allocation", {"stocks": 0.5, "crypto": 0.5})
        total_balance = self.get_balance()
        results = []
        # Allocate and buy stocks
        stock_funds = total_balance * allocation.get("stocks", 0.5)
        for asset in stocks:
            price = price_lookup.get(asset, 100)
            qty = int(stock_funds // (len(stocks) * price))
            if qty > 0:
                results.append(self.execute_trade(asset, qty, price))
        # Allocate and buy crypto
        crypto_funds = total_balance * allocation.get("crypto", 0.5)
        for asset in cryptos:
            price = price_lookup.get(asset, 1000)
            qty = int(crypto_funds // (len(cryptos) * price))
            if qty > 0:
                results.append(self.trade_crypto(asset, qty, price))
        return {"status": "executed", "positions": results}

# Test Case 1: Multiple inheritance setup and MRO
stock_trader = StockTrader("ST001", "John Doe", 50000.0)
crypto_trader = CryptoTrader("CT001", "Jane Smith", 25000.0)
pro_trader = ProfessionalTrader("PT001", "Mike Johnson", 100000.0)

# Check Method Resolution Order
mro_names = [cls.__name__ for cls in ProfessionalTrader.__mro__]
assert "ProfessionalTrader" in mro_names
assert "StockTrader" in mro_names
assert "CryptoTrader" in mro_names

# Test Case 2: Account management capabilities
assert stock_trader.account_id == "ST001"
assert stock_trader.balance == 50000.0

deposit_result = stock_trader.deposit(10000)
assert stock_trader.balance == 60000.0
assert deposit_result == True

withdrawal_result = stock_trader.withdraw(5000)
assert stock_trader.balance == 55000.0

# Test Case 3: Risk management functionality
# Stock trader should have risk assessment
risk_level = stock_trader.assess_portfolio_risk()
assert risk_level in ["Low", "Medium", "High"]

position_size = stock_trader.calculate_position_size("AAPL", 150.0)
assert isinstance(position_size, int)
assert position_size >= 0

# Test Case 4: Analytics capabilities
# Stock trader has analytics through inheritance
market_data = stock_trader.analyze_market_trend("AAPL")
assert isinstance(market_data, dict)
assert "trend" in market_data
assert "confidence" in market_data

# Test Case 5: Notification system for crypto trader
# Crypto trader should handle alerts
alert_set = crypto_trader.set_price_alert("BTC", 45000, "above")
assert alert_set == True

notifications = crypto_trader.get_pending_notifications()
assert isinstance(notifications, list)

# Test Case 6: Professional trader combining all features
# Should have access to all inherited methods
assert hasattr(pro_trader, 'assess_portfolio_risk')  # From RiskManagement
assert hasattr(pro_trader, 'analyze_market_trend')   # From AnalyticsEngine
assert hasattr(pro_trader, 'set_price_alert')        # From NotificationSystem

# Execute complex trading strategy
price_lookup = {"AAPL": 150, "GOOGL": 2800, "BTC": 30000, "ETH": 2000}
strategy_result = pro_trader.execute_diversified_strategy({
    "stocks": ["AAPL", "GOOGL"],
    "crypto": ["BTC", "ETH"],
    "allocation": {"stocks": 0.7, "crypto": 0.3}
}, price_lookup)
assert strategy_result["status"] == "executed"
assert len(strategy_result["positions"]) > 0

# Portfolio and performance metrics
assert isinstance(pro_trader.get_portfolio(), dict)
metrics = pro_trader.performance_metrics(price_lookup)
assert isinstance(metrics, dict)
assert "total_value" in metrics