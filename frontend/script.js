const ideaInput = document.getElementById('ideaInput');
const analyzeButton = document.getElementById('analyzeButton');
const clearButton = document.getElementById('clearButton');
const copyButton = document.getElementById('copyButton');
const resultsContainer = document.getElementById('resultsContainer');
const charCount = document.getElementById('charCount');
const errorDialog = document.getElementById('errorDialog');
const errorMessage = document.getElementById('errorMessage');

const API_URL = 'http://127.0.0.1:5000/analyze';
const examplePrompt = document.getElementById('examplePrompt');

const exampleIdeas = [
  'e.g., A marketplace connecting independent chefs with busy professionals who crave premium home-cooked meals.',
  'e.g., A subscription-based analytics dashboard that alerts SMB founders when churn spikes before customers cancel.',
  'e.g., A B2B SaaS platform that automates onboarding for remote teams and tracks productivity in real time.',
  'e.g., A fintech app that helps freelancers forecast taxes, automate savings, and issue invoices in one dashboard.',
  'e.g., A sustainability-focused delivery service that routes packages using only electric vehicles in urban zones.'
];
let exampleIndex = 0;

function updateCharCount() {
  const count = ideaInput.value.length;
  charCount.textContent = `${count} characters`;
}

function rotateExampleText() {
  exampleIndex = (exampleIndex + 1) % exampleIdeas.length;
  examplePrompt.textContent = exampleIdeas[exampleIndex];
  ideaInput.placeholder = exampleIdeas[exampleIndex];
}

function showMessage(text) {
  resultsContainer.innerHTML = `<div class="empty-state"><p>${text}</p></div>`;
}

function showLoading() {
  resultsContainer.innerHTML = `
    <div class="empty-state">
      <p><span class="loading-spinner"></span> KILLCRITIC is analyzing your idea...</p>
      <p style="font-size: 0.85rem; margin-top: 12px; color: #666;">Preparing to deliver brutally honest feedback</p>
    </div>
  `;
}

function createResultBlock(title, content) {
  const block = document.createElement('div');
  block.className = 'result-block';
  
  let contentHTML = '';
  if (Array.isArray(content)) {
    contentHTML = `<ul>${content.map(item => `<li>${item}</li>`).join('')}</ul>`;
  } else if (title.includes('Score') && typeof content === 'number') {
    contentHTML = `<div class="score-display"><div class="score-value">${content}/10</div></div>`;
  } else if (title.includes('Probability')) {
    contentHTML = `<div class="probability-display">${content.toUpperCase()}</div>`;
  } else if (title.includes('Verdict')) {
    contentHTML = `<div class="verdict-display">${content}</div>`;
  } else {
    contentHTML = `<p>${content}</p>`;
  }
  
  block.innerHTML = `<h3>${title}</h3>${contentHTML}`;
  return block;
}

