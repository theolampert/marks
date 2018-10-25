const dqs = document.querySelector;
const bookmarkList = document.querySelector('.bookmark-wrapper');
const form = document.querySelector('.add_bookmark');
const deleteButtons = document.querySelectorAll('.delete_bookmark');
const bookmarkLinks = document.querySelectorAll('.bookmark__link');


const stateContainer = (initialState, middleware = []) => {
  let state = initialState;

  const updateState = (newState) => {
    const nextState = { ...state, ...newState };
    state = nextState;
    middleware.map(m => m(nextState));
    return nextState;
  }

  return {
    updateState,
    getState: () => state,
  }
};

const store = stateContainer({
  bookmarkIndex: -1,
  nightMode: !!window.localStorage['night-mode'] || false,
}, [
  // console.log,
]);


function enableColorMode() {
  const colorModeButton = document.querySelector('.toggle-color-mode');

  // Nightmode
  if (store.getState().nightMode) {
    document.body.classList.toggle('night-mode');
  }

  colorModeButton.addEventListener('click', () => {
    const body = document.body;
    const { nightMode } = store.getState();

    if (!nightMode) {
      body.classList.add('night-mode');
      localStorage.setItem('night-mode', true);
      store.updateState({ nightMode: true });
    } else {
      body.classList.remove('night-mode');
      localStorage.removeItem('night-mode');
      store.updateState({ nightMode: false });
    }
  });
}

function enableShortcuts() {
  bookmarkLinks.forEach((link, index) => {
    link.addEventListener('focus', () => {
      store.updateState({ bookmarkIndex: index });
    });
  });

  function handleKeys(event) {
    const { key } = event;
    const bookmarks = bookmarkList.childNodes;
    const index = store.getState().bookmarkIndex;
    const isBeginningOfList = index < (bookmarkList.childNodes.length - 1);
    const isEndOfList = index > 0;

    if (key === 'j' && isBeginningOfList) {
      bookmarks[index + 1].childNodes[0].focus();
    }
    if (key === 'k' && isEndOfList) {
      bookmarks[index - 1].childNodes[0].focus();
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
