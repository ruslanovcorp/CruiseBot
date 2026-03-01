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