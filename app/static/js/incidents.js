const pendingBlock = document.getElementById('pendingBlock');
const waitingBlock = document.getElementById('waitingBlock');
const solvedBlock = document.getElementById('solvedBlock');

function showByStatus() {
    const selected = document.querySelector('input[name="status"]:checked')?.value;
    pendingBlock.hidden = selected !== 'pending';
    waitingBlock.hidden = selected !== 'waiting';
    solvedBlock.hidden = selected !== 'solved';
}
  document.querySelectorAll('input[name="status"]').forEach(radio => {
    radio.addEventListener('change', showByStatus);
  });

showByStatus();