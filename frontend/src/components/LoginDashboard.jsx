import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { url } from "./Login";


const tagLine = ["Record Your finance", "Take a close look at your Expenses", "Have a financial freedom"]

function Header({name}){
    const randomTag =Math.floor(Math.random() * tagLine.length)
    // console.log(randomTag)
    return (
        <div>
            <h2>{name}</h2>
            <p>{tagLine[randomTag]}</p>
        </div>
    )
}



function Summary(){
    return (
        <div className="summary">
            <div className="total">
                <h3>Total spend</h3>
                <p>$120</p>
            </div>
            <div className="top-most-expense">
                <h3>Most recent spend</h3>
                <p>$30 <span>Food</span></p>
            </div>
            <div>
                <h3>Total Income</h3>
                <p>$500</p>
            </div>
        </div>
    )
}

function AddChoice(){
    return (
        <div className="add-choice">
            <button>Add Expense</button>
            <button>Add Category</button>
            <button>View Categories</button>
            <button>View Status</button>
        </div>
    )
}

function ListExpenses({expenses}){
    return (
        <div className="expenses">
            <h2>Expenses</h2>
            <div>
                <ul>
                    {expenses.map((expense)=><li key={expense.id}>{expense.description} {expense.id}</li>)}
                </ul>
            </div>
        </div>
    )

}

export default function SuccessLogin() {
    const [expenses, setExpenses] = useState(["name", "Twp", "TE"])
    const [name , setName] = useState("")
    const location = useLocation();
    const {username, access_token} = location.state || {};

    useEffect(()=>{
        console.log(access_token)
        console.log(username)
        fetch(`${url}/${username}/dashboard`, {
            method: "GET",
            headers: {
                'Authorization': `Bearer ${access_token}`,
            }
        }).then((response)=>response.json()).then((data)=>{
            if (data.expenses == undefined){
                expenses = ['name', 1, 4]
            }else{
                setExpenses(data.expenses)
                setName(username)
            }
        })

    }, [])


  return (
    <div className="dashboard">
        <Header name={name}/>
        <Summary />
        <AddChoice />
        <ListExpenses expenses={expenses}/>
    </div>
  );
}
