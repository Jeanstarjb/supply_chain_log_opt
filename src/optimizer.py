import sqlite3
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value

class LogisticsOptimizer:
    """
    Core optimization engine using PuLP to minimize transportation costs.
    """
    
    def __init__(self, db_path="database/logistics.db"):
        self.db_path = db_path
        self.data = {}
        
    def fetch_data(self):
        """Fetches supply, demand, and cost data from SQLite."""
        conn = sqlite3.connect(self.db_path)
        
        # Load Suppliers (Capacity)
        self.data['suppliers'] = pd.read_sql_query("SELECT * FROM Suppliers", conn)
        # Load Hubs (Demand)
        self.data['hubs'] = pd.read_sql_query("SELECT * FROM Demand_Hubs", conn)
        # Load Costs
        self.data['costs'] = pd.read_sql_query("SELECT * FROM Transport_Costs", conn)
        
        conn.close()
        print("Data fetched successfully from database.")

    def solve(self):
        """
        Defines and solves the Linear Programming model.
        
        Mathematical Model:
        Minimize Z = sum(Cost_ij * Flow_ij) for all i (suppliers) and j (hubs)
        Subject to:
        1. sum(Flow_ij) <= Capacity_i (Supply constraint)
        2. sum(Flow_ij) >= Demand_j (Demand constraint)
        3. Flow_ij >= 0 (Non-negativity)
        """
        
        # Initialize the problem
        prob = LpProblem("Maize_Distribution_Optimization", LpMinimize)
        
        # Extract Indices
        suppliers = self.data['suppliers']['supplier_id'].tolist()
        hubs = self.data['hubs']['hub_id'].tolist()
        
        # Create a dictionary for costs for easy lookup
        # cost_map[(supplier_id, hub_id)] = cost_per_unit
        cost_map = self.data['costs'].set_index(['supplier_id', 'hub_id'])['cost_per_unit'].to_dict()
        
        # Decision Variables: Flow from supplier i to hub j
        flow_vars = LpVariable.dicts("Flow", 
                                     ((i, j) for i in suppliers for j in hubs), 
                                     lowBound=0)
        
        # Objective Function: Minimize Total Transportation Cost
        prob += lpSum([flow_vars[i, j] * cost_map[i, j] 
                       for i in suppliers for j in hubs]), "Total_Transport_Cost"
        
        # Constraint 1: Supply cannot exceed capacity
        for i in suppliers:
            capacity = self.data['suppliers'][self.data['suppliers']['supplier_id'] == i]['capacity'].values[0]
            prob += lpSum([flow_vars[i, j] for j in hubs]) <= capacity, f"Supply_Constraint_{i}"
            
        # Constraint 2: Demand must be met for each hub
        for j in hubs:
            demand = self.data['hubs'][self.data['hubs']['hub_id'] == j]['demand'].values[0]
            prob += lpSum([flow_vars[i, j] for i in suppliers]) >= demand, f"Demand_Constraint_{j}"
            
        # Solve the model
        status = prob.solve()
        
        print(f"Status: {LpStatus[status]}")
        print(f"Total Cost: KES {value(prob.objective):,.2f}")
        
        # Collect results
        results = []
        for i in suppliers:
            for j in hubs:
                if value(flow_vars[i, j]) > 0:
                    results.append({
                        'supplier_id': i,
                        'hub_id': j,
                        'flow': value(flow_vars[i, j])
                    })
        
        return pd.DataFrame(results)

    def save_results(self, results_df):
        """Saves the optimized routes to a CSV (or could be a new DB table)."""
        results_df.to_csv("data/processed/optimized_routes.csv", index=False)
        print("Optimized routes saved to data/processed/optimized_routes.csv")

if __name__ == "__main__":
    optimizer = LogisticsOptimizer()
    optimizer.fetch_data()
    routes = optimizer.solve()
    optimizer.save_results(routes)
