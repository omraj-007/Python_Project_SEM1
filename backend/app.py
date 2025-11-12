print("Starting Flask application...")

import os
import sys
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

# --- Data path checks (keep your helpful logs) ---
data_file_path = os.path.join('..', 'data', 'internship.csv')
print(f"Looking for data file at: {os.path.abspath(data_file_path)}")

parent_dir = '..'
if os.path.exists(parent_dir):
    print(f"Contents of parent directory: {os.listdir(parent_dir)}")
else:
    print("❌ Parent directory not accessible")

data_dir = os.path.join('..', 'data')
if os.path.exists(data_dir):
    print("✅ Data directory exists")
    print(f"Contents of data directory: {os.listdir(data_dir)}")
else:
    print("❌ Data directory not found")

if not os.path.exists(data_file_path):
    print("❌ Data file not found")
    print("Creating sample data file...")
    try:
        os.makedirs(data_dir, exist_ok=True)
        print(f"✅ Data directory created at: {os.path.abspath(data_dir)}")
    except Exception as e:
        print(f"❌ Error creating data directory: {e}")

    sample_data = """internship_title,company_name,location,start_date,duration,stipend
Java Development,SunbaseData,Work From Home,Immediately,6 Months,"₹ 30,000 /month"
Accounting and Finance,DAKSM & Co. LLP,Noida,Immediately,6 Months,"₹ 5,000-10,000 /month"
Sales & Digital Marketing,Bharat Natural Elements Private Limited,Bangalore,Immediately,6 Months,"₹ 5,000 /month"
Social Entrepreneurship,Hamari Pahchan NGO,Work From Home,Immediately,6 Months,Unpaid
Videography & Photography,Esquare Lifestyle,Bangalore,Immediately,6 Months,"₹ 12,000 /month"
English Curriculum Writing,Team Everest,Work From Home,Immediately,6 Months,Unpaid
Search Engine Optimization,Global Trend,Work From Home,Immediately,6 Months,"₹ 5,000 /month"
Digital Dreamweaver,Global Trend,Work From Home,Immediately,6 Months,"₹ 7,000 /month"
Graphic Design,Expedify,Work From Home,Immediately,6 Months,"₹ 10,000-15,000 /month"
Campus Ambassador,Internshala,Work From Home,Not specified,6 Months,"₹ 2000"
Customer Support,ClearTax,Bangalore,Immediately,6 Months,"₹ 30,000 /month"
Web Development,TechCorp,Mumbai,Immediately,6 Months,"₹ 25,000 /month"
Python Development,DevCorp,Work From Home,Immediately,6 Months,"₹ 35,000 /month"
UI/UX Design,DesignStudio,Pune,Immediately,6 Months,"₹ 20,000 /month"
Content Writing,MediaHouse,Work From Home,Immediately,6 Months,"₹ 15,000 /month"
"""
    try:
        with open(data_file_path, 'w', encoding='utf-8') as f:
            f.write(sample_data)
        print("✅ Sample data file created successfully")
    except Exception as e:
        print(f"❌ Error creating sample data file: {e}")
        alternative_path = 'internship.csv'
        try:
            with open(alternative_path, 'w', encoding='utf-8') as f:
                f.write(sample_data)
            data_file_path = alternative_path
            print(f"✅ Created data file in current directory: {alternative_path}")
        except Exception as e2:
            print(f"❌ Failed to create data file anywhere: {e2}")
            sys.exit(1)

# --- Flask app ---
app = Flask(__name__)
CORS(app)  # Safe even if already enabled elsewhere

print("Initializing data processor...")
try:
    from data_processor import DataProcessor
    data_processor = DataProcessor(data_file_path)
    print("✅ Data processor initialized successfully")
except Exception as e:
    print(f"❌ Error initializing data processor: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Initializing recommendation engine...")
try:
    from recommendation_engine import RecommendationEngine
    recommendation_engine = RecommendationEngine(data_processor)
    print("✅ Recommendation system initialized successfully")
