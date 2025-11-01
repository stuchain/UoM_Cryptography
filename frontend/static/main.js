// Main JavaScript for Secure Channel Demo Frontend

// Initialize phase cards
const phases = [
    { num: 1, title: 'Basic Diffie-Hellman', desc: 'Key exchange without authentication' },
    { num: 2, title: 'MITM Attack', desc: 'Man-in-the-Middle attack demonstration' },
    { num: 3, title: 'Authenticated DH', desc: 'Digital signatures prevent MITM' },
    { num: 4, title: 'Secure Channel', desc: 'AEAD encryption with ChaCha20-Poly1305' },
    { num: 5, title: 'Blockchain Integration', desc: 'Solana-based key registry' }
];

// Charts storage
const charts = {};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializePhases();
});

function initializePhases() {
    const grid = document.getElementById('phasesGrid');
    grid.innerHTML = '';
    
    phases.forEach(phase => {
        const card = createPhaseCard(phase);
        grid.appendChild(card);
    });
}

function createPhaseCard(phase) {
    const card = document.createElement('div');
    card.className = 'phase-card';
    card.id = `phase-${phase.num}`;
    
    card.innerHTML = `
        <div class="phase-header">
            <div>
                <span class="phase-number">Phase ${phase.num}</span>
                <span class="phase-title">${phase.title}</span>
            </div>
            <span class="status-indicator status-pending" id="status-${phase.num}"></span>
        </div>
        <p style="color: rgba(255, 255, 255, 0.7); margin-bottom: 15px;">${phase.desc}</p>
        <div class="results" id="results-${phase.num}">
            <div class="loading" style="display: none;" id="loading-${phase.num}">
                Running phase ${phase.num}...
            </div>
            <div id="content-${phase.num}">
                <p style="color: rgba(255, 255, 255, 0.6); font-style: italic;">Click button above to run this phase</p>
            </div>
        </div>
    `;
    
    return card;
}

function updateStatus(phaseNum, status) {
    const indicator = document.getElementById(`status-${phaseNum}`);
    indicator.className = `status-indicator status-${status}`;
    
    const card = document.getElementById(`phase-${phaseNum}`);
    if (status === 'running') {
        card.classList.add('active');
        document.getElementById(`loading-${phaseNum}`).style.display = 'block';
    } else {
        card.classList.remove('active');
        document.getElementById(`loading-${phaseNum}`).style.display = 'none';
    }
}

