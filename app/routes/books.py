from fastapi import APIRouter, HTTPException, Depends
from app.db import books_collection
from app.models import Book, BookUpdate, BookOut
from bson import ObjectId
import traceback
from app.auth import get_current_user


router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=Book)
async def add_book(book: Book, current_user: str = Depends(get_current_user)):
    book_dict = dict(book)
    book_dict["owner"] = current_user
    result = await books_collection.insert_one(book_dict)
    book_dict["_id"] = str(result.inserted_id)
    return book_dict




@router.get("/", response_model=list[BookOut])
async def get_books(current_user: str = Depends(get_current_user)):
    try:
        books_cursor = books_collection.find({"owner": current_user})
        books = []
        async for book in books_cursor:
            print("📘 DEBUG BOOK FROM DB:", book)
            books.append(BookOut(
                id=str(book["_id"]),
                title=book["title"],
                author=book["author"],
                genre=book.get("genre")
            ))
        return books
    except Exception as e:
        print("🔥 ERROR in get_books:", str(e))
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


#@router.get("/",response_model=list[BookOut])
#async def get_books(current_user: str = Depends(get_current_user)):
#    books_cursor = books_collection.find({"owner": current_user}).to_list(100)  # filter by user
#    books = []
#    for book in books_cursor:
#        books.append(BookOut(
#            id=str(book["_id"]),
#            title=book["title"],
#            author=book["author"],
#            description=book.get("description", None)
#        ))
#    return books

@router.get("/{book_id}")
async def get_book(book_id: str):
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book["_id"] = str(book["_id"])
    return book

@router.put("/{book_id}")
async def update_book(book_id: str, book: Book, current_user: str = Depends(get_current_user)):
    existing = await books_collection.find_one({"_id": ObjectId(book_id), "owner": current_user})
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found or not yours")

    await books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": book.dict()}
    )
    book_dict = await books_collection.find_one({"_id": ObjectId(book_id)})
    book_dict["id"] = str(book_dict["_id"])
    return book_dict

# Delete all books of the logged-in user
@router.delete("/", summary="Delete all books of the current user")
async def delete_all_books(current_user: str = Depends(get_current_user)):
    result = await books_collection.delete_many({"owner": current_user})

    if result.deleted_count == 0:
        return {"message": "No books found to delete."}

    return {"message": f"Deleted {result.deleted_count} books."}

# Delete specific book of the logged-in user
@router.delete("/{book_id}")
async def delete_book(book_id: str, current_user: str = Depends(get_current_user)):
    result = await books_collection.delete_one({"_id": ObjectId(book_id), "owner": current_user})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found or not yours")
    return {"message": "Book deleted"}