except Exception as e:
    print(f"❌ Error initializing recommendation engine: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# --- Helpers ---
def get_current_timestamp():
    # Keep UTC for deterministic logs
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


# --- Routes ---
@app.route('/')
def home():
    return jsonify({
        'message': 'Internship Recommendation Engine API',
        'status': 'running',
        'version': '1.0.0',
        'timestamp': get_current_timestamp(),
        'user': 'Om Raj Singh',
        'endpoints': {
            'health': '/health',
            'recommend': '/recommend',
            'test': '/test',
            'api_recommendations': '/api/recommendations'
        }
    })


@app.route('/health')
def health():
    try:
        if data_processor and hasattr(data_processor, 'df') and data_processor.df is not None:
            data_count = len(data_processor.df)
            status = 'healthy'
        else:
            data_count = 0
            status = 'unhealthy - no data'

        response = {
            'status': status,
            'data_loaded': data_count,
            'timestamp': get_current_timestamp(),
            'server': 'Flask Development Server',
            'user': 'Om Raj Singh',
            'endpoints_available': ['/', '/health', '/test', '/recommend', '/api/recommendations']
        }
        print(f"Health check requested - Status: {status}, Data count: {data_count}")
        return jsonify(response)

    except Exception as e:
        print(f"❌ Error in health endpoint: {e}")
        return jsonify({
            'status': 'error',
            'error_message': str(e),
            'timestamp': get_current_timestamp(),
            'user': 'Om Raj Singh'
        }), 500


# Legacy-style form/JSON endpoint you already had — unchanged except minor hygiene
@app.route('/recommend', methods=['POST'])
def get_recommendations_old():
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        print(f"Received recommendation request: {data}")

        required_fields = ['name', 'education', 'skills', 'location_preference', 'min_stipend']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'timestamp': get_current_timestamp()
                }), 400

        candidate_profile = {
            'name': data['name'],
            'education': data['education'],
            'skills': data['skills'] if isinstance(data['skills'], list) else [data['skills']],
            'location_preference': data['location_preference'],
            'min_stipend': float(data.get('min_stipend', 0))
        }

        print(f"Candidate profile: {candidate_profile}")
        recommendations = recommendation_engine.get_recommendations(candidate_profile)
        print(f"Generated {len(recommendations)} recommendations")

        return jsonify({
            'success': True,
            'candidate': candidate_profile,
            'recommendations': recommendations,
            'total_recommendations': len(recommendations),
            'timestamp': get_current_timestamp(),
            'processed_by': 'Om Raj Singh'
        })

    except Exception as e:
        print(f"Error in /recommend endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e),
            'timestamp': get_current_timestamp()
        }), 500


# ---- NEW: GET helper for /api/recommendations (so GET is no longer 405) ----
@app.route('/api/recommendations', methods=['GET'])
def recommendations_get():
    return jsonify({
        "message": "Use POST with JSON to fetch recommendations.",
        "examples": [
            {"education": "B.Tech", "skills": ["python", "ml"], "location_preference": "Bengaluru", "top_k": 5},
            {"query": "data science intern remote", "top_k": 5}
        ],
        "timestamp": get_current_timestamp()
    }), 200


