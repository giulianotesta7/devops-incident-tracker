const pendingBlock = document.getElementById('pendingBlock');
const waitingBlock = document.getElementById('waitingBlock');

function showByStatus() {
    const selected = document.querySelector('input[name="status"]:checked')?.value;
    pendingBlock.hidden = selected !== 'pending';
    waitingBlock.hidden = selected !== 'waiting';
}
  document.querySelectorAll('input[name="status"]').forEach(radio => {
    radio.addEventListener('change', showByStatus);
  });

showByStatus();