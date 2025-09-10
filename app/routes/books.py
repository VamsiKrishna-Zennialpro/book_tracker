from fastapi import APIRouter, HTTPException, Depends
from app.db import books_collection
from app.models import Book, BookUpdate, BookOut
from bson import ObjectId
import traceback
from app.auth import get_current_user

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=Book)
async def add_book(book: Book, current_user: str = Depends(get_current_user)):
    logger.info(f"Adding New books for {current_user}")
    book_dict = dict(book)
    book_dict["owner"] = current_user
    result = await books_collection.insert_one(book_dict)
    book_dict["_id"] = str(result.inserted_id)
    return book_dict




@router.get("/", response_model=list[BookOut])
async def get_books(current_user: str = Depends(get_current_user)):
    logger.info(f"Fetching books for {current_user}")
    try:
        books_cursor = books_collection.find({"owner": current_user})
        books = []
        async for book in books_cursor:
            print("📘 DEBUG BOOK FROM DB:", book)
            books.append(BookOut(
                id=str(book["_id"]),
                title=book["title"],
                author=book["author"],
                genre=book["genre"],
                status=book["status"]
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
    logger.info(f"User {current_user} attempting to update book {book_id}")

    # Validate ObjectId
    if not ObjectId.is_valid(book_id):
        logger.warning(f"Invalid book_id provided: {book_id}")
        raise HTTPException(status_code=400, detail="Invalid book ID")

    # Ensure the book belongs to the current user
    existing = await books_collection.find_one({"_id": ObjectId(book_id), "owner": current_user})
    if not existing:
        logger.warning(f"Book {book_id} not found or not owned by {current_user}")
        raise HTTPException(status_code=404, detail="Book not found or not yours")

    # Perform update (only fields provided in request body)
    update_data = book.dict(exclude_unset=True)
    await books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_data}
    )

    # Fetch updated book
    updated_book = await books_collection.find_one({"_id": ObjectId(book_id)})

    # Convert ObjectId -> str and clean response
    updated_book["id"] = str(updated_book["_id"])
    del updated_book["_id"]

    logger.info(f"Book {book_id} updated successfully for {current_user}")
    return updated_book

# Delete all books of the logged-in user
#@router.delete("/", summary="Delete all books of the current user")
#async def delete_all_books(
#    current_user: str = Depends(get_current_user),
#    confirm: bool = Query(False, description="Set to true to confirm deletion")
#):
#    if not confirm:
#        raise HTTPException(
#            status_code=400,
#            detail="You must confirm deletion by setting ?confirm=true"
#        )
#
#    result = await books_collection.delete_many({"owner": current_user})
#
#    if result.deleted_count == 0:
#        return {"message": "No books found to delete."}
#
#    return {"message": f"Deleted {result.deleted_count} books."}

@router.get("/", response_model=list[BookOut])
async def get_books(current_user: str = Depends(get_current_user)):
    books = await books_collection.find({"owner": current_user}).to_list(100)
    for book in books:
        book["_id"] = str(book["_id"])
    return books

# Delete specific book of the logged-in user
@router.delete("/{book_id}")
async def delete_book(book_id: str, current_user: str = Depends(get_current_user)):
    result = await books_collection.delete_one({"_id": ObjectId(book_id), "owner": current_user})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found or not yours")
    return {"message": "Book deleted"}


