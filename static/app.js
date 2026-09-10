// VibeStudy Frontend Logic

let currentSquad = null;
let userProfile = null;
let pomodoroSeconds = 50 * 60; // 50 mins
let pomodoroTotal = 50 * 60;
let pomodoroInterval = null;
let isPomodoroRunning = false;
let currentReviewRating = 5;

// DOM Elements
const onboardingSection = document.getElementById("onboardingSection");
const scanningSection = document.getElementById("scanningSection");
const resultsSection = document.getElementById("resultsSection");
const onboardingForm = document.getElementById("onboardingForm");
const quickDemoBtn = document.getElementById("quickDemoBtn");
const resetDbBtn = document.getElementById("resetDbBtn");

const userNameInput = document.getElementById("userName");
const userSectionInput = document.getElementById("userSection");
const userBioInput = document.getElementById("userBio");
const saveToPoolCheckbox = document.getElementById("saveToPoolCheckbox");
const cgpaSlider = document.getElementById("cgpaSlider");
const cgpaVal = document.getElementById("cgpaVal");
const strongSubjectSelect = document.getElementById("strongSubject");
const weakSubjectSelect = document.getElementById("weakSubject");
const subjectError = document.getElementById("subjectError");

// Header and Pool Elements
const viewPoolBtn = document.getElementById("viewPoolBtn");
const headerPeerCount = document.getElementById("headerPeerCount");
const poolBadgeCount = document.getElementById("poolBadgeCount");
const openRegisterModalBtn = document.getElementById("openRegisterModalBtn");
const peerPoolModal = document.getElementById("peerPoolModal");
const peerPoolGrid = document.getElementById("peerPoolGrid");
const poolAddBtn = document.getElementById("poolAddBtn");

// Register Modal Elements
const registerModal = document.getElementById("registerModal");
const directRegisterForm = document.getElementById("directRegisterForm");
const regNameInput = document.getElementById("regName");
const regSectionInput = document.getElementById("regSection");
const regBioInput = document.getElementById("regBio");
const regCgpaSlider = document.getElementById("regCgpaSlider");
const regCgpaVal = document.getElementById("regCgpaVal");
const regStrongSubject = document.getElementById("regStrongSubject");
const regWeakSubject = document.getElementById("regWeakSubject");
const regSubjectError = document.getElementById("regSubjectError");

// College Elements
const userCollegeSelect = document.getElementById("userCollege");
const regCollegeSelect = document.getElementById("regCollege");
const squadCollegeBadge = document.getElementById("squadCollegeBadge");
const poolCollegeFilters = document.getElementById("poolCollegeFilters");
let currentPoolCollegeFilter = "all";
let allCollegesList = [];

// Timer Elements
const timerDisplay = document.getElementById("timerDisplay");
const timerToggleBtn = document.getElementById("timerToggleBtn");
const timerPlayIcon = document.getElementById("timerPlayIcon");
const timerActionText = document.getElementById("timerActionText");
const timerResetBtn = document.getElementById("timerResetBtn");
const quickEndBtn = document.getElementById("quickEndBtn");
const timerProgressBar = document.getElementById("timerProgressBar");
const timerPill = document.getElementById("timerPill");

// Review Modal Elements
const reviewModal = document.getElementById("reviewModal");
const openReviewModalBtn = document.getElementById("openReviewModalBtn");
const reviewPeerSelect = document.getElementById("reviewPeerSelect");
const reviewPeerSummary = document.getElementById("reviewPeerSummary");
const reviewPunctual = document.getElementById("reviewPunctual");
const reviewFocused = document.getElementById("reviewFocused");
const starRatingContainer = document.getElementById("starRatingContainer");
const starRatingLabel = document.getElementById("starRatingLabel");
const submitReviewBtn = document.getElementById("submitReviewBtn");

// Squad Chat Elements
let currentSquadId = null;
let currentChatChannel = "lounge";
let currentSquadData = null;
let activePeerTarget = null;

const squadChatSection = document.getElementById("squadChatSection");
const chatTabsContainer = document.getElementById("chatTabsContainer");
const chatMessagesStream = document.getElementById("chatMessagesStream");
const chatChannelStatus = document.getElementById("chatChannelStatus");
const squadChatForm = document.getElementById("squadChatForm");
const chatInput = document.getElementById("chatInput");
const chatSendBtn = document.getElementById("chatSendBtn");

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  loadColleges();
  loadSubjects();
  setupEventListeners();
  renderStarRating();
  updateStudyHourCardStates();
  updateTrackCardStates();
  updatePeerPoolCount();
});

// Setup event listeners
function setupEventListeners() {
  // Slider live value
  cgpaSlider.addEventListener("input", (e) => {
    cgpaVal.textContent = parseFloat(e.target.value).toFixed(1);
  });

  if (regCgpaSlider) {
    regCgpaSlider.addEventListener("input", (e) => {
      regCgpaVal.textContent = parseFloat(e.target.value).toFixed(1);
    });
  }

  // Study hour cards styling
  document.querySelectorAll(".study-hour-radio").forEach((radio) => {
    radio.addEventListener("change", updateStudyHourCardStates);
  });

  // Track cards styling
  document.querySelectorAll(".track-radio").forEach((radio) => {
    radio.addEventListener("change", updateTrackCardStates);
  });

  // Demo Fill Button
  quickDemoBtn.addEventListener("click", autofillDemo);

  // Form Submission
  onboardingForm.addEventListener("submit", handleFormSubmit);

  // Timer controls
  timerToggleBtn.addEventListener("click", toggleTimer);
  timerResetBtn.addEventListener("click", resetTimer);
  quickEndBtn.addEventListener("click", () => {
    pomodoroSeconds = 10;
    pomodoroTotal = 10;
    updateTimerDisplay();
    showToast("Fast-forwarded timer to 10 seconds for demo test!", "info");
    if (!isPomodoroRunning) toggleTimer();
  });

  // Reset DB
  resetDbBtn.addEventListener("click", resetDatabase);

  // Review Modal
  openReviewModalBtn.addEventListener("click", () => openReviewModal());
  reviewPeerSelect.addEventListener("change", updateReviewPeerSummary);
  submitReviewBtn.addEventListener("click", submitReview);

  // Subject validation check
  strongSubjectSelect.addEventListener("change", checkSubjectConflict);
  weakSubjectSelect.addEventListener("change", checkSubjectConflict);

  // Candidate Pool & Register Modals
  if (viewPoolBtn) viewPoolBtn.addEventListener("click", openPeerPoolModal);
  if (openRegisterModalBtn) openRegisterModalBtn.addEventListener("click", openRegisterModal);
  if (poolAddBtn) poolAddBtn.addEventListener("click", () => { closePeerPoolModal(); openRegisterModal(); });
  if (directRegisterForm) directRegisterForm.addEventListener("submit", handleDirectRegisterSubmit);
  if (regStrongSubject) regStrongSubject.addEventListener("change", checkRegSubjectConflict);
  if (regWeakSubject) regWeakSubject.addEventListener("change", checkRegSubjectConflict);

  // Squad Chat Listeners
  if (squadChatForm) {
    squadChatForm.addEventListener("submit", handleChatSubmit);
  }
  document.querySelectorAll(".quick-prompt-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const prompt = e.currentTarget.dataset.prompt;
      if (chatInput) {
        chatInput.value = prompt;
        chatInput.focus();
      }
    });
  });
}

function updateStudyHourCardStates() {
  document.querySelectorAll(".study-hour-card").forEach((card) => {
    const radio = card.querySelector(".study-hour-radio");
    if (radio.checked) {
      card.classList.add("active");
    } else {
      card.classList.remove("active");
    }
  });
}

function updateTrackCardStates() {
  document.querySelectorAll(".track-card").forEach((card) => {
    const radio = card.querySelector(".track-radio");
    if (radio && radio.checked) {
      card.classList.add("active");
    } else if (card) {
      card.classList.remove("active");
    }
  });
}

function getRoleDisplay(role) {
  const r = (role || "no_preference").toLowerCase();
  switch (r) {
    case "concept_lead":
      return { label: "Concept Lead", icon: "🧠", color: "bg-purple-500/20 text-purple-300 border-purple-500/30" };
    case "scribe":
      return { label: "Scribe", icon: "✍️", color: "bg-blue-500/20 text-blue-300 border-blue-500/30" };
    case "time_tracker":
      return { label: "Time Tracker", icon: "⏱️", color: "bg-amber-500/20 text-amber-300 border-amber-500/30" };
    case "resource_lead":
      return { label: "Resource Lead", icon: "📚", color: "bg-teal-500/20 text-teal-300 border-teal-500/30" };
    default:
      return { label: "Pod Member", icon: "🤝", color: "bg-surface-700 text-slate-300 border-surface-600" };
  }
}

