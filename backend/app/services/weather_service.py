from typing import Dict, Any, List

class WeatherRiskService:
    """
    Transparent rule-based Weather Disease Risk Engine.
    Evaluates temperature, relative humidity, and rainfall to generate disease risk metrics.
    Can be swapped with a trained machine learning risk model.
    """

    @staticmethod
    def calculate_risk(temp_c: float, humidity_pct: float, rainfall_mm: float = 0.0, crop: str = "Tomato", disease: str = "Late Blight") -> Dict[str, Any]:
        risk_score = 0.0
        factors: List[str] = []

        # Temperature evaluation (Ideal fungal range: 15-28°C)
        if 18.0 <= temp_c <= 25.0:
            risk_score += 35.0
            factors.append(f"Optimal temperature for pathogen germination ({temp_c}°C)")
        elif 12.0 <= temp_c < 18.0 or 25.0 < temp_c <= 32.0:
            risk_score += 20.0
            factors.append(f"Moderate thermal favorability ({temp_c}°C)")
        else:
            risk_score += 5.0
            factors.append(f"Extreme temperature suppressing spore spread ({temp_c}°C)")

        # Humidity evaluation (Critical threshold >75%)
        if humidity_pct >= 85.0:
            risk_score += 45.0
            factors.append(f"High relative humidity level ({humidity_pct}%) accelerates foliar wetness")
        elif humidity_pct >= 70.0:
            risk_score += 30.0
            factors.append(f"Elevated humidity ({humidity_pct}%) promotes leaf dew")
        else:
            risk_score += 10.0
            factors.append(f"Low relative humidity ({humidity_pct}%) reduces sporulation")

        # Rainfall / Dew duration evaluation
        if rainfall_mm > 10.0:
            risk_score += 20.0
            factors.append(f"Substantial rainfall ({rainfall_mm} mm) splashing soil-borne spores")
        elif rainfall_mm > 0.0:
            risk_score += 10.0
            factors.append(f"Light precipitation ({rainfall_mm} mm) maintaining leaf wetness")

        # Normalize score to 0-100
        risk_score = round(min(100.0, max(0.0, risk_score)), 1)

        # Categorize Risk Level
        if risk_score >= 75.0:
            level = "Critical"
            advice = "High disease outbreak risk! Apply preventive organic/fungicidal spray immediately."
        elif risk_score >= 50.0:
            level = "High"
            advice = "Favorable weather for fungal growth. Inspect leaf undersides every 48 hours."
        elif risk_score >= 30.0:
            level = "Medium"
            advice = "Moderate risk. Ensure adequate crop drainage and avoid overhead watering."
        else:
            level = "Low"
            advice = "Weather conditions are currently dry and unfavourable for rapid disease transmission."

        return {
            "risk_score": risk_score,
            "risk_level": level,
            "contributing_factors": factors,
            "advice": advice
        }
