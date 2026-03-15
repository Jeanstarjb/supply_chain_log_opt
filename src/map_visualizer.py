import pandas as pd
import sqlite3
import folium

class MapVisualizer:
    """
    Visualizes the supply chain network and optimized routes on an interactive map.
    """
    
    def __init__(self, db_path="database/logistics.db", routes_path="data/processed/optimized_routes.csv"):
        self.db_path = db_path
        self.routes_path = routes_path
        
    def create_map(self):
        # Initialize map centered on Kenya
        m = folium.Map(location=[0.0236, 37.9062], zoom_start=6, tiles="cartodbpositron")
        
        conn = sqlite3.connect(self.db_path)
        suppliers_df = pd.read_sql_query("SELECT * FROM Suppliers", conn)
        hubs_df = pd.read_sql_query("SELECT * FROM Demand_Hubs", conn)
        conn.close()
        
        # Load optimized routes
        try:
            routes_df = pd.read_csv(self.routes_path)
        except FileNotFoundError:
            print("Error: Optimized routes file not found. Run the optimizer first.")
            return
            
        # Plot Suppliers (Green markers)
        for _, s in suppliers_df.iterrows():
            folium.Marker(
                location=[s['latitude'], s['longitude']],
                popup=f"Supplier: {s['name']}<br>Capacity: {s['capacity']}",
                icon=folium.Icon(color="green", icon="leaf")
            ).add_to(m)
            
        # Plot Demand Hubs (Red markers)
        for _, h in hubs_df.iterrows():
            folium.Marker(
                location=[h['latitude'], h['longitude']],
                popup=f"Hub: {h['name']}<br>Demand: {h['demand']}",
                icon=folium.Icon(color="red", icon="home")
            ).add_to(m)
            
        # Plot Routes
        for _, r in routes_df.iterrows():
            s_data = suppliers_df[suppliers_df['supplier_id'] == r['supplier_id']].iloc[0]
            h_data = hubs_df[hubs_df['hub_id'] == r['hub_id']].iloc[0]
            
            # Line weight based on flow volume
            weight = max(1, r['flow'] / 500)
            
            folium.PolyLine(
                locations=[[s_data['latitude'], s_data['longitude']], 
                           [h_data['latitude'], h_data['longitude']]],
                weight=weight,
                color="blue",
                opacity=0.7,
                tooltip=f"Route: {s_data['name']} -> {h_data['name']}<br>Tonnes: {r['flow']}"
            ).add_to(m)
            
        m.save("data/processed/logistics_map.html")
        print("Interactive map saved to data/processed/logistics_map.html")

if __name__ == "__main__":
    visualizer = MapVisualizer()
    visualizer.create_map()