function checkSubjectConflict() {
  const strong = strongSubjectSelect.value;
  const weak = weakSubjectSelect.value;
  if (strong && weak && strong === weak) {
    subjectError.classList.remove("hidden");
    return true;
  } else {
    subjectError.classList.add("hidden");
    return false;
  }
}

function checkRegSubjectConflict() {
  const strong = regStrongSubject.value;
  const weak = regWeakSubject.value;
  if (strong && weak && strong === weak) {
    regSubjectError.classList.remove("hidden");
    return true;
  } else {
    regSubjectError.classList.add("hidden");
    return false;
  }
}

// Load Engineering Subjects
async function loadSubjects() {
  try {
    const res = await fetch("/api/subjects");
    const data = await res.json();
    const subjects = data.subjects || [];

    strongSubjectSelect.innerHTML = '<option value="">Select Strong Subject (Teach)...</option>';
    weakSubjectSelect.innerHTML = '<option value="">Select Weak Subject (Learn)...</option>';

    if (regStrongSubject) regStrongSubject.innerHTML = '<option value="">Select Strong Subject...</option>';
    if (regWeakSubject) regWeakSubject.innerHTML = '<option value="">Select Weak Subject...</option>';

    subjects.forEach((subj) => {
      const opt1 = document.createElement("option");
      opt1.value = subj;
      opt1.textContent = subj;
      strongSubjectSelect.appendChild(opt1);

      const opt2 = document.createElement("option");
      opt2.value = subj;
      opt2.textContent = subj;
      weakSubjectSelect.appendChild(opt2);

      if (regStrongSubject) {
        const optR1 = document.createElement("option");
        optR1.value = subj;
        optR1.textContent = subj;
        regStrongSubject.appendChild(optR1);
      }
      if (regWeakSubject) {
        const optR2 = document.createElement("option");
        optR2.value = subj;
        optR2.textContent = subj;
        regWeakSubject.appendChild(optR2);
      }
    });
  } catch (err) {
    console.error("Failed to load subjects:", err);
  }
}

// Load Colleges List
async function loadColleges() {
  try {
    const res = await fetch("/api/colleges");
    const data = await res.json();
    allCollegesList = data.colleges || [];

    if (userCollegeSelect) {
      userCollegeSelect.innerHTML = "";
      allCollegesList.forEach(col => {
        const opt = document.createElement("option");
        opt.value = col;
        opt.textContent = col;
        userCollegeSelect.appendChild(opt);
      });
    }

    if (regCollegeSelect) {
      regCollegeSelect.innerHTML = "";
      allCollegesList.forEach(col => {
        const opt = document.createElement("option");
        opt.value = col;
        opt.textContent = col;
        regCollegeSelect.appendChild(opt);
      });
    }

    renderPoolCollegeFilters();
  } catch (err) {
    console.error("Failed to load colleges:", err);
  }
}

function renderPoolCollegeFilters() {
  if (!poolCollegeFilters) return;
  poolCollegeFilters.innerHTML = "";

  const allBtn = document.createElement("button");
  allBtn.type = "button";
  allBtn.className = `pool-filter-btn px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${currentPoolCollegeFilter === 'all' ? 'bg-brand-600 text-white' : 'bg-surface-700 text-slate-300 hover:text-white'}`;
  allBtn.textContent = "All Colleges";
  allBtn.onclick = () => filterPoolByCollege("all");
  poolCollegeFilters.appendChild(allBtn);

  allCollegesList.forEach(col => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `pool-filter-btn px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${currentPoolCollegeFilter === col ? 'bg-brand-600 text-white' : 'bg-surface-700 text-slate-300 hover:text-white'}`;
    btn.textContent = col;
    btn.onclick = () => filterPoolByCollege(col);
    poolCollegeFilters.appendChild(btn);
  });
}

function filterPoolByCollege(col) {
  currentPoolCollegeFilter = col;
  renderPoolCollegeFilters();
  fetchAndRenderPeerPool(col);
}

// Autofill realistic demo data
function autofillDemo() {
  userNameInput.value = "Aditya Kumar";
  userSectionInput.value = "CSE-A";
  if (userCollegeSelect) userCollegeSelect.value = "Apex Institute of Technology";
  if (userBioInput) userBioInput.value = "Preparing for DSA interviews & system design sprints.";
  if (saveToPoolCheckbox) saveToPoolCheckbox.checked = true;
  
  // Select Night Owl
  const nightOwlRadio = document.querySelector('input[name="studyHours"][value="Night Owl"]');
  if (nightOwlRadio) {
    nightOwlRadio.checked = true;
    updateStudyHourCardStates();
  }

  // Select Peer Exchange Track
  const exchangeRadio = document.querySelector('input[name="sessionTrack"][value="exchange"]');
  if (exchangeRadio) {
    exchangeRadio.checked = true;
    updateTrackCardStates();
  }

  const rolePrefSelect = document.getElementById("rolePreference");
  if (rolePrefSelect) rolePrefSelect.value = "concept_lead";

  const sprintTypeSelect = document.getElementById("sprintType");
  if (sprintTypeSelect) sprintTypeSelect.value = "48hr_exam_prep";

  // CGPA: 8.6
  cgpaSlider.value = "8.6";
  cgpaVal.textContent = "8.6";

  // Strong: Data Structures, Weak: Operating Systems
  if (strongSubjectSelect) {
    const opt = Array.from(strongSubjectSelect.options).find(o => o.value === "Data Structures" || o.value.includes("Data Structures"));
    if (opt) strongSubjectSelect.value = opt.value;
    else if (strongSubjectSelect.options.length > 1) strongSubjectSelect.selectedIndex = 1;
  }
  if (weakSubjectSelect) {
    const opt = Array.from(weakSubjectSelect.options).find(o => o.value === "Operating Systems" || o.value === "Digital Logic" || o.value.includes("Operating"));
    if (opt) weakSubjectSelect.value = opt.value;
    else if (weakSubjectSelect.options.length > 2) weakSubjectSelect.selectedIndex = 2;
  }
  checkSubjectConflict();

  showToast("Demo profile loaded: Aditya Kumar (Apex Institute, Concept Lead, 48hr Sprint)", "success");
}

// Form Submit -> Run Matching Engine
async function handleFormSubmit(e) {
  e.preventDefault();
  if (checkSubjectConflict()) {
    return;
  }

  const studyHoursRadio = document.querySelector('input[name="studyHours"]:checked');
  const studyHours = studyHoursRadio ? studyHoursRadio.value : "Night Owl";
  const college = userCollegeSelect ? userCollegeSelect.value : "Apex Institute of Technology";
  const trackRadio = document.querySelector('input[name="sessionTrack"]:checked');
  const track = trackRadio ? trackRadio.value : "exchange";
  const rolePrefSelect = document.getElementById("rolePreference");
  const rolePreference = rolePrefSelect ? rolePrefSelect.value : "no_preference";
  const sprintTypeSelect = document.getElementById("sprintType");
  const sprintType = sprintTypeSelect ? sprintTypeSelect.value : "48hr_exam_prep";

  const name = userNameInput ? userNameInput.value.trim() : "";
  const section = userSectionInput ? userSectionInput.value.trim() : "";
  const strong = strongSubjectSelect ? strongSubjectSelect.value : "";
  const weak = weakSubjectSelect ? weakSubjectSelect.value : "";

  if (!name) {
    showToast("Please enter your name.", "warning");
    userNameInput?.focus();
    return;
  }
  if (!section) {
    showToast("Please enter your section / branch.", "warning");
    userSectionInput?.focus();
    return;
  }
  if (!strong || !weak) {
    showToast("Please select both a strong and a weak subject.", "warning");
    return;
  }

  const payload = {
    name: name,
    college: college,
    section: section,
    study_hours: studyHours,
    target_cgpa: parseFloat(cgpaSlider.value) || 8.5,
    strong_subject: strong,
    weak_subject: weak,
    track: track,
    role_preference: rolePreference,
    sprint_type: sprintType,
    bio: userBioInput ? userBioInput.value.trim() : "",
    save_to_pool: saveToPoolCheckbox ? saveToPoolCheckbox.checked : false
  };

  userProfile = payload;

  // Show Scanning Animation for UX
  onboardingSection.classList.add("hidden");
  resultsSection.classList.add("hidden");
  scanningSection.classList.remove("hidden");

  try {
    const res = await fetch("/api/match", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Matching request failed");
    }

    const data = await res.json();
    currentSquad = data.squad;

    if (data.saved_to_pool) {
      updatePeerPoolCount();
      showToast("💾 Profile successfully saved to candidate pool!", "success");
    }

    // Smooth scanning transition
    setTimeout(() => {
      try {
        renderSquadResults(currentSquad, data.initial_messages);
        scanningSection.classList.add("hidden");
        resultsSection.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: "smooth" });
      } catch (renderErr) {
        console.error("Error rendering squad results:", renderErr);
        scanningSection.classList.add("hidden");
        onboardingSection.classList.remove("hidden");
        showToast("Display error rendering squad: " + renderErr.message, "error");
      }
    }, 600);

  } catch (err) {
    scanningSection.classList.add("hidden");
    onboardingSection.classList.remove("hidden");
    showToast("Error finding squad: " + err.message, "error");
  }
}

