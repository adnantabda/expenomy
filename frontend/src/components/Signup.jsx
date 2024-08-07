import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./autho.css"
import Copyright from "./copyright"

export let access_token = "";
export let username = "";
export const url = "http://127.0.0.1:5000";

export function Logo({ width, height }) {
  return (
    <img
      src="/Logo.png"
      alt="Logo of Expenenomy"
      width={width}
      height={height}
    />
  );
}

export default function SignUp() {
  const [formData, setFormData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const history = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const formDataToSend = new FormData();
  formDataToSend.append("username", formData.username);
  formDataToSend.append("password", formData.password);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);

    fetch(`${url}/login`, {
      method: "POST",
      body: formDataToSend,
    })
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        if (json.success) {
          username = json.username;
          access_token = json.access_token;
          history(`/dashboard`, {
            state: { username: formData.username, access_token: access_token },
          });
        } else {
          if (formData.username == "") {
            setMessage("Please Enter Some Data");
          } else {
            setMessage(json.message);
          }
        }
      });
  };

  return (
    <div className="form-container">
      <div className="login-header">
        <Logo width={"100px"} height={"100px"} />
        <h2>Sign-up</h2>
      </div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">username</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
        />
        <label htmlFor="email">Email</label>
        <input
          type="text"
          name="email"
          value={formData.email}
          onChange={handleChange}
        />
        <label htmlFor="first_name">First Name</label>
        <input
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
        />
        <label htmlFor="last_name">Last Name</label>
        <input
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
        />

        <label htmlFor="password">password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
        />

        <button type="submit">Submit</button>
        <div className="error-message">
        <p >{message}</p>

        </div>
      </form>
      <Copyright />
    </div>
  );
}
