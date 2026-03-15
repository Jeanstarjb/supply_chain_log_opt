-- Supply Chain Logistics Optimizer Schema
-- Optimized for SQLite and 3rd Normal Form (3NF)

-- Suppliers Table: Stores location and production capacity information
CREATE TABLE IF NOT EXISTS Suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    capacity REAL NOT NULL -- Maximum units (e.g., tons of maize) available
);

-- DemandHubs Table: Stores location and demand requirements
CREATE TABLE IF NOT EXISTS Demand_Hubs (
    hub_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    demand REAL NOT NULL -- Minimum units required
);

-- TransportCosts Table: Stores the unit cost of transportation between supplier and hub
-- This table represents the relationship between suppliers and hubs with associated cost attributes
CREATE TABLE IF NOT EXISTS Transport_Costs (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER NOT NULL,
    hub_id INTEGER NOT NULL,
    distance_km REAL NOT NULL,
    cost_per_unit REAL NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
    FOREIGN KEY (hub_id) REFERENCES Demand_Hubs(hub_id),
    UNIQUE(supplier_id, hub_id)
);
