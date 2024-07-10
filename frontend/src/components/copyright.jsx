const Copyright = ()=>{
    const date = new Date()
    return (
        <div className="copyright">
            <p>Copyright &copy; {date.getFullYear()}</p>
            <p>Developer <span>Adnan T.</span></p>
        </div>
    )
}

export default Copyright