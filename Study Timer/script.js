// ==================== TIMER VARIABLES ====================
let timerInterval;
let timeLeft = 1500; // 25 minutes in seconds
let isRunning = false;
let currentMinutes = 25;
let editingTimerId = null; // Track if we're editing a timer

// ==================== DOM ELEMENTS ====================
const timerDisplay = document.getElementById('timer');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const resetBtn = document.getElementById('resetBtn');
const saveCurrentBtn = document.getElementById('saveCurrentBtn');
const presetBtns = document.querySelectorAll('.preset-btn');
const customMinutes = document.getElementById('customMinutes');
const setCustomBtn = document.getElementById('setCustomBtn');
const timerList = document.getElementById('timerList');
const themeToggle = document.getElementById('themeToggle');
const timerNameInput = document.getElementById('timerNameInput');
const cancelEditBtn = document.getElementById('cancelEditBtn');

// ==================== TIMER FUNCTIONS ====================
function updateDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    // Change color based on time left
    if (timeLeft <= 60) {
        timerDisplay.style.color = '#ff4444';
    } else if (timeLeft <= 300) {
        timerDisplay.style.color = '#ffaa00';
    } else {
        timerDisplay.style.color = '';
    }
}

function startTimer() {
    if (!isRunning && timeLeft > 0) {
        isRunning = true;
        timerInterval = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
                updateDisplay();
            } else {
                pauseTimer();
                alert('⏰ Time is up!');
            }
        }, 1000);
    }
}

function pauseTimer() {
    clearInterval(timerInterval);
    isRunning = false;
}

function resetTimer() {
    pauseTimer();
    timeLeft = currentMinutes * 60;
    updateDisplay();
}

function setTimer(minutes) {
    pauseTimer();
    currentMinutes = minutes;
    timeLeft = minutes * 60;
    updateDisplay();
    
    // Update active preset button
    presetBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.minutes == minutes) {
            btn.classList.add('active');
        }
    });
}

// ==================== API FUNCTIONS ====================
// Fetch all timers from database
async function fetchTimers() {
    try {
        const response = await fetch('/timers');
        const data = await response.json();
        
        if (data.success) {
            renderSavedTimers(data.data);
        } else {
            console.error('Error fetching timers:', data.error);
            timerList.innerHTML = '<div class="loading-message">Error loading timers</div>';
        }
    } catch (error) {
        console.error('Fetch error:', error);
        timerList.innerHTML = '<div class="loading-message">Error connecting to server</div>';
    }
}

// Save or Update timer
async function saveTimerToDB() {
    const timerName = timerNameInput.value.trim();
    
    // Validate input
    if (!timerName) {
        alert('Please enter a timer name');
        timerNameInput.focus();
        return;
    }
    
    // Show saving message
    saveCurrentBtn.textContent = editingTimerId ? 'Updating...' : 'Saving...';
    saveCurrentBtn.disabled = true;
    
    try {
        let url = '/create_time';
        let method = 'POST';
        
        // If editing, use update endpoint
        if (editingTimerId) {
            url = `/update_timer/${editingTimerId}`;
            method = 'PUT';
        }
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: timerName,
                minutes: currentMinutes
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Clear input and cancel edit mode
            timerNameInput.value = '';
            cancelEditMode();
            
            // Show success message
            alert(`✅ Timer "${timerName}" ${editingTimerId ? 'updated' : 'saved'} successfully!`);
            
            // Refresh the timer list
            fetchTimers();
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Failed to save timer. Check console for details.');
    } finally {
        // Reset button
        saveCurrentBtn.textContent = 'Save Timer';
        saveCurrentBtn.disabled = false;
    }
}

