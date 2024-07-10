import './LoginDashboard.css'

function TodayCal() {
  const hashDay = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
  };

  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth();
  const date = today.getDate();

  return (
    <div className="date">
      <p>
        <span>{year}</span>
        <span>{month}</span>
        <span>{date}</span>
      </p>
      <p className='day'>{hashDay[today.getDay()]}</p>
    </div>
  );
}
function Name({name}){
  return (
    <div className='name'>
      <h3>{name}</h3>
    </div>
  )
}

function Header(){
  return (
    <div className='header'>
      <TodayCal></TodayCal>
      <Name name={"Adnan Tahir"}></Name>
    </div>
  )
}


function Nav(){
  return (
    <div className='nav-b'>
      <div>Expenses</div>
      <div>Budget</div>
      <div>Income</div>
      <div>Stats</div>
    </div>
  )
}

function CenterDash(){
  const Li = []
  return (
    <div>
      <ul>
        {Li.map((l)=><li className='list-item'>{l}</li>)}
      </ul>
      
    </div>
  )
}

function LeftDash(){
  return (
    <div>
   </div>
  )
}

function RightDash(){
  return (
    <div>
    </div>
  )
}



function Dashboard(){
  return (
    <div className='sub-dashboard'>
      <LeftDash></LeftDash>
      <CenterDash></CenterDash>
      <RightDash></RightDash>
    </div>
  )
}

export default function SuccessLogin() {
  return (
    <div className='dashboard'>
      <Header></Header>
      <Nav></Nav>
      <Dashboard></Dashboard>
    </div>
  );
}
