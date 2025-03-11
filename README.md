Install the required dependencies: pip install -r requirements.txt  
Set up environment variables: Create a .env file in the backend folder and add the following: 
DATABASE_URL=postgresql://username:password@localhost:5432/photoshare SECRET_KEY=your_jwt_secret_key ALGORITHM=HS256 ACCESS_TOKEN_EXPIRE_MINUTES=30 
Run docker yml file: docker-compose up -d 
Database Setup: Set up the PostgreSQL database: alembic upgrade head  
Run the application: Start the backend server: uvicorn Project.src.main:app --reload 
The backend should be accessible at http://localhost:8000.
