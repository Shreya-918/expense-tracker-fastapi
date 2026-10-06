from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..models.expense_model import Expense
from ..schemas.expense import ExpenseRequest, ExpenseResponse,ExpenseUpdate
from ..schemas.api import ApiResponse
from typing import Optional
from datetime import datetime
from sqlalchemy import func
from ..core.dependencies import get_current_user
from ..models.user_model import User

#very very importanr craetes apirouter then use in a main py file and include this router to app
expense_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)
#create expense
@expense_router.post("/create_expense",response_model=ApiResponse)
def create_expense(request: ExpenseRequest,db: Session = Depends(get_db), current_user: User = Depends(get_current_user),):

    try:
        new_expense = Expense(
            title=request.title,
            description=request.description,
            amount=request.amount,
            user_id=current_user.id
        )

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return ApiResponse(
            status="success",
            message="Expense created successfully",
            success=True,
            data={
                "expense": ExpenseResponse.model_validate(new_expense)
            }
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to create expense"
        )
#access all expense
@expense_router.get("/all", response_model=ApiResponse)
def access_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id
    ).all()

    return ApiResponse(
        status="success",
        message="Expenses fetched successfully",
        success=True,
        data={
            "expenses": [
                ExpenseResponse.model_validate(expense)
                for expense in expenses
            ]
        }
    )

#FILTER expenses
@expense_router.get("/filter", response_model=ApiResponse)
def filter_expenses(
    min_amount: float | None = None,
    max_amount: float | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Expense).filter(
        Expense.user_id == current_user.id
    )

    if min_amount is not None:
        query = query.filter(
            Expense.amount >= min_amount
        )

    if max_amount is not None:
        query = query.filter(
            Expense.amount <= max_amount
        )

    expenses = query.all()

    expense_data = [
        ExpenseResponse.model_validate(expense)
        for expense in expenses
    ]

    return ApiResponse(
        status="success",
        message="Expenses filtered successfully",
        success=True,
        data={
            "expenses": expense_data
        }
    )

#summary of your expenses
@expense_router.get( "/summary", response_model=ApiResponse)
def expense_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    total_expense =db.query(
        func.sum(Expense.amount)
        ).filter(Expense.user_id == current_user.id
        ).scalar()

    average_expense = db.query(
        func.avg(Expense.amount)
        ).filter(Expense.user_id == current_user.id
    ).scalar()

    maximum_expense = db.query(
        func.max(Expense.amount)
        ).filter(Expense.user_id == current_user.id
    ).scalar()

    minimum_expense = db.query(
        func.min(Expense.amount)
        ).filter(Expense.user_id == current_user.id
    ).scalar()

    expense_count = db.query(
        func.count(Expense.id)
        ).filter(Expense.user_id == current_user.id
    ).scalar()

    return ApiResponse(
        status="success",
        message="Expense summary fetched successfully",
        success=True,
        data={
            "total_expense": total_expense or 0,
            "average_expense": average_expense or 0,
            "maximum_expense": maximum_expense or 0,
            "minimum_expense": minimum_expense or 0,
            "expense_count": expense_count or 0
        }
    )
#access particular expense
@expense_router.get("/{expense_id}",response_model=ApiResponse
)
def acess_expense(expense_id: int,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    expenses = db.query(Expense).filter(
                Expense.user_id == current_user.id
            ).all()

    if not expenses:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return ApiResponse(
        status="success",
        message="Expense fetched successfully",
        success=True,
        data={
            "expense": ExpenseResponse.model_validate(expenses)
        }
    )
#monthly analytics
@expense_router.get("/analytics/monthly",response_model=ApiResponse)
def monthly_expenses( year: int,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):

        results = db.query(
        func.strftime("%m", Expense.created_at).label("month"),
        func.sum(Expense.amount).label("total")
    ).filter(
        Expense.user_id == current_user.id,
        func.strftime("%Y", Expense.created_at) == str(year)
    ).group_by(
        func.strftime("%m", Expense.created_at)
    ).order_by(
        func.strftime("%m", Expense.created_at)
    ).all()
        monthly_data = {
            f"{year}-{month}": total
            for month, total in results
        }

        return ApiResponse(
            status="success",
            message="Monthly expenses fetched successfully",
            success=True,
            data={
                "year": year,
                "monthly_expenses": monthly_data
            }
        )

#full update expense
@expense_router.put("/{expense_id}", response_model=ApiResponse)
def update_expense(expense_id: int,
                   request: ExpenseRequest,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):

    expense = db.query(Expense).filter(
    Expense.id == expense_id,
    Expense.user_id == current_user.id
).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense.title = request.title
    expense.description = request.description
    expense.amount = request.amount

    db.commit()
    db.refresh(expense)

    return ApiResponse(
        status="success",
        message="Expense updated successfully",
        success=True,
        data={
            "expense": ExpenseResponse.model_validate(expense)
        }
    )

#particular update 
@expense_router.patch("/{expense_id}",response_model=ApiResponse)
def update_expense( expense_id: int, 
                   request: ExpenseUpdate, 
                   db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):

    expense = db.query(Expense).filter(
    Expense.id == expense_id,
    Expense.user_id == current_user.id
).first()
    

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    if request.title is not None:
        expense.title = request.title

    if request.description is not None:
        expense.description = request.description

    if request.amount is not None:
        expense.amount = request.amount

    db.commit()
    db.refresh(expense)

    return ApiResponse(
        status="success",
        message="Expense updated successfully",
        success=True,
        data={
            "expense": ExpenseResponse.model_validate(expense)
        }
    )

#delete expense
@expense_router.delete("/{expense_id}", response_model=ApiResponse)
def delete_expense(expense_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return ApiResponse(
        status="success",
        message="Expense deleted successfully",
        success=True,
        data=None
    )