// Render Squad Results
function renderSquadResults(squad, initialMessages = null) {
  const user = squad.user;
  const topPeers = squad.top_candidates || [];
  const synergy = squad.synergy_score || 0;
  const cohesion = squad.group_cohesion_score || 0;

  // Synergy Score Header
  document.getElementById("synergyScoreVal").textContent = `${synergy}%`;
  const synergyCircle = document.getElementById("synergyCircle");
  synergyCircle.setAttribute("stroke-dasharray", `${Math.round(synergy)}, 100`);

  // Pod Cohesion Score
  const cohesionVal = document.getElementById("cohesionScoreVal");
  if (cohesionVal) cohesionVal.textContent = `${cohesion}%`;
  const cohesionCircle = document.getElementById("cohesionCircle");
  if (cohesionCircle) cohesionCircle.setAttribute("stroke-dasharray", `${Math.round(cohesion)}, 100`);

  // Squad College Badge
  if (squadCollegeBadge) {
    squadCollegeBadge.textContent = squad.college || user.college || "Same Campus";
  }

  // Squad Track & Sprint Badges
  const squadTrackBadge = document.getElementById("squadTrackBadge");
  if (squadTrackBadge) {
    if (squad.track === "honor_roll") {
      squadTrackBadge.className = "px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-bold border border-amber-500/30 font-mono";
      squadTrackBadge.textContent = "🏆 Honor-Roll Sprint";
    } else {
      squadTrackBadge.className = "px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold border border-indigo-500/30 font-mono";
      squadTrackBadge.textContent = "🔄 Peer Exchange";
    }
  }

  const squadSprintBadge = document.getElementById("squadSprintBadge");
  if (squadSprintBadge) {
    if (squad.sprint_type === "weekly_lab") {
      squadSprintBadge.className = "px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-bold border border-blue-500/30 font-mono";
      squadSprintBadge.textContent = "📅 Weekly Lab Cadence";
    } else {
      squadSprintBadge.className = "px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/30 font-mono";
      squadSprintBadge.textContent = "⚡ 48hr Exam Prep";
    }
  }

  // Live Credits & Priority indicators
  const userCreditsVal = document.getElementById("userCreditsDisplay");
  if (userCreditsVal) userCreditsVal.textContent = user.study_credits ?? 50;
  const userPriorityVal = document.getElementById("userPriorityDisplay");
  if (userPriorityVal) userPriorityVal.textContent = `${user.matching_priority ?? 1.0}x`;

  // Squad Strengths Pills
  const strengthContainer = document.getElementById("squadStrengthPills");
  if (strengthContainer) {
    const strengths = squad.squad_strengths || [];
    strengthContainer.innerHTML = '<span class="text-slate-500 mr-1">Covered Topics:</span>' +
      strengths.map(s => 
        `<span class="px-2 py-0.5 rounded-md bg-surface-900 border border-surface-700 text-brand-300 font-medium">${s}</span>`
      ).join(" ");
  }

  // Render 4-Person Squad Grid
  const grid = document.getElementById("squadGrid");
  if (!grid) return;
  grid.innerHTML = "";

  // 1. User Card (Lead)
  // 1. User Card (Lead)
  const userRole = getRoleDisplay(user.assigned_role);
  const isUserMentor = (user.is_mentor == 1 || user.verified_mentor == 1 || (user.sessions_taught >= 15));
  const userMentorBadge = isUserMentor 
    ? `<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full border text-[11px] font-extrabold bg-gradient-to-r from-amber-500/25 to-yellow-500/20 text-amber-300 border-amber-400/60 shadow-sm shadow-amber-500/20">👑 Verified Mentor</span>` 
    : "";
  const userBorderClasses = isUserMentor ? "border-amber-400/80 shadow-lg shadow-amber-500/20" : "border-2";

  const userCard = document.createElement("div");
  userCard.className = `squad-card-lead ${userBorderClasses} rounded-2xl p-5 shadow-xl flex flex-col justify-between relative overflow-hidden transition-all`;
  userCard.innerHTML = `
    <div>
      <div class="flex items-center justify-between mb-3 flex-wrap gap-1">
        <div class="flex items-center gap-1.5 flex-wrap">
          <span class="px-2.5 py-1 rounded-full bg-brand-500/25 border border-brand-500/40 text-brand-300 text-[11px] font-extrabold uppercase tracking-wide">
            👑 Squad Lead (You)
          </span>
          <span class="px-2 py-0.5 rounded-md border text-[10px] font-bold ${userRole.color}">
            ${userRole.icon} ${userRole.label}
          </span>
        </div>
        <span class="text-xs font-mono text-slate-400 font-semibold">${user.section}</span>
      </div>
      ${userMentorBadge ? `<div class="mb-3">${userMentorBadge}</div>` : ''}

      <div class="text-[11px] text-accent-400 font-semibold mb-3 flex items-center gap-1.5">
        <span>🏛️</span>
        <span class="truncate">${user.college || 'Apex Institute'}</span>
      </div>

      <div class="flex items-center space-x-3 mb-4">
        <img src="${user.avatar || 'https://api.dicebear.com/7.x/bottts/svg?seed=' + user.name}" class="w-14 h-14 rounded-2xl bg-surface-900 border border-brand-500/30 p-1" alt="Avatar" />
        <div>
          <div class="flex items-center gap-1.5 flex-wrap">
            <h4 class="text-lg font-bold text-white leading-snug">${user.name}</h4>
            ${isUserMentor ? `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full border text-[10px] font-extrabold bg-gradient-to-r from-amber-500/25 to-yellow-500/20 text-amber-300 border-amber-400/60 shadow-sm shadow-amber-500/20">👑 Verified Mentor</span>` : ''}
          </div>
          ${isUserMentor ? `<div class="text-[11px] font-semibold text-amber-400/90 flex items-center gap-1 mt-0.5"><span>⚡</span><span>15+ Verified Sprints Led</span></div>` : ''}
          <div class="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
            <span>${user.study_hours === 'Night Owl' ? '🌙 Night Owl' : '🌅 Early Bird'}</span>
            <span>•</span>
            <span class="text-accent-400 font-bold">🎯 ${user.target_cgpa ? user.target_cgpa.toFixed(1) : '9.0'} CGPA</span>
          </div>
        </div>
      </div>

      ${isUserMentor && user.id ? `
      <div class="mb-3 p-2 rounded-xl bg-gradient-to-r from-amber-500/10 via-yellow-500/5 to-transparent border border-amber-400/30 flex items-center justify-between gap-2">
        <div class="flex items-center gap-1.5 text-xs text-amber-300 font-semibold">
          <span>👑</span>
          <span>15+ Verified Sprints Led</span>
        </div>
        <a href="/certificate/${user.id}" target="_blank" class="text-[10px] font-bold px-2.5 py-1 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 shadow-sm transition-all flex items-center gap-1 cursor-pointer">
          <span>📜</span>
          <span>View Certificate</span>
        </a>
      </div>
      ` : ''}

      <!-- Skills -->
      <div class="space-y-2 mt-4 text-xs">
        <div class="p-2.5 rounded-xl bg-surface-900/90 border border-emerald-500/30">
          <div class="text-[10px] font-bold text-emerald-400 uppercase tracking-wider mb-0.5">Can Teach (Strong)</div>
          <div class="font-semibold text-white">${user.strong_subject}</div>
        </div>
        <div class="p-2.5 rounded-xl bg-surface-900/90 border border-rose-500/30">
          <div class="text-[10px] font-bold text-rose-400 uppercase tracking-wider mb-0.5">Needs Help (Weak)</div>
          <div class="font-semibold text-white">${user.weak_subject}</div>
        </div>
      </div>
    </div>

    <div class="mt-5 pt-3 border-t border-surface-700/60 flex items-center justify-between text-xs text-slate-400">
      <span>Credits: <strong class="text-emerald-400">${user.study_credits ?? 50}</strong></span>
      <span class="font-bold text-emerald-400">100% (Session Host)</span>
    </div>
  `;
  grid.appendChild(userCard);

  // 2. Top 3 Matched Peers
  if (topPeers.length === 0) {
    const emptyNotice = document.createElement("div");
    emptyNotice.className = "col-span-full md:col-span-3 p-6 rounded-2xl bg-surface-800/80 border border-surface-700 text-center flex flex-col items-center justify-center";
    emptyNotice.innerHTML = `
      <span class="text-3xl mb-2">🔍</span>
      <h4 class="text-base font-bold text-white mb-1">No Matching Peers in ${user.college || 'Selected Campus'}</h4>
      <p class="text-xs text-slate-400 max-w-sm mb-3">No peers matched the current study track and criteria. Try switching tracks or registering more candidates.</p>
    `;
    grid.appendChild(emptyNotice);
  }

  topPeers.forEach((peer, idx) => {
    const isPeerMentor = (peer.is_mentor == 1 || peer.verified_mentor == 1 || (peer.sessions_taught >= 15));
    const cardBorderClasses = isPeerMentor
      ? "border-amber-400/80 shadow-lg shadow-amber-500/20"
      : "border border-surface-700/80";

    const card = document.createElement("div");
    card.className = `squad-card-peer rounded-2xl p-5 shadow-lg flex flex-col justify-between relative group transition-all ${cardBorderClasses}`;
    card.id = `peer-card-${peer.id}`;

    const peerRole = getRoleDisplay(peer.assigned_role);
    const peerMentorBadge = isPeerMentor 
      ? `<span class="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full border font-extrabold bg-gradient-to-r from-amber-500/25 to-yellow-500/20 text-amber-300 border-amber-400/60 shadow-sm shadow-amber-500/20">👑 Verified Mentor</span>` 
      : "";

    // Generate Tag Badges
    const tagsHtml = (peer.tags || []).map(t => {
      let bg = "bg-surface-800 text-slate-300 border-surface-700";
      if (t.type === "college") bg = "bg-accent-500/15 text-accent-300 border-accent-500/30 font-semibold";
      else if (t.type.includes("perfect")) bg = "bg-emerald-500/20 text-emerald-300 border-emerald-500/40";
      else if (t.type === "schedule") bg = "bg-indigo-500/20 text-indigo-300 border-indigo-500/40";
      else if (t.type === "cgpa") bg = "bg-accent-500/20 text-accent-300 border-accent-500/40";
      else if (t.type === "skill-swap") bg = "bg-teal-500/20 text-teal-300 border-teal-500/40";

      return `<span class="inline-block text-[10px] px-2 py-0.5 rounded-md border font-medium ${bg}">${t.label}</span>`;
    }).join(" ");

    card.innerHTML = `
      <div>
        <!-- Card Top Bar -->
        <div class="flex items-center justify-between mb-2 flex-wrap gap-1">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="px-2.5 py-0.5 rounded-full bg-gradient-to-r from-accent-500 to-teal-400 text-slate-950 font-black text-xs shadow-sm">
              ${peer.match_score}% MATCH
            </span>
            <span class="px-2 py-0.5 rounded-md border text-[10px] font-bold ${peerRole.color}">
              ${peerRole.icon} ${peerRole.label}
            </span>
          </div>
          <span class="text-xs font-mono text-slate-400 font-semibold">${peer.section}</span>
        </div>
        ${peerMentorBadge ? `<div class="mb-2">${peerMentorBadge}</div>` : ''}

        <div class="text-[11px] text-accent-400 font-semibold mb-3 flex items-center gap-1.5">
          <span>🏛️</span>
          <span class="truncate">${peer.college || 'Apex Institute'}</span>
        </div>

        <!-- Peer Info -->
        <div class="flex items-center space-x-3 mb-3">
          <img src="${peer.avatar}" class="w-14 h-14 rounded-2xl bg-surface-900 border border-surface-700 p-1" alt="Avatar" />
          <div>
            <div class="flex items-center gap-1.5 flex-wrap">
              <h4 class="text-base font-bold text-white leading-snug">${peer.name}</h4>
              ${isPeerMentor ? `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full border text-[10px] font-extrabold bg-gradient-to-r from-amber-500/25 to-yellow-500/20 text-amber-300 border-amber-400/60 shadow-sm shadow-amber-500/20">👑 Verified Mentor</span>` : ''}
            </div>
            ${isPeerMentor ? `<div class="text-[11px] font-semibold text-amber-400/90 flex items-center gap-1 mt-0.5"><span>⚡</span><span>15+ Verified Sprints Led</span></div>` : ''}
            <div class="flex items-center gap-2 text-xs text-slate-400 mt-0.5">
              <span>${peer.study_hours === 'Night Owl' ? '🌙 Night Owl' : '🌅 Early Bird'}</span>
              <span>•</span>
              <span class="text-accent-400 font-bold">🎯 ${peer.target_cgpa} CGPA</span>
            </div>
          </div>
        </div>

        ${isPeerMentor ? `
        <div class="mb-3 p-2 rounded-xl bg-gradient-to-r from-amber-500/10 via-yellow-500/5 to-transparent border border-amber-400/30 flex items-center justify-between gap-2">
          <div class="flex items-center gap-1.5 text-xs text-amber-300 font-semibold">
            <span>👑</span>
            <span>15+ Verified Sprints Led</span>
          </div>
          <a href="/certificate/${peer.id}" target="_blank" class="text-[10px] font-bold px-2.5 py-1 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 shadow-sm transition-all flex items-center gap-1 cursor-pointer">
            <span>📜</span>
            <span>View Certificate</span>
          </a>
        </div>
        ` : ''}

        <p class="text-[11px] text-slate-400 italic line-clamp-2 mb-3">"${peer.bio || 'Motivated engineering student.'}"</p>

        <!-- Reason Tags -->
        <div class="flex flex-wrap gap-1.5 mb-4">
          ${peer.cohesion_score !== undefined ? `<span class="inline-block text-[10px] px-2 py-0.5 rounded-md border font-semibold bg-emerald-500/20 text-emerald-300 border-emerald-500/40">🤝 Cohesion: ${peer.cohesion_score}%</span>` : ''}
          ${tagsHtml}
        </div>

        <!-- Subjects -->
        <div class="space-y-1.5 text-xs">
          <div class="px-2.5 py-1.5 rounded-lg bg-surface-900/70 border border-surface-700/60 flex items-center justify-between">
            <span class="text-slate-400 text-[11px]">Strong:</span>
            <span class="font-semibold text-emerald-300 truncate max-w-[150px]">${peer.strong_subject}</span>
          </div>
          <div class="px-2.5 py-1.5 rounded-lg bg-surface-900/70 border border-surface-700/60 flex items-center justify-between">
            <span class="text-slate-400 text-[11px]">Weak:</span>
            <span class="font-semibold text-rose-300 truncate max-w-[150px]">${peer.weak_subject}</span>
          </div>
        </div>
      </div>

      <!-- Card Footer with Reliability & Review CTA & Chat -->
      <div class="mt-4 pt-3 border-t border-surface-700/60 flex items-center justify-between text-xs gap-1.5 flex-wrap">
        <div class="flex items-center gap-1">
          <span class="text-amber-400">★</span>
          <span class="font-bold text-slate-200 peer-reliability-score" id="score-${peer.id}">${peer.reliability_score}%</span>
        </div>
        <div class="flex items-center gap-1.5 flex-wrap">
          ${isPeerMentor ? `
            <a href="/certificate/${peer.id}" target="_blank" class="text-[11px] px-2.5 py-1 rounded-md bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 hover:text-white border border-amber-400/40 font-semibold transition-all flex items-center gap-1" title="View Verified Mentor Certificate">
              <span>📜</span>
              <span>View Certificate</span>
            </a>
          ` : ''}
          <button onclick="switchToChatChannel('dm_${peer.id}')" class="text-[11px] px-2 py-1 rounded-md bg-brand-500/20 hover:bg-brand-600 text-brand-300 hover:text-white border border-brand-500/30 font-semibold transition-all flex items-center gap-1">
            <span>💬</span>
            <span>Chat</span>
          </button>
          <button onclick="openReviewModalForPeer(${peer.id})" class="text-[11px] px-2 py-1 rounded-md bg-surface-700 hover:bg-surface-600 text-slate-300 hover:text-white font-semibold transition-all">
            Review
          </button>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });

  // Setup Squad Messaging Hub
  setupSquadChat(squad, initialMessages);

  // Render Full Candidates Table
  renderCandidatesTable(squad.all_ranked || []);
}

