const tagRemove = e => {
    const badgeElement = e.target.parentElement;
    const targetName = badgeElement.dataset.target;
    const pk = badgeElement.dataset.pk;

    const displayElement = document.getElementById(`${targetName}-display`);
    displayElement.removeChild(badgeElement);

    const formValuesElement = document.getElementById(`${targetName}-values`);
    const tagValueElement = document.querySelector(`input[name="${targetName}"][value="${pk}"]`);
    formValuesElement.removeChild(tagValueElement);

};

const tagCreateBadge = element => {
    const displayElement = document.getElementById(`${element.dataset.target}-display`);
    const badge = document.createElement('span');
    badge.dataset.pk = element.dataset.pk;
    badge.dataset.target = element.dataset.target;
    badge.textContent = element.dataset.text;
    badge.classList.add('tag');

    const closeButton = document.createElement('span');
    closeButton.classList.add('tag-close', 'close');
    closeButton.addEventListener('click', tagRemove);
    badge.appendChild(closeButton);
    displayElement.appendChild(badge);
};

const tagCreateFormValue = element => {
    const targetName = element.dataset.target;
    const formValuesElement = document.getElementById(`${targetName}-values`);
    const inputHiddenElement = document.createElement('input');

    inputHiddenElement.name = targetName;
    inputHiddenElement.type = 'hidden';
    inputHiddenElement.value = element.dataset.pk;
    formValuesElement.appendChild(inputHiddenElement);
};

const tagClickSuggest = e => {
    const element = e.target;
    const targetName = element.dataset.target;
    const pk = element.dataset.pk;
    if (!document.querySelector(`input[name="${targetName}"][value="${pk}"]`)) {
        document.getElementById(`${element.dataset.target}-input`).value = '';
        tagCreateBadge(element);
        tagCreateFormValue(element);
    }
};


for (const element of document.getElementsByClassName('tag-suggest')) {
    const targetName = element.dataset.target;
    const suggestListElement = document.getElementById(`${targetName}-list`);

    element.addEventListener('keyup', () => {
        const keyword = element.value;
        const url = `${element.dataset.url}?keyword=${keyword}`;
        if (keyword) {
            fetch(url)
                .then(response => {
                    return response.json();
                })
                .then(response => {
                    let isFound = false;
                    const frag = document.createDocumentFragment();
                    suggestListElement.innerHTML = '';
                    for (const tag of response.tag_list) {
                        const li = document.createElement('li');
                        li.textContent = tag.name_with_count;
                        li.dataset.pk = tag.pk;
                        li.dataset.target = targetName;
                        li.dataset.text = tag.name;
                        li.addEventListener('mousedown', tagClickSuggest);
                        frag.appendChild(li);
                        isFound = true;
                    }

                    if (isFound) {
                        suggestListElement.appendChild(frag);
                        suggestListElement.style.display = 'block';

                    } else {
                        suggestListElement.style.display = 'none';
                    }

                })
                .catch(error => {
                    console.log(error);
                });
        }
    });

    element.addEventListener('blur', () => {
        suggestListElement.style.display = 'none';
    });
}

for (const element of document.getElementsByClassName('tag-close')) {
    element.addEventListener('click', tagRemove);
}