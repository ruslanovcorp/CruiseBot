from sqlalchemy import text

def find_faq_answer(message: str, db, company_id: int):
    result = db.execute(text("""
        SELECT * FROM faqs
        WHERE company_id = :company_id
        AND to_tsvector('russian', question)
        @@ plainto_tsquery('russian', :query)
        LIMIT 1
    """), {"query": message, "company_id": company_id})

    return result.fetchone()

def smart_search(db, company_id: int, message: str):
    query = text("""
        SELECT id, question, answer,
               similarity(question, :message) AS score
        FROM faqs
        WHERE company_id = :company_id
        ORDER BY score DESC
        LIMIT 1
    """)

    result = db.execute(query, {
        "message": message,
        "company_id": company_id
    }).fetchone()

    if result and result.score > 0.25:
        return result.answer

    return None