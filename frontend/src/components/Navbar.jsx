import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function Navbar() {
  const [solutions, setSolutions] = useState([]);

  useEffect(() => {
    // Fetch solutions data from Flask backend
    fetch('http://localhost:5000/api/v1/solutions')
      .then((response) => response.json())
      .then((data) => setSolutions(data.solutions))
      .catch((error) => console.error('Error fetching solutions:', error));
  }, []);

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <a className="navbar-brand" href="/">Home</a>
        <div className="collapse navbar-collapse" id="navbarNavDropdown">
          <ul className="navbar-nav">
            <li className="nav-item">
              <a className="nav-link" href="#">Dashboard</a>
            </li>
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                id="navbarDropdownMenuLink"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Solutions
              </a>
              <ul className="dropdown-menu" aria-labelledby="navbarDropdownMenuLink" id="dropdown_1">
                {solutions.map((solution, index) => (
                  <li key={index}>
                    <a className="dropdown-item" href={solution.link}>{solution.name}</a>
                  </li>
                ))}
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;