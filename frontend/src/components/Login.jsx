import { useState } from "react"
import {  useNavigate } from 'react-router-dom'


export let access_token = "";
export let username = "";
export const url = "http://127.0.0.1:5000"

export default function Login(){
    const [formData, setFormData] = useState({
        username: "",
        password: ""
    })

    const [message, setMessage] = useState("")
    const history = useNavigate()

    const handleChange =(e)=>{
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        })
    }

    const formDataToSend = new FormData()
    formDataToSend.append('username', formData.username)
    formDataToSend.append('password', formData.password)

    const handleSubmit = (e)=>{
        e.preventDefault();
        console.log(formData)
    
        fetch(`${url}/login`, {
            method: 'POST',
            body: formDataToSend
        }).then((response)=>response.json())
          .then((json)=>{
            console.log(json);
            if (json.success){
                username = json.username;
                access_token = json.access_token;
                history(`/dashboard`, 
                        {state: {username: formData.username, 
                            access_token: access_token}}
                );
            } else{
               if (formData.username == "") {
                setMessage("Please Enter Some Data")

               }else{
                   setMessage(json.message);

               }
            }
          });
    }
    



    return (
        <div>
            <form onSubmit={handleSubmit}>
              <label htmlFor="username">username</label>
              <input type="text" name="username" value={formData.username} onChange={handleChange}/>

              <label htmlFor="password">password</label>
              <input type="password" name="password" value={formData.password}  onChange={handleChange}/>

              <button type="submit">Submit</button>


            </form>
            <p>{message}</p>

        </div>
    )
}