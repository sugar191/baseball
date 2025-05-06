document.querySelector('#open-search-popup').addEventListener('click', () => {
    document.querySelector('#search-modal').classList.remove('hidden');
});

document.querySelector('#close-search-popup').addEventListener('click', () => {
    document.querySelector('#search-modal').classList.add('hidden');
});