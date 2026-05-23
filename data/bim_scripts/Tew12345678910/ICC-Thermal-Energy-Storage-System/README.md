# ICC Heat Energy Calculation

A Python-based simulation project for calculating heat energy transfer in the International Commerce Centre (ICC) in Hong Kong.

## Overview

This project simulates and calculates the heat energy entering the International Commerce Centre (ICC), one of Hong Kong's iconic skyscrapers, with a focus on **Thermal Energy Storage (TES) systems for HVAC applications**. The primary goal is to develop greener, more sustainable solutions for building energy management.

### Purpose

The simulation evaluates the effectiveness of **Thermal Energy Storage systems** integrated with HVAC systems to:

- Reduce peak energy demand
- Optimize cooling/heating efficiency
- Lower carbon footprint
- Provide cost-effective energy management solutions
- Support Hong Kong's sustainability goals

The simulation takes into account various factors including:

- External temperature fluctuations
- Building thermal properties
- Heat transfer coefficients
- Time-based energy calculations
- Thermal energy storage capacity and efficiency
- HVAC system integration
- Visualization of energy transfer patterns

## Project Structure

```
ICC-Heat-Energy-Calculation/
├── README.md                    # Project documentation
├── main_simulation.py           # Primary heat energy simulation with visualization
├── year_simulation.py           # Extended year-long calculation (development version)
├── demo_simulation.py           # Demonstration version with sample parameters
└── calculated_data.csv          # Output data from simulations
```

## Files Description

### Core Simulation Files

- **`main_simulation.py`**: The primary simulation script that calculates heat energy transfer with real-time visualization capabilities. This is the main working version of the project.

- **`year_simulation.py`**: Extended simulation designed for year-long calculations. Currently in development phase.

- **`demo_simulation.py`**: Simplified demonstration version with pre-configured parameters for quick testing and presentation purposes.

### Data Files

- **`calculated_data.csv`**: Contains calculated heat energy data output from the simulations, including timestamps and energy values.

## Features

### Thermal Energy Storage (TES) Analysis

- **TES System Modeling**: Simulates thermal energy storage integration with HVAC systems
- **Energy Efficiency Optimization**: Calculates optimal charging/discharging cycles for maximum efficiency
- **Peak Load Management**: Analyzes how TES systems can reduce peak energy demand
- **Cost-Benefit Analysis**: Evaluates economic advantages of implementing TES solutions

### Heat Transfer & Simulation

- **Heat Transfer Simulation**: Calculates heat energy entering the ICC building based on thermal dynamics
- **Time-Series Analysis**: Processes energy data over specified time periods
- **HVAC Integration Modeling**: Simulates integration between TES systems and existing HVAC infrastructure

### Green Technology Solutions

- **Carbon Footprint Reduction**: Quantifies environmental benefits of TES implementation
- **Sustainability Metrics**: Measures improvement in building energy efficiency
- **Renewable Energy Integration**: Models compatibility with solar and other renewable sources

### Visualization & Analysis

- **Data Visualization**: Generates plots and charts to visualize energy transfer patterns
- **CSV Export**: Saves calculated data for further analysis
- **Configurable Parameters**: Adjustable building properties and environmental conditions

## Requirements

The project requires the following Python packages:

- `numpy` - for numerical calculations
- `matplotlib` - for data visualization
- `pandas` - for data manipulation and CSV handling

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/ICC-Heat-Energy-Calculation.git
cd ICC-Heat-Energy-Calculation
```

2. Install required dependencies:

```bash
pip install numpy matplotlib pandas
```

## Usage

### Running the Main Simulation

```bash
python main_simulation.py
```

This will run the primary heat energy calculation and display visualization results.

### Running the Demo

```bash
python demo_simulation.py
```

This provides a quick demonstration with pre-configured parameters.

### Year-Long Simulation

```bash
python year_simulation.py
```

Note: This is currently in development and may require additional configuration.

## Output

The simulations generate:

- Real-time plots showing heat energy transfer over time
- CSV files with calculated data points
- Console output with key statistics and results

## ICC Building Context

The International Commerce Centre (ICC) is a 108-story commercial skyscraper in Hong Kong, standing at 484 meters tall. This simulation project focuses on understanding the thermal dynamics and energy transfer characteristics of this significant architectural structure.
