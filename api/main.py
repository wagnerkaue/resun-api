import json
import os
from contextlib import asynccontextmanager
from typing import Any, Optional, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Depends, Query
from google.cloud import firestore
from google.oauth2 import service_account

from .models import Meal

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown events.
    Initializes the Firestore client on startup.
    """
    # Startup
    try:
        # Load service account details from environment variable
        service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_KEY"])

        # Create credentials using google.oauth2.service_account
        cred = service_account.Credentials.from_service_account_info(service_account_info)

        # Initialize the Firestore client with the correct credentials
        app.state.db = firestore.Client(credentials=cred)
        print("Firestore client initialized successfully.")
    except KeyError:
        print("ERROR: 'GOOGLE_SERVICE_ACCOUNT_KEY' environment variable not found.")
        raise RuntimeError("Configuration error: Missing Google service account key.")
    except json.JSONDecodeError:
        print("ERROR: 'GOOGLE_SERVICE_ACCOUNT_KEY' is not valid JSON.")
        raise RuntimeError("Configuration error: Invalid JSON in service account key.")
    except Exception as exc:
        print(f"Failed to initialize Firestore client: {exc}")
        raise RuntimeError("Failed to initialize Firestore client") from exc

    try:
        yield  # The application runs here
    finally:
        # Shutdown
        # The google-cloud-firestore client manages its connections automatically.
        # No explicit db.close() is needed.
        print("Shutdown complete.")


app = FastAPI(lifespan=lifespan)


def get_db(request: Request) -> firestore.Client:
    """
    Dependency to get the Firestore client from the application state.
    """
    db = getattr(request.app.state, "db", None)
    if not db:
        # This will be triggered if the lifespan startup fails.
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
    Retrieves a list of meals from Firestore with optional filtering and pagination.
    """
    try:
        # Start with the base collection reference.
        query: Any = db.collection("meals")

        # Apply equality filters
        if campus:
            query = query.where(field_path="campus", op_string="==", value=campus)
        if meal_type:
            query = query.where(field_path="meal_type", op_string="==", value=meal_type)
        if supplier:
            query = query.where(field_path="supplier", op_string="==", value=supplier)
        if date:
            query = query.where(field_path="date", op_string="==", value=date)

        # Apply date range filters
        if start_date:
            query = query.where(field_path="date", op_string=">=", value=start_date)
        if end_date:
            query = query.where(field_path="date", op_string="<=", value=end_date)

        # Calculate offset for pagination
        offset = (page - 1) * limit

        # Order by date for consistent pagination results, then apply limit and offset.
        paginated_query = query.order_by("date").limit(limit).offset(offset)

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
    doc_ref = db.collection("meals").document(meal_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Meal not found")

    return Meal.from_firestore(doc)


@app.get(path="/campuses", summary="Get list of all campuses")
def get_campuses():
    return ["sao-cristovao", "lagarto", "itabaiana", "sertao", "central"]


@app.get(path="/suppliers", summary="Get list of all suppliers")
def get_suppliers():
    return ["ism-restaurantes-ltda", "prs-alimentacao-e-servicos-ltda"]


@app.get("/meal-types", summary="Get list of all meal types")
def get_meal_types():
    return ["lunch", "dinner"]