function renderAnalysis(data) {
  resultsContainer.innerHTML = '';
  
  const analysis = data.analysis;
  
  // Header with verdict
  if (analysis.verdict) {
    const verdictBlock = document.createElement('div');
    verdictBlock.className = 'verdict-block';
    verdictBlock.innerHTML = `
      <h2>🔥 KILLCRITIC VERDICT</h2>
      <p>${analysis.verdict}</p>
    `;
    resultsContainer.appendChild(verdictBlock);
  }
  
  // Summary (at top)
  if (analysis.summary) {
    resultsContainer.appendChild(createResultBlock('📋 Executive Summary', analysis.summary));
  }
  
  // Overall Clarity
  if (analysis.overall_clarity) {
    resultsContainer.appendChild(createResultBlock('🎯 Clarity Assessment', analysis.overall_clarity));
  }
  
  // Opportunity Analysis
  if (analysis.opportunity_analysis) {
    resultsContainer.appendChild(createResultBlock('💰 Market Opportunity', analysis.opportunity_analysis));
  }
  
  // Competitive Landscape
  if (analysis.competitive_landscape) {
    resultsContainer.appendChild(createResultBlock('🏆 Competitive Reality', analysis.competitive_landscape));
  }
  
  // Scoring Grid
  const scoreBlock = document.createElement('div');
  scoreBlock.className = 'score-grid-block';
  let scoreHTML = '<div class="score-grid">';
  
  if (analysis.clarity_score) scoreHTML += `<div class="score-item"><span>Clarity</span><div class="mini-score">${analysis.clarity_score}/10</div></div>`;
  if (analysis.opportunity_score) scoreHTML += `<div class="score-item"><span>Opportunity</span><div class="mini-score">${analysis.opportunity_score}/10</div></div>`;
  if (analysis.competitive_score) scoreHTML += `<div class="score-item"><span>Competitive</span><div class="mini-score">${analysis.competitive_score}/10</div></div>`;
  if (analysis.execution_score) scoreHTML += `<div class="score-item"><span>Execution</span><div class="mini-score">${analysis.execution_score}/10</div></div>`;
  
  scoreHTML += '</div>';
  scoreBlock.innerHTML = scoreHTML;
  resultsContainer.appendChild(scoreBlock);
  
  // Strengths
  if (analysis.strengths && analysis.strengths.length > 0) {
    resultsContainer.appendChild(createResultBlock('✅ Strengths', analysis.strengths));
  }
  
  // Fatal Flaws (if exists)
  if (analysis.fatal_flaws && analysis.fatal_flaws.length > 0) {
    resultsContainer.appendChild(createResultBlock('❌ FATAL FLAWS', analysis.fatal_flaws));
  }
  
  // Risks
  if (analysis.risks && analysis.risks.length > 0) {
    resultsContainer.appendChild(createResultBlock('⚠️ Major Risks', analysis.risks));
  }
  
  // Improvement Suggestions
  if (analysis.improvement_suggestions && analysis.improvement_suggestions.length > 0) {
    resultsContainer.appendChild(createResultBlock('🚀 What You MUST Do', analysis.improvement_suggestions));
  }
  
  // MVP Roadmap
  if (analysis.mvp_roadmap && analysis.mvp_roadmap.length > 0) {
    resultsContainer.appendChild(createResultBlock('🛣️ Build Plan', analysis.mvp_roadmap));
  }
  
  // Overall Score
  if (analysis.score) {
    const scoreBlockFinal = document.createElement('div');
    scoreBlockFinal.className = 'final-score-block';
    const score = analysis.score;
    let scoreClass = 'score-low';
    if (score >= 7) scoreClass = 'score-high';
    else if (score >= 5) scoreClass = 'score-medium';
    
    scoreBlockFinal.innerHTML = `
      <div class="final-score ${scoreClass}">
        <div class="score-label">VIABILITY SCORE</div>
        <div class="score-number">${score}</div>
        <div class="score-max">/10</div>
      </div>
    `;
    resultsContainer.appendChild(scoreBlockFinal);
  }
  
  // Failure Probability
  if (analysis.failure_probability) {
    resultsContainer.appendChild(createResultBlock('📊 Failure Risk', analysis.failure_probability));
  }
  
  // Mode indicator
  const modeBlock = document.createElement('div');
  modeBlock.className = 'mode-indicator';
  modeBlock.innerHTML = `<p>🔥 ${data.mode || 'BRUTAL HONESTY'} - ${data.ai_model || 'KILLCRITIC Analysis'}</p>`;
  resultsContainer.appendChild(modeBlock);
}

function showError(message) {
  errorMessage.textContent = message;
  errorDialog.classList.remove('hidden');
}

function closeError() {
  errorDialog.classList.add('hidden');
}

async function analyzeIdea(useExample = false) {
  let idea = ideaInput.value.trim();
  const isExample = useExample || !idea;

  if (!idea) {
    idea = exampleIdeas[exampleIndex];
  }

  if (!idea || idea.length < 20) {
    showMessage('📝 Give us more details. We need at least 20 characters to deliver proper feedback.');
    return;
  }

  analyzeButton.disabled = true;
  analyzeButton.textContent = '⏳ ANALYZING...';
  showLoading();

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ idea, use_example: isExample })
    });
    
    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }
    
    const data = await response.json();
    renderAnalysis(data);
  } catch (error) {
    console.error('Error:', error);
    showError(`⚠️ Error analyzing idea: ${error.message}. Make sure the backend server is running on http://127.0.0.1:5000`);
    showMessage('💡 Please check that the backend server is running and try again.');
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.textContent = 'Get Brutally Honest Feedback';
  }
}

function copyResults() {
  const text = resultsContainer.innerText;
  if (!text || text.includes('Enter your startup')) {
    showError('No results to copy yet. Analyze an idea first!');
    return;
  }
  
  navigator.clipboard.writeText(text).then(() => {
    copyButton.textContent = '✅ COPIED';
    setTimeout(() => {
      copyButton.textContent = '📋';
    }, 2000);
  }).catch(() => {
    showError('Failed to copy results');
  });
}

function clearInput() {
  ideaInput.value = '';
  updateCharCount();
  resultsContainer.innerHTML = `
    <div class="empty-state">
      <p class="empty-icon">💡</p>
      <p>Enter your startup idea and click "Analyze Idea" to get brutally honest AI-driven insights</p>
    </div>
  `;
}

analyzeButton.addEventListener('click', analyzeIdea);
clearButton.addEventListener('click', clearInput);
copyButton.addEventListener('click', copyResults);
ideaInput.addEventListener('input', updateCharCount);
ideaInput.addEventListener('keydown', event => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    const useExample = event.target.value.trim() === '';
    analyzeIdea(useExample);
  }

  if (event.key === 'Enter' && event.shiftKey) {
    event.stopPropagation();
    return;
  }
});

// Initialize
updateCharCount();
examplePrompt.textContent = exampleIdeas[0];
ideaInput.placeholder = exampleIdeas[0];
setInterval(rotateExampleText, 5000);
