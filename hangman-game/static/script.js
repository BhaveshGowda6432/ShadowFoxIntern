/**
 * Hangman Game - Elegant Web Interface JavaScript
 * Handles all game interactions with smooth animations
 */

class HangmanWebGame {
    constructor() {
        this.currentDifficulty = null;
        this.gameActive = false;
        this.initializeEventListeners();
        this.loadStats();
        this.generateKeyboard();
    }

    /**
     * Initialize all event listeners
     */
    initializeEventListeners() {
        // Difficulty buttons with active state
        document.querySelectorAll('.difficulty-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.difficulty-btn').forEach(b => b.classList.remove('active'));
                e.target.closest('.difficulty-btn').classList.add('active');
                this.startGame(e.target.closest('.difficulty-btn').dataset.level);
            });
        });

        // Guess form
        document.getElementById('guess-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitGuess();
        });

        // Play again button
        document.getElementById('play-again-btn').addEventListener('click', () => {
            this.showSection('game-start');
        });

        // Home button
        document.getElementById('home-btn').addEventListener('click', () => {
            this.showSection('game-start');
        });

        // Keyboard buttons with animation
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('key-btn') && !e.target.disabled) {
                e.target.classList.add('bounce');
                setTimeout(() => e.target.classList.remove('bounce'), 600);
                this.guessLetter(e.target.textContent);
            }
        });
    }

    /**
     * Load game statistics
     */
    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            if (data.status === 'success') {
                document.getElementById('word-count').textContent = data.word_count;
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    /**
     * Generate keyboard buttons
     */
    generateKeyboard() {
        const keyboard = document.getElementById('keyboard');
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
        
        letters.forEach(letter => {
            const btn = document.createElement('button');
            btn.className = 'key-btn';
            btn.textContent = letter;
            btn.dataset.letter = letter;
            btn.type = 'button';
            keyboard.appendChild(btn);
        });
    }

    /**
     * Start a new game with selected difficulty
     */
    async startGame(difficulty) {
        this.currentDifficulty = difficulty;
        
        try {
            const response = await fetch('/api/initialize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ difficulty: difficulty })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.gameActive = true;
                this.resetKeyboard();
                this.resetLetterInput();
                this.showSection('game-active');
                setTimeout(() => this.updateGameDisplay(), 100);
                this.updateStatus(data.message, 'success');
            } else {
                this.updateStatus(data.message, 'error');
            }
        } catch (error) {
            console.error('Error starting game:', error);
            this.updateStatus('Error starting game', 'error');
        }
    }

    /**
     * Submit a guess
     */
    async submitGuess() {
        const letterInput = document.getElementById('letter-input');
        const letter = letterInput.value.trim().toLowerCase();

        if (!letter) {
            this.updateStatus('Please enter a letter', 'error');
            letterInput.classList.add('pulse');
            setTimeout(() => letterInput.classList.remove('pulse'), 1500);
            return;
        }

        if (!/^[a-z]$/.test(letter)) {
            this.updateStatus('Please enter a single letter (A-Z)', 'error');
            letterInput.value = '';
            return;
        }

        await this.guessLetter(letter);
        letterInput.value = '';
        letterInput.focus();
    }

    /**
     * Process a letter guess
     */
    async guessLetter(letter) {
        if (!this.gameActive) return;

        const letterLower = letter.toLowerCase();

        try {
            const response = await fetch('/api/guess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ letter: letterLower })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.updateGameDisplay(data.game_state);
                
                if (data.is_correct) {
                    this.updateStatus('✓ Correct! ' + data.message, 'success');
                    this.markKeyboardButton(letterLower, 'guessed');
                } else {
                    this.updateStatus('✗ Wrong! ' + data.message, 'error');
                    this.markKeyboardButton(letterLower, 'wrong');
                }

                // Check if game is over
                if (data.game_state.is_game_over) {
                    this.gameActive = false;
                    setTimeout(() => this.endGame(data.game_state), 600);
                }
            } else {
                this.updateStatus(data.message, 'error');
            }
        } catch (error) {
            console.error('Error making guess:', error);
            this.updateStatus('Error processing guess', 'error');
        }
    }

    /**
     * Update game display with current state
     */
    updateGameDisplay(gameState = null) {
        if (!gameState) {
            this.fetchAndUpdateDisplay();
        } else {
            this.displayGameState(gameState);
        }
    }

    /**
     * Fetch current game state and update display
     */
    async fetchAndUpdateDisplay() {
        try {
            const response = await fetch('/api/game-state');
            const data = await response.json();

            if (data.status === 'success') {
                this.displayGameState(data.game_state);
            }
        } catch (error) {
            console.error('Error fetching game state:', error);
        }
    }

    /**
     * Display the game state on the UI with elegant animations
     */
    displayGameState(state) {
        if (!state) return;

        // Update hangman visual with animation
        const hangmanVisual = document.getElementById('hangman-visual');
        hangmanVisual.style.opacity = '0.7';
        hangmanVisual.textContent = state.hangman_visual;
        setTimeout(() => hangmanVisual.style.opacity = '1', 100);

        // Update word progress
        const wordProgress = document.getElementById('word-progress');
        wordProgress.textContent = state.word_progress;

        // Update word length
        document.getElementById('word-length').textContent = state.word_progress.split(' ').filter(w => w !== '_').length;

        // Update attempts
        document.getElementById('remaining-attempts').textContent = state.remaining_attempts;
        document.getElementById('max-attempts').textContent = state.max_attempts;

        // Update attempt bar with smooth transition
        const percentage = (state.remaining_attempts / state.max_attempts) * 100;
        document.getElementById('attempt-progress').style.width = percentage + '%';

        // Update guessed letters with animation
        const guessedLettersDiv = document.getElementById('guessed-letters');
        if (state.guessed_letters.length === 0) {
            guessedLettersDiv.innerHTML = '<span class="empty-state">None yet</span>';
        } else {
            guessedLettersDiv.innerHTML = state.guessed_letters
                .map((letter, idx) => `<span style="animation: slideInUp 0.3s ease ${idx * 50}ms">${letter.toUpperCase()}</span>`)
                .join('');
        }
    }

    /**
     * End the game and show result with animation
     */
    endGame(gameState) {
        const resultDiv = document.getElementById('game-result');
        const won = gameState.player_won;

        if (won) {
            resultDiv.innerHTML = `
                <div class="game-result-title">🎉 YOU WON!</div>
                <div class="game-result-message">Congratulations!</div>
                <div class="game-result-word">${gameState.word_progress.toUpperCase()}</div>
                <div class="game-result-stats">
                    <div class="stat-item">
                        <div class="stat-label">Difficulty</div>
                        <div class="stat-value">${this.currentDifficulty.toUpperCase()}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Attempts Used</div>
                        <div class="stat-value">${gameState.max_attempts - gameState.remaining_attempts}</div>
                    </div>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="game-result-title">💀 GAME OVER</div>
                <div class="game-result-message">The word was:</div>
                <div class="game-result-word">${gameState.word.toUpperCase()}</div>
                <div class="game-result-stats">
                    <div class="stat-item">
                        <div class="stat-label">Incorrect Guesses</div>
                        <div class="stat-value">${gameState.incorrect_count}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Total Guesses</div>
                        <div class="stat-value">${gameState.guessed_letters.length}</div>
                    </div>
                </div>
            `;
        }

        this.showSection('game-over');
    }

    /**
     * Update status message with smooth animation
     */
    updateStatus(message, type = 'default') {
        const statusMessage = document.getElementById('status-message');
        statusMessage.style.opacity = '0.7';
        setTimeout(() => {
            statusMessage.textContent = message;
            statusMessage.className = `status-message ${type}`;
            statusMessage.style.opacity = '1';
        }, 100);
    }

    /**
     * Mark keyboard button as guessed or wrong
     */
    markKeyboardButton(letter, className) {
        const btn = document.querySelector(`[data-letter="${letter.toUpperCase()}"]`);
        if (btn) {
            btn.classList.add(className);
            btn.disabled = true;
        }
    }

    /**
     * Reset keyboard buttons
     */
    resetKeyboard() {
        document.querySelectorAll('.key-btn').forEach(btn => {
            btn.classList.remove('guessed', 'wrong', 'bounce');
            btn.disabled = false;
        });
    }

    /**
     * Reset letter input
     */
    resetLetterInput() {
        document.getElementById('letter-input').value = '';
    }

    /**
     * Show a specific section with smooth transition
     */
    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });

        // Show the selected section
        const newSection = document.getElementById(sectionId);
        newSection.classList.add('active');

        // Reset game if going back to start
        if (sectionId === 'game-start') {
            this.gameActive = false;
            this.resetKeyboard();
            this.resetLetterInput();
            this.resetGameDisplay();
            document.querySelectorAll('.difficulty-btn').forEach(b => b.classList.remove('active'));
        }

        // Focus on input if showing game
        if (sectionId === 'game-active') {
            setTimeout(() => {
                document.getElementById('letter-input').focus();
            }, 100);
        }
    }

    /**
     * Reset game display
     */
    resetGameDisplay() {
        document.getElementById('word-progress').textContent = '_ _ _ _ _ _';
        document.getElementById('guessed-letters').innerHTML = '<span class="empty-state">None yet</span>';
        document.getElementById('remaining-attempts').textContent = '6';
        document.getElementById('attempt-progress').style.width = '100%';
        document.getElementById('status-message').textContent = 'Select a difficulty level to begin';
        document.getElementById('hangman-visual').textContent = '';
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.game = new HangmanWebGame();
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && window.game.gameActive) {
        document.getElementById('guess-form').dispatchEvent(new Event('submit'));
    }
});
