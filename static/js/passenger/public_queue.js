(() => {
  const queueBody = document.getElementById('queueTableBody');
  const mobileCards = document.getElementById('mobileQueueCards');
  const emptyState = document.getElementById('queueEmptyState');
  const routeFilter = document.getElementById('routeFilter');
  let selectedRoute = routeFilter?.value || 'all';
  let entries = [];
  let queueServerOffset = Math.floor(Date.now() / 1000);

  const initialStateEl = document.getElementById('initialQueueState');
  if (initialStateEl) {
    try {
      const payload = JSON.parse(initialStateEl.textContent || '{}');
      entries = payload.entries || [];
      const serverTime = payload.server_time || Math.floor(Date.now() / 1000);
      queueServerOffset = Math.floor(Date.now() / 1000) - serverTime;
      renderEntries();
    } catch (err) {
      console.error('Invalid initial queue state', err);
    }
  }

  routeFilter?.addEventListener('change', () => {
    selectedRoute = routeFilter.value;
    renderEntries();
  });

  function connectQueueSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const queueSocket = new WebSocket(`${protocol}://${window.location.host}/ws/queue/`);

    queueSocket.addEventListener('message', (event) => {
      try {
        const payload = JSON.parse(event.data);
        entries = payload.entries || [];
        const serverTime = payload.server_time || Math.floor(Date.now() / 1000);
        queueServerOffset = Math.floor(Date.now() / 1000) - serverTime;
        renderEntries();
      } catch (err) {
        console.error('Invalid queue payload', err);
      }
    });

    queueSocket.addEventListener('close', () => {
      setTimeout(connectQueueSocket, 2000);
    });
  }

  connectQueueSocket();

  function renderEntries() {
    const filtered = selectedRoute === 'all'
      ? entries
      : entries.filter(entry => entry.route_id && String(entry.route_id) === selectedRoute);

    queueBody && (queueBody.innerHTML = filtered.map(renderRow).join(''));
    mobileCards && (mobileCards.innerHTML = filtered.map(renderCard).join(''));
    if (emptyState) {
      emptyState.classList.toggle('d-none', filtered.length > 0);
    }
  }

  function renderRow(entry) {
    const statusClass = (entry.status || 'idle').toLowerCase();
    return `
      <tr class="${entry.status === 'Departed' ? 'departed-row' : ''}">
        <td class="entry-time-cell">${escapeHtml(entry.entry_time_numeric)}</td>
        <td>${escapeHtml(entry.vehicle_plate)}</td>
        <td><span class="route-badge">${escapeHtml(entry.route)}</span></td>
        <td>${escapeHtml(entry.driver_name)}</td>
        <td>
          <span class="status-pill status-pill-${statusClass}">
            ${escapeHtml(entry.status)}
          </span>
        </td>
        <td>${escapeHtml(entry.departure_time_display)}</td>
        <td>${renderCountdown(entry)}</td>
      </tr>`;
  }

  function renderCard(entry) {
    const statusClass = (entry.status || 'idle').toLowerCase();
    return `
      <div class="vehicle-card vehicle-card--landscape ${entry.status === 'Departed' ? 'departed-row' : ''}">
        <div class="card-header">
          <div class="vehicle-info">
            <div class="vehicle-icon">
              <i class="bi bi-truck"></i>
            </div>
            <div class="vehicle-details">
              <div class="vehicle-plate">${escapeHtml(entry.vehicle_plate)}</div>
              <div class="driver-name">${escapeHtml(entry.driver_name)}</div>
            </div>
          </div>
          <span class="status-pill status-pill-${statusClass}">${escapeHtml(entry.status)}</span>
          <div class="card-countdown">
            ${renderCountdown(entry)}
          </div>
        </div>
        <div class="card-body">
          <div class="info-section">
            <div class="info-label">
              <i class="bi bi-signpost"></i>
              <span>Route</span>
            </div>
            <div class="route-tag">${escapeHtml(entry.route)}</div>
          </div>
          <div class="times-grid">
            <div class="time-item">
              <div class="time-label">
                <i class="bi bi-clock"></i>
                <span>Entry</span>
              </div>
              <div class="time-value">${escapeHtml(entry.entry_time_display)}</div>
            </div>
            <div class="time-item">
              <div class="time-label">
                <i class="bi bi-calendar2-check"></i>
                <span>Departure</span>
              </div>
              <div class="time-value">${escapeHtml(entry.departure_time_display)}</div>
            </div>
          </div>
        </div>
      </div>`;
  }

  function renderCountdown(entry) {
    if (entry.countdown_active && entry.expiry_timestamp) {
      return `<span class="countdown" data-boarding-expiry="${entry.expiry_timestamp}">--</span>`;
    }
    if (entry.departed_countdown_active && entry.departed_countdown_expiry) {
      return `<span class="departed-countdown" data-departed-expiry="${entry.departed_countdown_expiry}">--</span>`;
    }
    if (entry.status === 'Queued') {
      return '<span class="badge bg-secondary">Waiting in line</span>';
    }
    return '<span class="badge bg-danger">Departed</span>';
  }

  function updateCountdowns() {
    const now = Math.floor(Date.now() / 1000) - queueServerOffset;
    document.querySelectorAll('[data-boarding-expiry]').forEach(updateBoardingCountdown(now));
    document.querySelectorAll('[data-departed-expiry]').forEach(updateDepartedCountdown(now));
    requestAnimationFrame(updateCountdowns);
  }

  function updateBoardingCountdown(now) {
    return (element) => {
      const expiry = parseInt(element.dataset.boardingExpiry, 10);
      if (isNaN(expiry)) return;
      const remaining = expiry - now;
      if (remaining <= 0) {
        element.textContent = '00:00';
        element.classList.add('text-danger');
        return;
      }
      element.textContent = formatDuration(remaining);
      element.classList.toggle('text-danger', remaining <= 60);
    };
  }

  function updateDepartedCountdown(now) {
    return (element) => {
      const expiry = parseInt(element.dataset.departedExpiry, 10);
      if (isNaN(expiry)) return;
      const remaining = expiry - now;
      if (remaining <= 0) {
        element.textContent = '00:00';
        element.classList.add('text-danger');
        return;
      }
      element.textContent = formatDuration(remaining);
    };
  }

  function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  function escapeHtml(value) {
    const div = document.createElement('div');
    div.textContent = value ?? '';
    return div.innerHTML;
  }

  function handleResponsiveSwitch() {
    const isMobile = window.innerWidth <= 768;
    const table = document.querySelector('table');
    if (table) table.style.display = isMobile ? 'none' : 'table';
    if (mobileCards) mobileCards.style.display = isMobile ? 'flex' : 'none';
  }

  handleResponsiveSwitch();
  window.addEventListener('resize', handleResponsiveSwitch);
  requestAnimationFrame(updateCountdowns);
})();