async function runPhase(phaseNum) {
    updateStatus(phaseNum, 'running');
    const contentDiv = document.getElementById(`content-${phaseNum}`);
    
    try {
        const response = await fetch(`/api/phase${phaseNum}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateStatus(phaseNum, 'success');
            displayPhaseResults(phaseNum, data);
        } else {
            updateStatus(phaseNum, 'error');
            contentDiv.innerHTML = `
                <div class="summary error">
                    <strong>Error:</strong> ${data.error || 'Unknown error'}
                </div>
            `;
        }
    } catch (error) {
        updateStatus(phaseNum, 'error');
        contentDiv.innerHTML = `
            <div class="summary error">
                <strong>Error:</strong> ${error.message}
            </div>
        `;
    }
}

function displayPhaseResults(phaseNum, data) {
    const contentDiv = document.getElementById(`content-${phaseNum}`);
    
    switch(phaseNum) {
        case 1:
            displayPhase1Results(contentDiv, data);
            break;
        case 2:
            displayPhase2Results(contentDiv, data);
            break;
        case 3:
            displayPhase3Results(contentDiv, data);
            break;
        case 4:
            displayPhase4Results(contentDiv, data);
            break;
        case 5:
            displayPhase5Results(contentDiv, data);
            break;
    }
}

function displayPhase1Results(div, data) {
    const viz = data.visualization;
    const d = data.data;
    
    div.innerHTML = `
        <div class="comparison-grid">
            <div class="comparison-item ${viz.keys_match ? 'match' : 'differ'}">
                <strong>Alice's Shared Key</strong>
                <div class="key-display">${d.alice.shared_key}</div>
            </div>
            <div class="comparison-item ${viz.keys_match ? 'match' : 'differ'}">
                <strong>Bob's Shared Key</strong>
                <div class="key-display">${d.bob.shared_key}</div>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="chart-phase1"></canvas>
        </div>
        <div class="summary ${viz.keys_match ? '' : 'error'}">
            <strong>Result:</strong> ${data.summary}
        </div>
    `;
    
    // Create comparison chart
    createKeyComparisonChart('chart-phase1', {
        alice: d.alice.shared_key.substring(0, 16) + '...',
        bob: d.bob.shared_key.substring(0, 16) + '...',
        match: viz.keys_match
    });
}

function displayPhase2Results(div, data) {
    const viz = data.visualization;
    const d = data.data;
    
    div.innerHTML = `
        <h3 style="margin: 15px 0; color: rgba(244, 67, 54, 0.9);">Attack Results</h3>
        <div class="comparison-grid">
            <div class="comparison-item ${d.alice_bob_keys_differ ? 'differ' : 'match'}">
                <strong>Alice's Key</strong>
                <div class="key-display">${d.alice.shared_key.substring(0, 32)}...</div>
            </div>
            <div class="comparison-item ${d.alice_bob_keys_differ ? 'differ' : 'match'}">
                <strong>Bob's Key</strong>
                <div class="key-display">${d.bob.shared_key.substring(0, 32)}...</div>
            </div>
            <div class="comparison-item">
                <strong>Mallory's Key (with Alice)</strong>
                <div class="key-display">${d.mallory.key_with_alice.substring(0, 32)}...</div>
            </div>
            <div class="comparison-item">
                <strong>Mallory's Key (with Bob)</strong>
                <div class="key-display">${d.mallory.key_with_bob.substring(0, 32)}...</div>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="chart-phase2"></canvas>
        </div>
        <div class="summary ${d.attack_success ? 'error' : ''}">
            <strong>Result:</strong> ${data.summary}
        </div>
    `;
    
    // Create MITM visualization
    createMITMChart('chart-phase2', viz.keys);
}

function displayPhase3Results(div, data) {
    const d = data.data;
    
    div.innerHTML = `
        <h3 style="margin: 15px 0; color: rgba(255, 255, 255, 0.95);">Authentication Results</h3>
        <div class="result-item">
            <strong>Alice's Signature:</strong> 
            <span style="color: ${d.bob.signature_valid ? '#4caf50' : '#f44336'};">
                ${d.bob.signature_valid ? '✓ Valid' : '✗ Invalid'}
            </span>
        </div>
        <div class="result-item">
            <strong>Bob's Signature:</strong> 
            <span style="color: ${d.alice.signature_valid ? '#4caf50' : '#f44336'};">
                ${d.alice.signature_valid ? '✓ Valid' : '✗ Invalid'}
            </span>
        </div>
        <div class="result-item">
            <strong>Keys Match:</strong> 
            <span style="color: ${d.keys_match ? '#4caf50' : '#f44336'};">
                ${d.keys_match ? '✓ Yes' : '✗ No'}
            </span>
        </div>
        <div class="result-item">
            <strong>MITM Attack Prevented:</strong> 
            <span style="color: ${d.mallory_attack_failed ? '#4caf50' : '#f44336'};">
                ${d.mallory_attack_failed ? '✓ Yes' : '✗ No'}
            </span>
        </div>
        <div class="chart-container">
            <canvas id="chart-phase3"></canvas>
        </div>
        <div class="summary ${d.authenticated ? '' : 'error'}">
            <strong>Result:</strong> ${data.summary}
        </div>
    `;
    
    createAuthenticationChart('chart-phase3', data.visualization);
}

function displayPhase4Results(div, data) {
    const d = data.data;
    const viz = data.visualization;
    
    div.innerHTML = `
        <h3 style="margin: 15px 0; color: rgba(255, 255, 255, 0.95);">Encryption Results</h3>
        <div class="result-item">
            <strong>Original Message:</strong> "${d.message_original}"
        </div>
        <div class="result-item">
            <strong>Message Length:</strong> ${d.message_length} bytes
        </div>
        <div class="result-item">
            <strong>Ciphertext Length:</strong> ${d.ciphertext_length} bytes
            <span style="color: rgba(255, 255, 255, 0.6);">(overhead: ${viz.message_sizes.overhead} bytes)</span>
        </div>
        <div class="result-item">
            <strong>Decryption:</strong> 
            <span style="color: ${d.decryption_success ? '#4caf50' : '#f44336'};">
                ${d.decryption_success ? '✓ Success' : '✗ Failed'}
            </span>
        </div>
        <div class="result-item">
            <strong>Tampering Detection:</strong> 
            <span style="color: ${d.tampering_detected ? '#4caf50' : '#f44336'};">
                ${d.tampering_detected ? '✓ Detected' : '✗ Not Detected'}
            </span>
        </div>
        <div class="chart-container">
            <canvas id="chart-phase4"></canvas>
        </div>
        <div class="summary ${d.decryption_success && d.tampering_detected ? '' : 'error'}">
            <strong>Result:</strong> ${data.summary}
        </div>
    `;
    
    createEncryptionChart('chart-phase4', viz);
}

function displayPhase5Results(div, data) {
    const d = data.data;
    
    div.innerHTML = `
        <h3 style="margin: 15px 0; color: rgba(255, 255, 255, 0.95);">Blockchain Verification</h3>
        <div class="result-item">
            <strong>Network:</strong> ${d.blockchain.network}
        </div>
        <div class="result-item">
            <strong>Program ID:</strong> 
            <div class="key-display">${d.blockchain.registry_program}</div>
        </div>
        <div style="margin-top: 20px;">
            <h4>Alice:</h4>
            <div class="result-item">
                <strong>Address:</strong> ${d.alice.address}
            </div>
            <div class="result-item">
                <strong>Key Registered:</strong> 
                <span style="color: ${d.alice.registered ? '#4caf50' : '#f44336'};">
                    ${d.alice.registered ? '✓ Yes' : '✗ No'}
                </span>
            </div>
            <div class="result-item">
                <strong>Key Verified:</strong> 
                <span style="color: ${d.alice.verified ? '#4caf50' : '#f44336'};">
                    ${d.alice.verified ? '✓ Yes' : '✗ No'}
                </span>
            </div>
        </div>
        <div style="margin-top: 20px;">
            <h4>Bob:</h4>
            <div class="result-item">
                <strong>Address:</strong> ${d.bob.address}
            </div>
            <div class="result-item">
                <strong>Key Registered:</strong> 
                <span style="color: ${d.bob.registered ? '#4caf50' : '#f44336'};">
                    ${d.bob.registered ? '✓ Yes' : '✗ No'}
                </span>
            </div>
            <div class="result-item">
                <strong>Key Verified:</strong> 
                <span style="color: ${d.bob.verified ? '#4caf50' : '#f44336'};">
                    ${d.bob.verified ? '✓ Yes' : '✗ No'}
                </span>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="chart-phase5"></canvas>
        </div>
        <div class="summary ${data.visualization.verification_success ? '' : 'error'}">
            <strong>Result:</strong> ${data.summary}
        </div>
    `;
    
    createBlockchainChart('chart-phase5', data.visualization);
}

// Chart creation functions
function createKeyComparisonChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (charts[canvasId]) charts[canvasId].destroy();
    
    charts[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Alice', 'Bob'],
            datasets: [{
                label: 'Shared Key (first 16 bytes)',
                data: [data.alice, data.bob],
                backgroundColor: data.match ? ['#4caf50', '#4caf50'] : ['#f44336', '#f44336'],
                borderColor: data.match ? ['#388e3c', '#388e3c'] : ['#d32f2f', '#d32f2f'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: data.match ? 'Keys Match ✓' : 'Keys Differ ✗',
                    color: data.match ? '#4caf50' : '#f44336'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createMITMChart(canvasId, keys) {
    const ctx = document.getElementById(canvasId);
    if (charts[canvasId]) charts[canvasId].destroy();
    
    charts[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Alice', 'Bob', 'Mallory↔Alice', 'Mallory↔Bob'],
            datasets: [{
                label: 'Keys (first 16 bytes)',
                data: [keys.alice, keys.bob, keys.mallory_alice, keys.mallory_bob],
                backgroundColor: ['#f44336', '#f44336', '#ff9800', '#ff9800'],
                borderColor: ['#d32f2f', '#d32f2f', '#f57c00', '#f57c00'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'MITM Attack: Alice and Bob Have Different Keys',
                    color: '#f44336'
                }
            }
        }
    });
}

function createAuthenticationChart(canvasId, viz) {
    const ctx = document.getElementById(canvasId);
    if (charts[canvasId]) charts[canvasId].destroy();
    
    charts[canvasId] = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Signature Valid', 'Keys Match', 'Attack Prevented'],
            datasets: [{
                data: [
                    viz.signatures_valid ? 1 : 0,
                    viz.keys_match ? 1 : 0,
                    viz.attack_prevented ? 1 : 0
                ],
                backgroundColor: [
                    viz.signatures_valid ? '#4caf50' : '#f44336',
                    viz.keys_match ? '#4caf50' : '#f44336',
                    viz.attack_prevented ? '#4caf50' : '#f44336'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Authentication Status',
                    color: '#667eea'
                }
            }
        }
    });
}

function createEncryptionChart(canvasId, viz) {
    const ctx = document.getElementById(canvasId);
    if (charts[canvasId]) charts[canvasId].destroy();
    
    charts[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Original', 'Encrypted', 'Overhead'],
            datasets: [{
                label: 'Size (bytes)',
                data: [
                    viz.message_sizes.original,
                    viz.message_sizes.encrypted,
                    viz.message_sizes.overhead
                ],
                backgroundColor: ['#2196f3', '#9c27b0', '#ff9800'],
                borderColor: ['#1976d2', '#7b1fa2', '#f57c00'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Message Encryption Overhead',
                    color: '#667eea'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createBlockchainChart(canvasId, viz) {
    const ctx = document.getElementById(canvasId);
    if (charts[canvasId]) charts[canvasId].destroy();
    
    charts[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Alice', 'Bob'],
            datasets: [{
                label: 'Registration Status',
                data: [
                    viz.registrations[0].verified ? 1 : 0,
                    viz.registrations[1].verified ? 1 : 0
                ],
                backgroundColor: [
                    viz.registrations[0].verified ? '#4caf50' : '#f44336',
                    viz.registrations[1].verified ? '#4caf50' : '#f44336'
                ],
                borderColor: [
                    viz.registrations[0].verified ? '#388e3c' : '#d32f2f',
                    viz.registrations[1].verified ? '#388e3c' : '#d32f2f'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Blockchain Key Verification',
                    color: '#667eea'
                },
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

async function runAllPhases() {
    for (let i = 1; i <= 5; i++) {
        await runPhase(i);
        // Small delay between phases
        await new Promise(resolve => setTimeout(resolve, 500));
    }
}

