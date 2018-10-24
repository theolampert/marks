const bookmarkList = document.querySelector('.bookmark-wrapper');
const form = document.querySelector('.add_bookmark');
const deleteButtons = document.querySelectorAll('.delete_bookmark');
const bookmarkLinks = document.querySelectorAll('.bookmark__link');


function enableColorMode() {
  const colorModeButton = document.querySelector('.toggle-color-mode');

  // Nightmode
  if (!!window.localStorage.getItem('night-mode')) {
    document.body.classList.toggle('night-mode');
  }

  colorModeButton.addEventListener('click', () => {
    document.body.classList.toggle('night-mode');
    window.localStorage.setItem('night-mode', document.body.classList.includes('night-mode'));
  });
}

function enableShortcuts() {
  // Vim-ish shortcuts
  let focusedBookmarkIndex = -1;

  bookmarkLinks.forEach((link, index) => {
    link.addEventListener('focus', () => {
      focusedBookmarkIndex = index;
    })
  });

  function handleKeys(event) {
    const { key } = event;
    const bookmarks = bookmarkList.childNodes;

    if (key === 'j') {
      if (focusedBookmarkIndex < (bookmarkList.childNodes.length - 1)) {
        bookmarks[focusedBookmarkIndex + 1].childNodes[0].focus();
      }
    }
    if (key === 'k') {
      if (focusedBookmarkIndex > 0) {
        bookmarks[focusedBookmarkIndex - 1].childNodes[0].focus();
      }
    }

  }

  document.addEventListener('keydown', handleKeys, true);
}

function enableDeleteBookmarks() {
  deleteButtons.forEach((deleteButton) => {
    deleteButton.addEventListener('click', (event) => {
      event.preventDefault();
      const headers = new Headers();
      const url = deleteButton.dataset.url;
      headers.set('Content-Type', 'application/json');
      const body = JSON.stringify({
        url,
      });
      fetch('/bookmarks', {
        method: 'DELETE',
        headers,
        body,
      })
        .then(r => r.json())
        .then(r => {
          window.location.reload();
        })
        .catch(err => console.log(err))
    });
  });
}

function enableAddBookmarkForm() {
  const form = document.querySelector('.add_bookmark');

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const url = form.children[0].value;
    const tags = form.children[1].value.split(' ');
    const headers = new Headers();

    headers.set('Content-Type', 'application/json');

    const body = JSON.stringify({
      url,
      tags,
    });

    fetch('/bookmarks', {
      method: 'POST',
      headers,
      body,
    })
      .then(r => r.json())
      .then(r => {
        const bmWrapper = document.createElement('li');
        bmWrapper.classList.add('bookmark');

        bmWrapper.innerHTML = `
          <a class="bookmark__link" href="${r.url}">${r.url}</a>
          ${r.tags.map(t => `<a class="bookmark__tag" href="/tags/${t}">${t}</a>`).join('')}
        `;

        bookmarkList.appendChild(bmWrapper);
      })
      .catch(err => console.log(err))
  });
}

document.addEventListener('DOMContentLoaded', () => {
  enableShortcuts();
  enableColorMode();
  enableAddBookmarkForm();
  enableDeleteBookmarks();
});