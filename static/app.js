(() => {
  const container = document.querySelector('#sets-container');
  const addButton = document.querySelector('#add-set');
  let nextId = 0;

  function updateTotal(card) {
    let total = 0;
    card.querySelectorAll('.quadrant-input').forEach((input) => {
      const value = Number.parseInt(input.value, 10);
      if (Number.isInteger(value)) total += value;
    });
    const totalElement = card.querySelector('.set-total');
    totalElement.textContent = `Total: ${total} / 15`;
    totalElement.classList.toggle('valid-total', total === 15);
  }

  function renumberSets() {
    [...container.querySelectorAll('.set-card')].forEach((card, position) => {
      const index = position + 1;
      card.querySelector('legend').textContent = `Conjunto de quadrantes ${index}`;
      card.querySelector('input[name="set_id"]').value = index;
      card.querySelectorAll('.quadrant-input').forEach((input) => {
        const quadrant = input.name.match(/^q(\d+)_/)[1];
        input.name = `q${quadrant}_${position}`;
      });
      const gamesInput = card.querySelector('input[name^="number_of_games_"]');
      gamesInput.name = `number_of_games_${position}`;
    });
  }

  function addSet() {
    const index = nextId++;
    const card = document.createElement('fieldset');
    card.className = 'set-card';
    card.innerHTML = `
      <legend>Conjunto de quadrantes ${index + 1}</legend>
      <input type="hidden" name="set_id" value="${index + 1}">
      <div class="quadrant-grid">
        ${[1, 2, 3, 4, 5].map((q) => `
          <label>Q${q}<span>${(q - 1) * 5 + 1}–${q * 5}</span>
          <input class="quadrant-input" name="q${q}_${index}" type="number" min="0" max="5" required placeholder="0">
        `).join('')}
      </div>
      <div class="set-footer">
        <label>Quantidade de jogos
          <input name="number_of_games_${index}" type="number" min="1" required placeholder="Ex.: 5">
        </label>
        <strong class="set-total">Total: 0 / 15</strong>
        <button type="button" class="remove-set">Remover</button>
      </div>`;

    card.querySelectorAll('.quadrant-input').forEach((input) => input.addEventListener('input', () => updateTotal(card)));
    card.querySelector('.remove-set').addEventListener('click', () => {
      card.remove();
      renumberSets();
    });
    container.appendChild(card);
  }

  addButton.addEventListener('click', addSet);
  addSet();
})();
