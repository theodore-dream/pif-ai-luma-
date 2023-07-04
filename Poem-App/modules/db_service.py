import psycopg2
from psycopg2 import Error
from modules.logger import setup_logger

logger = setup_logger("db_service")

def write_to_database(session_id, session_state, entropy):
    try:
        connection = psycopg2.connect(
            dbname="game",
            host="localhost",
            user="pi",
            password="raspberry",
            port="5432",
            connect_timeout=3,
        )
        cursor = connection.cursor()
        query = f"INSERT INTO poem_game (session_id, session_state, entropy) VALUES (%s, %s, %s)"
        logger.debug(f"Executing insert: {query} on session: {session_id}")
        cursor.execute(query, (session_id, session_state, entropy))
        connection.commit()
        logger.debug("Query executed successfully")
        cursor.close()
        connection.close()
    except (Exception, Error) as error:
        logger.error("Error while updating column in PostgreSQL", error)

def save_game(session_id, level, entropy):
    try:
        connection = psycopg2.connect(
            dbname="game",
            host="localhost",
            user="pi",
            password="raspberry",
            port="5432",
            connect_timeout=3,
        )
        cursor = connection.cursor()
        query = "UPDATE poem_game SET level = %s, entropy = %s WHERE session_id = %s"
        logger.debug(f"Executing update: {query} on session: {session_id}")
        cursor.execute(query, (level, entropy, session_id))
        connection.commit()
        logger.debug("Query executed successfully")
        cursor.close()
        connection.close()
    except (Exception, Error) as error:
        logger.error("Error while updating column in PostgreSQL", error)

def read_from_database(session_id):
    try:
        connection = psycopg2.connect(
            dbname="game",
            host="localhost",
            user="pi",
            password="raspberry",
            port="5432",
            connect_timeout=3,
        )
        cursor = connection.cursor()
        query = f"SELECT persona, session_state, gametext, entropy, session_id FROM poem_game WHERE session_id = %s ORDER BY tstz DESC LIMIT 1"
        logger.debug(f"Executing query: {query} on session: {session_id}")
        cursor.execute(query, (session_id,))
        result = cursor.fetchone()
        logger.debug(f"Query executed successfully, result: {result}")
        cursor.close()
        connection.close()
        if result is None:
            return (None if result is None else result[0]), \
                   (None if result is None else result[1]), \
                   (None if result is None else result[2]), \
                   (None if result is None else result[3]), \
                   (None if result is None else result[4])
        else:
            return result[0], result[1], result[2], result[3], result[4]

    except (Exception, Error) as error:
        logger.error("Error while reading column from PostgreSQL", error)
        return None, None, None, None, None



# Example usage:
# write_to_database(session_id, 'prompt', 'your_prompt_here')
# write_to_database(session_id, 'player-optiona', 'option_a_here')
# write_to_database(session_id, 'player-optionb', 'option_b_here')
# write_to_database(session_id, 'entropy', 42.0)
#
# prompt = read_from_database(session_id, 'prompt')
# player_optiona = read_from_database(session_id, 'player-optiona')
# player_optionb = read_from_database(session_id, 'player-optionb')
# entropy = read_from_database(session_id, 'entropy')