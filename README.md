# Supply Chain Logistics Optimizer: Kenyan Agricultural Distribution

## Project Overview
This project models and optimizes a staple crop (maize) distribution network in Kenya. It demonstrates the application of **Operations Research (OR)** and **Linear Programming (LP)** to minimize transportation costs across a multi-node supply chain.

By leveraging rural supply counties as production nodes and major urban centers as demand hubs, the optimizer calculates the most cost-effective flow of goods while respecting capacity and demand constraints.

## Tech Stack
- **Language:** Python 3.x
- **Optimization:** PuLP (Linear Programming)
- **Data Handling:** Pandas, NumPy
- **Database:** SQLite3 (Normalized 3NF Schema)
- **Visualization:** Folium (Geospatial Mapping)

## Project Structure
- `data/`: Contains raw and processed data.
- `database/`: SQL schema and SQLite database.
- `src/`: Core Python logic.
    - `generate_data.py`: Synthesizes realistic Kenyan geographic and logistics data.
    - `optimizer.py`: Problem formulation and cost minimization logic.
    - `map_visualizer.py`: Interactive geospatial visualization of routes.

## How It Works
1. **Mathematical Model:**
   - **Objective:** Minimize $Z = \sum_{i} \sum_{j} C_{ij} \cdot X_{ij}$
   - **Constraints:**
     - Supply: $\sum_{j} X_{ij} \leq \text{Capacity}_{i}$
     - Demand: $\sum_{i} X_{ij} \geq \text{Demand}_{j}$
2. **Data-Driven:** Costs are calculated based on the Haversine distance between coordinates and a unit transportation rate.
3. **Database-Backed:** All nodes and costs are managed in a relational SQLite database.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Generate base data: `python src/generate_data.py`
3. Run the optimizer: `python src/optimizer.py`
4. Visualize results: `python src/map_visualizer.py` (Outputs `data/processed/logistics_map.html`)
