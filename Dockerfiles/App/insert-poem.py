import os
import openai
import psycopg2
from psycopg2 import Error
from flask import Flask, request, jsonify

# Load OpenAI API key from the environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

def test_db_connection():
    conn = None
    try:
        conn = psycopg2.connect("dbname=poems user=postgres host=db port=5432 password=raspberry")
        print("Database connection successful!")
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
    finally:
        if conn:
            conn.close()

# Initialize the Flask app
app = Flask(__name__)

# sets up the api endpoint for the front end to call
@app.route("/api/submit-text", methods=["POST"])
def generate_poem():
    if not request.is_json:
        return "Invalid request, data must be in JSON format.", 400

    input_text = request.json.get("input_text")
  #  if not input_text:
  #      return "Missing input_text field", 400

    # Call the OpenAI API to generate a poem based on the user input
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Write a short poem based on the following text: {input_text}",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Save the poem to the database
    try:
        connection = psycopg2.connect(
            dbname="poems",
            host="db",
            user="postgres",
            password="raspberry",
            port="5432",
            connect_timeout=3,
        )
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO poetry (poem_contents) VALUES (%s)", (response.choices[0].text,)
        )
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, Error) as error:
        print("Error while saving poem to PostgreSQL", error)

    # Return the generated poem in the HTTP response
    return jsonify({"poem": response.choices[0].text})


print("Testing the database connection...")
test_db_connection()

if __name__ == "__main__":
    print("Running the app...")
    app.run(host="app", port=5000, debug=True)