// Render candidates breakdown table
function renderCandidatesTable(candidates) {
  const tbody = document.getElementById("candidatesTableBody");
  if (!tbody) return;
  tbody.innerHTML = "";

  (candidates || []).forEach((cand, idx) => {
    const isTop3 = idx < 3;
    const tr = document.createElement("tr");
    tr.className = isTop3 ? "bg-brand-500/10 hover:bg-brand-500/15" : "hover:bg-surface-850";
    const roleInfo = getRoleDisplay(cand.assigned_role || cand.role_preference);
    const isMentor = cand.is_mentor == 1 || cand.verified_mentor == 1 || (cand.sessions_taught >= 15);
    const mentorTag = isMentor ? `<a href="/certificate/${cand.id}" target="_blank" class="text-[9px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold ml-1 hover:bg-amber-500/30 transition-all inline-flex items-center gap-0.5" title="View Verified Mentor Certificate"><span>👑</span><span>Mentor</span></a>` : '';
    const trackTag = cand.track === 'honor_roll' ? '<span class="text-[9px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold ml-1">🏆 HR</span>' : '<span class="text-[9px] px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-bold ml-1">🔄 Ex</span>';
    
    const schedPts = cand.breakdown ? cand.breakdown.schedule_pts : 0;
    const cgpaPts = cand.breakdown ? cand.breakdown.cgpa_pts : 0;
    const skillPts = cand.breakdown ? cand.breakdown.skill_pts : 0;

    tr.innerHTML = `
      <td class="p-3 font-medium flex items-center gap-2 text-white">
        <span class="w-5 h-5 rounded-full ${isTop3 ? 'bg-brand-500 text-white font-bold' : 'bg-surface-700 text-slate-400'} inline-flex items-center justify-center text-[10px]">
          ${idx + 1}
        </span>
        <div class="flex flex-col">
          <div class="flex items-center">
            <span class="font-semibold">${cand.name}</span>
            ${mentorTag}
            ${trackTag}
          </div>
          <span class="text-slate-400 text-[10px]">${cand.section} • ${roleInfo.icon} ${roleInfo.label}</span>
        </div>
      </td>
      <td class="p-3 font-mono text-slate-300">
        +${schedPts} pts
        <span class="text-[10px] text-slate-400">(${cand.study_hours})</span>
      </td>
      <td class="p-3 font-mono text-slate-300">
        +${cgpaPts} pts
        <span class="text-[10px] text-slate-400">(Goal: ${cand.target_cgpa})</span>
      </td>
      <td class="p-3 font-mono text-slate-300">
        +${skillPts} pts
        ${cand.cohesion_score !== undefined ? `<div class="text-[10px] text-emerald-400">Cohesion: ${cand.cohesion_score}%</div>` : ''}
      </td>
      <td class="p-3 font-mono font-bold text-accent-400 text-sm">
        ${cand.match_score}%
      </td>
      <td class="p-3">
        ${isTop3 
          ? '<span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold">Selected in Squad</span>' 
          : '<span class="text-slate-500 text-[10px]">Reserve</span>'}
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// Return to onboarding
function resetToOnboarding() {
  resultsSection.classList.add("hidden");
  onboardingSection.classList.remove("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Session Checkin API (Credits & Priority)
async function checkinSession(action) {
  const studentId = userProfile?.id || currentSquad?.user?.id || 0;
  try {
    const res = await fetch("/api/session/checkin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ student_id: studentId, action: action })
    });
    const data = await res.json();
    if (data.status === "success") {
      const creditsDisplay = document.getElementById("userCreditsDisplay");
      if (creditsDisplay && data.study_credits !== undefined) {
        creditsDisplay.textContent = data.study_credits;
      }
      const priorityDisplay = document.getElementById("userPriorityDisplay");
      if (priorityDisplay && data.matching_priority !== undefined) {
        priorityDisplay.textContent = `${data.matching_priority}x`;
      }
      const depositStatus = document.getElementById("creditsDepositStatus");
      if (depositStatus) {
        if (action === "start") {
          depositStatus.textContent = "🔒 10 Credits Deposited (In-Sprint)";
          depositStatus.className = "text-[11px] px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/40 font-mono";
        } else if (action === "complete") {
          depositStatus.textContent = "🎉 +5 Bonus Credits Awarded!";
          depositStatus.className = "text-[11px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-mono";
        } else if (action === "noshow") {
          depositStatus.textContent = "⚠️ Deposit Forfeited (No-Show)";
          depositStatus.className = "text-[11px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40 font-mono";
        }
      }
      if (action !== "start") {
        showToast(data.message, action === "complete" ? "success" : "warning");
      }
    }
  } catch (err) {
    console.warn("Session checkin notification:", err);
  }
}

// Pomodoro Timer Logic
function toggleTimer() {
  if (isPomodoroRunning) {
    pauseTimer();
  } else {
    startTimer();
  }
}

function startTimer() {
  isPomodoroRunning = true;
  timerPlayIcon.textContent = "⏸";
  timerActionText.textContent = "Pause";
  timerToggleBtn.classList.remove("bg-brand-600", "hover:bg-brand-500");
  timerToggleBtn.classList.add("bg-amber-600", "hover:bg-amber-500");
  timerPill.textContent = "Focus Sprint Active";
  timerPill.classList.remove("bg-emerald-500/20", "text-emerald-300", "border-emerald-500/30");
  timerPill.classList.add("bg-amber-500/20", "text-amber-300", "border-amber-500/30", "animate-pulse");

  // Lock 10-credit deposit on session start
  checkinSession("start");

  pomodoroInterval = setInterval(() => {
    if (pomodoroSeconds > 0) {
      pomodoroSeconds--;
      updateTimerDisplay();
    } else {
      finishTimer();
    }
  }, 1000);
}

function pauseTimer() {
  isPomodoroRunning = false;
  clearInterval(pomodoroInterval);
  timerPlayIcon.textContent = "▶";
  timerActionText.textContent = "Resume";
  timerToggleBtn.classList.remove("bg-amber-600", "hover:bg-amber-500");
  timerToggleBtn.classList.add("bg-brand-600", "hover:bg-brand-500");
  timerPill.textContent = "Sprint Paused";
  timerPill.classList.remove("animate-pulse");
}

function resetTimer() {
  pauseTimer();
  pomodoroSeconds = 50 * 60;
  pomodoroTotal = 50 * 60;
  timerActionText.textContent = "Start Sprint";
  timerPill.textContent = "Deep Work Sprint";
  timerPill.classList.remove("bg-amber-500/20", "text-amber-300", "border-amber-500/30");
  timerPill.classList.add("bg-emerald-500/20", "text-emerald-300", "border-emerald-500/30");
  updateTimerDisplay();
}

function updateTimerDisplay() {
  const m = Math.floor(pomodoroSeconds / 60);
  const s = pomodoroSeconds % 60;
  timerDisplay.textContent = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  
  const pct = Math.max(0, Math.min(100, ((pomodoroTotal - pomodoroSeconds) / pomodoroTotal) * 100));
  timerProgressBar.style.width = `${pct}%`;
}

function finishTimer() {
  pauseTimer();
  playChime();
  timerDisplay.textContent = "00:00";
  timerProgressBar.style.width = "100%";
  showToast("⏰ 50m Focus Sprint Complete! Log your peer review now.", "success");
  
  // Refund deposit + award 5 bonus credits
  checkinSession("complete");

  // Post system announcement to Squad Chat
  if (currentSquadId) {
    fetch(`/api/squad/${encodeURIComponent(currentSquadId)}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        channel: "lounge",
        sender_name: "System",
        sender_avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=System&backgroundColor=6366f1",
        sender_role: "System",
        sender_id: 0,
        message: "⏱️ 50-minute Pomodoro study sprint completed! Great focus session squad—time for peer reviews."
      })
    }).then(() => {
      if (currentChatChannel === "lounge") fetchChatMessages();
    }).catch(console.error);
  }

  // Prompt review modal after completion
  setTimeout(() => {
    openReviewModal();
  }, 800);
}

