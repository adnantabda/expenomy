function Usage() {
  return (
    <div>
      <h2>Usage</h2>
      <div className="usage">
        <div>
          <div>Login or Sign up</div>
          <div>
            <p>when You login or signup you will see your personal dashboard</p>
          </div>
        </div>

        <div>
          <div>Add Expenses</div>
          <div>
            <p>
              You can add your expenses by clicking on the Add add Expenses on
              you Dashboard
            </p>
          </div>
        </div>

        <div>
          <div>categorize Expenses</div>
          <div>
            <p>categorize related Expenses together for better productivity</p>
          </div>
        </div>

        <div>
          <div>See generated chart</div>
          <div>
            <p>
              from generated charts see Expenses and which one has the highest
              expense
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function WhatCanYouDoSection() {
  return (
    <div>
      <h2>What You Can Do</h2>

      <div className="what-you-can-do">
        <div>
          <h3>Log your Expenses</h3>
          <p>add expenses with amount, date, description and more</p>
        </div>
        <div>
          <h3>Categorize your Expenses</h3>
          <p>Add and manage expense categories</p>
        </div>
        <div>
          <h3>Generate Insightful reports</h3>
          <p>Generate and view detailed expenses reports with charts</p>
        </div>
        <div>
          <h3>Update, Delete, and Create Expenses</h3>
          <p>
            designed for ease use for creating, updating, deleting and reading
            expenses
          </p>
        </div>
      </div>
    </div>
  );
}

function HeroSection() {
  return (
    <div>
      <div>
        <h1>Manage Your Expenses, Simplify Your Life</h1>
        <p>
          Keep track of your expenses effortlessly with our intuitive and secure
          Expense Tracker : Expenomy
        </p>
        <a href="login">
        <button>Login</button>
        </a>
      </div>
    </div>
  );
}

export function Home() {
  return (
    <div>
      <div>
        <img src="#" alt="Logo of expenomy" />
      </div>
      <nav>
        <ul>
          <li>About</li>
          <li>Login</li>
          <li>Sign in</li>
        </ul>
      </nav>
      <HeroSection />
      <WhatCanYouDoSection />
      <Usage />
    </div>
  );
}
