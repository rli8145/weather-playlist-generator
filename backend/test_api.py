"""
Test script for Forecast.fm API
Tests the /predict endpoint with sample audio features
"""
import requests
import json

# API base URL (update if running on different host/port)
BASE_URL = "http://localhost:8000"

# Sample audio features for testing
test_cases = [
    {
        "name": "Sunny Song",
        "features": {
            "energy": 0.85,
            "valence": 0.9,
            "tempo": 128.0,
            "acousticness": 0.15,
            "loudness": -4.5
        },
        "expected": "sunny"
    },
    {
        "name": "Rainy Song",
        "features": {
            "energy": 0.3,
            "valence": 0.2,
            "tempo": 70.0,
            "acousticness": 0.7,
            "loudness": -12.0
        },
        "expected": "rainy"
    },
    {
        "name": "Cloudy Song",
        "features": {
            "energy": 0.5,
            "valence": 0.5,
            "tempo": 100.0,
            "acousticness": 0.4,
            "loudness": -8.0
        },
        "expected": "cloudy"
    },
    {
        "name": "Snowy Song",
        "features": {
            "energy": 0.2,
            "valence": 0.3,
            "tempo": 60.0,
            "acousticness": 0.8,
            "loudness": -15.0
        },
        "expected": "snowy"
    }
]


def test_health():
    """Test the health endpoint"""
    print("\n🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Health check passed")
        print(f"  Status: {data['status']}")
        print(f"  Model loaded: {data['model_loaded']}")
        if data.get('model_info'):
            print(f"  Model type: {data['model_info'].get('type')}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API. Is the server running?")
        print(f"  Start server with: cd backend/app && uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False


def test_features():
    """Test the features endpoint"""
    print("\n🔍 Testing /features endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/features")
        response.raise_for_status()
        data = response.json()
        print(f"✓ Features endpoint working")
        print(f"  Expected features: {data['features']}")
        return True
    except Exception as e:
        print(f"✗ Features endpoint failed: {e}")
        return False


def test_predictions():
    """Test the prediction endpoint with sample data"""
    print("\n🔍 Testing /predict endpoint...")

    for test_case in test_cases:
        print(f"\n  Testing: {test_case['name']}")
        print(f"    Features: {test_case['features']}")

        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=test_case['features']
            )
            response.raise_for_status()
            data = response.json()

            prediction = data['weather']
            confidence = data['confidence']

            print(f"    ✓ Prediction: {prediction} (confidence: {confidence:.2%})")

            if prediction == test_case['expected']:
                print(f"    ✓ Matches expected: {test_case['expected']}")
            else:
                print(f"    ⚠ Expected {test_case['expected']}, got {prediction}")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 503:
                print(f"    ✗ Model not loaded. Please place model.pkl in backend/models/")
                return False
            else:
                print(f"    ✗ HTTP error: {e}")
        except Exception as e:
            print(f"    ✗ Prediction failed: {e}")

    return True


def test_invalid_input():
    """Test the API with invalid input"""
    print("\n🔍 Testing invalid input handling...")

    invalid_cases = [
        {
            "name": "Energy out of range",
            "features": {
                "energy": 1.5,  # Invalid: should be 0-1
                "valence": 0.5,
                "tempo": 120.0,
                "acousticness": 0.3,
                "loudness": -5.0
            }
        },
        {
            "name": "Missing field",
            "features": {
                "energy": 0.5,
                "valence": 0.5,
                # Missing tempo
                "acousticness": 0.3,
                "loudness": -5.0
            }
        }
    ]

    for test_case in invalid_cases:
        print(f"\n  Testing: {test_case['name']}")
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=test_case['features']
            )
            if response.status_code == 422 or response.status_code == 400:
                print(f"    ✓ Correctly rejected invalid input (status {response.status_code})")
            else:
                print(f"    ⚠ Unexpected status code: {response.status_code}")
        except Exception as e:
            print(f"    ✗ Error: {e}")

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Forecast.fm API Test Suite")
    print("=" * 60)

    # Test health endpoint
    if not test_health():
        print("\n⚠ Server not running. Please start the server first:")
        print("  cd backend/app")
        print("  uvicorn main:app --reload")
        exit(1)

    # Test features endpoint
    test_features()

    # Test predictions
    test_predictions()

    # Test invalid input
    test_invalid_input()

    print("\n" + "=" * 60)
    print("✓ Test suite completed!")
    print("=" * 60)