// Web Audio API Gentle Chime (No external audio file needed)
function playChime() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
    notes.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.1, ctx.currentTime + idx * 0.15);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.15 + 0.6);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(ctx.currentTime + idx * 0.15);
      osc.stop(ctx.currentTime + idx * 0.15 + 0.7);
    });
  } catch (e) {
    console.log("Audio not allowed yet by browser autoplay policy");
  }
}

// Peer Review Modal Logic
function openReviewModal() {
  if (!currentSquad || !currentSquad.top_candidates || currentSquad.top_candidates.length === 0) {
    showToast("Please find a squad first before reviewing peers.", "warning");
    return;
  }
  populateReviewPeers();
  reviewModal.classList.remove("hidden");
}

function openReviewModalForPeer(peerId) {
  openReviewModal();
  reviewPeerSelect.value = peerId;
  updateReviewPeerSummary();
}

function closeReviewModal() {
  reviewModal.classList.add("hidden");
}

function populateReviewPeers() {
  reviewPeerSelect.innerHTML = "";
  const peers = currentSquad.top_candidates;
  peers.forEach((peer) => {
    const opt = document.createElement("option");
    opt.value = peer.id;
    opt.textContent = `${peer.name} (${peer.section}) — ${peer.study_hours}`;
    reviewPeerSelect.appendChild(opt);
  });
  updateReviewPeerSummary();
}

