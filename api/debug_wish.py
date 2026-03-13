from db.database import SessionLocal
import model as models
import schemas as schemas
from sqlalchemy.orm import Session

def debug_wish_creation():
    db: Session = SessionLocal()
    try:
        # Simulate the request data
        wish_data = schemas.WishCreate(
            categories="Test Category",
            wishes="Test Wish",
            status="Planning"
        )
        
        # Simulate getting the user
        user = db.query(models.User).filter(models.User.id == 1).first()
        if not user:
            print("❌ User 1 not found")
            return

        print(f"User found: {user.emailID}")
        
        # Create the wish
        print("Attempting to create wish model...")
        # Use model_dump() for Pydantic v2 if dict() fails or to be modern
        # But routers use .dict()
        data = wish_data.dict()
        print(f"Data for model: {data}")
        
        new_wish = models.Wish(**data, user_id=user.id)
        db.add(new_wish)
        print("Model added to session. Committing...")
        db.commit()
        db.refresh(new_wish)
        print(f"✅ Created wish: {new_wish.wish_id}")
        
    except Exception as e:
        print(f"❌ Error during wish creation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_wish_creation()
