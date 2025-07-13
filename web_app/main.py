# web_app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

# Import our existing, tested logic!
# This works because of our installable project setup.
from core_logic.calculations import BuildingProject

# --- API Data Models ---
# Pydantic models define the structure and data types for our API requests.
# This ensures we receive valid data.

class Element(BaseModel):
    element_type: str
    quantity: int
    dimensions: Dict[str, float] # e.g., {"length": 5, "width": 0.4, "height": 0.6}

class CalculationRequest(BaseModel):
    mix_ratio: str
    elements: List[Element] = []
    deductions: List[Element] = []

# --- FastAPI Application ---
app = FastAPI(
    title="Architecture Calculator API",
    description="An API to calculate material quantities for building projects.",
    version="1.0.0"
)

@app.post("/calculate/")
async def calculate_materials(request: CalculationRequest):
    """
    Receives a list of building elements and deductions, calculates the
    net volume, and returns the required material quantities.
    """
    try:
        # 1. Initialize our BuildingProject with the mix ratio from the request
        project = BuildingProject(mix_ratio=request.mix_ratio)

        # 2. Add all the elements from the request to the project
        for elem in request.elements:
            project.add_element(
                element_type=elem.element_type,
                quantity=elem.quantity,
                dimensions=elem.dimensions
            )
        
        # 3. Add all the deductions from the request to the project
        for ded in request.deductions:
            project.add_deduction(
                deduction_type=ded.element_type,
                quantity=ded.quantity,
                dimensions=ded.dimensions
            )
        
        # 4. Perform the final calculation
        net_volume = project.calculate_total_net_volume()
        materials = project.calculate_total_materials()
        
        # 5. Return a successful response with the results
        return {
            "status": "success",
            "net_volume_cubic_meters": net_volume,
            "required_materials": materials
        }
    except ValueError as e:
        # Handle potential errors, e.g., invalid mix ratio
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {"message": "Welcome to the Arch Calculator API. Go to /docs for the interactive API documentation."}