function updateReviewPeerSummary() {
  const peerId = parseInt(reviewPeerSelect.value);
  const peer = currentSquad.top_candidates.find(p => p.id === peerId);
  if (!peer) return;

  reviewPeerSummary.innerHTML = `
    <img src="${peer.avatar}" class="w-10 h-10 rounded-xl bg-surface-800 border border-surface-700 p-0.5" alt="Avatar" />
    <div class="flex-1">
      <div class="text-xs font-bold text-white flex items-center justify-between">
        <span>${peer.name}</span>
        <span class="text-amber-400 font-mono">★ ${peer.reliability_score}%</span>
      </div>
      <div class="text-[11px] text-slate-400">
        ${peer.section} • Strong in <span class="text-emerald-400">${peer.strong_subject}</span>
      </div>
    </div>
  `;
}

function renderStarRating() {
  starRatingContainer.innerHTML = "";
  for (let i = 1; i <= 5; i++) {
    const star = document.createElement("button");
    star.type = "button";
    star.className = "text-xl focus:outline-none transition-transform hover:scale-125";
    star.innerHTML = i <= currentReviewRating ? "★" : "☆";
    star.style.color = i <= currentReviewRating ? "#f59e0b" : "#64748b";
    
    star.addEventListener("click", () => {
      currentReviewRating = i;
      starRatingLabel.textContent = `${i} / 5 Stars`;
      renderStarRating();
    });
    starRatingContainer.appendChild(star);
  }
}

async function submitReview() {
  const studentId = parseInt(reviewPeerSelect.value);
  const punctual = reviewPunctual.checked;
  const focused = reviewFocused.checked;
  const rating = currentReviewRating;

  submitReviewBtn.disabled = true;
  submitReviewBtn.textContent = "Submitting Review...";

  try {
    const res = await fetch("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_id: studentId,
        reviewer_name: userProfile ? userProfile.name : "Squad Lead",
        punctual: punctual,
        focused: focused,
        rating: rating
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Failed to submit review");
    }

    const data = await res.json();

    // Update in-memory peer data
    const peer = currentSquad.top_candidates.find(p => p.id === studentId);
    if (peer) {
      peer.reliability_score = data.new_score;
      peer.review_count = data.review_count;
      peer.teaching_sessions_completed = data.teaching_sessions_completed;
      peer.verified_mentor = data.verified_mentor;
      
      // Update DOM element
      const scoreBadge = document.getElementById(`score-${peer.id}`);
      if (scoreBadge) {
        scoreBadge.textContent = `${data.new_score}%`;
        scoreBadge.parentElement.classList.add("scale-110", "transition-transform");
        setTimeout(() => scoreBadge.parentElement.classList.remove("scale-110"), 400);
      }
    }

    closeReviewModal();
    let toastMsg = `🎉 Review saved! ${data.message} (Score: ${data.old_score}% → ${data.new_score}%)`;
    if (data.verified_mentor === 1) {
      toastMsg += " 🎖️ Verified Mentor Badge unlocked!";
    }
    showToast(toastMsg, "success");

  } catch (err) {
    alert("Error submitting review: " + err.message);
  } finally {
    submitReviewBtn.disabled = false;
    submitReviewBtn.textContent = "Submit Review & Update Score";
  }
}

// Reset Database API call
async function resetDatabase() {
  if (!confirm("Reset peer ratings and candidates to default seed?")) return;
  try {
    const res = await fetch("/api/reset", { method: "POST" });
    const data = await res.json();
    showToast("✅ Database reset to initial 6 candidates successfully.", "success");
    if (userProfile && !resultsSection.classList.contains("hidden")) {
      // Re-run match to refresh view
      handleFormSubmit(new Event("submit"));
    }
  } catch (err) {
    alert("Error resetting database: " + err.message);
  }
}