# ---- Existing POST (with OPTIONS) endpoint; kept and hardened ----
@app.route('/api/recommendations', methods=['POST', 'OPTIONS'])
def get_recommendations():
    """Newer API endpoint your frontend calls."""
    # Handle CORS preflight explicitly (Flask-CORS also helps)
    if request.method == 'OPTIONS':
        print("📥 CORS preflight request received")
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    try:
        print(f"\n📥 API recommendation request received at {get_current_timestamp()}")

        if not data_processor or not recommendation_engine:
            print("❌ System not initialized")
            return jsonify({
                'success': False,
                'message': 'System not initialized properly',
                'timestamp': get_current_timestamp()
            }), 500

        data = request.get_json(silent=True) or {}
        print(f"📊 Request data: {data}")

        # Accept either the structured profile (education/skills/location) or a plain query string
        query = data.get("query", "").strip()

        if query:
            # If 'query' is provided, let engine interpret it (if supported)
            try:
                # Try common signatures without breaking your engine API
                if hasattr(recommendation_engine, "recommend"):
                    try:
                        recommendations = recommendation_engine.recommend(query=query, top_k=int(data.get("top_k", 5)))
                    except TypeError:
                        try:
                            recommendations = recommendation_engine.recommend(query, int(data.get("top_k", 5)))
                        except TypeError:
                            recommendations = recommendation_engine.recommend(query)
                else:
                    # Fallback to your existing method using a synthesized profile
                    user_profile = {
                        "education": data.get("education", ""),
                        "skills": data.get("skills", query.split()),
                        "location_preference": data.get("location_preference", ""),
                        "min_stipend": data.get("min_stipend", 0)
                    }
                    recommendations = recommendation_engine.get_recommendations(user_profile)
            except Exception:
                # Final fallback to your current profile-based API
                user_profile = {
                    "education": data.get("education", ""),
                    "skills": data.get("skills", query.split()),
                    "location_preference": data.get("location_preference", ""),
                    "min_stipend": data.get("min_stipend", 0)
                }
                recommendations = recommendation_engine.get_recommendations(user_profile)
        else:
            # Structured profile path (your existing contract)
            required_fields = ['education', 'skills', 'location_preference']
            missing_fields = [f for f in required_fields if f not in data or not data[f]]
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
                return jsonify({
                    'success': False,
                    'message': f'Missing required fields: {", ".join(missing_fields)}',
                    'timestamp': get_current_timestamp()
                }), 400

            if not isinstance(data['skills'], list) or len(data['skills']) == 0:
                print("❌ No skills provided")
                return jsonify({
                    'success': False,
                    'message': 'At least one skill must be selected',
                    'timestamp': get_current_timestamp()
                }), 400

            user_profile = {
                'education': data['education'],
                'skills': data['skills'],
                'location_preference': data['location_preference'],
                'min_stipend': data.get('min_stipend', 0)
            }
            print(f"🎯 User profile: {user_profile}")
            print("🔍 Getting recommendations...")
            recommendations = recommendation_engine.get_recommendations(user_profile)

        print(f"✅ Generated {len(recommendations)} recommendations")
        for i, rec in enumerate(recommendations[:3]):
            title = rec.get('title', rec.get('internship_title', 'Unknown'))
            company = rec.get('company', rec.get('company_name', 'Unknown'))
            print(f"  {i+1}. {title} at {company}")

        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations),
            'timestamp': get_current_timestamp(),
            'message': f'Found {len(recommendations)} matching internships',
            'processed_by': 'Om Raj Singh'
        })

    except Exception as e:
        error_msg = f"Error getting recommendations: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': error_msg,
            'timestamp': get_current_timestamp()
        }), 500


# ---- Fixed /test route (no get_data() call) ----
@app.route("/test", methods=["GET"])
def test_endpoint():
    """Return a tiny sample without assuming get_data() exists."""
    try:
        if hasattr(data_processor, "df"):
            df = data_processor.df
        elif hasattr(data_processor, "data"):
            df = data_processor.data
        else:
            return jsonify({"ok": False, "error": "No dataframe found on data_processor"}), 500

        sample = df.head(5).to_dict(orient="records")
        return jsonify({"ok": True, "rows": len(sample), "sample": sample})
    except Exception as e:
        app.logger.exception("Test endpoint failed")
        return jsonify({"ok": False, "error": str(e)}), 500


# ---- Small niceties ----
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "ok": False,
        "error": "Method Not Allowed",
        "hint": "Use POST for /api/recommendations, GET for usage."
    }), 405


@app.route("/favicon.ico")
def favicon():
    # Quiet the dev 404 spam
    return "", 204


if __name__ == '__main__':
    print("\n🚀 Starting Flask development server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("📍 Health check: http://localhost:5000/health")
    print("📍 API documentation: http://localhost:5000")
    print("📍 Test endpoint: http://localhost:5000/test")
    print("📍 Recommendations API: http://localhost:5000/api/recommendations")
    print(f"📍 User: Om Raj Singh")
    print(f"📍 Date: {get_current_timestamp()}")
    print("\n" + "="*50)
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
