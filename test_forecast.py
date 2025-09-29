"""
Test suite for pest forecasting components
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestPestForecastEngine:
    """Test cases for the forecast engine"""
    
    def test_engine_initialization(self):
        """Test that the forecast engine initializes properly"""
        from prediction.forecast_engine import PestForecastEngine
        
        engine = PestForecastEngine()
        assert engine is not None
        assert engine.forecast_cache == {}
        assert engine.last_update is None
    
    def test_bounds_calculation(self):
        """Test bounds calculation for forecast area"""
        from prediction.forecast_engine import PestForecastEngine
        
        engine = PestForecastEngine()
        center_lat, center_lon = 40.0, -74.0
        radius_km = 10
        
        bounds = engine._calculate_bounds(center_lat, center_lon, radius_km)
        
        assert len(bounds) == 4
        min_lat, min_lon, max_lat, max_lon = bounds
        
        assert min_lat < center_lat < max_lat
        assert min_lon < center_lon < max_lon

class TestWeatherCollector:
    """Test cases for weather data collection"""
    
    def test_weather_suitability_calculation(self):
        """Test weather suitability calculation"""
        from data.weather_collector import WeatherCollector
        
        # Mock weather data
        weather_data = pd.DataFrame({
            'temperature': [20, 25, 30, 35],
            'humidity': [60, 70, 80, 50],
            'wind_speed': [5, 10, 15, 25]
        })
        
        collector = WeatherCollector(api_key="test_key")
        result = collector.calculate_weather_suitability(weather_data, 'aphids')
        
        assert 'suitability' in result.columns
        assert all(0 <= s <= 1 for s in result['suitability'])

class TestPestDataManager:
    """Test cases for pest data management"""
    
    def test_observation_addition(self):
        """Test adding pest observations"""
        from data.pest_data import PestDataManager, PestObservation
        
        manager = PestDataManager()
        
        obs = PestObservation(
            timestamp=datetime.now(),
            lat=40.0,
            lon=-74.0,
            pest_type='aphids',
            count=10,
            severity=0.5,
            field_id='test_field',
            observer='test'
        )
        
        manager.add_observation(obs)
        assert len(manager.observations) == 1
        assert manager.observations[0].pest_type == 'aphids'
    
    def test_density_calculation(self):
        """Test pest density calculation"""
        from data.pest_data import PestDataManager
        
        manager = PestDataManager()
        
        # Test with empty observations
        bounds = (39.9, -74.1, 40.1, -73.9)
        density_grid = manager.get_pest_density_grid(bounds)
        
        assert isinstance(density_grid, pd.DataFrame)
        assert 'lat' in density_grid.columns
        assert 'lon' in density_grid.columns
        assert 'density' in density_grid.columns

class TestRiskAssessment:
    """Test cases for risk assessment"""
    
    def test_risk_score_calculation(self):
        """Test risk score calculation"""
        from models.risk_assessment import RiskAssessmentEngine
        
        engine = RiskAssessmentEngine()
        
        location_data = {
            'weather_suitability': 0.8,
            'current_pest_count': 15,
            'crop_vulnerability': 0.7,
            'historical_risk': 0.6,
            'seasonal_factor': 0.5
        }
        
        risk_score = engine.calculate_risk_score(location_data)
        
        assert 0 <= risk_score <= 1
    
    def test_risk_categorization(self):
        """Test risk level categorization"""
        from models.risk_assessment import RiskAssessmentEngine
        
        engine = RiskAssessmentEngine()
        
        assert engine.categorize_risk(0.1) == 'low'
        assert engine.categorize_risk(0.4) == 'medium'
        assert engine.categorize_risk(0.7) == 'high'
        assert engine.categorize_risk(0.9) == 'critical'

class TestSpreadCalculator:
    """Test cases for spread calculation"""
    
    def test_diffusion_model(self):
        """Test diffusion-based spread calculation"""
        from prediction.spread_calculator import DiffusionModel
        
        model = DiffusionModel(diffusion_rate=0.1)
        
        initial_points = [(40.0, -74.0, 10), (40.01, -74.01, 15)]
        time_hours = 24
        
        result = model.calculate_spread(initial_points, time_hours)
        
        assert isinstance(result, pd.DataFrame)
        assert 'lat' in result.columns
        assert 'lon' in result.columns
        assert 'predicted_intensity' in result.columns

class TestRouteOptimizer:
    """Test cases for drone route optimization"""
    
    def test_distance_calculation(self):
        """Test distance calculation between points"""
        from mapping.route_optimizer import DroneRouteOptimizer
        
        optimizer = DroneRouteOptimizer()
        
        # Test known distance (approximately)
        lat1, lon1 = 40.0, -74.0
        lat2, lon2 = 40.1, -74.0
        
        distance = optimizer._calculate_distance(lat1, lon1, lat2, lon2)
        
        # Should be approximately 11.1 km (0.1 degree latitude)
        assert 10 < distance < 12
    
    def test_route_optimization(self):
        """Test basic route optimization"""
        from mapping.route_optimizer import DroneRouteOptimizer
        
        optimizer = DroneRouteOptimizer()
        
        # Create sample intervention areas
        areas = pd.DataFrame({
            'area_id': [1, 2, 3],
            'lat': [40.0, 40.01, 40.02],
            'lon': [-74.0, -74.01, -74.02],
            'priority_score': [0.8, 0.6, 0.9],
            'area_hectares': [10, 15, 8]
        })
        
        base_location = (40.0, -74.0)
        
        result = optimizer.optimize_spray_routes(areas, base_location, max_drones=1)
        
        assert 'routes' in result
        assert 'summary' in result

if __name__ == "__main__":
    pytest.main([__file__])