// Toast notification helper
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  
  let border = "border-brand-500/40 bg-surface-800 text-slate-200";
  if (type === "success") border = "border-emerald-500/50 bg-surface-800 text-emerald-300";
  if (type === "warning") border = "border-amber-500/50 bg-surface-800 text-amber-300";

  toast.className = `toast-enter max-w-sm p-4 rounded-xl border shadow-2xl text-xs font-medium flex items-center gap-2.5 backdrop-blur-md ${border}`;
  toast.innerHTML = `
    <span class="text-sm">${type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️'}</span>
    <span class="flex-1">${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ----------------------------------------------------
// PEER POOL & PROFILE REGISTRATION LOGIC
// ----------------------------------------------------

async function updatePeerPoolCount() {
  try {
    const res = await fetch("/api/candidates");
    const data = await res.json();
    const count = data.count || (data.candidates ? data.candidates.length : 0);
    if (headerPeerCount) headerPeerCount.textContent = count;
    if (poolBadgeCount) poolBadgeCount.textContent = `${count} Profiles`;
    return data.candidates || [];
  } catch (err) {
    console.error("Failed to update candidate pool count:", err);
    return [];
  }
}

async function openPeerPoolModal() {
  peerPoolModal.classList.remove("hidden");
  await fetchAndRenderPeerPool();
}

function closePeerPoolModal() {
  peerPoolModal.classList.add("hidden");
}

function openRegisterModal() {
  registerModal.classList.remove("hidden");
  if (regNameInput) regNameInput.focus();
}

function closeRegisterModal() {
  registerModal.classList.add("hidden");
}

async function fetchAndRenderPeerPool(college = currentPoolCollegeFilter) {
  peerPoolGrid.innerHTML = `
    <div class="col-span-full py-12 text-center text-slate-400 text-xs">
      <div class="inline-block w-6 h-6 border-2 border-brand-500/20 border-t-brand-500 rounded-full animate-spin mb-2"></div>
      <div>Loading stored campus profiles from SQLite...</div>
    </div>
  `;

  try {
    const url = (college && college !== "all") 
      ? `/api/candidates?college=${encodeURIComponent(college)}` 
      : "/api/candidates";

    const res = await fetch(url);
    const data = await res.json();
    const candidates = data.candidates || [];
    
    if (college === "all" || !college) {
      if (headerPeerCount) headerPeerCount.textContent = candidates.length;
      if (poolBadgeCount) poolBadgeCount.textContent = `${candidates.length} Profiles`;
    } else {
      if (poolBadgeCount) poolBadgeCount.textContent = `${candidates.length} in ${college}`;
    }

    peerPoolGrid.innerHTML = "";

    if (candidates.length === 0) {
      peerPoolGrid.innerHTML = `<div class="col-span-full py-8 text-center text-slate-400 text-xs">No candidate profiles found for ${college === 'all' ? 'any college' : college}.</div>`;
      return;
    }

    candidates.forEach((cand) => {
      const card = document.createElement("div");
      const candRole = getRoleDisplay(cand.role_preference);
      const isMentor = cand.is_mentor == 1 || cand.verified_mentor == 1 || (cand.sessions_taught >= 15);
      const isHonorRoll = cand.track === "honor_roll";
      const cardBorderClasses = isMentor ? "border-amber-400/80 shadow-lg shadow-amber-500/20" : "border-surface-700/80";
      card.className = `p-4 rounded-xl bg-surface-900/90 border ${cardBorderClasses} shadow-md flex flex-col justify-between hover:border-brand-500/50 transition-all`;

      card.innerHTML = `
        <div>
          <div class="flex items-center justify-between mb-2 flex-wrap gap-1">
            <div class="flex items-center gap-1">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${cand.study_hours === 'Night Owl' ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'}">
                ${cand.study_hours === 'Night Owl' ? '🌙 Night Owl' : '🌅 Early Bird'}
              </span>
              <span class="text-[10px] font-bold px-1.5 py-0.5 rounded ${isHonorRoll ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'}">
                ${isHonorRoll ? '🏆 HR' : '🔄 Ex'}
              </span>
            </div>
            <span class="text-xs font-mono text-slate-400 font-bold">${cand.section}</span>
          </div>

          ${isMentor ? `
          <div class="mb-2 flex items-center justify-between gap-1">
            <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-md bg-amber-500/20 text-amber-300 border border-amber-400/50 flex items-center gap-1">
              <span>👑</span>
              <span>Verified Mentor</span>
            </span>
            <a href="/certificate/${cand.id}" target="_blank" class="text-[9px] font-bold px-2 py-0.5 rounded bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 hover:text-white border border-amber-400/40 transition-all flex items-center gap-0.5 cursor-pointer">
              <span>📜 Certificate</span>
            </a>
          </div>
          ` : ''}

          <div class="text-[11px] text-accent-400 font-semibold mb-2 flex items-center gap-1">
            <span>🏛️</span>
            <span class="truncate">${cand.college || 'Apex Institute'}</span>
          </div>

          <div class="flex items-center gap-2.5 mb-2">
            <img src="${cand.avatar}" class="w-10 h-10 rounded-xl bg-surface-800 border border-surface-700 p-0.5" alt="Avatar" />
            <div>
              <div class="flex items-center gap-1.5 flex-wrap">
                <h5 class="text-sm font-bold text-white leading-tight">${cand.name}</h5>
              </div>
              ${isMentor ? `<div class="text-[10px] text-amber-400 font-semibold mt-0.5 flex items-center gap-1"><span>⚡</span><span>15+ Verified Sprints Led</span></div>` : ''}
              <div class="text-[11px] text-accent-400 font-mono font-semibold mt-0.5">🎯 Target: ${cand.target_cgpa} CGPA</div>
              <div class="text-[10px] text-slate-400 mt-0.5">${candRole.icon} ${candRole.label}</div>
            </div>
          </div>

          <p class="text-[10px] text-slate-400 italic line-clamp-2 mb-2">"${cand.bio || 'Engineering student.'}"</p>

          <div class="space-y-1 text-[11px]">
            <div class="px-2 py-1 rounded bg-surface-800/80 border border-surface-700 flex items-center justify-between">
              <span class="text-slate-400 text-[10px]">Teaches:</span>
              <span class="font-semibold text-emerald-400 truncate max-w-[130px]">${cand.strong_subject}</span>
            </div>
            <div class="px-2 py-1 rounded bg-surface-800/80 border border-surface-700 flex items-center justify-between">
              <span class="text-slate-400 text-[10px]">Needs:</span>
              <span class="font-semibold text-rose-400 truncate max-w-[130px]">${cand.weak_subject}</span>
            </div>
          </div>
        </div>

        <div class="mt-3 pt-2 border-t border-surface-800 flex items-center justify-between text-[11px] text-slate-400">
          <span class="text-amber-400 font-mono">★ ${cand.reliability_score}%</span>
          <div class="flex items-center gap-1.5">
            ${isMentor ? `<a href="/certificate/${cand.id}" target="_blank" class="text-[10px] text-amber-400 hover:text-amber-300 font-semibold underline">Certificate</a>` : ''}
            <span class="text-[10px] text-slate-500">${cand.review_count} reviews</span>
          </div>
        </div>
      `;
      peerPoolGrid.appendChild(card);
    });

  } catch (err) {
    peerPoolGrid.innerHTML = `<div class="col-span-full py-6 text-center text-rose-400 text-xs">Failed to load profiles: ${err.message}</div>`;
  }
}

async function handleDirectRegisterSubmit(e) {
  e.preventDefault();
  if (checkRegSubjectConflict()) return;

  const regSubmitBtn = document.getElementById("regSubmitBtn");
  regSubmitBtn.disabled = true;
  regSubmitBtn.textContent = "Storing Profile in SQLite...";

  const studyHours = document.querySelector('input[name="regHours"]:checked').value;
  const college = regCollegeSelect ? regCollegeSelect.value : "Apex Institute of Technology";
  const regTrack = document.getElementById("regTrack") ? document.getElementById("regTrack").value : "exchange";
  const regRolePref = document.getElementById("regRolePreference") ? document.getElementById("regRolePreference").value : "no_preference";

  const payload = {
    name: regNameInput.value.trim(),
    college: college,
    section: regSectionInput.value.trim(),
    study_hours: studyHours,
    target_cgpa: parseFloat(regCgpaSlider.value),
    strong_subject: regStrongSubject.value,
    weak_subject: regWeakSubject.value,
    track: regTrack,
    role_preference: regRolePref,
    bio: regBioInput.value.trim() || "Ready for deep focus study sprints."
  };

  try {
    const res = await fetch("/api/students", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Failed to register profile");
    }

    const data = await res.json();
    closeRegisterModal();
    directRegisterForm.reset();
    regCgpaSlider.value = "8.5";
    regCgpaVal.textContent = "8.5";

    await updatePeerPoolCount();
    showToast(`🎉 Success! Profile for ${data.student.name} stored in campus database!`, "success");

    // If pool modal was open or user wants to see it:
    openPeerPoolModal();

  } catch (err) {
    alert("Registration failed: " + err.message);
  } finally {
    regSubmitBtn.disabled = false;
    regSubmitBtn.textContent = "Save Profile to SQLite";
  }
}

// ==========================================
// SQUAD MESSAGING & DIRECT PEER CHAT ENGINE
// ==========================================

function setupSquadChat(squadResult, initialMessages = null) {
  currentSquadId = squadResult.squad_id;
  currentSquadData = squadResult;
  currentChatChannel = "lounge";
  activePeerTarget = null;

  if (!chatTabsContainer) return;
  chatTabsContainer.innerHTML = "";

  // 1. #squad-lounge Tab (All 4 Members)
  const loungeTab = document.createElement("button");
  loungeTab.type = "button";
  loungeTab.className = "chat-tab-btn active px-4 py-2 text-xs font-bold rounded-t-xl transition-all flex items-center gap-2 border-b-2";
  loungeTab.dataset.channel = "lounge";
  loungeTab.innerHTML = `<span>📢 #squad-lounge (All 4)</span>`;
  loungeTab.addEventListener("click", () => switchToChatChannel("lounge"));
  chatTabsContainer.appendChild(loungeTab);

  // 2. Direct Message tabs for each top peer
  (squadResult.top_candidates || []).forEach(peer => {
    const dmTab = document.createElement("button");
    dmTab.type = "button";
    dmTab.className = "chat-tab-btn px-4 py-2 text-xs font-bold rounded-t-xl transition-all flex items-center gap-2 border-b-2";
    dmTab.dataset.channel = `dm_${peer.id}`;
    dmTab.dataset.peerId = peer.id;
    dmTab.dataset.peerName = peer.name;
    const firstName = peer.name.split(" ")[0];
    dmTab.innerHTML = `<span>💬 @${escapeHtml(firstName)}</span>`;
    dmTab.addEventListener("click", () => switchToChatChannel(`dm_${peer.id}`, peer));
    chatTabsContainer.appendChild(dmTab);
  });

  updateChatChannelHeader();

  if (initialMessages && initialMessages.length > 0) {
    renderChatMessages(initialMessages);
  } else {
    fetchChatMessages();
  }
}

