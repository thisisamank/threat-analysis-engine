import fastapi as FastAPI
import uvicorn
from engine import Engine
from mapping import MitreCloudTrailMapping
from fastapi.middleware.cors import CORSMiddleware
from cloudtrail_client import CloudtrailClient  # Make sure to import your CloudtrailClient class

app = FastAPI.FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

engine = Engine()
mapping = MitreCloudTrailMapping.init()

# Initialize CloudtrailClient
cloudtrail_client = CloudtrailClient(cloud_id="your_cloud_id", elastic_password="your_password")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search/{attack_id}")
def search(attack_id: str):
    return engine.search(attack_id)

@app.get("/total_attacks")
def total_attacks():
    return {"total_attacks": len(mapping.get_all_attacks())}

@app.get("/events")
def fetch_all_events():
    try:
        events = cloudtrail_client.fetch_all_events(index="cloudtrail-*")
        return {"events": events}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)