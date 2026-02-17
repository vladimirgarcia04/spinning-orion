/**
 * Google Cloud Summit 2026 – Client-Side Search & Filter
 */

(function () {
    "use strict";

    const searchInput = document.getElementById("searchInput");
    const categoryFilter = document.getElementById("categoryFilter");
    const timeline = document.getElementById("timeline");
    const noResults = document.getElementById("noResults");
    const themeToggle = document.getElementById("themeToggle");

    let debounceTimer = null;

    // ─── Theme Logic ──────────────────────────────────────────────
    const savedTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);

    themeToggle.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "light" ? "dark" : "light";
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
    });

    /**
     * Fetch filtered talks from the API and re-render the timeline.
     */
    async function fetchAndRender() {
        const query = searchInput.value.trim();
        const category = categoryFilter.value;

        const params = new URLSearchParams();
        if (query) params.set("q", query);
        if (category) params.set("category", category);

        try {
            const res = await fetch(`/api/talks?${params.toString()}`);
            const talks = await res.json();
            renderTimeline(talks);
        } catch (err) {
            console.error("Failed to fetch talks:", err);
        }
    }

    /**
     * Build the timeline HTML from an array of talk objects.
     */
    function renderTimeline(talks) {
        if (talks.length === 0) {
            timeline.innerHTML = "";
            noResults.style.display = "block";
            return;
        }

        noResults.style.display = "none";
        let html = "";

        talks.forEach((talk) => {
            // Insert lunch break before afternoon sessions (sort_order >= 5)
            if (talk.sort_order === 5) {
                html += buildLunchCard();
            }
            html += buildTalkCard(talk);
        });

        timeline.innerHTML = html;
    }

    /**
     * Build HTML for the lunch break card.
     */
    function buildLunchCard() {
        return `
        <div class="timeline-item lunch-item" data-permanent="true">
            <div class="timeline-dot lunch-dot">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 8h1a4 4 0 0 1 0 8h-1"/>
                    <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/>
                    <line x1="6" y1="1" x2="6" y2="4"/>
                    <line x1="10" y1="1" x2="10" y2="4"/>
                    <line x1="14" y1="1" x2="14" y2="4"/>
                </svg>
            </div>
            <div class="talk-card lunch-card">
                <div class="talk-time">12:00 PM – 1:00 PM</div>
                <h3 class="talk-title">🍽️ Lunch Break</h3>
                <p class="talk-description">Enjoy a catered lunch, network with speakers and fellow attendees, and recharge for the afternoon sessions.</p>
            </div>
        </div>`;
    }

    /**
     * Build HTML for a single talk card.
     */
    function buildTalkCard(talk) {
        const badgeClass =
            talk.category === "Cloud Strategy"
                ? "badge-strategy"
                : talk.category === "Infrastructure"
                    ? "badge-infra"
                    : "badge-data";

        const speakersHTML = talk.speaker_details
            .map((sp) => {
                const initials = sp.first_name[0] + sp.last_name[0];
                return `
                <a href="${sp.linkedin}" target="_blank" rel="noopener noreferrer" class="speaker-chip">
                    <span class="speaker-avatar">${initials}</span>
                    <span class="speaker-name">${sp.first_name} ${sp.last_name}</span>
                    <svg class="linkedin-icon" width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                </a>`;
            })
            .join("");

        return `
        <div class="timeline-item" data-talk-id="${talk.id}">
            <div class="timeline-dot">
                <span class="dot-number">${talk.sort_order}</span>
            </div>
            <div class="talk-card">
                <div class="talk-header">
                    <div class="talk-time">${talk.time}</div>
                    <span class="category-badge ${badgeClass}">${talk.category}</span>
                </div>
                <h3 class="talk-title">${talk.title}</h3>
                <p class="talk-description">${talk.description}</p>
                <div class="talk-speakers">${speakersHTML}</div>
                <div class="talk-id">${talk.id}</div>
            </div>
        </div>`;
    }

    // ─── Event Listeners ─────────────────────────────────────────────

    searchInput.addEventListener("input", () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchAndRender, 250);
    });

    categoryFilter.addEventListener("change", fetchAndRender);
})();