function switchToChatChannel(channel, peerObj = null) {
  currentChatChannel = channel;
  if (!peerObj && channel.startsWith("dm_")) {
    const peerId = parseInt(channel.replace("dm_", ""));
    peerObj = (currentSquadData?.top_candidates || []).find(p => p.id === peerId);
  }
  activePeerTarget = peerObj;

  // Update tab active styling
  document.querySelectorAll(".chat-tab-btn").forEach(tab => {
    if (tab.dataset.channel === channel) {
      tab.classList.add("active");
    } else {
      tab.classList.remove("active");
    }
  });

  updateChatChannelHeader();
  fetchChatMessages();

  if (squadChatSection) {
    squadChatSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

function updateChatChannelHeader() {
  if (!chatChannelStatus || !chatInput) return;

  if (currentChatChannel === "lounge") {
    chatChannelStatus.textContent = "Channel: #squad-lounge";
    chatInput.placeholder = "Message #squad-lounge... (Press Enter to send)";
  } else if (activePeerTarget) {
    chatChannelStatus.textContent = `Direct Message: @${activePeerTarget.name} (${activePeerTarget.section})`;
    chatInput.placeholder = `Direct message to ${activePeerTarget.name}... (Press Enter to send)`;
  } else {
    chatChannelStatus.textContent = `Direct Message`;
    chatInput.placeholder = `Direct message to peer... (Press Enter to send)`;
  }
}

async function fetchChatMessages() {
  if (!currentSquadId) return;
  try {
    const res = await fetch(`/api/squad/${encodeURIComponent(currentSquadId)}/messages?channel=${encodeURIComponent(currentChatChannel)}`);
    const data = await res.json();
    if (data.status === "success" || data.messages) {
      renderChatMessages(data.messages || []);
    }
  } catch (err) {
    console.error("Error fetching squad messages:", err);
  }
}

function renderChatMessages(messages) {
  if (!chatMessagesStream) return;
  chatMessagesStream.innerHTML = "";

  if (messages.length === 0) {
    chatMessagesStream.innerHTML = `
      <div class="text-center py-10 text-slate-500 text-xs">
        <div class="text-2xl mb-2">💬</div>
        <p>No messages yet in this channel.</p>
        <p class="text-[11px] text-slate-600 mt-0.5">Send a greeting or use a quick prompt below to start the conversation!</p>
      </div>
    `;
    return;
  }

  messages.forEach(msg => {
    const msgEl = createMessageElement(msg);
    chatMessagesStream.appendChild(msgEl);
  });

  chatMessagesStream.scrollTop = chatMessagesStream.scrollHeight;
}

function createMessageElement(msg) {
  const isSystem = msg.sender_role === "System" || msg.sender_name === "System";
  const isUser = msg.sender_role && (msg.sender_role.includes("Lead") || msg.sender_role.includes("You"));

  const wrap = document.createElement("div");

  if (isSystem) {
    wrap.className = "flex justify-center my-2";
    wrap.innerHTML = `
      <div class="chat-bubble-system px-4 py-1.5 rounded-full text-[11px] flex items-center gap-2 shadow-sm font-sans">
        <span>⚡</span>
        <span>${escapeHtml(msg.message)}</span>
        <span class="text-[9px] text-indigo-300 font-mono">${formatChatTime(msg.created_at)}</span>
      </div>
    `;
    return wrap;
  }

  if (isUser) {
    wrap.className = "flex items-end justify-end gap-2.5 my-1.5";
    wrap.innerHTML = `
      <div class="flex flex-col items-end max-w-[80%]">
        <div class="flex items-center gap-2 mb-1">
          <span class="text-[10px] text-slate-400 font-mono">${formatChatTime(msg.created_at)}</span>
          <span class="text-[11px] font-bold text-white">${escapeHtml(msg.sender_name)}</span>
          <span class="text-[9px] px-1.5 py-0.2 rounded bg-brand-500/30 text-brand-300 border border-brand-500/40 uppercase font-semibold">Lead</span>
        </div>
        <div class="chat-bubble-user p-3.5 shadow-md text-xs leading-relaxed break-words font-sans">
          ${escapeHtml(msg.message)}
        </div>
      </div>
      <img src="${msg.sender_avatar}" class="w-8 h-8 rounded-xl bg-surface-900 border border-brand-500/40 p-0.5 mb-1 flex-shrink-0" alt="${escapeHtml(msg.sender_name)}" />
    `;
    return wrap;
  }

  // Peer message
  wrap.className = "flex items-end justify-start gap-2.5 my-1.5";
  wrap.innerHTML = `
    <img src="${msg.sender_avatar}" class="w-8 h-8 rounded-xl bg-surface-900 border border-surface-700 p-0.5 mb-1 flex-shrink-0" alt="${escapeHtml(msg.sender_name)}" />
    <div class="flex flex-col items-start max-w-[80%]">
      <div class="flex items-center gap-2 mb-1">
        <span class="text-[11px] font-bold text-slate-200">${escapeHtml(msg.sender_name)}</span>
        <span class="text-[9px] px-1.5 py-0.2 rounded bg-accent-500/20 text-accent-300 border border-accent-500/30 uppercase font-semibold">Peer</span>
        <span class="text-[10px] text-slate-500 font-mono">${formatChatTime(msg.created_at)}</span>
      </div>
      <div class="chat-bubble-peer p-3.5 shadow-md text-xs leading-relaxed break-words font-sans">
        ${escapeHtml(msg.message)}
      </div>
    </div>
  `;
  return wrap;
}

function formatChatTime(dateStr) {
  if (!dateStr) return "";
  try {
    const d = new Date(dateStr.replace(" ", "T") + "Z");
    if (isNaN(d.getTime())) return dateStr.split(" ")[1]?.slice(0, 5) || "";
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } catch {
    return "";
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

async function handleChatSubmit(e) {
  e.preventDefault();
  if (!currentSquadId) {
    showToast("Match a study squad first to begin messaging!", "warning");
    return;
  }

  const text = chatInput.value.trim();
  if (!text) return;

  chatInput.value = "";
  chatInput.focus();

  const user = currentSquadData?.user || { name: "Squad Lead", avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=Lead", id: 0 };

  // Optimistically display user message
  const tempMsg = {
    sender_name: user.name,
    sender_avatar: user.avatar,
    sender_role: "Squad Lead (You)",
    sender_id: user.id || 0,
    message: text,
    created_at: new Date().toISOString()
  };
  chatMessagesStream.appendChild(createMessageElement(tempMsg));
  chatMessagesStream.scrollTop = chatMessagesStream.scrollHeight;

  try {
    const res = await fetch(`/api/squad/${encodeURIComponent(currentSquadId)}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        channel: currentChatChannel,
        sender_name: user.name,
        sender_avatar: user.avatar,
        sender_role: "Squad Lead (You)",
        sender_id: user.id || 0,
        message: text
      })
    });
    const result = await res.json();
    if (result.status !== "success") {
      showToast(result.error || "Failed to send message", "error");
      return;
    }

    // Trigger simulated peer reply for interactive experience
    setTimeout(() => {
      triggerSimulatedPeerReply(text);
    }, 1200);

  } catch (err) {
    console.error("Failed to post message:", err);
    showToast("Error sending message to squad", "error");
  }
}

async function triggerSimulatedPeerReply(userMessage) {
  if (!currentSquadId || !currentSquadData) return;

  // Pick target peer
  let peer = activePeerTarget;
  if (!peer) {
    const peers = currentSquadData.top_candidates || [];
    if (peers.length > 0) {
      peer = peers[Math.floor(Math.random() * peers.length)];
    }
  }
  if (!peer) return;

  try {
    const res = await fetch(`/api/squad/${encodeURIComponent(currentSquadId)}/simulate_reply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        channel: currentChatChannel,
        user_message: userMessage,
        peer_id: peer.id,
        peer_name: peer.name,
        peer_avatar: peer.avatar,
        peer_strong: peer.strong_subject
      })
    });
    const result = await res.json();
    if (result.status === "success" && result.message) {
      chatMessagesStream.appendChild(createMessageElement(result.message));
      chatMessagesStream.scrollTop = chatMessagesStream.scrollHeight;
    }
  } catch (err) {
    console.error("Failed to fetch simulated peer response:", err);
  }
}