// Delete timer from database
async function deleteTimerFromDB(id, name) {
    if (!confirm(`Are you sure you want to delete "${name}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/del_timer/${id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`✅ Timer "${name}" deleted`);
            fetchTimers(); // Refresh the list
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error deleting timer:', error);
        alert('❌ Failed to delete timer');
    }
}

// Edit timer - load into input field
function editTimer(id, name, minutes) {
    editingTimerId = id;
    timerNameInput.value = name;
    setTimer(minutes); // Set the timer minutes
    timerNameInput.focus();
    
    // Show cancel edit button
    document.getElementById('cancelEditBtn').style.display = 'inline-block';
    saveCurrentBtn.textContent = 'Update Timer';
}

// Cancel edit mode
function cancelEditMode() {
    editingTimerId = null;
    timerNameInput.value = '';
    document.getElementById('cancelEditBtn').style.display = 'none';
    saveCurrentBtn.textContent = 'Save Timer';
}

// ==================== RENDER FUNCTIONS ====================
function renderSavedTimers(timers) {
    if (!timers || timers.length === 0) {
        timerList.innerHTML = '<div class="loading-message">No saved timers yet</div>';
        return;
    }
    
    timerList.innerHTML = timers.map(timer => {
        // Format date
        const createdDate = new Date(timer.created_at);
        const formattedDate = createdDate.toLocaleString();
        
        return `
            <div class="timer-item ${editingTimerId == timer.id ? 'editing' : ''}" data-id="${timer.id}">
                <div class="timer-item-info">
                    <span>⏰ ${timer.name}</span>
                    <small>${timer.minutes} minutes • Created: ${formattedDate}</small>
                </div>
                <div class="timer-item-actions">
                    <button onclick="loadTimer(${timer.minutes})" class="load-btn" title="Load this timer">▶</button>
                    <button onclick="editTimer(${timer.id}, '${timer.name}', ${timer.minutes})" class="edit-btn" title="Edit timer">✏️</button>
                    <button onclick="deleteTimerFromDB(${timer.id}, '${timer.name}')" class="delete-btn" title="Delete timer">🗑</button>
                </div>
            </div>
        `;
    }).join('');
}

// Load timer from saved list
function loadTimer(minutes) {
    setTimer(minutes);
    alert(`✅ Timer loaded: ${minutes} minutes`);
}

// ==================== THEME TOGGLE ====================
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    document.body.classList.toggle('dark-mode');
    
    // Update button text
    if (document.body.classList.contains('light-mode')) {
        themeToggle.textContent = '🌙 Dark';
    } else {
        themeToggle.textContent = '☀️ Light';
    }
});

// ==================== EVENT LISTENERS ====================
startBtn.addEventListener('click', startTimer);
pauseBtn.addEventListener('click', pauseTimer);
resetBtn.addEventListener('click', resetTimer);

// Save/Update timer button
saveCurrentBtn.addEventListener('click', saveTimerToDB);

// Cancel edit button
document.getElementById('cancelEditBtn').addEventListener('click', cancelEditMode);

// Enter key in name input
timerNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        saveTimerToDB();
    }
});

// Preset buttons
presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        setTimer(parseInt(btn.dataset.minutes));
    });
});

// Custom minutes
setCustomBtn.addEventListener('click', () => {
    const minutes = parseInt(customMinutes.value);
    if (minutes && minutes > 0) {
        setTimer(minutes);
        customMinutes.value = '';
    } else {
        alert('Please enter valid minutes');
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && !e.target.matches('input, button')) {
        e.preventDefault();
        if (isRunning) {
            pauseTimer();
        } else {
            startTimer();
        }
    } else if (e.code === 'KeyR' && !e.target.matches('input')) {
        resetTimer();
    } else if (e.code === 'Escape' && editingTimerId) {
        cancelEditMode();
    }
});

// ==================== INITIALIZATION ====================
// Load timers when page opens
document.addEventListener('DOMContentLoaded', () => {
    updateDisplay();
    fetchTimers();
    
    // Set active preset to 25
    document.querySelector('[data-minutes="25"]').classList.add('active');
});

// Enter key in name input - Save timer
timerNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault(); // Prevent form submission if any
        saveTimerToDB();
    }
});