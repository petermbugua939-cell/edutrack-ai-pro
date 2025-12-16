from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
import numpy as np
import json
import asyncio

# Create FastAPI app
app = FastAPI(title="EduTrack AI Pro", version="2.0")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Sample student data
students = [
    {"id": 1, "name": "John Doe", "class": "Form 4", "score": 85, "attendance": 92},
    {"id": 2, "name": "Jane Smith", "class": "Form 4", "score": 92, "attendance": 95},
    {"id": 3, "name": "Mike Johnson", "class": "Form 3", "score": 78, "attendance": 80},
    {"id": 4, "name": "Sarah Williams", "class": "Form 3", "score": 65, "attendance": 70},
    {"id": 5, "name": "David Brown", "class": "Form 2", "score": 88, "attendance": 90}
]

# ========== API ENDPOINTS ==========

# Home page
@app.get("/")
async def home():
    return {"message": "EduTrack AI Pro API", "status": "running", "version": "2.0"}

# Health check
@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Dashboard statistics
@app.get("/api/dashboard/stats")
async def dashboard_stats():
    return {
        "total_students": len(students),
        "average_score": round(np.mean([s["score"] for s in students]), 1),
        "average_attendance": round(np.mean([s["attendance"] for s in students]), 1),
        "performance_trend": "improving",
        "at_risk_students": len([s for s in students if s["score"] < 70]),
        "ai_predictions_made": 42,
        "timestamp": datetime.now().isoformat()
    }

# Get all students
@app.get("/api/students")
async def get_students():
    return {
        "students": students,
        "count": len(students),
        "summary": {
            "top_performer": max(students, key=lambda x: x["score"])["name"],
            "needs_attention": min(students, key=lambda x: x["score"])["name"]
        }
    }

# AI analysis for a student
@app.get("/api/ai/analyze/{student_id}")
async def analyze_student(student_id: int):
    student = next((s for s in students if s["id"] == student_id), None)
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Simulate AI prediction
    risk_score = np.random.uniform(0.1, 0.9)
    
    return {
        "student_info": student,
        "dropout_risk_analysis": {
            "risk_score": float(risk_score),
            "confidence": 0.85,
            "risk_level": "High" if risk_score > 0.7 else "Medium" if risk_score > 0.4 else "Low",
            "recommendations": [
                "Schedule parent meeting",
                "Assign peer mentor",
                "Extra tutoring sessions"
            ]
        },
        "performance_analysis": {
            "current_average": student["score"],
            "trend": "improving" if student["score"] > 80 else "stable" if student["score"] > 70 else "declining",
            "predicted_next_term": student["score"] + np.random.uniform(-5, 10),
            "recommendations": [
                "Focus on Mathematics practice",
                "Join study group",
                "Watch tutorial videos"
            ]
        }
    }

# Batch predictions
@app.post("/api/ai/predict-batch")
async def predict_batch():
    predictions = []
    for student in students:
        risk_score = np.random.uniform(0.1, 0.9)
        predictions.append({
            "student_id": student["id"],
            "student_name": student["name"],
            "risk_score": risk_score,
            "risk_level": "High" if risk_score > 0.7 else "Medium" if risk_score > 0.4 else "Low"
        })
    
    return {
        "predictions": predictions,
        "summary": {
            "high_risk": len([p for p in predictions if p["risk_level"] == "High"]),
            "medium_risk": len([p for p in predictions if p["risk_level"] == "Medium"]),
            "low_risk": len([p for p in predictions if p["risk_level"] == "Low"])
        }
    }

# WebSocket for real-time updates
connected_clients = []

@app.websocket("/ws/ai/updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            # Send updates every 5 seconds
            await asyncio.sleep(5)
            
            data = {
                "timestamp": datetime.now().isoformat(),
                "active_sessions": len(connected_clients),
                "predictions_processed": np.random.randint(100, 500),
                "alerts": np.random.randint(0, 3),
                "system_health": "optimal"
            }
            
            await websocket.send_json(data)
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)

# Class analytics
@app.get("/api/analytics/class/{class_name}")
async def class_analytics(class_name: str):
    class_students = [s for s in students if s["class"] == class_name]
    
    if not class_students:
        raise HTTPException(status_code=404, detail="Class not found")
    
    return {
        "class": class_name,
        "student_count": len(class_students),
        "average_score": round(np.mean([s["score"] for s in class_students]), 1),
        "average_attendance": round(np.mean([s["attendance"] for s in class_students]), 1),
        "recommendations": [
            "Organize group study sessions",
            "Schedule extra classes",
            "Implement peer tutoring"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
