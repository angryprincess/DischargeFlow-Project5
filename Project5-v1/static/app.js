document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('run-btn');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');
    const timelineContainer = document.getElementById('timeline-container');
    const timeline = document.getElementById('timeline');
    const agentStatusText = document.getElementById('agent-status-text');
    const pulseDot = document.querySelector('.pulse-dot');

    runBtn.addEventListener('click', async () => {
        // Reset UI
        runBtn.disabled = true;
        btnText.textContent = 'Processing...';
        spinner.classList.remove('hidden');
        timelineContainer.classList.remove('hidden');
        timeline.innerHTML = '';
        agentStatusText.textContent = 'Agent is coordinating...';
        pulseDot.style.animation = 'pulse 1s infinite';
        pulseDot.style.background = 'var(--accent)';

        try {
            const response = await fetch('/api/discharge', {
                method: 'POST'
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            const logs = result.logs;

            // Render logs one by one for a timeline effect
            for (let i = 0; i < logs.length; i++) {
                await new Promise(r => setTimeout(r, 400)); // 400ms delay per log for visual effect
                renderLog(logs[i]);
                timelineContainer.scrollTop = timelineContainer.scrollHeight;
            }

            // Finish UI
            agentStatusText.textContent = 'Workflow Completed';
            pulseDot.style.animation = 'none';
            pulseDot.style.background = 'var(--ehr-color)';
            
        } catch (error) {
            console.error('Error:', error);
            agentStatusText.textContent = 'Error occurred';
            pulseDot.style.animation = 'none';
            pulseDot.style.background = 'var(--error-color)';
            renderLog({
                role: 'error',
                message: 'Failed to execute workflow via API.',
                data: error.toString()
            });
        } finally {
            runBtn.disabled = false;
            btnText.textContent = 'Run Another Discharge';
            spinner.classList.add('hidden');
        }
    });

    function renderLog(log) {
        const entry = document.createElement('div');
        entry.className = `log-entry role-${log.role.toLowerCase()}`;
        
        let iconText = 'SYS';
        if (log.role === 'ehr') iconText = 'EHR';
        if (log.role === 'pharmacy') iconText = 'PHRM';
        if (log.role === 'billing') iconText = 'BILL';
        if (log.role === 'agent') iconText = 'AGT';
        if (log.role === 'error') iconText = 'ERR';

        let dataHtml = '';
        if (log.data) {
            let formattedData = typeof log.data === 'object' ? JSON.stringify(log.data, null, 2) : log.data;
            dataHtml = `<div class="log-data">${escapeHtml(formattedData)}</div>`;
        }

        const timeString = log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();

        entry.innerHTML = `
            <div class="log-icon">${iconText}</div>
            <div class="log-content">
                <span class="log-time">${timeString} - ${log.role.toUpperCase()}</span>
                <span class="log-msg">${escapeHtml(log.message)}</span>
                ${dataHtml}
            </div>
        `;
        
        timeline.appendChild(entry);
    }

    function escapeHtml(unsafe) {
        if (!unsafe) return '';
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
});
