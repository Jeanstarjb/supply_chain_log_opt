import sqlite3
import math

class DataGenerator:
    """
    Generates realistic dummy data for the Kenyan agricultural distribution network.
    """
    
    def __init__(self, db_path="database/logistics.db"):
        self.db_path = db_path
        # Kenyan Counties (Rural Supply centers) - Representative coordinates
        self.suppliers = [
            {"name": "Uasin Gishu (Eldoret)", "lat": 0.5143, "lon": 35.2698, "capacity": 5000},
            {"name": "Trans Nzoia (Kitale)", "lat": 1.0191, "lon": 35.0023, "capacity": 6000},
            {"name": "Nakuru", "lat": -0.3031, "lon": 36.0800, "capacity": 4500},
            {"name": "Bungoma", "lat": 0.5635, "lon": 34.5606, "capacity": 4000},
            {"name": "Narok", "lat": -1.0785, "lon": 35.8601, "capacity": 3500},
        ]
        
        # Kenyan Major Hubs (Demand centers)
        self.hubs = [
            {"name": "Nairobi", "lat": -1.286389, "lon": 36.817223, "demand": 3000},
            {"name": "Mombasa", "lat": -4.0435, "lon": 39.6682, "demand": 2500},
            {"name": "Kisumu", "lat": -0.0917, "lon": 34.7680, "demand": 2000},
            {"name": "Machakos", "lat": -1.5177, "lon": 37.2634, "demand": 1500},
            {"name": "Thika", "lat": -1.0333, "lon": 37.0667, "demand": 1200},
            {"name": "Garissa", "lat": -0.4532, "lon": 39.6461, "demand": 1000},
            {"name": "Eldoret", "lat": 0.5143, "lon": 35.2698, "demand": 1800},
            {"name": "Kisii", "lat": -0.6773, "lon": 34.7796, "demand": 1400},
            {"name": "Nyeri", "lat": -0.4167, "lon": 36.9500, "demand": 1100},
            {"name": "Malindi", "lat": -3.2175, "lon": 40.1169, "demand": 900},
        ]

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        R = 6371  # Earth radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    def generate(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open("database/schema.sql", "r") as f:
            cursor.executescript(f.read())
        
        # Insert Suppliers
        for s in self.suppliers:
            cursor.execute(
                "INSERT INTO Suppliers (name, latitude, longitude, capacity) VALUES (?, ?, ?, ?)",
                (s["name"], s["lat"], s["lon"], s["capacity"])
            )
        
        # Insert Hubs
        for h in self.hubs:
            cursor.execute(
                "INSERT INTO Demand_Hubs (name, latitude, longitude, demand) VALUES (?, ?, ?, ?)",
                (h["name"], h["lat"], h["lon"], h["demand"])
            )
            
        # Generate Transport Costs
        # Cost logic: Base cost + (distance * rate)
        # Assuming a rate of 0.5 KES per Ton-Km (fictional scaling)
        rate_per_km = 0.5
        base_handling_fee = 10
        
        cursor.execute("SELECT supplier_id, latitude, longitude FROM Suppliers")
        db_suppliers = cursor.fetchall()
        
        cursor.execute("SELECT hub_id, latitude, longitude FROM Demand_Hubs")
        db_hubs = cursor.fetchall()
        
        for s_id, s_lat, s_lon in db_suppliers:
            for h_id, h_lat, h_lon in db_hubs:
                dist = self.haversine(s_lat, s_lon, h_lat, h_lon)
                cost = base_handling_fee + (dist * rate_per_km)
                
                cursor.execute(
                    "INSERT INTO Transport_Costs (supplier_id, hub_id, distance_km, cost_per_unit) VALUES (?, ?, ?, ?)",
                    (s_id, h_id, round(dist, 2), round(cost, 2))
                )
        
        conn.commit()
        conn.close()
        print(f"Database populated successfully at {self.db_path}")

if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate()
