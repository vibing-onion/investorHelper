const copyToSubmit = (v) => {
    let input = document.getElementById('sicInput');
    input.value = v;
}

const searchItem = document.querySelectorAll('.select-item');
searchItem.forEach(i => {
    i.addEventListener('click', () => {
        document.querySelectorAll('.active').forEach(j => {
            j.classList.remove('active');
        })
        i.classList.add('active');
        copyToSubmit(i.value);
    })
})

const searchInput = document.getElementById('searchInput');
searchInput.style.width = document.querySelector('.list-group').offsetWidth + 'px';
searchInput.addEventListener('change', () => {
    s = document.getElementById('searchInput').value.toLowerCase()
    searchItem.forEach(i => {
        if (i.innerHTML.toLowerCase().includes(s)) {
            i.style.display = 'block';
        } else {
            i.style.display = 'none';
        }
    })
})