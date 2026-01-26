/**
 * TV Display JavaScript (Legacy fallback)
 * 
 * NOTE: This file is kept for backwards compatibility.
 * The main logic is now inline in tv_display.html using WebSocket/Fetch
 * for partial updates without full page reloads.
 * 
 * Full page reloads are DISABLED to preserve fullscreen mode.
 */

function updateDateTime() {
  const now = new Date();
  const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  const timeOptions = { hour12: true, hour: 'numeric', minute: '2-digit', second: '2-digit' };

  const dateEl = document.getElementById('current-date');
  const timeEl = document.getElementById('current-time');
  if (dateEl) dateEl.textContent = now.toLocaleDateString('en-US', dateOptions);
  if (timeEl) timeEl.textContent = now.toLocaleTimeString('en-US', timeOptions);
}

function updateCountdowns() {
  const now = Math.floor(Date.now() / 1000);
  document.querySelectorAll('.countdown-element').forEach(element => {
    const expiryTimestamp = parseInt(element.dataset.expiry, 10);
    if (isNaN(expiryTimestamp)) return;
    const remaining = expiryTimestamp - now;
    const label = element.querySelector('.countdown-text');
    if (!label) return;
    if (remaining <= 0) {
      label.textContent = '00:00';
      element.classList.add('countdown-expired');
      return;
    }
    const minutes = Math.floor(remaining / 60);
    const seconds = remaining % 60;
    label.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    element.classList.remove('countdown-expired');
  });
}

// NOTE: Auto-refresh is DISABLED to preserve fullscreen mode
// Data updates are now handled via WebSocket/Fetch in the template
// function scheduleAutoRefresh() { ... } - REMOVED

document.addEventListener('DOMContentLoaded', () => {
  // Clock and countdown timers only - no page reloads
  updateDateTime();
  setInterval(updateDateTime, 1000);
  updateCountdowns();
  setInterval(updateCountdowns, 1000);
  // NO auto-refresh - handled by WebSocket/Fetch in template
});

document.getElementById('fullscreenBtn')?.addEventListener('click', () => {
  const button = document.getElementById('fullscreenBtn');
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
    if (button) button.innerHTML = '<i class="fa-solid fa-compress"></i><span>Exit Fullscreen</span>';
  } else {
    document.exitFullscreen();
    if (button) button.innerHTML = '<i class="fa-solid fa-expand"></i><span>Fullscreen</span>';
  }
});
