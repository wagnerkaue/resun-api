from typing import cast, Any, Optional, List

from fastapi import FastAPI, HTTPException, Request, Depends, Query
from contextlib import asynccontextmanager
from google.cloud import firestore
from google.oauth2 import service_account
import os
from api.models import Meal

KEY_FILE_PATH = "serviceAccountKey.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    Initializes the Firestore client on startup.
    """
    # Startup
    try:
        # Check for the existence of the service account key file in production environments
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
             print("Using credentials from GOOGLE_APPLICATION_CREDENTIALS env var.")
             app.state.db = firestore.Client()
        elif os.path.exists(KEY_FILE_PATH):
            print(f"Using credentials from file: {KEY_FILE_PATH}")
            credentials = service_account.Credentials.from_service_account_file(KEY_FILE_PATH)
            app.state.db = firestore.Client(credentials=credentials)
        else:
            print("No credentials found. Attempting to use default credentials.")
            app.state.db = firestore.Client()

        print("Firestore client initialized successfully.")
    except Exception as exc:
        print(f"Failed to initialize Firestore client: {exc}")
        raise RuntimeError("Failed to initialize Firestore client") from exc

    try:
        yield  # The application runs here
    finally:
        # Shutdown
        db = getattr(app.state, "db", None)
        if db and hasattr(db, 'close'):
            db.close()
        print("Shutdown complete.")


app = FastAPI(lifespan=lifespan)

def get_db(request: Request) -> firestore.Client:
    """
    Dependency to get the Firestore client from the application state.
    """
    db = getattr(request.app.state, "db", None)
    if not db:
        raise HTTPException(status_code=503, detail="Firestore not available")
    return db


@app.get(path="/meals", summary="Get a list of meals with filters", response_model=List[Meal])
def get_meals(
    db: firestore.Client = Depends(get_db),
    campus: Optional[str] = Query(None, description="Filter by campus (e.g., sao-cristovao)"),
    meal_type: Optional[str] = Query(None, description="Filter by meal type (e.g., lunch, dinner)"),
    supplier: Optional[str] = Query(None, description="Filter by supplier"),
    date: Optional[str] = Query(None, description="Filter by a specific date (YYYY-MM-DD)"),
    start_date: Optional[str] = Query(None, description="Start of date range (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End of date range (YYYY-MM-DD)"),
    limit: int = Query(20, ge=1, le=100, description="Number of meals to return per page"),
    page: int = Query(1, ge=1, description="Page number")
):
    """
    Retrieves a list of meals from Firestore with optional filtering and pagination
    """
    # Start with the base collection reference.
    query: Any = db.collection("meals")

    # Apply equality filters
    if campus:
        query = query.where("campus", "==", campus)
    if meal_type:
        query = query.where("meal_type", "==", meal_type)
    if supplier:
        query = query.where("supplier", "==", supplier)
    if date:
        query = query.where("date", "==", date)

    # Apply date range filters
    if start_date:
        query = query.where("date", ">=", start_date)
    if end_date:
        query = query.where("date", "<=", end_date)

    # Calculate offset for pagination
    offset = (page - 1) * limit

    # Apply ordering for consistent pagination results, then apply limit and offset.
    # Ordering by date is a sensible default.
    paginated_query = query.order_by("date").limit(limit).offset(offset)

    try:
        docs = paginated_query.stream()
        meals = [meal for doc in docs if (meal := Meal.from_firestore(doc)) is not None]
        return meals
    except Exception as e:
        # This often occurs if a required composite index is missing in Firestore.
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while querying the database. This might be due to a missing Firestore index. Details: {e}"
        )


@app.get(path="/meals/{meal_id}", summary="Get meal by id", response_model=Meal)
def get_meal_from_id(meal_id: str, db: firestore.Client = Depends(get_db)):
    """
    Retrieves a single meal by its unique ID.
    The ID is in the format: campus_YYYY-MM-DD_meal_type
    """
    doc = db.collection("meals").document(meal_id).get()
    meal = Meal.from_firestore(doc)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal


@app.get(path="/campuses", summary="Get list of all campuses")
def get_campuses():
    return ["sao-cristovao", "lagarto", "itabaiana", "sertao", "central"]


@app.get(path="/suppliers", summary="Get list of all suppliers")
def get_suppliers():
    return ["ism-restaurantes-ltda", "prs-alimentacao-e-servicos-ltda"]


@app.get("/meal-types", summary="Get list of all meal types")
def get_meal_types():
    return ["lunch", "dinner"]
