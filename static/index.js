{/* <div class="container-fluid">
        <a class="navbar-brand" href="/">Home</a>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="#">Features</a>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Solutions
              </a>
              <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink" id="dropdown_1">
                <li><a class="dropdown-item" href="/search_cik">CIK lookup</a></li>
                <li><a class="dropdown-item" href="/search_company">Company Facts</a></li>
                <li><a class="dropdown-item" href="/historical_10Q">Historical 10Q</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div> */}

let sol = document.getElementById('dropdown_1');
const sol_options = ['CIK lookup', 'Company Facts', 'Historical 10Q'];
const sol_links = ['/search_cik', '/search_company', '/historical_10Q'];
for (let i = 0; i < sol_options.length; i++) {
    let dom_li = document.createElement('li');
    let dom_a = document.createElement('a');
    dom_a.setAttribute('class', 'dropdown-item');
    dom_a.setAttribute('href', sol_links[i]);
    dom_a.innerHTML = sol_options[i];
    dom_li.appendChild(dom_a);
    sol.appendChild(dom_li);
}