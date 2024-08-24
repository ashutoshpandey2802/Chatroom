from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import numpy as np
import pandas as pd
from cohere_client import get_cohere_client
from search_index import create_search_index
from llm_model import ask_llm
from dateutil import parser

API_KEY = 'SkWcFdTpyIwsVAAoCIgW9b6vdnssYMgViMpI7AJg'

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class QuestionRequest(BaseModel):
    question: str

def fetch_data_from_db(db_path='employee_database.db'):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT EmployeeID, FirstName, LastName, Email, PhoneNumber, HireDate, JobTitle, Salary, Department FROM Employees')
        data = c.fetchall()
        conn.close()
        
        combined_data = [
            (
                f"EmployeeID: {row[0]}, FirstName: {row[1]}, LastName: {row[2]}, Email: {row[3]}, "
                f"PhoneNumber: {row[4]}, HireDate: {row[5]}, JobTitle: {row[6]}, Salary: {row[7]}, "
                f"Department: {row[8]}"
            ) for row in data
        ]
        return combined_data, data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return [], []

def fetch_data_from_csv(csv_path='info.csv'):
    try:
        df = pd.read_csv(csv_path)
        return df['text'].tolist()
    except Exception as e:
        print(f"CSV read error: {e}")
        return []

def parse_date(date_str):
    try:
        date = parser.parse(date_str, fuzzy=False)
        if date.year == 1900:  # Adjusting for missing year
            date = date.replace(year=pd.Timestamp.today().year)
        return date
    except ValueError:
        return None

# Preload data and create the search index when the app starts
db_texts, db_data = fetch_data_from_db()
csv_texts = fetch_data_from_csv()
texts = db_texts + csv_texts
texts = np.array([t.strip(' \n') for t in texts if t])

co = get_cohere_client(API_KEY)
response = co.embed(texts=texts.tolist()).embeddings
embeds = np.array(response)
search_index = create_search_index(embeds)

def answer_question(question, db_data):
    question_lower = question.lower()

    if "hired before" in question_lower:
        date_str = question.split("before")[1].strip()
        date = parse_date(date_str)
        if date is None:
            return "Invalid date format. Please use a format like '22 January 2023' or '22-01-2023'."

        result = []
        for row in db_data:
            hire_date = pd.to_datetime(row[5], errors='coerce')
            if hire_date and hire_date < date:
                result.append(f"{row[1]} {row[2]} - Hire Date: {row[5]}")

        return "\n".join(result) if result else "No employees hired before the specified date."

    if "hired after" in question_lower:
        date_str = question.split("after")[1].strip()
        date = parse_date(date_str)
        if date is None:
            return "Invalid date format. Please use a format like '22 January 2023' or '22-01-2023'."

        result = []
        for row in db_data:
            hire_date = pd.to_datetime(row[5], errors='coerce')
            if hire_date and hire_date > date:
                result.append(f"{row[1]} {row[2]} - Hire Date: {row[5]}")

        return "\n".join(result) if result else "No employees hired after the specified date."

    if "highest salary" in question_lower or "greatest salary" in question_lower:
        df = pd.DataFrame(db_data, columns=['EmployeeID', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'HireDate', 'JobTitle', 'Salary', 'Department'])
        highest_salary = df['Salary'].max()
        result = df[df['Salary'] == highest_salary]
        if not result.empty:
            return f"Employee with the highest salary is {result.iloc[0]['FirstName']} {result.iloc[0]['LastName']} with a salary of {highest_salary}."

    if "lowest salary" in question_lower:
        df = pd.DataFrame(db_data, columns=['EmployeeID', 'FirstName', 'LastName', 'Email', 'PhoneNumber', 'HireDate', 'JobTitle', 'Salary', 'Department'])
        lowest_salary = df['Salary'].min()
        result = df[df['Salary'] == lowest_salary]
        if not result.empty:
            return f"Employee with the lowest salary is {result.iloc[0]['FirstName']} {result.iloc[0]['LastName']} with a salary of {lowest_salary}."
    
    try:
        results = ask_llm(co, search_index, texts, question)
        response = results[0].text
        return {"answer": response}
    except Exception as e:
        return {"error": f"An error occurred while querying the model: {e}"}

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    answer = answer_question(request.question, db_data)
    if not answer:
        raise HTTPException(status_code=404, detail="No answer found.")
    return {"question": request.question, "answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
