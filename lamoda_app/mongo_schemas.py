lamoda_item_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "brand", "price", "category"],
        "properties": {
            "title": {
                "bsonType": "string",
            },
            "brand": {
                "bsonType": "string",
            },
            "price": {
                "bsonType": "number",
            },
            "category": {
                "bsonType": "string",
            }
        }
    }
}
