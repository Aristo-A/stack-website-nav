/**
 * Browser Navigation Visualizer Frontend Controller
 * Synchronizes Two Stacks, Doubly Linked List, and Dynamic Array visualizations.
 * Includes Visited Websites Carousel, Light/Dark theme switching, and zero emojis.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements - Theme Switcher
    const themeToggle = document.getElementById('theme-toggle');
    const themeToggleText = document.getElementById('theme-toggle-text');

    // DOM Elements - Browser Frame
    const btnBack = document.getElementById('btn-back');
    const btnForward = document.getElementById('btn-forward');
    const btnReload = document.getElementById('btn-reload');
    const btnVisit = document.getElementById('btn-visit');
    const btnReset = document.getElementById('btn-reset');
    const urlInput = document.getElementById('url-input');
    const activeTabTitle = document.getElementById('active-tab-title');
    const currentPageBadge = document.getElementById('current-page-badge');
    const currentPageTitle = document.getElementById('current-page-title');
    const currentPageDesc = document.getElementById('current-page-desc');
    const lastOpType = document.getElementById('last-op-type');
    const lastOpDetail = document.getElementById('last-op-detail');

    // DOM Elements - Visited Websites Carousel
    const carouselTrack = document.getElementById('carousel-track');
    const carouselViewport = document.getElementById('carousel-viewport');
    const carouselBtnPrev = document.getElementById('carousel-btn-prev');
    const carouselBtnNext = document.getElementById('carousel-btn-next');
    const carouselCountBadge = document.getElementById('carousel-count-badge');
    const carouselPageIndicator = document.getElementById('carousel-page-indicator');

    // DOM Elements - Two Stacks
    const backStackContainer = document.getElementById('back-stack-container');
    const forwardStackContainer = document.getElementById('forward-stack-container');
    const backStackCount = document.getElementById('back-stack-count');
    const forwardStackCount = document.getElementById('forward-stack-count');
    const stacksCurrentPage = document.getElementById('stacks-current-page');
    const stacksLastOp = document.getElementById('stacks-last-op');
    const stacksPeekBack = document.getElementById('stacks-peek-back');
    const stacksPeekForward = document.getElementById('stacks-peek-forward');

    // DOM Elements - Doubly Linked List & Carousel Controls
    const dllNodesContainer = document.getElementById('dll-nodes-container');
    const dllScrollLeft = document.getElementById('dll-scroll-left');
    const dllScrollRight = document.getElementById('dll-scroll-right');
    const dllCurrentPointer = document.getElementById('dll-current-pointer');
    const dllPrevNode = document.getElementById('dll-prev-node');
    const dllNextNode = document.getElementById('dll-next-node');

    // DOM Elements - Single Dynamic Array & Carousel Controls
    const arrayCellsContainer = document.getElementById('array-cells-container');
    const arrayScrollLeft = document.getElementById('array-scroll-left');
    const arrayScrollRight = document.getElementById('array-scroll-right');
    const arrayLength = document.getElementById('array-length');
    const arrayCurrentIndex = document.getElementById('array-current-index');
    const arraySliceInfo = document.getElementById('array-slice-info');

    // DOM Elements - Demo Walkthrough
    const btnDemoPrev = document.getElementById('btn-demo-prev');
    const btnDemoNext = document.getElementById('btn-demo-next');
    const btnDemoAutoplay = document.getElementById('btn-demo-autoplay');
    const btnDemoReset = document.getElementById('btn-demo-reset');
    const stepperTrack = document.getElementById('stepper-track');
    const stepNumPill = document.getElementById('step-num-pill');
    const stepDescText = document.getElementById('step-desc-text');
    const autoplayText = document.getElementById('autoplay-text');

    // DOM Elements - Timeline & Code Inspector
    const timelineStream = document.getElementById('timeline-stream');
    const btnClearLog = document.getElementById('btn-clear-log');
    const viewTabs = document.querySelectorAll('.view-tab');
    const visualizerPanels = {
        'two-stacks': document.getElementById('panel-two-stacks'),
        'linked-list': document.getElementById('panel-linked-list'),
        'dynamic-array': document.getElementById('panel-dynamic-array')
    };
    const codeTabs = document.querySelectorAll('.code-tab');
    const codePanels = {
        'stacks-code': document.getElementById('code-stacks-code'),
        'dll-code': document.getElementById('code-dll-code'),
        'array-code': document.getElementById('code-array-code')
    };

    // State Variables
    let demoSteps = [];
    let currentDemoStepIndex = 0;
    let autoPlayInterval = null;

    // ==========================================================================
    // THEME MANAGEMENT (Light Mode & Dark Mode)
    // ==========================================================================
    function initTheme() {
        const savedTheme = localStorage.getItem('browser_nav_theme') || 'dark';
        applyTheme(savedTheme);

        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                applyTheme(newTheme);
            });
        }
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('browser_nav_theme', theme);
        if (themeToggleText) {
            themeToggleText.textContent = theme === 'dark' ? 'Dark' : 'Light';
        }
    }

    // ==========================================================================
    // INITIALIZATION & API CALLS
    // ==========================================================================
    async function init() {
        initTheme();
        bindEvents();
        await loadDemoSteps();
        await fetchState();
    }

    async function fetchState() {
        try {
            const res = await fetch('/api/state');
            const data = await res.json();
            renderAll(data);
        } catch (err) {
            console.error('Error fetching state:', err);
        }
    }

    async function sendAction(action, url = null) {
        try {
            const res = await fetch('/api/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action, url })
            });
            const data = await res.json();
            if (data.success) {
                renderAll(data.state);
                addTimelineLog(action, url, data.state);
            }
        } catch (err) {
            console.error('Action error:', err);
        }
    }

    async function loadDemoSteps() {
        try {
            const res = await fetch('/api/demo_steps');
            const data = await res.json();
            demoSteps = data.steps || [];
            renderStepper();
        } catch (err) {
            console.error('Error loading demo steps:', err);
        }
    }

    // ==========================================================================
    // RENDER FUNCTIONS
    // ==========================================================================
    function renderAll(state) {
        if (!state) return;
        const ts = state.two_stacks || {};
        const dll = state.doubly_linked_list || {};
        const arr = state.dynamic_array || {};
        const activeUrl = state.current_page || 'Empty';

        // 1. Mock Browser UI
        btnBack.disabled = !ts.can_back;
        btnForward.disabled = !ts.can_forward;
        activeTabTitle.textContent = activeUrl;
        if (state.current_page) {
            urlInput.value = state.current_page;
        }
        currentPageTitle.textContent = activeUrl;
        currentPageBadge.textContent = activeUrl ? activeUrl.replace('Page ', '').trim().charAt(0) : '-';
        currentPageDesc.textContent = activeUrl !== 'Empty' 
            ? `Active in viewport: ${activeUrl}. Browser session history synchronized across all 3 models.`
            : 'No page currently visited. Choose a page or click Demo.';
        
        lastOpType.textContent = ts.last_operation || 'READY';
        lastOpDetail.textContent = ts.operation_details || 'Ready for operations.';

        // 2. Render Visited Websites Carousel Bar
        renderWebsitesCarousel(state);

        // 3. Render Two Stacks
        renderTwoStacks(ts);

        // 4. Render Doubly Linked List
        renderDoublyLinkedList(dll);

        // 5. Render Dynamic Array
        renderDynamicArray(arr);
    }

    // Render Visited Websites Carousel (Small tabs carousel preventing page size expansion)
    function renderWebsitesCarousel(state) {
        if (!carouselTrack) return;
        carouselTrack.innerHTML = '';

        const arr = state.dynamic_array || {};
        const history = arr.history_array || [];
        const currIdx = arr.current_index !== undefined ? arr.current_index : -1;

        if (history.length === 0) {
            carouselTrack.innerHTML = '<span class="carousel-empty-text">No websites visited yet</span>';
            if (carouselCountBadge) carouselCountBadge.textContent = '0 Pages';
            if (carouselPageIndicator) carouselPageIndicator.textContent = '0 / 0';
            return;
        }

        if (carouselCountBadge) {
            carouselCountBadge.textContent = `${history.length} Page${history.length === 1 ? '' : 's'}`;
        }
        if (carouselPageIndicator) {
            carouselPageIndicator.textContent = `${currIdx >= 0 ? currIdx + 1 : 1} / ${history.length}`;
        }

        let activeCardEl = null;

        history.forEach((page, idx) => {
            const isActive = (idx === currIdx);
            const isForward = (idx > currIdx);
            const card = document.createElement('div');
            card.className = `website-tab-card ${isActive ? 'is-active' : ''} ${isForward ? 'is-forward' : ''}`;

            let stateLabel = 'Back History';
            if (isActive) stateLabel = 'Active';
            else if (isForward) stateLabel = 'Forward';

            card.innerHTML = `
                <div class="tab-card-top">
                    <span class="tab-card-badge">#${idx + 1}</span>
                    <span class="tab-card-state">${stateLabel}</span>
                </div>
                <div class="tab-card-url" title="${escapeHtml(page)}">${escapeHtml(page)}</div>
            `;

            // Clicking any website in carousel peeks it or sets input
            card.addEventListener('click', () => {
                urlInput.value = page;
            });

            if (isActive) activeCardEl = card;
            carouselTrack.appendChild(card);
        });

        // Auto-scrolling removed per user request: navigation is manual via carousel buttons
    }

    // Render Two Stacks
    function renderTwoStacks(ts) {
        backStackCount.textContent = `${ts.back_count || 0} item${ts.back_count === 1 ? '' : 's'}`;
        forwardStackCount.textContent = `${ts.forward_count || 0} item${ts.forward_count === 1 ? '' : 's'}`;
        stacksCurrentPage.textContent = ts.current_page || 'None';
        stacksLastOp.textContent = ts.last_operation || 'None';
        stacksPeekBack.textContent = ts.peek_back || 'Empty';
        stacksPeekForward.textContent = ts.peek_forward || 'Empty';

        // Back Stack (stack-shelf-container has flex-direction: column-reverse)
        backStackContainer.innerHTML = '';
        if (!ts.back_stack || ts.back_stack.length === 0) {
            backStackContainer.innerHTML = '<div class="stack-empty-msg">Back Stack is Empty</div>';
        } else {
            ts.back_stack.forEach((page, idx) => {
                const isTop = (idx === ts.back_stack.length - 1);
                const el = document.createElement('div');
                el.className = `stack-item ${isTop ? 'top-of-stack' : ''}`;
                el.title = `Stack Position #${idx + 1}: ${page}${isTop ? ' (TOP - Next pop target on Back)' : ''}`;
                el.innerHTML = `
                    <div class="stack-item-meta">
                        <span class="stack-item-idx">#${idx + 1}</span>
                        <span class="stack-item-title" title="${escapeHtml(page)}">${escapeHtml(page)}</span>
                    </div>
                    ${isTop ? '<span class="top-badge back-top-badge" title="Top of Stack (Peek / Pop Target)">TOP</span>' : ''}
                `;
                el.addEventListener('click', () => {
                    urlInput.value = page;
                });
                backStackContainer.appendChild(el);
            });
        }

        // Forward Stack
        forwardStackContainer.innerHTML = '';
        if (!ts.forward_stack || ts.forward_stack.length === 0) {
            forwardStackContainer.innerHTML = '<div class="stack-empty-msg">Forward Stack is Empty</div>';
        } else {
            ts.forward_stack.forEach((page, idx) => {
                const isTop = (idx === ts.forward_stack.length - 1);
                const el = document.createElement('div');
                el.className = `stack-item ${isTop ? 'top-of-stack' : ''}`;
                el.title = `Stack Position #${idx + 1}: ${page}${isTop ? ' (TOP - Next pop target on Forward)' : ''}`;
                el.innerHTML = `
                    <div class="stack-item-meta">
                        <span class="stack-item-idx">#${idx + 1}</span>
                        <span class="stack-item-title" title="${escapeHtml(page)}">${escapeHtml(page)}</span>
                    </div>
                    ${isTop ? '<span class="top-badge forward-top-badge" title="Top of Stack (Peek / Pop Target)">TOP</span>' : ''}
                `;
                el.addEventListener('click', () => {
                    urlInput.value = page;
                });
                forwardStackContainer.appendChild(el);
            });
        }
    }

    // Render Doubly Linked List (with Carousel Scroll Support)
    function renderDoublyLinkedList(dll) {
        dllNodesContainer.innerHTML = '';
        const nodes = dll.nodes || [];
        
        let currPtr = 'None';
        let prevPtr = 'None';
        let nextPtr = 'None';
        let activeNodeEl = null;

        if (nodes.length === 0) {
            dllNodesContainer.innerHTML = '<div class="dll-empty-msg">Doubly Linked List is empty</div>';
        } else {
            nodes.forEach((node, idx) => {
                const isCurrent = node.is_current;
                if (isCurrent) {
                    currPtr = node.url;
                    prevPtr = node.prev_url || 'NULL (Head)';
                    nextPtr = node.next_url || 'NULL (Tail)';
                }

                const wrap = document.createElement('div');
                wrap.className = 'dll-node-wrap';

                wrap.innerHTML = `
                    <div class="dll-node-card ${isCurrent ? 'is-current' : ''}">
                        ${isCurrent ? `
                            <div class="current-pointer-arrow">
                                <span class="ptr-label">CURRENT</span>
                                <div class="ptr-arrow-down"></div>
                            </div>
                        ` : ''}
                        <div class="node-url">${escapeHtml(node.url)}</div>
                        <div class="node-pointers-meta">
                            <span class="node-ptr-badge">&larr; ${node.has_prev ? 'prev' : 'null'}</span>
                            <span class="node-ptr-badge">${node.has_next ? 'next' : 'null'} &rarr;</span>
                        </div>
                    </div>
                `;

                if (idx < nodes.length - 1) {
                    const conn = document.createElement('div');
                    conn.className = 'dll-connector';
                    conn.innerHTML = `<span class="connector-arrows">&lt;===&gt;</span>`;
                    wrap.appendChild(conn);
                }

                if (isCurrent) activeNodeEl = wrap;
                dllNodesContainer.appendChild(wrap);
            });
        }

        dllCurrentPointer.textContent = currPtr;
        dllPrevNode.textContent = prevPtr;
        dllNextNode.textContent = nextPtr;

        // Auto-scrolling removed per user request
    }

    // Render Single Dynamic Array (with Carousel Scroll Support)
    function renderDynamicArray(arr) {
        arrayCellsContainer.innerHTML = '';
        const history = arr.history_array || [];
        const currIdx = arr.current_index !== undefined ? arr.current_index : -1;
        let activeCellEl = null;

        arrayLength.textContent = history.length;
        arrayCurrentIndex.textContent = currIdx;
        arraySliceInfo.textContent = currIdx >= 0 ? `history[:${currIdx + 1}]` : 'Empty';

        if (history.length === 0) {
            arrayCellsContainer.innerHTML = '<div class="array-empty-msg">Dynamic Array is empty</div>';
        } else {
            history.forEach((page, idx) => {
                const isCurrent = (idx === currIdx);
                const isForward = (idx > currIdx);

                const col = document.createElement('div');
                col.className = 'array-cell-col';

                col.innerHTML = `
                    <div class="cell-pointer-indicator">
                        ${isCurrent ? '<span class="index-ptr-badge">&darr; PTR</span>' : ''}
                    </div>
                    <div class="array-box ${isCurrent ? 'is-current' : ''} ${isForward ? 'is-forward' : ''}">
                        ${escapeHtml(page)}
                    </div>
                    <span class="cell-index-label">[${idx}]</span>
                `;

                if (isCurrent) activeCellEl = col;
                arrayCellsContainer.appendChild(col);
            });
        }

        // Auto-scrolling removed per user request
    }

    // Render Demo Stepper
    function renderStepper() {
        stepperTrack.innerHTML = '';
        demoSteps.forEach((step, idx) => {
            const node = document.createElement('div');
            const isCompleted = idx < currentDemoStepIndex;
            const isActive = idx === currentDemoStepIndex - 1;

            node.className = `step-node ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`;
            node.innerHTML = `
                <div class="step-circle">${idx + 1}</div>
                <div class="step-title">${escapeHtml(step.description)}</div>
            `;

            node.addEventListener('click', () => {
                jumpToDemoStep(idx + 1);
            });

            stepperTrack.appendChild(node);
        });

        // Update callout text
        stepNumPill.textContent = `Step ${currentDemoStepIndex}/${demoSteps.length}`;
        if (currentDemoStepIndex === 0) {
            stepDescText.textContent = 'Click "Next Step" or "Auto Play" to begin canonical flow: A → B → C → D → Back → Back → E.';
        } else if (currentDemoStepIndex <= demoSteps.length) {
            const currentStep = demoSteps[currentDemoStepIndex - 1];
            stepDescText.innerHTML = `<strong>${escapeHtml(currentStep.description)}:</strong> ${escapeHtml(currentStep.explanation)}`;
        }
    }

    // ==========================================================================
    // CANONICAL DEMO RUNNER
    // ==========================================================================
    async function stepDemo(direction = 'next') {
        try {
            const res = await fetch('/api/demo/step', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ direction })
            });
            const data = await res.json();
            currentDemoStepIndex = data.step_index || 0;
            renderAll(data.state);
            renderStepper();

            if (data.last_step) {
                addTimelineLog(
                    data.last_step.action,
                    data.last_step.url,
                    data.state,
                    `[Canonical Step ${data.step_index}] ${data.last_step.description}`
                );
            }

            if (data.completed && autoPlayInterval) {
                stopAutoPlay();
            }
        } catch (err) {
            console.error('Demo step error:', err);
            stopAutoPlay();
        }
    }

    async function jumpToDemoStep(targetStepNum) {
        stopAutoPlay();
        await stepDemo('reset');
        for (let i = 0; i < targetStepNum; i++) {
            await stepDemo('next');
        }
    }

    function toggleAutoPlay() {
        if (autoPlayInterval) {
            stopAutoPlay();
        } else {
            startAutoPlay();
        }
    }

    function startAutoPlay() {
        if (currentDemoStepIndex >= demoSteps.length) {
            stepDemo('reset');
        }
        btnDemoAutoplay.classList.add('accent');
        autoplayText.textContent = 'Pause';
        autoPlayInterval = setInterval(async () => {
            if (currentDemoStepIndex >= demoSteps.length) {
                stopAutoPlay();
                return;
            }
            await stepDemo('next');
        }, 1800);
    }

    function stopAutoPlay() {
        if (autoPlayInterval) {
            clearInterval(autoPlayInterval);
            autoPlayInterval = null;
        }
        autoplayText.textContent = 'Auto Play';
    }

    // ==========================================================================
    // TIMELINE LOGGING
    // ==========================================================================
    function addTimelineLog(action, param, state, customSummary = null) {
        const item = document.createElement('div');
        const actClass = action.toLowerCase();
        item.className = `timeline-item ${actClass}`;

        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        const summary = customSummary || `${action.toUpperCase()}${param ? ` ('${param}')` : ''} -> Current page is '${state.current_page || 'None'}'`;

        item.innerHTML = `
            <div class="tl-item-header">
                <span class="tl-badge">${escapeHtml(action.toUpperCase())}</span>
                <span class="tl-time">${timeStr}</span>
            </div>
            <div class="tl-summary">${escapeHtml(summary)}</div>
        `;

        timelineStream.insertBefore(item, timelineStream.firstChild);
        
        while (timelineStream.children.length > 40) {
            timelineStream.removeChild(timelineStream.lastChild);
        }
    }

    // ==========================================================================
    // EVENT BINDINGS
    // ==========================================================================
    function bindEvents() {
        // Carousel Bar Controls
        if (carouselBtnPrev && carouselViewport) {
            carouselBtnPrev.addEventListener('click', () => {
                carouselViewport.scrollBy({ left: -220, behavior: 'smooth' });
            });
        }
        if (carouselBtnNext && carouselViewport) {
            carouselBtnNext.addEventListener('click', () => {
                carouselViewport.scrollBy({ left: 220, behavior: 'smooth' });
            });
        }

        // Doubly Linked List Carousel Buttons
        if (dllScrollLeft && dllNodesContainer) {
            dllScrollLeft.addEventListener('click', () => {
                dllNodesContainer.scrollBy({ left: -180, behavior: 'smooth' });
            });
        }
        if (dllScrollRight && dllNodesContainer) {
            dllScrollRight.addEventListener('click', () => {
                dllNodesContainer.scrollBy({ left: 180, behavior: 'smooth' });
            });
        }

        // Dynamic Array Carousel Buttons
        if (arrayScrollLeft && arrayCellsContainer) {
            arrayScrollLeft.addEventListener('click', () => {
                arrayCellsContainer.scrollBy({ left: -160, behavior: 'smooth' });
            });
        }
        if (arrayScrollRight && arrayCellsContainer) {
            arrayScrollRight.addEventListener('click', () => {
                arrayCellsContainer.scrollBy({ left: 160, behavior: 'smooth' });
            });
        }

        // Browser Navigation
        btnBack.addEventListener('click', () => {
            stopAutoPlay();
            sendAction('back');
        });

        btnForward.addEventListener('click', () => {
            stopAutoPlay();
            sendAction('forward');
        });

        btnReload.addEventListener('click', () => {
            fetchState();
        });

        btnVisit.addEventListener('click', () => {
            const url = urlInput.value.trim();
            if (url) {
                stopAutoPlay();
                sendAction('visit', url);
            }
        });

        urlInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const url = urlInput.value.trim();
                if (url) {
                    stopAutoPlay();
                    sendAction('visit', url);
                }
            }
        });

        btnReset.addEventListener('click', () => {
            stopAutoPlay();
            sendAction('reset');
            currentDemoStepIndex = 0;
            renderStepper();
        });

        // Preset Pills
        document.querySelectorAll('.pill-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                const page = chip.getAttribute('data-page');
                urlInput.value = page;
                stopAutoPlay();
                sendAction('visit', page);
            });
        });

        // Demo Controls
        btnDemoNext.addEventListener('click', () => {
            stopAutoPlay();
            stepDemo('next');
        });

        btnDemoPrev.addEventListener('click', () => {
            stopAutoPlay();
            if (currentDemoStepIndex > 1) {
                jumpToDemoStep(currentDemoStepIndex - 1);
            } else {
                stepDemo('reset');
            }
        });

        btnDemoAutoplay.addEventListener('click', () => {
            toggleAutoPlay();
        });

        btnDemoReset.addEventListener('click', () => {
            stopAutoPlay();
            stepDemo('reset');
            renderStepper();
        });

        // View Mode Tabs
        viewTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                viewTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                const view = tab.getAttribute('data-view');
                const grid = document.getElementById('visualizer-grid');

                if (view === 'all') {
                    Object.values(visualizerPanels).forEach(p => p.style.display = 'flex');
                    grid.style.gridTemplateColumns = 'repeat(3, minmax(0, 1fr))';
                } else {
                    Object.values(visualizerPanels).forEach(p => p.style.display = 'none');
                    if (visualizerPanels[view]) {
                        visualizerPanels[view].style.display = 'flex';
                        grid.style.gridTemplateColumns = 'minmax(0, 1fr)';
                    }
                }
            });
        });

        // Code Inspector Tabs
        codeTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                codeTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                const targetKey = tab.getAttribute('data-tab');

                Object.values(codePanels).forEach(p => p.classList.remove('active'));
                if (codePanels[targetKey]) {
                    codePanels[targetKey].classList.add('active');
                }
            });
        });

        // Clear Timeline Log
        btnClearLog.addEventListener('click', () => {
            timelineStream.innerHTML = '';
        });
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Start App
    init();
});
