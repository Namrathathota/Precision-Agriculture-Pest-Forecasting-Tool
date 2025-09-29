"""
Main entry point for the Pest Forecasting Tool
Provides command-line interface and demonstration functionality
"""
import sys
import os
import logging
from datetime import datetime

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pest_forecast.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def run_demo():
    """Run a demonstration of the pest forecasting system"""
    print("🌾 Precision Agriculture Pest Forecasting Tool")
    print("=" * 50)
    
    try:
        # Import components
        from prediction.forecast_engine import PestForecastEngine
        from mapping.visualization import InteractiveMapBuilder
        from data.pest_data import PestObservation
        
        print("📡 Initializing forecast engine...")
        forecast_engine = PestForecastEngine(demo_mode=True)
        forecast_engine.initialize_components()
        
        # Sample location (Central Valley, California)
        center_lat = 36.7783
        center_lon = -119.4179
        radius_km = 15
        pest_type = 'aphids'
        
        print(f"📍 Generating forecast for location: {center_lat}, {center_lon}")
        print(f"🐛 Pest type: {pest_type}")
        print(f"📏 Radius: {radius_km} km")
        
        # Add some sample observations
        print("\n👁️ Adding sample pest observations...")
        
        # Add a few sample observations around the center
        sample_observations = [
            (center_lat + 0.01, center_lon - 0.01, 15, 0.7),
            (center_lat - 0.01, center_lon + 0.01, 8, 0.5),
            (center_lat + 0.005, center_lon + 0.005, 12, 0.6)
        ]
        
        for lat, lon, count, severity in sample_observations:
            forecast_engine.update_pest_observation(
                lat=lat, lon=lon, pest_type=pest_type,
                count=count, severity=severity, observer="demo"
            )
            print(f"  📝 Added observation: {count} pests at ({lat:.4f}, {lon:.4f})")
        
        # Generate forecast
        print("\n🔮 Generating pest forecast...")
        forecast_data = forecast_engine.generate_forecast(
            center_lat=center_lat,
            center_lon=center_lon,
            radius_km=radius_km,
            pest_type=pest_type,
            forecast_hours=[24, 48, 72]
        )
        
        if forecast_data['status'] == 'success':
            print("✅ Forecast generated successfully!")
            
            # Display summary
            summary = forecast_data.get('summary', {})
            print(f"\n📊 Forecast Summary:")
            print(f"  Overall Risk Level: {summary.get('overall_risk', 'unknown').title()}")
            print(f"  High-Risk Areas: {summary.get('high_risk_area_count', 0)}")
            print(f"  Peak Risk Time: {summary.get('peak_risk_time', 'N/A')}")
            
            # Show recommendations
            recommendations = summary.get('recommendations', [])
            if recommendations:
                print(f"\n💡 Recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {i}. {rec}")
            
            # Show forecast details for each time horizon
            forecasts = forecast_data.get('forecasts', {})
            for time_horizon, forecast in forecasts.items():
                print(f"\n📈 {time_horizon} Forecast:")
                high_risk_areas = forecast.get('high_risk_areas', [])
                print(f"  High-risk locations: {len(high_risk_areas)}")
                
                intervention_priorities = forecast.get('intervention_priorities', [])
                if intervention_priorities:
                    top_priority = intervention_priorities[0]
                    print(f"  Top priority field: {top_priority.get('field_id', 'unknown')} "
                          f"(score: {top_priority.get('priority_score', 0):.2f})")
                
                print(f"  Confidence: {forecast.get('confidence', 0.5):.1%}")
            
            # Generate maps
            print(f"\n🗺️ Generating visualization maps...")
            try:
                map_builder = InteractiveMapBuilder()
                maps = map_builder.build_comprehensive_map(forecast_data)
                
                # Save maps to files
                output_dir = "output_maps"
                os.makedirs(output_dir, exist_ok=True)
                map_builder.save_all_maps(maps, output_dir)
                
                print(f"  📁 Maps saved to '{output_dir}' directory")
                print(f"  🌐 Open the HTML files in a web browser to view interactive maps")
                
            except Exception as e:
                print(f"  ⚠️ Map generation failed: {e}")
            
        else:
            print(f"❌ Forecast generation failed: {forecast_data.get('message', 'Unknown error')}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        logging.exception("Demo execution failed")

def run_web_app():
    """Run the Streamlit web application"""
    print("🌐 Starting web application...")
    print("👆 Open your browser to the URL shown below")
    
    try:
        import subprocess
        import sys
        
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/web/app.py", "--server.port", "8501"
        ])
        
    except ImportError:
        print("❌ Streamlit not installed. Install with: pip install streamlit")
    except Exception as e:
        print(f"❌ Failed to start web app: {e}")

def main():
    """Main function with CLI interface"""
    setup_logging()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "demo":
            run_demo()
        elif command == "web":
            run_web_app()
        elif command == "help":
            show_help()
        else:
            print(f"Unknown command: {command}")
            show_help()
    else:
        # Default: run demo
        run_demo()

def show_help():
    """Show help information"""
    print("""
🌾 Precision Agriculture Pest Forecasting Tool

Usage:
  python main.py [command]

Commands:
  demo    - Run a demonstration with sample data (default)
  web     - Start the web application interface
  help    - Show this help message

Examples:
  python main.py demo          # Run demo with sample forecast
  python main.py web           # Start web interface
  
Features:
  📊 24-72 hour pest infestation forecasts
  🗺️ Interactive risk maps
  🚁 Drone route optimization
  💰 Cost-benefit analysis
  🎯 Targeted intervention planning

Requirements:
  - Python 3.8+
  - See requirements.txt for dependencies
  - OpenWeatherMap API key (optional, for real weather data)

Configuration:
  - Set API keys in config/settings.py
  - Modify pest parameters as needed
  - Adjust grid resolution for performance

For more information, see README.md
""")

if __name__ == "__main__":
    main()
