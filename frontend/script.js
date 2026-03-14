/**
 * MicroLesson AI - Frontend JavaScript
 * Handles form submission, API calls, and content rendering
 */

// Configuration
const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : '';

// Global state
let currentSlideIndex = 0;
let slides = [];

// DOM Elements
const form = document.getElementById('lessonForm');
const topicInput = document.getElementById('topic');
const resultDiv = document.getElementById('result');
const generateBtn = document.getElementById('generateBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    form.addEventListener('submit', handleFormSubmit);
});

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    const topic = topicInput.value.trim();
    const style = document.querySelector('input[name="style"]:checked').value;

    if (!topic) {
        showError('Please enter a topic');
        return;
    }

    // Show loading state
    showLoading();
    generateBtn.disabled = true;

    try {
        // Call API
        const response = await fetch(`${API_URL}/generate-lesson`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic, style })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate lesson');
        }

        const data = await response.json();

        // Render based on type
        if (data.type === 'text') {
            renderTextLesson(data.content, topic);
        } else if (data.type === 'voice') {
            window.currentLessonAudioBase64 = data.audio_base64;
            window.currentLessonMimeType = data.mime_type;
            renderVoiceLesson(data.content, topic);
        } else if (data.type === 'slides') {
            renderSlides(data.slides, topic);
        }

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        generateBtn.disabled = false;
    }
}

/**
 * Show loading state
 */
function showLoading() {
    resultDiv.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Generating your personalized lesson...</p>
        </div>
    `;
    resultDiv.classList.add('show');
}

/**
 * Show error message
 */
function showError(message) {
    resultDiv.innerHTML = `
        <div class="error">
            <h3>Error</h3>
            <p>${message}</p>
        </div>
    `;
    resultDiv.classList.add('show');
}

/**
 * Render text lesson
 */
function renderTextLesson(content, topic) {
    // Format the content with proper HTML structure
    const formattedContent = formatTextContent(content);

    resultDiv.innerHTML = `
        <div class="text-content">
            <h1>📖 ${topic}</h1>
            <hr style="margin: 20px 0; border: none; border-top: 2px solid #667eea;">
            ${formattedContent}
        </div>
    `;
    resultDiv.classList.add('show');
}

/**
 * Format text content with proper HTML
 */
function formatTextContent(content) {
    // Split by double newlines to get paragraphs
    const paragraphs = content.split('\n\n');

    return paragraphs.map(para => {
        para = para.trim();
        if (!para) return '';

        // Check if it's a heading (starts with # or is all caps and short)
        if (para.startsWith('#')) {
            const text = para.replace(/^#+\s*/, '');
            return `<h2>${text}</h2>`;
        } else if (para.length < 100 && para === para.toUpperCase() && para.split(' ').length < 8) {
            return `<h2>${para}</h2>`;
        } else if (para.match(/^(Introduction|Concept|Summary|Key|Conclusion)/i)) {
            // Likely a section header
            return `<h2>${para}</h2>`;
        } else {
            return `<p>${para}</p>`;
        }
    }).join('\n');
}

/**
 * Render voice lesson with TTS
 */
function renderVoiceLesson(content, topic) {
    const audioBase64 = window.currentLessonAudioBase64;
    const mimeType = window.currentLessonMimeType || 'audio/mpeg';
    const audioSrc = `data:${mimeType};base64,${audioBase64}`;

    resultDiv.innerHTML = `
        <div class="voice-content">
            <h1>🎧 ${topic}</h1>
            <hr style="margin: 20px 0; border: none; border-top: 2px solid #667eea;">

            <div class="audio-controls">
                <audio controls preload="metadata" style="width: 100%;">
                    <source src="${audioSrc}" type="${mimeType}">
                    Your browser does not support audio playback.
                </audio>
                <p style="margin-top: 15px; color: #666;">Narration generated with ElevenLabs</p>
            </div>

            <div class="transcript">
                <h3 style="color: #667eea; margin-bottom: 15px;">📝 Transcript</h3>
                <div>${formatTextContent(content)}</div>
            </div>
        </div>
    `;
    resultDiv.classList.add('show');
}

/**
 * Render visual slides
 */
function renderSlides(slidesData, topic) {
    slides = slidesData;
    currentSlideIndex = 0;

    const slidesHTML = slides.map((slide, index) => `
        <div class="slide ${index === 0 ? 'active' : ''}" data-slide="${index}">
            ${slide.image ? `<img src="${slide.image}" alt="${slide.title}" class="slide-image" />` : ''}
            <h2>${slide.title}</h2>
            <p>${slide.text}</p>
        </div>
    `).join('');

    resultDiv.innerHTML = `
        <div class="slides-container">
            <h1 style="margin-bottom: 20px; color: #667eea;">📊 ${topic}</h1>

            ${slidesHTML}

            <div class="slide-nav">
                <button onclick="previousSlide()" id="prevBtn">← Previous</button>
                <span class="slide-counter">
                    <span id="currentSlide">1</span> / ${slides.length}
                </span>
                <button onclick="nextSlide()" id="nextBtn">Next →</button>
            </div>
        </div>
    `;

    updateSlideButtons();
    resultDiv.classList.add('show');
}

/**
 * Navigate to next slide
 */
function nextSlide() {
    if (currentSlideIndex < slides.length - 1) {
        currentSlideIndex++;
        updateSlides();
    }
}

/**
 * Navigate to previous slide
 */
function previousSlide() {
    if (currentSlideIndex > 0) {
        currentSlideIndex--;
        updateSlides();
    }
}

/**
 * Update slide display
 */
function updateSlides() {
    const slideElements = document.querySelectorAll('.slide');
    slideElements.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlideIndex);
    });

    document.getElementById('currentSlide').textContent = currentSlideIndex + 1;
    updateSlideButtons();
}

/**
 * Update navigation button states
 */
function updateSlideButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (prevBtn) {
        prevBtn.disabled = currentSlideIndex === 0;
    }

    if (nextBtn) {
        nextBtn.disabled = currentSlideIndex === slides.length - 1;
        if (currentSlideIndex === slides.length - 1) {
            nextBtn.textContent = '✓ Complete';
        } else {
            nextBtn.textContent = 'Next →';
        }
    }
}

/**
 * Add keyboard navigation for slides
 */
document.addEventListener('keydown', (e) => {
    if (slides.length > 0) {
        if (e.key === 'ArrowRight') {
            nextSlide();
        } else if (e.key === 'ArrowLeft') {
            previousSlide();
        }
    }
});
