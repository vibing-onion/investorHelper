let sol = document.getElementById('dropdown_1');
const sol_options = ['CIK lookup', 'Company Facts', 'Historical 10Q', 'Sector Search'];
const sol_links = ['/search_cik', '/search_company', '/historical_10Q', '/sector_search'];
for (let i = 0; i < sol_options.length; i++) {
    let dom_li = document.createElement('li');
    let dom_a = document.createElement('a');
    dom_a.setAttribute('class', 'dropdown-item');
    dom_a.setAttribute('href', sol_links[i]);
    dom_a.innerHTML = sol_options[i];
    dom_li.appendChild(dom_a);
    sol.appendChild(dom_li);
}