import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App.jsx'
import './index.css'
import SuccessLogin from './components/LoginDashboard.jsx'
import Login from './components/Login.jsx'
import SignUp from './components/Signup.jsx'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />
  },
  {
    path: 'login',
    element: <Login />
  }, 
  {
    path: `dashboard`,
    element: <SuccessLogin />
  },
  {
    path: 'signup',
    element: <SignUp />
  }
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
)


